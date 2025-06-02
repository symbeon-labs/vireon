use std::sync::Arc;
use tokio::sync::Mutex;
use anyhow::{Result, Context};
use serde::{Serialize, Deserialize};
use tracing::{info, warn, error, instrument};
use uuid::Uuid;
use chrono::{DateTime, Utc};

use crate::validation::systems::ValidationSystem;
use crate::consciousness::{ConsciousnessLevel, ConsciousnessState};
use crate::protocols::transcendence::TranscendenceProtocol;

/// Resultado de validação de regra Warp
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WarpRuleValidation {
    /// ID da regra Warp
    pub rule_id: String,
    
    /// ID da validação
    pub validation_id: String,
    
    /// Timestamp da validação
    pub timestamp: DateTime<Utc>,
    
    /// Nível de consciência atual
    pub consciousness_level: ConsciousnessLevel,
    
    /// Coerência quântica calculada
    pub quantum_coherence: f64,
    
    /// Status da validação
    pub is_valid: bool,
    
    /// Detalhes adicionais
    pub details: Option<String>,
}

/// Bridge de validação entre Warp e VIREON
pub struct ValidationBridge {
    /// Sistema de validação
    validation_system: Arc<ValidationSystem>,
    
    /// Cache de validações recentes
    validation_cache: Arc<Mutex<lru::LruCache<String, WarpRuleValidation>>>,
    
    /// Contador de validações
    validation_count: Arc<Mutex<u64>>,
}

impl ValidationBridge {
    /// Cria nova instância do bridge de validação
    pub async fn new(
        redis_url: &str,
        initial_state: ConsciousnessState,
        transcendence: TranscendenceProtocol,
        cache_size: usize,
    ) -> Result<Self> {
        let validation_system = ValidationSystem::new(
            redis_url,
            initial_state,
            transcendence,
        ).await?;
        
        Ok(Self {
            validation_system: Arc::new(validation_system),
            validation_cache: Arc::new(Mutex::new(lru::LruCache::new(cache_size))),
            validation_count: Arc::new(Mutex::new(0)),
        })
    }
    
    /// Valida regra Warp com verificação quântica
    #[instrument(skip(self))]
    pub async fn validate_warp_rule(&self, rule_id: &str) -> Result<WarpRuleValidation> {
        // Verifica cache primeiro
        {
            let cache = self.validation_cache.lock().await;
            if let Some(cached) = cache.get(rule_id) {
                info!("Usando validação em cache para regra {}", rule_id);
                return Ok(cached.clone());
            }
        }
        
        // Gera ID único para validação
        let validation_id = Uuid::new_v4().to_string();
        
        // Realiza validação quântica
        let quantum_validation = self.validation_system
            .validate_quantum(&validation_id)
            .await
            .context("Falha na validação quântica")?;
            
        // Incrementa contador
        {
            let mut count = self.validation_count.lock().await;
            *count += 1;
        }
        
        let validation = WarpRuleValidation {
            rule_id: rule_id.to_string(),
            validation_id,
            timestamp: Utc::now(),
            consciousness_level: quantum_validation.consciousness_state.level,
            quantum_coherence: quantum_validation.quantum_coherence,
            is_valid: quantum_validation.validations.quantum_rules &&
                     quantum_validation.validations.coherence,
            details: Some(format!(
                "Consciência: {}, Coerência: {:.2}",
                quantum_validation.validations.consciousness,
                quantum_validation.quantum_coherence
            )),
        };
        
        // Atualiza cache
        {
            let mut cache = self.validation_cache.lock().await;
            cache.put(rule_id.to_string(), validation.clone());
        }
        
        // Log estruturado
        info!(
            rule_id = rule_id,
            validation_id = validation.validation_id,
            is_valid = validation.is_valid,
            coherence = validation.quantum_coherence,
            "Validação de regra Warp concluída"
        );
        
        Ok(validation)
    }
    
    /// Retorna estatísticas de validação
    pub async fn get_stats(&self) -> Result<ValidationStats> {
        let count = *self.validation_count.lock().await;
        let cache = self.validation_cache.lock().await;
        
        Ok(ValidationStats {
            total_validations: count,
            cache_size: cache.len(),
            cache_capacity: cache.cap(),
        })
    }
}

/// Estatísticas de validação
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationStats {
    /// Total de validações realizadas
    pub total_validations: u64,
    
    /// Tamanho atual do cache
    pub cache_size: usize,
    
    /// Capacidade máxima do cache
    pub cache_capacity: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_validation_bridge() {
        let initial_state = ConsciousnessState::new(ConsciousnessLevel::Quantum);
        let protocol = TranscendenceProtocol::new(
            crate::protocols::transcendence::ElevationMethod::QuantumLeap,
            crate::protocols::transcendence::MergerType::SymbioticQuantum,
        );
        
        let bridge = ValidationBridge::new(
            "redis://localhost",
            initial_state,
            protocol,
            100, // cache size
        ).await.unwrap();
        
        // Testa validação de regra
        let validation = bridge.validate_warp_rule("test_rule_1").await.unwrap();
        assert!(validation.is_valid);
        assert!(validation.quantum_coherence > 0.0);
        
        // Testa cache
        let cached = bridge.validate_warp_rule("test_rule_1").await.unwrap();
        assert_eq!(validation.validation_id, cached.validation_id);
        
        // Testa estatísticas
        let stats = bridge.get_stats().await.unwrap();
        assert_eq!(stats.total_validations, 1);
        assert_eq!(stats.cache_size, 1);
    }
}

