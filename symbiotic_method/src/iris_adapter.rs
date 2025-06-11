//! # Adaptador IRIS
//!
//! Este módulo implementa a interface FFI para integração com o sistema IRIS,
//! fornecendo funcionalidades unificadas de consciência, emoção e cognição.

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info, warn, error};
use chrono::{DateTime, Utc};
use uuid::Uuid;

use crate::consciousness::{ConsciousnessAdapter, EmotionalState, ConsciousnessLevel};
use crate::quantum_bridge::{QuantumBridgeAdapter, QuantumMessage};
use crate::quantum_memory::{QuantumMemoryAdapter, QuantumMemoryBlock, QuantumMemoryType};

/// Modos de operação do IRIS
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[pyclass]
pub enum IrisMode {
    Reactive,      // Modo reativo básico
    Proactive,     // Modo proativo com antecipação
    Symbiotic,     // Modo simbiótico integrado
    Transcendent,  // Modo transcendente evolutivo
}

#[pymethods]
impl IrisMode {
    #[new]
    fn new() -> Self {
        IrisMode::Reactive
    }
    
    fn get_complexity_level(&self) -> f64 {
        match self {
            IrisMode::Reactive => 0.25,
            IrisMode::Proactive => 0.50,
            IrisMode::Symbiotic => 0.75,
            IrisMode::Transcendent => 1.0,
        }
    }
    
    fn get_processing_power(&self) -> f64 {
        match self {
            IrisMode::Reactive => 1.0,
            IrisMode::Proactive => 1.5,
            IrisMode::Symbiotic => 2.0,
            IrisMode::Transcendent => 3.0,
        }
    }
    
    fn can_evolve_to(&self, target: IrisMode) -> bool {
        let current_level = self.get_complexity_level();
        let target_level = target.get_complexity_level();
        target_level > current_level
    }
    
    fn __str__(&self) -> String {
        format!("{:?}", self)
    }
    
    fn __repr__(&self) -> String {
        format!("IrisMode::{:?}", self)
    }
}

/// Estado cognitivo do IRIS
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct CognitiveState {
    #[pyo3(get, set)]
    pub attention_focus: f64,
    #[pyo3(get, set)]
    pub memory_consolidation: f64,
    #[pyo3(get, set)]
    pub pattern_recognition: f64,
    #[pyo3(get, set)]
    pub decision_confidence: f64,
    #[pyo3(get, set)]
    pub learning_rate: f64,
    #[pyo3(get, set)]
    pub creativity_index: f64,
    #[pyo3(get, set)]
    pub timestamp: String,
}

#[pymethods]
impl CognitiveState {
    #[new]
    fn new() -> Self {
        Self {
            attention_focus: 0.5,
            memory_consolidation: 0.5,
            pattern_recognition: 0.5,
            decision_confidence: 0.5,
            learning_rate: 0.5,
            creativity_index: 0.5,
            timestamp: Utc::now().to_rfc3339(),
        }
    }
    
    fn get_overall_performance(&self) -> f64 {
        (self.attention_focus + self.memory_consolidation + 
         self.pattern_recognition + self.decision_confidence + 
         self.learning_rate + self.creativity_index) / 6.0
    }
    
    fn normalize(&mut self) {
        let values = vec![
            &mut self.attention_focus, &mut self.memory_consolidation,
            &mut self.pattern_recognition, &mut self.decision_confidence,
            &mut self.learning_rate, &mut self.creativity_index
        ];
        
        for value in values {
            *value = value.max(0.0).min(1.0);
        }
        
        self.timestamp = Utc::now().to_rfc3339();
    }
    
    fn update_from_feedback(&mut self, performance_delta: f64, learning_factor: f64) {
        let adjustment = performance_delta * learning_factor;
        
        self.attention_focus += adjustment * 0.2;
        self.memory_consolidation += adjustment * 0.15;
        self.pattern_recognition += adjustment * 0.25;
        self.decision_confidence += adjustment * 0.2;
        self.learning_rate += adjustment * 0.1;
        self.creativity_index += adjustment * 0.1;
        
        self.normalize();
    }
    
