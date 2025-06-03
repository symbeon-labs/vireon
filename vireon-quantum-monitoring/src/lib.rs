//! VIREON Quantum Monitoring System
//!
//! Este módulo implementa o sistema de monitoramento quântico do VIREON,
//! responsável por observar e registrar estados quânticos do sistema.

mod quantum_state;
pub use quantum_state::{QuantumMonitor, QuantumState, QuantumEvent, QuantumAlert};

use anyhow::Result;
use tracing::{info, warn};
use serde::{Serialize, Deserialize};
use tokio::time::Duration;

/// Configuração do monitor quântico
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumMonitorConfig {
    /// Intervalo de monitoramento em milissegundos
    pub monitoring_interval: u64,
    
    /// Limite de alerta para coerência
    pub coherence_threshold: f64,
    
    /// Capacidade máxima da memória quântica
    pub quantum_memory_capacity: usize,
}

impl Default for QuantumMonitorConfig {
    fn default() -> Self {
        Self {
            monitoring_interval: 1000,
            coherence_threshold: 0.5,
            quantum_memory_capacity: 1000,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quantum_monitor_config() {
        let config = QuantumMonitorConfig::default();
        assert_eq!(config.monitoring_interval, 1000);
        assert_eq!(config.coherence_threshold, 0.5);
        assert_eq!(config.quantum_memory_capacity, 1000);
    }
}

