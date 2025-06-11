//! # Adaptador QuantumBridge
//!
//! Este módulo implementa a interface FFI para o QuantumBridge do VIREON,
//! permitindo comunicação quântica segura entre componentes Rust e Python.

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{RwLock, Mutex};
use tracing::{debug, info, warn, error};
use chrono::{DateTime, Utc};
use uuid::Uuid;

/// Estados de conexão quântica
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[pyclass]
pub enum QuantumConnectionState {
    Disconnected,
    Connecting,
    Connected,
    Entangled,
    Superposition,
    Error,
}

#[pymethods]
impl QuantumConnectionState {
    #[new]
    fn new() -> Self {
        QuantumConnectionState::Disconnected
    }
    
    fn is_active(&self) -> bool {
        matches!(self, 
            QuantumConnectionState::Connected | 
            QuantumConnectionState::Entangled | 
            QuantumConnectionState::Superposition
        )
    }
    
    fn to_string(&self) -> String {
        format!("{:?}", self)
    }
    
    fn __str__(&self) -> String {
        self.to_string()
    }
    
    fn __repr__(&self) -> String {
        format!("QuantumConnectionState::{:?}", self)
    }
}

/// Configuração de canal quântico
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct QuantumChannelConfig {
    #[pyo3(get, set)]
    pub channel_id: String,
    #[pyo3(get, set)]
    pub entanglement_strength: f64,
    #[pyo3(get, set)]
    pub coherence_time: f64,
    #[pyo3(get, set)]
    pub error_correction: bool,
    #[pyo3(get, set)]
    pub encryption_level: i32,
    #[pyo3(get, set)]
    pub max_transmission_rate: f64,
}

#[pymethods]
impl QuantumChannelConfig {
    #[new]
    fn new(channel_id: Option<String>) -> Self {
        Self {
            channel_id: channel_id.unwrap_or_else(|| Uuid::new_v4().to_string()),
            entanglement_strength: 1.0,
            coherence_time: 1000.0,
            error_correction: true,
            encryption_level: 256,
            max_transmission_rate: 1000.0,
        }
    }
    
    fn validate(&self) -> bool {
        self.entanglement_strength >= 0.0 && self.entanglement_strength <= 1.0 &&
        self.coherence_time > 0.0 &&
        self.encryption_level > 0 &&
        self.max_transmission_rate > 0.0
    }
    
    fn to_dict(&self) -> HashMap<String, PyObject> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        
        let mut result = HashMap::new();
        result.insert("channel_id".to_string(), self.channel_id.to_object(py));
        result.insert("entanglement_strength".to_string(), self.entanglement_strength.to_object(py));
        result.insert("coherence_time".to_string(), self.coherence_time.to_object(py));
        result.insert("error_correction".to_string(), self.error_correction.to_object(py));
        result.insert("encryption_level".to_string(), self.encryption_level.to_object(py));
        result.insert("max_transmission_rate".to_string(), self.max_transmission_rate.to_object(py));
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "QuantumChannelConfig(id={}, strength={:.2}, coherence={:.2})",
            self.channel_id,
            self.entanglement_strength,
            self.coherence_time
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "QuantumChannelConfig(channel_id='{}', entanglement_strength={}, coherence_time={}, error_correction={}, encryption_level={}, max_transmission_rate={})",
            self.channel_id,
            self.entanglement_strength,
            self.coherence_time,
            self.error_correction,
            self.encryption_level,
            self.max_transmission_rate
        )
    }
}

/// Mensagem quântica para transmissão
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct QuantumMessage {
    #[pyo3(get, set)]
    pub id: String,
    #[pyo3(get, set)]
    pub sender: String,
    #[pyo3(get, set)]
    pub receiver: String,
    #[pyo3(get, set)]
    pub payload: String,
    #[pyo3(get, set)]
    pub timestamp: String,
    #[pyo3(get, set)]
    pub quantum_signature: String,
    #[pyo3(get, set)]
    pub entanglement_id: Option<String>,
}