    fn to_dict(&self) -> HashMap<String, f64> {
        let mut result = HashMap::new();
        result.insert("attention_focus".to_string(), self.attention_focus);
        result.insert("memory_consolidation".to_string(), self.memory_consolidation);
        result.insert("pattern_recognition".to_string(), self.pattern_recognition);
        result.insert("decision_confidence".to_string(), self.decision_confidence);
        result.insert("learning_rate".to_string(), self.learning_rate);
        result.insert("creativity_index".to_string(), self.creativity_index);
        result.insert("overall_performance".to_string(), self.get_overall_performance());
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "CognitiveState(performance={:.2}, focus={:.2}, learning={:.2})",
            self.get_overall_performance(),
            self.attention_focus,
            self.learning_rate
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "CognitiveState(attention_focus={}, memory_consolidation={}, pattern_recognition={}, decision_confidence={}, learning_rate={}, creativity_index={})",
            self.attention_focus,
            self.memory_consolidation,
            self.pattern_recognition,
            self.decision_confidence,
            self.learning_rate,
            self.creativity_index
        )
    }
}

/// Configuração do sistema IRIS
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct IrisConfig {
    #[pyo3(get, set)]
    pub mode: IrisMode,
    #[pyo3(get, set)]
    pub evolution_enabled: bool,
    #[pyo3(get, set)]
    pub quantum_integration: bool,
    #[pyo3(get, set)]
    pub consciousness_threshold: f64,
    #[pyo3(get, set)]
    pub emotional_sensitivity: f64,
    #[pyo3(get, set)]
    pub learning_acceleration: f64,
    #[pyo3(get, set)]
    pub memory_retention: f64,
}

#[pymethods]
impl IrisConfig {
    #[new]
    fn new() -> Self {
        Self {
            mode: IrisMode::Reactive,
            evolution_enabled: true,
            quantum_integration: true,
            consciousness_threshold: 0.7,
            emotional_sensitivity: 0.8,
            learning_acceleration: 1.0,
            memory_retention: 0.9,
        }
    }
    
    fn validate(&self) -> bool {
        self.consciousness_threshold >= 0.0 && self.consciousness_threshold <= 1.0 &&
        self.emotional_sensitivity >= 0.0 && self.emotional_sensitivity <= 1.0 &&
        self.learning_acceleration > 0.0 &&
        self.memory_retention >= 0.0 && self.memory_retention <= 1.0
    }
    
    fn to_dict(&self) -> HashMap<String, PyObject> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        
        let mut result = HashMap::new();
        result.insert("mode".to_string(), format!("{:?}", self.mode).to_object(py));
        result.insert("evolution_enabled".to_string(), self.evolution_enabled.to_object(py));
        result.insert("quantum_integration".to_string(), self.quantum_integration.to_object(py));
        result.insert("consciousness_threshold".to_string(), self.consciousness_threshold.to_object(py));
        result.insert("emotional_sensitivity".to_string(), self.emotional_sensitivity.to_object(py));
        result.insert("learning_acceleration".to_string(), self.learning_acceleration.to_object(py));
        result.insert("memory_retention".to_string(), self.memory_retention.to_object(py));
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "IrisConfig(mode={:?}, evolution={}, quantum={})",
            self.mode,
            self.evolution_enabled,
            self.quantum_integration
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "IrisConfig(mode={:?}, evolution_enabled={}, quantum_integration={}, consciousness_threshold={}, emotional_sensitivity={}, learning_acceleration={}, memory_retention={})",
            self.mode,
            self.evolution_enabled,
            self.quantum_integration,
            self.consciousness_threshold,
            self.emotional_sensitivity,
            self.learning_acceleration,
            self.memory_retention
        )
    }
}

