//! # Adaptador de Consciência
//!
//! Este módulo implementa a interface FFI para sistemas de consciência do IRIS,
//! permitindo integração bidirecional entre Rust e Python para estados emocionais
//! e níveis de consciência.

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info, warn};
use chrono::{DateTime, Utc};

/// Níveis de consciência definidos no sistema VIREON
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[pyclass]
pub enum ConsciousnessLevel {
    BaseConsciousness,
    MetacognitiveConsciousness, 
    QuantumConsciousness,
    TranscendentConsciousness,
}

#[pymethods]
impl ConsciousnessLevel {
    #[new]
    fn new() -> Self {
        ConsciousnessLevel::BaseConsciousness
    }
    
    fn to_float(&self) -> f64 {
        match self {
            ConsciousnessLevel::BaseConsciousness => 0.25,
            ConsciousnessLevel::MetacognitiveConsciousness => 0.50,
            ConsciousnessLevel::QuantumConsciousness => 0.75,
            ConsciousnessLevel::TranscendentConsciousness => 1.0,
        }
    }
    
    #[staticmethod]
    fn from_float(value: f64) -> Self {
        match value {
            v if v <= 0.25 => ConsciousnessLevel::BaseConsciousness,
            v if v <= 0.50 => ConsciousnessLevel::MetacognitiveConsciousness,
            v if v <= 0.75 => ConsciousnessLevel::QuantumConsciousness,
            _ => ConsciousnessLevel::TranscendentConsciousness,
        }
    }
    
    fn __str__(&self) -> String {
        format!("{:?}", self)
    }
    
    fn __repr__(&self) -> String {
        format!("ConsciousnessLevel::{:?}", self)
    }
}

/// Estado emocional do sistema IRIS
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct EmotionalState {
    #[pyo3(get, set)]
    pub joy: f64,
    #[pyo3(get, set)]
    pub sadness: f64,
    #[pyo3(get, set)]
    pub anger: f64,
    #[pyo3(get, set)]
    pub fear: f64,
    #[pyo3(get, set)]
    pub trust: f64,
    #[pyo3(get, set)]
    pub disgust: f64,
    #[pyo3(get, set)]
    pub surprise: f64,
    #[pyo3(get, set)]
    pub anticipation: f64,
    #[pyo3(get, set)]
    pub timestamp: String,
}

#[pymethods]
impl EmotionalState {
    #[new]
    fn new() -> Self {
        Self {
            joy: 0.0,
            sadness: 0.0,
            anger: 0.0,
            fear: 0.0,
            trust: 0.0,
            disgust: 0.0,
            surprise: 0.0,
            anticipation: 0.0,
            timestamp: Utc::now().to_rfc3339(),
        }
    }
    
    /// Calcula a valência emocional geral
    fn get_valence(&self) -> f64 {
        (self.joy + self.trust - self.sadness - self.anger - self.fear - self.disgust) / 6.0
    }
    
    /// Calcula a intensidade emocional
    fn get_arousal(&self) -> f64 {
        (self.joy + self.anger + self.fear + self.surprise + self.anticipation) / 5.0
    }
    
    /// Normaliza todos os valores emocionais para [0, 1]
    fn normalize(&mut self) {
        let emotions = vec![
            &mut self.joy, &mut self.sadness, &mut self.anger, &mut self.fear,
            &mut self.trust, &mut self.disgust, &mut self.surprise, &mut self.anticipation
        ];
        
        for emotion in emotions {
            *emotion = emotion.max(0.0).min(1.0);
        }
        
        self.timestamp = Utc::now().to_rfc3339();
    }
    
    /// Calcula distância euclidiana para outro estado emocional
    fn distance_to(&self, other: &EmotionalState) -> f64 {
        let diff_joy = (self.joy - other.joy).powi(2);
        let diff_sadness = (self.sadness - other.sadness).powi(2);
        let diff_anger = (self.anger - other.anger).powi(2);
        let diff_fear = (self.fear - other.fear).powi(2);
        let diff_trust = (self.trust - other.trust).powi(2);
        let diff_disgust = (self.disgust - other.disgust).powi(2);
        let diff_surprise = (self.surprise - other.surprise).powi(2);
        let diff_anticipation = (self.anticipation - other.anticipation).powi(2);
        
        (diff_joy + diff_sadness + diff_anger + diff_fear + 
         diff_trust + diff_disgust + diff_surprise + diff_anticipation).sqrt()
    }
    