#[pymethods]
impl QuantumMessage {
    #[new]
    fn new(sender: String, receiver: String, payload: String) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            sender,
            receiver,
            payload,
            timestamp: Utc::now().to_rfc3339(),
            quantum_signature: Uuid::new_v4().to_string(), // Simulação de assinatura quântica
            entanglement_id: None,
        }
    }
    
    fn set_entanglement(&mut self, entanglement_id: String) {
        self.entanglement_id = Some(entanglement_id);
    }
    
    fn is_entangled(&self) -> bool {
        self.entanglement_id.is_some()
    }
    
    fn get_size(&self) -> usize {
        self.payload.len()
    }
    
    fn validate_signature(&self, expected_signature: String) -> bool {
        self.quantum_signature == expected_signature
    }
    
    fn to_dict(&self) -> HashMap<String, PyObject> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        
        let mut result = HashMap::new();
        result.insert("id".to_string(), self.id.to_object(py));
        result.insert("sender".to_string(), self.sender.to_object(py));
        result.insert("receiver".to_string(), self.receiver.to_object(py));
        result.insert("payload".to_string(), self.payload.to_object(py));
        result.insert("timestamp".to_string(), self.timestamp.to_object(py));
        result.insert("quantum_signature".to_string(), self.quantum_signature.to_object(py));
        result.insert("entanglement_id".to_string(), self.entanglement_id.to_object(py));
        result.insert("size".to_string(), self.get_size().to_object(py));
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "QuantumMessage(id={}, from={}, to={}, size={})",
            &self.id[..8],
            self.sender,
            self.receiver,
            self.get_size()
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "QuantumMessage(id='{}', sender='{}', receiver='{}', payload_len={}, entangled={})",
            self.id,
            self.sender,
            self.receiver,
            self.get_size(),
            self.is_entangled()
        )
    }
}

/// Estatísticas de transmissão quântica
#[derive(Debug, Clone, Default)]
struct QuantumStats {
    total_messages: u64,
    successful_transmissions: u64,
    failed_transmissions: u64,
    total_bytes_transmitted: u64,
    average_latency: f64,
    quantum_fidelity: f64,
}

/// Adaptador principal para QuantumBridge
#[derive(Debug)]
#[pyclass]
pub struct QuantumBridgeAdapter {
    connection_state: Arc<RwLock<QuantumConnectionState>>,
    active_channels: Arc<RwLock<HashMap<String, QuantumChannelConfig>>>,
    message_queue: Arc<Mutex<Vec<QuantumMessage>>>,
    stats: Arc<RwLock<QuantumStats>>,
    node_id: String,
    active: Arc<RwLock<bool>>,
}

#[pymethods]
impl QuantumBridgeAdapter {
    #[new]
    fn new(node_id: Option<String>) -> Self {
        let node_id = node_id.unwrap_or_else(|| Uuid::new_v4().to_string());
        info!("Inicializando QuantumBridgeAdapter para nó: {}", node_id);
        
        Self {
            connection_state: Arc::new(RwLock::new(QuantumConnectionState::Disconnected)),
            active_channels: Arc::new(RwLock::new(HashMap::new())),
            message_queue: Arc::new(Mutex::new(Vec::new())),
            stats: Arc::new(RwLock::new(QuantumStats::default())),
            node_id,
            active: Arc::new(RwLock::new(false)),
        }
    }
    