/// Adaptador principal do sistema IRIS
#[derive(Debug)]
#[pyclass]
pub struct IrisAdapter {
    config: Arc<RwLock<IrisConfig>>,
    consciousness_adapter: Arc<RwLock<ConsciousnessAdapter>>,
    quantum_bridge: Arc<RwLock<QuantumBridgeAdapter>>,
    quantum_memory: Arc<RwLock<QuantumMemoryAdapter>>,
    cognitive_state: Arc<RwLock<CognitiveState>>,
    integration_history: Arc<RwLock<Vec<(DateTime<Utc>, String, serde_json::Value)>>>,
    active: Arc<RwLock<bool>>,
    iris_id: String,
}

#[pymethods]
impl IrisAdapter {
    #[new]
    fn new(config: Option<IrisConfig>) -> Self {
        let iris_id = Uuid::new_v4().to_string();
        let config = config.unwrap_or_else(IrisConfig::new);
        
        info!("Inicializando IrisAdapter com ID: {}", iris_id);
        
        Self {
            config: Arc::new(RwLock::new(config)),
            consciousness_adapter: Arc::new(RwLock::new(ConsciousnessAdapter::new())),
            quantum_bridge: Arc::new(RwLock::new(QuantumBridgeAdapter::new(Some(iris_id.clone())))),
            quantum_memory: Arc::new(RwLock::new(QuantumMemoryAdapter::new(None))),
            cognitive_state: Arc::new(RwLock::new(CognitiveState::new())),
            integration_history: Arc::new(RwLock::new(Vec::new())),
            active: Arc::new(RwLock::new(false)),
            iris_id,
        }
    }
    