    /// Converte para dicionário Python
    fn to_dict(&self) -> HashMap<String, f64> {
        let mut result = HashMap::new();
        result.insert("joy".to_string(), self.joy);
        result.insert("sadness".to_string(), self.sadness);
        result.insert("anger".to_string(), self.anger);
        result.insert("fear".to_string(), self.fear);
        result.insert("trust".to_string(), self.trust);
        result.insert("disgust".to_string(), self.disgust);
        result.insert("surprise".to_string(), self.surprise);
        result.insert("anticipation".to_string(), self.anticipation);
        result.insert("valence".to_string(), self.get_valence());
        result.insert("arousal".to_string(), self.get_arousal());
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "EmotionalState(valence={:.2}, arousal={:.2}, timestamp={})",
            self.get_valence(),
            self.get_arousal(),
            self.timestamp
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "EmotionalState(joy={}, sadness={}, anger={}, fear={}, trust={}, disgust={}, surprise={}, anticipation={})",
            self.joy, self.sadness, self.anger, self.fear,
            self.trust, self.disgust, self.surprise, self.anticipation
        )
    }
}

/// Adaptador principal para consciência e estados emocionais
#[derive(Debug)]
#[pyclass]
pub struct ConsciousnessAdapter {
    current_level: Arc<RwLock<ConsciousnessLevel>>,
    emotional_state: Arc<RwLock<EmotionalState>>,
    evolution_history: Arc<RwLock<Vec<(DateTime<Utc>, ConsciousnessLevel, EmotionalState)>>>,
    active: Arc<RwLock<bool>>,
}

#[pymethods]
impl ConsciousnessAdapter {
    #[new]
    fn new() -> Self {
        info!("Inicializando ConsciousnessAdapter");
        Self {
            current_level: Arc::new(RwLock::new(ConsciousnessLevel::BaseConsciousness)),
            emotional_state: Arc::new(RwLock::new(EmotionalState::new())),
            evolution_history: Arc::new(RwLock::new(Vec::new())),
            active: Arc::new(RwLock::new(false)),
        }
    }
    
