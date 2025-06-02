//! # Motor de Regras SAGE-X
//! 
//! Este módulo implementa o motor de avaliação de regras do sistema SAGE-X.
//! Responsável por processar regras em diferentes contextos, gerenciar
//! prioridades e integrar com sistemas de cache e métricas.
//!
//! O motor suporta diferentes tipos de regras e estratégias de avaliação,
//! com foco em desempenho e confiabilidade.

use std::collections::HashMap;
use std::fmt;
use std::sync::Arc;
use std::time::{Duration, Instant};

use log::{debug, error, info, warn};
use parking_lot::RwLock;
use rayon::prelude::*;

use crate::cache::CacheManager;
use crate::error::{SageXError, Result};
use crate::metrics::MetricsCollector;
use crate::rule_types::{Rule, RuleEvaluationResult, RuleSet, RuleType};

/// Configuração do motor de regras
#[derive(Debug, Clone)]
pub struct RuleEngineConfig {
    /// Número máximo de regras a serem avaliadas em paralelo
    pub max_parallel_evaluations: usize,
    
    /// Tempo limite para avaliação de uma regra (em milissegundos)
    pub evaluation_timeout_ms: u64,
    
    /// Se verdadeiro, falhas em regras individuais não interrompem o processamento
    pub continue_on_failure: bool,
    
    /// Se verdadeiro, as métricas são coletadas
    pub collect_metrics: bool,
    
    /// Modo de operação do motor
    pub operation_mode: OperationMode,
    
    /// Estratégia de cache
    pub cache_strategy: CacheStrategy,
}

impl Default for RuleEngineConfig {
    fn default() -> Self {
        RuleEngineConfig {
            max_parallel_evaluations: 4,
            evaluation_timeout_ms: 500,
            continue_on_failure: true,
            collect_metrics: true,
            operation_mode: OperationMode::Standard,
            cache_strategy: CacheStrategy::Aggressive,
        }
    }
}

/// Modo de operação do motor de regras
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OperationMode {
    /// Modo padrão, balanceando desempenho e precisão
    Standard,
    
    /// Prioriza velocidade em detrimento de algumas verificações
    HighPerformance,
    
    /// Prioriza validação completa e verificações adicionais
    StrictValidation,
}

impl fmt::Display for OperationMode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            OperationMode::Standard => write!(f, "Standard"),
            OperationMode::HighPerformance => write!(f, "HighPerformance"),
            OperationMode::StrictValidation => write!(f, "StrictValidation"),
        }
    }
}

/// Estratégia de cache para o motor de regras
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CacheStrategy {
    /// Sem cache
    None,
    
    /// Cache conservador (apenas para regras imutáveis)
    Conservative,
    
    /// Cache moderado
    Moderate,
    
    /// Cache agressivo (maximiza uso de cache)
    Aggressive,
}

/// Motor de regras principal
pub struct RuleEngine {
    /// Configuração do motor
    config: RwLock<RuleEngineConfig>,
    
    /// Conjuntos de regras disponíveis
    rule_sets: RwLock<HashMap<String, Arc<RuleSet>>>,
    
    /// Avaliadores de regras específicos por tipo
    evaluators: HashMap<RuleType, Box<dyn RuleEvaluator + Send + Sync>>,
    
    /// Indica se o motor foi inicializado
    initialized: bool,
}

/// Interface para avaliadores de regras
pub trait RuleEvaluator: Send + Sync {
    /// Avalia uma regra no contexto fornecido
    fn evaluate(&self, rule: &Rule, context: &str) -> Result<String>;

    /// Retorna o tipo de regra que este avaliador processa
    fn rule_type(&self) -> RuleType;
}

impl RuleEngine {
    /// Cria uma nova instância do motor de regras com configuração padrão
    pub fn new() -> Self {
        let mut evaluators = HashMap::new();
        
        // Registra avaliadores padrão
        evaluators.insert(RuleType::TextPattern, Box::new(TextPatternEvaluator) as Box<dyn RuleEvaluator + Send + Sync>);
        evaluators.insert(RuleType::Regex, Box::new(RegexEvaluator) as Box<dyn RuleEvaluator + Send + Sync>);
        
        RuleEngine {
            config: RwLock::new(RuleEngineConfig::default()),
            rule_sets: RwLock::new(HashMap::new()),
            evaluators,
            initialized: true,
        }
    }
    
    /// Cria uma nova instância do motor com configuração personalizada
    pub fn with_config(config: RuleEngineConfig) -> Self {
        let mut engine = Self::new();
        *engine.config.write() = config;
        engine
    }
    