    /// Ativa o adaptador QuantumBridge
    fn activate(&self) -> PyResult<()> {
        debug!("Ativando QuantumBridgeAdapter");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            let connection_state = Arc::clone(&self.connection_state);
            
            async move {
                let mut active_guard = active.write().await;
                let mut state_guard = connection_state.write().await;
                
                *active_guard = true;
                *state_guard = QuantumConnectionState::Connecting;
                
                // Simular processo de conexão
                tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
                *state_guard = QuantumConnectionState::Connected;
                
                info!("QuantumBridgeAdapter ativado e conectado");
            }
        })?;
        
        Ok(())
    }
    
    /// Desativa o adaptador
    fn deactivate(&self) -> PyResult<()> {
        debug!("Desativando QuantumBridgeAdapter");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            let connection_state = Arc::clone(&self.connection_state);
            let active_channels = Arc::clone(&self.active_channels);
            
            async move {
                let mut active_guard = active.write().await;
                let mut state_guard = connection_state.write().await;
                let mut channels_guard = active_channels.write().await;
                
                *active_guard = false;
                *state_guard = QuantumConnectionState::Disconnected;
                channels_guard.clear();
                
                info!("QuantumBridgeAdapter desativado");
            }
        })?;
        
        Ok(())
    }
    
    /// Verifica se o adaptador está ativo
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
    
    /// Obtém o estado da conexão
    fn get_connection_state(&self) -> PyResult<QuantumConnectionState> {
        let result = pyo3_asyncio::run_in_async_thread({
            let connection_state = Arc::clone(&self.connection_state);
            async move {
                let state_guard = connection_state.read().await;
                *state_guard
            }
        })?;
        Ok(result)
    }
    
    /// Cria um novo canal quântico
    fn create_channel(&self, config: QuantumChannelConfig) -> PyResult<bool> {
        if !config.validate() {
            return Ok(false);
        }
        
        debug!("Criando canal quântico: {}", config.channel_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let active_channels = Arc::clone(&self.active_channels);
            let connection_state = Arc::clone(&self.connection_state);
            
            async move {
                let state_guard = connection_state.read().await;
                if !state_guard.is_active() {
                    return false;
                }
                
                let mut channels_guard = active_channels.write().await;
                channels_guard.insert(config.channel_id.clone(), config);
                
                info!("Canal quântico criado com sucesso");
                true
            }
        })?;
        
        Ok(result)
    }
    
    /// Remove um canal quântico
    fn remove_channel(&self, channel_id: String) -> PyResult<bool> {
        debug!("Removendo canal quântico: {}", channel_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let active_channels = Arc::clone(&self.active_channels);
            
            async move {
                let mut channels_guard = active_channels.write().await;
                let removed = channels_guard.remove(&channel_id).is_some();
                
                if removed {
                    info!("Canal quântico removido: {}", channel_id);
                } else {
                    warn!("Tentativa de remover canal inexistente: {}", channel_id);
                }
                
                removed
            }
        })?;
        
        Ok(result)
    }
    
    /// Lista canais ativos
    fn list_channels(&self) -> PyResult<Vec<String>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let active_channels = Arc::clone(&self.active_channels);
            
            async move {
                let channels_guard = active_channels.read().await;
                channels_guard.keys().cloned().collect()
            }
        })?;
        
        Ok(result)
    }
    
    /// Envia uma mensagem quântica
    fn send_message(&self, message: QuantumMessage, channel_id: String) -> PyResult<bool> {
        debug!("Enviando mensagem quântica via canal: {}", channel_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let active_channels = Arc::clone(&self.active_channels);
            let stats = Arc::clone(&self.stats);
            let connection_state = Arc::clone(&self.connection_state);
            
            async move {
                let state_guard = connection_state.read().await;
                if !state_guard.is_active() {
                    return false;
                }
                
                let channels_guard = active_channels.read().await;
                if !channels_guard.contains_key(&channel_id) {
                    warn!("Tentativa de envio em canal inexistente: {}", channel_id);
                    return false;
                }
                
                // Simular transmissão
                let transmission_success = rand::random::<f64>() > 0.05; // 95% de sucesso
                
                let mut stats_guard = stats.write().await;
                stats_guard.total_messages += 1;
                stats_guard.total_bytes_transmitted += message.get_size() as u64;
                
                if transmission_success {
                    stats_guard.successful_transmissions += 1;
                    info!("Mensagem quântica enviada com sucesso: {}", message.id);
                } else {
                    stats_guard.failed_transmissions += 1;
                    warn!("Falha na transmissão da mensagem: {}", message.id);
                }
                
                transmission_success
            }
        })?;
        
        Ok(result)
    }
    
    /// Recebe mensagens da fila
    fn receive_messages(&self) -> PyResult<Vec<QuantumMessage>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let message_queue = Arc::clone(&self.message_queue);
            
            async move {
                let mut queue_guard = message_queue.lock().await;
                let messages = queue_guard.drain(..).collect();
                messages
            }
        })?;
        
        if !result.is_empty() {
            debug!("Recebidas {} mensagens da fila", result.len());
        }
        
        Ok(result)
    }
    
    /// Estabelece emaranhamento quântico
    fn establish_entanglement(&self, target_node: String, channel_id: String) -> PyResult<String> {
        debug!("Estabelecendo emaranhamento com nó: {} via canal: {}", target_node, channel_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let active_channels = Arc::clone(&self.active_channels);
            let connection_state = Arc::clone(&self.connection_state);
            
            async move {
                let channels_guard = active_channels.read().await;
                let mut state_guard = connection_state.write().await;
                
                if !channels_guard.contains_key(&channel_id) {
                    return None;
                }
                
                // Simular estabelecimento de emaranhamento
                tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
                *state_guard = QuantumConnectionState::Entangled;
                
                let entanglement_id = Uuid::new_v4().to_string();
                info!("Emaranhamento estabelecido: {}", entanglement_id);
                
                Some(entanglement_id)
            }
        })?;
        
        result.ok_or_else(|| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Falha ao estabelecer emaranhamento"))
    }
    
    /// Obtém estatísticas de transmissão
    fn get_stats(&self) -> PyResult<HashMap<String, f64>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let stats = Arc::clone(&self.stats);
            
            async move {
                let stats_guard = stats.read().await;
                let mut result = HashMap::new();
                
                result.insert("total_messages".to_string(), stats_guard.total_messages as f64);
                result.insert("successful_transmissions".to_string(), stats_guard.successful_transmissions as f64);
                result.insert("failed_transmissions".to_string(), stats_guard.failed_transmissions as f64);
                result.insert("total_bytes_transmitted".to_string(), stats_guard.total_bytes_transmitted as f64);
                
                let success_rate = if stats_guard.total_messages > 0 {
                    stats_guard.successful_transmissions as f64 / stats_guard.total_messages as f64
                } else {
                    0.0
                };
                result.insert("success_rate".to_string(), success_rate);
                result.insert("quantum_fidelity".to_string(), stats_guard.quantum_fidelity);
                
                result
            }
        })?;
        
        Ok(result)
    }
    
    /// Reseta estatísticas
    fn reset_stats(&self) -> PyResult<()> {
        pyo3_asyncio::run_in_async_thread({
            let stats = Arc::clone(&self.stats);
            
            async move {
                let mut stats_guard = stats.write().await;
                *stats_guard = QuantumStats::default();
                info!("Estatísticas resetadas");
            }
        })?;
        
        Ok(())
    }
    
    fn get_node_id(&self) -> String {
        self.node_id.clone()
    }
    
    fn __str__(&self) -> String {
        format!("QuantumBridgeAdapter(node_id={}, active=unknown)", self.node_id)
    }
    
    fn __repr__(&self) -> String {
        format!("QuantumBridgeAdapter(node_id='{}')", self.node_id)
    }
}