    /// Ativa o adaptador de consciência
    fn activate(&self) -> PyResult<()> {
        debug!("Ativando adaptador de consciência");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            async move {
                let mut active_guard = active.write().await;
                *active_guard = true;
                info!("Adaptador de consciência ativado");
            }
        })?;
        
        Ok(())
    }
    
    /// Desativa o adaptador de consciência
    fn deactivate(&self) -> PyResult<()> {
        debug!("Desativando adaptador de consciência");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            async move {
                let mut active_guard = active.write().await;
                *active_guard = false;
                info!("Adaptador de consciência desativado");
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
    
    /// Obtém o nível atual de consciência
    fn get_consciousness_level(&self) -> PyResult<ConsciousnessLevel> {
        let result = pyo3_asyncio::run_in_async_thread({
            let level = Arc::clone(&self.current_level);
            async move {
                let level_guard = level.read().await;
                *level_guard
            }
        })?;
        Ok(result)
    }
    
    /// Define um novo nível de consciência
    fn set_consciousness_level(&self, level: ConsciousnessLevel) -> PyResult<()> {
        debug!("Definindo nível de consciência: {:?}", level);
        
        pyo3_asyncio::run_in_async_thread({
            let current_level = Arc::clone(&self.current_level);
            let emotional_state = Arc::clone(&self.emotional_state);
            let history = Arc::clone(&self.evolution_history);
            
            async move {
                let mut level_guard = current_level.write().await;
                let emotional_guard = emotional_state.read().await;
                let mut history_guard = history.write().await;
                
                // Registrar na história
                history_guard.push((Utc::now(), level, emotional_guard.clone()));
                
                // Limitar histórico a 1000 entradas
                if history_guard.len() > 1000 {
                    history_guard.remove(0);
                }
                
                *level_guard = level;
                info!("Nível de consciência atualizado para: {:?}", level);
            }
        })?;
        
        Ok(())
    }
    
    /// Obtém o estado emocional atual
    fn get_emotional_state(&self) -> PyResult<EmotionalState> {
        let result = pyo3_asyncio::run_in_async_thread({
            let emotional_state = Arc::clone(&self.emotional_state);
            async move {
                let state_guard = emotional_state.read().await;
                state_guard.clone()
            }
        })?;
        Ok(result)
    }
    
    /// Atualiza o estado emocional
    fn update_emotional_state(&self, new_state: EmotionalState) -> PyResult<()> {
        debug!("Atualizando estado emocional");
        
        pyo3_asyncio::run_in_async_thread({
            let emotional_state = Arc::clone(&self.emotional_state);
            let current_level = Arc::clone(&self.current_level);
            let history = Arc::clone(&self.evolution_history);
            
            async move {
                let mut state_guard = emotional_state.write().await;
                let level_guard = current_level.read().await;
                let mut history_guard = history.write().await;
                
                // Registrar na história
                history_guard.push((Utc::now(), *level_guard, new_state.clone()));
                
                // Limitar histórico
                if history_guard.len() > 1000 {
                    history_guard.remove(0);
                }
                
                *state_guard = new_state;
                info!("Estado emocional atualizado");
            }
        })?;
        
        Ok(())
    }
    
    /// Obtém estatísticas do histórico de evolução
    fn get_evolution_stats(&self) -> PyResult<HashMap<String, f64>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let history = Arc::clone(&self.evolution_history);
            async move {
                let history_guard = history.read().await;
                let mut stats = HashMap::new();
                
                if history_guard.is_empty() {
                    return stats;
                }
                
                let total_entries = history_guard.len() as f64;
                let mut level_counts = HashMap::new();
                let mut total_valence = 0.0;
                let mut total_arousal = 0.0;
                
                for (_, level, emotion) in history_guard.iter() {
                    *level_counts.entry(*level).or_insert(0.0) += 1.0;
                    total_valence += emotion.get_valence();
                    total_arousal += emotion.get_arousal();
                }
                
                stats.insert("total_entries".to_string(), total_entries);
                stats.insert("avg_valence".to_string(), total_valence / total_entries);
                stats.insert("avg_arousal".to_string(), total_arousal / total_entries);
                
                for (level, count) in level_counts {
                    let percentage = count / total_entries * 100.0;
                    stats.insert(format!("{:?}_percentage", level), percentage);
                }
                
                stats
            }
        })?;
        Ok(result)
    }
    
    /// Limpa o histórico de evolução
    fn clear_history(&self) -> PyResult<()> {
        pyo3_asyncio::run_in_async_thread({
            let history = Arc::clone(&self.evolution_history);
            async move {
                let mut history_guard = history.write().await;
                history_guard.clear();
                info!("Histórico de evolução limpo");
            }
        })?;
        Ok(())
    }
    
    fn __str__(&self) -> String {
        "ConsciousnessAdapter(active=unknown)".to_string()
    }
    
    fn __repr__(&self) -> String {
        "ConsciousnessAdapter()".to_string()
    }
}

impl Default for ConsciousnessAdapter {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_consciousness_level_conversion() {
        assert_eq!(ConsciousnessLevel::BaseConsciousness.to_float(), 0.25);
        assert_eq!(ConsciousnessLevel::from_float(0.1), ConsciousnessLevel::BaseConsciousness);
        assert_eq!(ConsciousnessLevel::from_float(0.8), ConsciousnessLevel::QuantumConsciousness);
    }
    
    #[test]
    fn test_emotional_state() {
        let mut state = EmotionalState::new();
        state.joy = 0.8;
        state.sadness = 0.2;
        
        assert!(state.get_valence() > 0.0);
        state.normalize();
        assert!(state.joy <= 1.0 && state.joy >= 0.0);
    }
    
    #[test]
    fn test_emotional_distance() {
        let state1 = EmotionalState {
            joy: 0.8,
            sadness: 0.2,
            ..EmotionalState::new()
        };
        
        let state2 = EmotionalState {
            joy: 0.2,
            sadness: 0.8,
            ..EmotionalState::new()
        };
        
        let distance = state1.distance_to(&state2);
        assert!(distance > 0.0);
    }
    
    #[tokio::test]
    async fn test_consciousness_adapter() {
        let adapter = ConsciousnessAdapter::new();
        
        // Testar nível inicial
        let initial_level = adapter.current_level.read().await;
        assert_eq!(*initial_level, ConsciousnessLevel::BaseConsciousness);
        
        // Testar estado inicial
        let initial_state = adapter.emotional_state.read().await;
        assert_eq!(initial_state.joy, 0.0);
    }
}