    /// Ativa o sistema IRIS completo
    fn activate(&self) -> PyResult<()> {
        debug!("Ativando sistema IRIS: {}", self.iris_id);
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            let quantum_bridge = Arc::clone(&self.quantum_bridge);
            let quantum_memory = Arc::clone(&self.quantum_memory);
            let config = Arc::clone(&self.config);
            
            async move {
                let mut active_guard = active.write().await;
                let config_guard = config.read().await;
                
                // Ativar componentes baseado na configuração
                let consciousness = consciousness_adapter.read().await;
                if let Err(e) = consciousness.activate() {
                    error!("Falha ao ativar adaptador de consciência: {:?}", e);
                    return;
                }
                
                if config_guard.quantum_integration {
                    let bridge = quantum_bridge.read().await;
                    if let Err(e) = bridge.activate() {
                        error!("Falha ao ativar quantum bridge: {:?}", e);
                        return;
                    }
                    
                    let memory = quantum_memory.read().await;
                    if let Err(e) = memory.activate() {
                        error!("Falha ao ativar quantum memory: {:?}", e);
                        return;
                    }
                }
                
                *active_guard = true;
                info!("Sistema IRIS ativado com sucesso");
            }
        })?;
        
        Ok(())
    }
    
    /// Desativa o sistema IRIS
    fn deactivate(&self) -> PyResult<()> {
        debug!("Desativando sistema IRIS: {}", self.iris_id);
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            let quantum_bridge = Arc::clone(&self.quantum_bridge);
            let quantum_memory = Arc::clone(&self.quantum_memory);
            
            async move {
                let mut active_guard = active.write().await;
                
                // Desativar todos os componentes
                let consciousness = consciousness_adapter.read().await;
                let _ = consciousness.deactivate();
                
                let bridge = quantum_bridge.read().await;
                let _ = bridge.deactivate();
                
                let memory = quantum_memory.read().await;
                let _ = memory.deactivate();
                
                *active_guard = false;
                info!("Sistema IRIS desativado");
            }
        })?;
        
        Ok(())
    }
    
    /// Verifica se o sistema IRIS está ativo
    fn is_active(&self) -> PyResult<bool> {
        let result = pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            async move {
                let active_guard = active.read().await;
                *active_guard
            }
        })?;
        Ok(result)
    }
    
    /// Atualiza a configuração do IRIS
    fn update_config(&self, new_config: IrisConfig) -> PyResult<bool> {
        if !new_config.validate() {
            return Ok(false);
        }
        
        debug!("Atualizando configuração do IRIS");
        
        let result = pyo3_asyncio::run_in_async_thread({
            let config = Arc::clone(&self.config);
            let integration_history = Arc::clone(&self.integration_history);
            
            async move {
                let mut config_guard = config.write().await;
                let mut history_guard = integration_history.write().await;
                
                // Registrar mudança na história
                let event = serde_json::json!({
                    "event_type": "config_update",
                    "old_mode": format!("{:?}", config_guard.mode),
                    "new_mode": format!("{:?}", new_config.mode),
                    "changes": {
                        "evolution_enabled": new_config.evolution_enabled,
                        "quantum_integration": new_config.quantum_integration,
                        "consciousness_threshold": new_config.consciousness_threshold
                    }
                });
                
                history_guard.push((Utc::now(), "config_update".to_string(), event));
                
                // Limitar histórico
                if history_guard.len() > 1000 {
                    history_guard.remove(0);
                }
                
                *config_guard = new_config;
                info!("Configuração do IRIS atualizada");
                true
            }
        })?;
        
        Ok(result)
    }
    
    /// Processa informação de entrada e gera resposta integrada
    fn process_input(&self, input_data: String, context: Option<HashMap<String, String>>) -> PyResult<HashMap<String, PyObject>> {
        debug!("Processando entrada no IRIS: {} caracteres", input_data.len());
        
        let result = pyo3_asyncio::run_in_async_thread({
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            let quantum_memory = Arc::clone(&self.quantum_memory);
            let cognitive_state = Arc::clone(&self.cognitive_state);
            let config = Arc::clone(&self.config);
            let integration_history = Arc::clone(&self.integration_history);
            let iris_id = self.iris_id.clone();
            
            async move {
                let config_guard = config.read().await;
                let mut cognitive_guard = cognitive_state.write().await;
                let mut history_guard = integration_history.write().await;
                
                let gil = Python::acquire_gil();
                let py = gil.python();
                
                // Simular processamento cognitivo
                let processing_complexity = input_data.len() as f64 / 1000.0; // Normalizar
                let mode_multiplier = config_guard.mode.get_processing_power();
                
                // Atualizar estado cognitivo baseado no processamento
                cognitive_guard.attention_focus += processing_complexity * 0.1;
                cognitive_guard.pattern_recognition += processing_complexity * 0.15;
                cognitive_guard.normalize();
                
                // Criar resposta
                let mut response = HashMap::new();
                response.insert("iris_id".to_string(), iris_id.to_object(py));
                response.insert("processing_time".to_string(), (processing_complexity * mode_multiplier).to_object(py));
                response.insert("cognitive_performance".to_string(), cognitive_guard.get_overall_performance().to_object(py));
                response.insert("mode".to_string(), format!("{:?}", config_guard.mode).to_object(py));
                response.insert("confidence".to_string(), cognitive_guard.decision_confidence.to_object(py));
                
                // Determinar tipo de resposta baseado no modo
                let response_type = match config_guard.mode {
                    IrisMode::Reactive => "reactive_response",
                    IrisMode::Proactive => "proactive_suggestion",
                    IrisMode::Symbiotic => "symbiotic_integration",
                    IrisMode::Transcendent => "transcendent_insight",
                };
                response.insert("response_type".to_string(), response_type.to_object(py));
                
                // Simular conteúdo da resposta
                let response_content = format!(
                    "IRIS processou entrada com {} caracteres em modo {:?}. Confiança: {:.2}%",
                    input_data.len(),
                    config_guard.mode,
                    cognitive_guard.decision_confidence * 100.0
                );
                response.insert("content".to_string(), response_content.to_object(py));
                
                // Registrar processoção na história
                let event = serde_json::json!({
                    "event_type": "input_processing",
                    "input_length": input_data.len(),
                    "processing_complexity": processing_complexity,
                    "cognitive_performance": cognitive_guard.get_overall_performance(),
                    "mode": format!("{:?}", config_guard.mode),
                    "context": context
                });
                
                history_guard.push((Utc::now(), "input_processing".to_string(), event));
                
                // Armazenar na memória quântica se configurado
                if config_guard.quantum_integration {
                    let memory = quantum_memory.read().await;
                    let memory_block = QuantumMemoryBlock::new(
                        format!("Input: {} | Response: {}", input_data, response_content),
                        QuantumMemoryType::Working
                    );
                    
                    if let Ok(block_id) = memory.store_block(memory_block) {
                        response.insert("memory_block_id".to_string(), block_id.to_object(py));
                    }
                }
                
                info!("Entrada processada pelo IRIS com sucesso");
                response
            }
        })?;
        
        Ok(result)
    }
    
    /// Evolui o sistema IRIS para um nível superior
    fn evolve_mode(&self, target_mode: IrisMode) -> PyResult<bool> {
        debug!("Tentando evoluir IRIS para modo: {:?}", target_mode);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let config = Arc::clone(&self.config);
            let cognitive_state = Arc::clone(&self.cognitive_state);
            let integration_history = Arc::clone(&self.integration_history);
            
            async move {
                let mut config_guard = config.write().await;
                let cognitive_guard = cognitive_state.read().await;
                let mut history_guard = integration_history.write().await;
                
                if !config_guard.evolution_enabled {
                    warn!("Evolução desabilitada nas configurações");
                    return false;
                }
                
                if !config_guard.mode.can_evolve_to(target_mode) {
                    warn!("Evolução não possível do modo {:?} para {:?}", config_guard.mode, target_mode);
                    return false;
                }
                
                // Verificar se o desempenho cognitivo é suficiente
                let required_performance = target_mode.get_complexity_level();
                if cognitive_guard.get_overall_performance() < required_performance {
                    warn!("Desempenho cognitivo insuficiente para evolução");
                    return false;
                }
                
                let old_mode = config_guard.mode;
                config_guard.mode = target_mode;
                
                // Registrar evolução
                let event = serde_json::json!({
                    "event_type": "mode_evolution",
                    "from_mode": format!("{:?}", old_mode),
                    "to_mode": format!("{:?}", target_mode),
                    "cognitive_performance": cognitive_guard.get_overall_performance(),
                    "required_performance": required_performance
                });
                
                history_guard.push((Utc::now(), "mode_evolution".to_string(), event));
                
                info!("IRIS evoluiu de {:?} para {:?}", old_mode, target_mode);
                true
            }
        })?;
        
        Ok(result)
    }
    
    /// Obtém estado emocional integrado
    fn get_emotional_state(&self) -> PyResult<EmotionalState> {
        let result = pyo3_asyncio::run_in_async_thread({
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            
            async move {
                let consciousness = consciousness_adapter.read().await;
                consciousness.get_emotional_state()
            }
        })?;
        
        match result {
            Ok(state) => Ok(state),
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Erro ao obter estado emocional: {:?}", e)))
        }
    }
    
    /// Atualiza estado emocional
    fn update_emotional_state(&self, new_state: EmotionalState) -> PyResult<()> {
        pyo3_asyncio::run_in_async_thread({
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            let config = Arc::clone(&self.config);
            let cognitive_state = Arc::clone(&self.cognitive_state);
            
            async move {
                let consciousness = consciousness_adapter.read().await;
                let config_guard = config.read().await;
                let mut cognitive_guard = cognitive_state.write().await;
                
                if let Ok(()) = consciousness.update_emotional_state(new_state.clone()) {
                    // Ajustar estado cognitivo baseado na emoção
                    let emotional_impact = new_state.get_valence() * config_guard.emotional_sensitivity;
                    cognitive_guard.update_from_feedback(emotional_impact, config_guard.learning_acceleration);
                    
                    info!("Estado emocional do IRIS atualizado");
                }
            }
        })?;
        
        Ok(())
    }
    
    /// Obtém estatísticas integradas do IRIS
    fn get_integrated_stats(&self) -> PyResult<HashMap<String, PyObject>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let config = Arc::clone(&self.config);
            let cognitive_state = Arc::clone(&self.cognitive_state);
            let consciousness_adapter = Arc::clone(&self.consciousness_adapter);
            let quantum_bridge = Arc::clone(&self.quantum_bridge);
            let quantum_memory = Arc::clone(&self.quantum_memory);
            let integration_history = Arc::clone(&self.integration_history);
            
            async move {
                let config_guard = config.read().await;
                let cognitive_guard = cognitive_state.read().await;
                let history_guard = integration_history.read().await;
                
                let gil = Python::acquire_gil();
                let py = gil.python();
                
                let mut stats = HashMap::new();
                
                // Estatísticas básicas
                stats.insert("iris_id".to_string(), self.iris_id.to_object(py));
                stats.insert("mode".to_string(), format!("{:?}", config_guard.mode).to_object(py));
                stats.insert("cognitive_performance".to_string(), cognitive_guard.get_overall_performance().to_object(py));
                stats.insert("complexity_level".to_string(), config_guard.mode.get_complexity_level().to_object(py));
                stats.insert("processing_power".to_string(), config_guard.mode.get_processing_power().to_object(py));
                stats.insert("evolution_enabled".to_string(), config_guard.evolution_enabled.to_object(py));
                stats.insert("quantum_integration".to_string(), config_guard.quantum_integration.to_object(py));
                stats.insert("total_integrations".to_string(), history_guard.len().to_object(py));
                
                // Estatísticas dos componentes
                let consciousness = consciousness_adapter.read().await;
                if let Ok(evo_stats) = consciousness.get_evolution_stats() {
                    for (key, value) in evo_stats {
                        stats.insert(format!("consciousness_{}", key), value.to_object(py));
                    }
                }
                
                if config_guard.quantum_integration {
                    let bridge = quantum_bridge.read().await;
                    if let Ok(bridge_stats) = bridge.get_stats() {
                        for (key, value) in bridge_stats {
                            stats.insert(format!("quantum_bridge_{}", key), value.to_object(py));
                        }
                    }
                    
                    let memory = quantum_memory.read().await;
                    if let Ok(memory_stats) = memory.get_stats() {
                        for (key, value) in memory_stats {
                            stats.insert(format!("quantum_memory_{}", key), value.to_object(py));
                        }
                    }
                }
                
                stats
            }
        })?;
        
        Ok(result)
    }
    
    fn get_iris_id(&self) -> String {
        self.iris_id.clone()
    }
    
    fn __str__(&self) -> String {
        format!("IrisAdapter(id={}, active=unknown)", &self.iris_id[..8])
    }
    
    fn __repr__(&self) -> String {
        format!("IrisAdapter(iris_id='{}')", self.iris_id)
    }
}

