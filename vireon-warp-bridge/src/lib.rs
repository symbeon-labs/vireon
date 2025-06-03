//! VIREON WARP Bridge Integration
//!
//! Este módulo fornece integração entre o VIREON e o sistema WARP,
//! implementando comunicação simbiótica e transcendência quântica.

mod quantum_bridge;
pub use quantum_bridge::{WarpBridge, WarpMessage, ConnectionState};

use anyhow::{Result, Context};
use tracing::{info, warn};
use serde::{Serialize, Deserialize};

/// Configuração do WARP Bridge
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WarpBridgeConfig {
    /// Tamanho do buffer de mensagens
    pub buffer_size: usize,
    
    /// Intervalo de heartbeat em milissegundos
    pub heartbeat_interval: u64,
    
    /// Timeout de conexão em segundos
    pub connection_timeout: u64,
}

impl Default for WarpBridgeConfig {
    fn default() -> Self {
        Self {
            buffer_size: 100,
            heartbeat_interval: 1000,
            connection_timeout: 30,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::time::Duration;

    #[tokio::test]
    async fn test_warp_bridge_config() {
        let config = WarpBridgeConfig::default();
        assert_eq!(config.buffer_size, 100);
        assert_eq!(config.heartbeat_interval, 1000);
        assert_eq!(config.connection_timeout, 30);
    }
}