impl Default for QuantumBridgeAdapter {
    fn default() -> Self {
        Self::new(None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_quantum_connection_state() {
        let state = QuantumConnectionState::Connected;
        assert!(state.is_active());
        
        let state = QuantumConnectionState::Disconnected;
        assert!(!state.is_active());
    }
    
    #[test]
    fn test_quantum_channel_config() {
        let config = QuantumChannelConfig::new(Some("test_channel".to_string()));
        assert!(config.validate());
        assert_eq!(config.channel_id, "test_channel");
        
        let mut invalid_config = config;
        invalid_config.entanglement_strength = -1.0;
        assert!(!invalid_config.validate());
    }
    
    #[test]
    fn test_quantum_message() {
        let message = QuantumMessage::new(
            "sender".to_string(),
            "receiver".to_string(),
            "test payload".to_string()
        );
        
        assert_eq!(message.sender, "sender");
        assert_eq!(message.receiver, "receiver");
        assert_eq!(message.get_size(), "test payload".len());
        assert!(!message.is_entangled());
    }
    
    #[tokio::test]
    async fn test_quantum_bridge_adapter() {
        let adapter = QuantumBridgeAdapter::new(Some("test_node".to_string()));
        
        // Testar estado inicial
        let initial_state = adapter.connection_state.read().await;
        assert_eq!(*initial_state, QuantumConnectionState::Disconnected);
        
        // Testar nó ID
        assert_eq!(adapter.get_node_id(), "test_node");
        
        // Testar canais vazios
        let channels = adapter.active_channels.read().await;
        assert!(channels.is_empty());
    }
}