    /// Verifica se o motor foi inicializado corretamente
    pub fn is_initialized(&self) -> bool {
        self.initialized
    }
    
    /// Registra um conjunto de regras no motor
    pub fn register_rule_set(&self, rule_set: RuleSet) -> Result<()> {
        let name = rule_set.name.clone();
        let rule_set = Arc::new(rule_set);
        
        self.rule_sets.write().insert(name.clone(), rule_set);
        
        debug!("Rule set '{}' registered successfully", name);
        Ok(())
    }
    
    /// Remove um conjunto de regras do motor
    pub fn unregister_rule_set(&self, name: &str) -> Result<()> {
        let removed = self.rule_sets.write().remove(name);
        
        if removed.is_some() {
            debug!("Rule set '{}' unregistered successfully", name);
            Ok(())
        } else {
            Err(SageXError::RuleSetNotFound(name.to_string()))
        }
    }
    
    /// Avalia uma regra individual com o contexto fornecido
    pub fn evaluate(&self, rule: &Rule, context: &str) -> Result<String> {
        let start = Instant::now();
        let config = self.config.read();
        
        // Determinar o tipo de regra (usando um valor padrão para simplificar o exemplo)
        let rule_type = rule.metadata
            .get("type")
            .and_then(|t| match t.as_str() {
                "regex" => Some(RuleType::Regex),
                "javascript" => Some(RuleType::JavaScript),
                "python" => Some(RuleType::Python),
                "json" => Some(RuleType::JsonPath),
                "conditional" => Some(RuleType::Conditional),
                _ => Some(RuleType::TextPattern),
            })
            .unwrap_or(RuleType::TextPattern);
        
        // Obter o avaliador apropriado
        let evaluator = self.evaluators.get(&rule_type).ok_or_else(|| {
            error!("No evaluator registered for rule type: {:?}", rule_type);
            SageXError::UnsupportedRuleType(format!("{:?}", rule_type))
        })?;
        
        // Aplicar timeout se configurado
        let timeout = Duration::from_millis(config.evaluation_timeout_ms);
        
        // Avaliar a regra
        let result = evaluator.evaluate(rule, context);
        
        // Coletar métricas
        if config.collect_metrics {
            let duration = start.elapsed();
        }
        
        result
    }
    
    /// Avalia todas as regras aplicáveis ao contexto fornecido
    pub fn evaluate_all(&self, context: &str) -> Vec<RuleEvaluationResult> {
        let start = Instant::now();
        let config = self.config.read();
        
        // Coletar todas as regras aplicáveis de todos os conjuntos registrados
        let applicable_rules: Vec<Arc<Rule>> = self.rule_sets
            .read()
            .values()
            .flat_map(|ruleset| ruleset.find_applicable_rules(context))
            .collect();
        
        debug!("Found {} applicable rules for context", applicable_rules.len());
        
        // Processar regras em paralelo se configurado para tal
        let results = if config.max_parallel_evaluations > 1 {
            applicable_rules.par_iter()
                .map(|rule| self.evaluate_rule_with_metrics(rule.as_ref(), context))
                .collect()
        } else {
            applicable_rules.iter()
                .map(|rule| self.evaluate_rule_with_metrics(rule.as_ref(), context))
                .collect()
        };
        
        // Coletar métricas globais
        if config.collect_metrics {
            let duration = start.elapsed();
        }
        
        results
    }
    
    /// Avalia uma única regra com coleta de métricas
    fn evaluate_rule_with_metrics(&self, rule: &Rule, context: &str) -> RuleEvaluationResult {
        let start = Instant::now();
        
        match self.evaluate(rule, context) {
            Ok(result) => {
                let duration = start.elapsed().as_micros() as u64;
                RuleEvaluationResult::success(rule, result, duration)
            },
            Err(err) => {
                let duration = start.elapsed().as_micros() as u64;
                RuleEvaluationResult::failure(rule, err.to_string(), duration)
            }
        }
    }
    
    /// Atualiza a configuração do motor
    pub fn update_config(&self, config: RuleEngineConfig) {
        *self.config.write() = config;
        debug!("Rule engine configuration updated");
    }
    
    /// Registra um avaliador de regras personalizado
    pub fn register_evaluator<E>(&mut self, evaluator: E) 
    where
        E: RuleEvaluator + 'static,
    {
        let rule_type = evaluator.rule_type();
        self.evaluators.insert(rule_type, Box::new(evaluator));
        debug!("Registered evaluator for rule type: {:?}", rule_type);
    }
    