impl Default for IrisAdapter {
    fn default() -> Self {
        Self::new(None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_iris_mode() {
        assert_eq!(IrisMode::Reactive.get_complexity_level(), 0.25);
        assert_eq!(IrisMode::Transcendent.get_complexity_level(), 1.0);
        assert!(IrisMode::Reactive.can_evolve_to(IrisMode::Proactive));
        assert!(!IrisMode::Transcendent.can_evolve_to(IrisMode::Reactive));
    }
    
    #[test]
    fn test_cognitive_state() {
        let mut state = CognitiveState::new();
        assert_eq!(state.get_overall_performance(), 0.5);
        
        state.update_from_feedback(0.2, 1.0);
        assert!(state.get_overall_performance() > 0.5);
        
        // Testar normalização
        state.attention_focus = 2.0;
        state.normalize();
        assert_eq!(state.attention_focus, 1.0);
    }
    
    #[test]
    fn test_iris_config() {
        let config = IrisConfig::new();
        assert!(config.validate());
        
        let mut invalid_config = config;
        invalid_config.consciousness_threshold = 2.0;
        assert!(!invalid_config.validate());
    }
    
    #[tokio::test]
    async fn test_iris_adapter() {
        let adapter = IrisAdapter::new(None);
        
        // Testar ID único
        assert!(!adapter.get_iris_id().is_empty());
        
        // Testar estado inicial
        let initial_active = adapter.active.read().await;
        assert!(!*initial_active);
        
        // Testar configuração inicial
        let initial_config = adapter.config.read().await;
        assert_eq!(initial_config.mode, IrisMode::Reactive);
    }
}

