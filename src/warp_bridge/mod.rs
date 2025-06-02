//! Módulo de integração entre VIREON e Warp
//!
//! Este módulo fornece a infraestrutura necessária para integração simbiótica
//! entre o sistema VIREON e o Warp, incluindo:
//! - Validação quântica de regras
//! - Bridge de comunicação bidirecional
//! - Cache e otimização de validações
//! - Feedback para evolução de consciência

mod validation_bridge;

use anyhow::Result;
use serde::{Serialize, Deserialize};
use std::sync::Arc;

// Re-exports públicos
pub use validation_bridge::{
    ValidationBridge,
    WarpRuleValidation,
    ValidationStats,
};

/// Configuração do Bridge Warp
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WarpBridgeConfig {
    /// URL do Redis para cache
    pub redis_url: String,
    
    /// Tamanho do cache LRU
    pub cache_size: usize,
    
    /// Tempo de expiração do cache em segundos
    pub cache_ttl: u64,
    
    /// Nível mínimo de consciência requerido
    pub min_consciousness_level: crate::consciousness::ConsciousnessLevel,
}

impl Default for WarpBridgeConfig {
    fn default() -> Self {
        Self {
            redis_url: "redis://localhost".to_string(),
            cache_size: 1000,
            cache_ttl: 3600,
            min_consciousness_level: crate::consciousness::ConsciousnessLevel::Base,
        }
    }
}

/// Interface principal do Bridge Warp
#[async_trait::async_trait]
pub trait WarpBridge: Send + Sync {
    /// Valida regra com verificação quântica
    async fn validate_rule(&self, rule_id: &str) -> Result<WarpRuleValidation>;
    
    /// Obtém estatísticas do bridge
    async fn get_statistics(&self) -> Result<ValidationStats>;
    
    /// Limpa cache de validações
    async fn clear_cache(&self) -> Result<()>;
}

// Constantes do módulo
pub const DEFAULT_REDIS_URL: &str = "redis://localhost:6379";
pub const DEFAULT_CACHE_SIZE: usize = 1000;
pub const DEFAULT_CACHE_TTL: u64 = 3600;

/// Erros específicos do Bridge
#[derive(Debug, thiserror::Error)]
pub enum BridgeError {
    #[error("Falha na validação quântica: {0}")]
    QuantumValidationFailed(String),
    
    #[error("Nível de consciência insuficiente: requerido {required:?}, atual {current:?}")]
    InsufficientConsciousness {
        required: crate::consciousness::ConsciousnessLevel,
        current: crate::consciousness::ConsciousnessLevel,
    },
    
    #[error("Erro de cache: {0}")]
    CacheError(String),
}

// Tipos comuns do módulo
pub type BridgeResult<T> = Result<T, BridgeError>;
pub type ValidatorFunction = Arc<dyn Fn(&str) -> BridgeResult<bool> + Send + Sync>;

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_bridge_config() {
        let config = WarpBridgeConfig::default();
        assert_eq!(config.cache_size, DEFAULT_CACHE_SIZE);
        assert_eq!(config.cache_ttl, DEFAULT_CACHE_TTL);
    }
}