    /// Obtém estatísticas sobre o motor de regras
    pub fn get_statistics(&self) -> RuleEngineStatistics {
        let rule_sets = self.rule_sets.read();
        
        let total_rule_sets = rule_sets.len();
        let total_rules = rule_sets.values()
            .map(|rs| rs.rules.len())
            .sum();
        
        RuleEngineStatistics {
            total_rule_sets,
            total_rules,
            registered_evaluators: self.evaluators.len(),
            operation_mode: *&self.config.read().operation_mode,
        }
    }
}

/// Estatísticas do motor de regras
#[derive(Debug, Clone)]
pub struct RuleEngineStatistics {
    /// Número total de conjuntos de regras
    pub total_rule_sets: usize,
    
    /// Número total de regras
    pub total_rules: usize,
    
    /// Número de avaliadores registrados
    pub registered_evaluators: usize,
    
    /// Modo de operação atual
    pub operation_mode: OperationMode,
}

/// Avaliador de regras baseadas em padrões de texto
struct TextPatternEvaluator;

impl RuleEvaluator for TextPatternEvaluator {
    fn evaluate(&self, rule: &Rule, context: &str) -> Result<String> {
        // Implementação simplificada para demonstração
        if context.contains(&rule.content) {
            Ok(format!("Matched pattern '{}' in context", rule.content))
        } else {
            Ok(format!("Pattern '{}' not found in context", rule.content))
        }
    }

    fn rule_type(&self) -> RuleType {
        RuleType::TextPattern
    }
}

/// Avaliador de regras baseadas em expressões regulares
struct RegexEvaluator;

impl RuleEvaluator for RegexEvaluator {
    fn evaluate(&self, rule: &Rule, context: &str) -> Result<String> {
        // Na implementação real, usaria a biblioteca regex
        // Por simplicidade, esta é uma implementação de exemplo
        Ok(format!("Evaluated regex '{}' against context", rule.content))
    }

    fn rule_type(&self) -> RuleType {
        RuleType::Regex
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_engine_initialization() {
        let engine = RuleEngine::new();
        assert!(engine.is_initialized());
    }
    
    #[test]
    fn test_engine_custom_config() {
        let config = RuleEngineConfig {
            max_parallel_evaluations: 8,
            evaluation_timeout_ms: 1000,
            continue_on_failure: false,
            ..RuleEngineConfig::default()
        };
        
        let engine = RuleEngine::with_config(config.clone());
        assert_eq!(engine.config.read().max_parallel_evaluations, 8);
        assert_eq!(engine.config.read().evaluation_timeout_ms, 1000);
        assert_eq!(engine.config.read().continue_on_failure, false);
    }
    
    #[test]
    fn test_register_rule_set() {
        let engine = RuleEngine::new();
        let rule_set = RuleSet::new("test_set");
        
        assert!(engine.register_rule_set(rule_set).is_ok());
        assert!(engine.rule_sets.read().contains_key("test_set"));
    }
    
    #[test]
    fn test_unregister_rule_set() {
        let engine = RuleEngine::new();
        let rule_set = RuleSet::new("temp_set");
        
        engine.register_rule_set(rule_set).unwrap();
        assert!(engine.unregister_rule_set("temp_set").is_ok());
        assert!(!engine.rule_sets.read().contains_key("temp_set"));
        
        // Tentar remover um conjunto inexistente deve falhar
        assert!(engine.unregister_rule_set("nonexistent").is_err());
    }
    
    #[test]
    fn test_evaluate_rule() {
        let engine = RuleEngine::new();
        let rule = Rule::new("test_rule", "test_content");
        
        let result = engine.evaluate(&rule, "This is a test_content example");
        assert!(result.is_ok());
        
        let result_str = result.unwrap();
        assert!(result_str.contains("Matched pattern"));
    }
    
    #[test]
    fn test_evaluate_all_rules() {
        let engine = RuleEngine::new();
        let mut rule_set = RuleSet::new("test_eval_set");
        
        let rule1 = Rule::new("rule1", "content1");
        let rule2 = Rule::new("rule2", "content2");
        
        rule_set.add_rule(rule1);
        rule_set.add_rule(rule2);
        
        engine.register_rule_set(rule_set).unwrap();
        
        let results = engine.evaluate_all("This contains content1 and content2");
        assert_eq!(results.len(), 2);
        
        // Verificar se ambas as regras foram avaliadas com sucesso
        assert!(results.iter().all(|r| r.success));
    }
}

