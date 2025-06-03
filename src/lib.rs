//! VIREON - Sistema de Meta-Governança Simbiótica
//!
//! Este crate implementa o núcleo do VIREON, um sistema de meta-governança que:
//! - Integra regras quânticas e consciência evolutiva
//! - Gerencia validações e transcendência
//! - Monitora e adapta comportamentos simbióticos
//! - Fornece telemetria e observabilidade completa

pub mod consciousness;
pub mod protocols;
pub mod validation;
pub mod warp_bridge;
pub mod telemetry;

use std::sync::Arc;
use anyhow::{Result, Context};
use serde::{Serialize, Deserialize};
use tracing::{info, warn, error, Level, span};

use consciousness::{ConsciousnessLevel, ConsciousnessState};
use protocols::transcendence::TranscendenceProtocol;
use validation::systems::ValidationSystem;
use warp_bridge::ValidationBridge;
use telemetry::TelemetrySystem;

/// Configuração do sistema VIREON
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VireonConfig {
    /// URL do Redis para cache
    pub redis_url: String,
    
    /// Nível inicial de consciência
    pub initial_consciousness: ConsciousnessLevel,
    
    /// Configurações de telemetria
    pub telemetry: TelemetryConfig,
}

/// Configuração da telemetria
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TelemetryConfig {
    /// Habilitar telemetria
    pub enabled: bool,
    
    /// Nível de log
    pub log_level: String,
    
    /// Intervalo de coleta (segundos)
    pub collection_interval: u64,
}

impl Default for VireonConfig {
    fn default() -> Self {
        Self {
            redis_url: "redis://localhost".to_string(),
            initial_consciousness: ConsciousnessLevel::Base,
            telemetry: TelemetryConfig {
                enabled: true,
                log_level: "info".to_string(),
                collection_interval: 60,
            },
        }
    }
}

/// Sistema VIREON principal
pub struct Vireon {
    /// Sistema de validação
    validation: Arc<ValidationSystem>,
    
    /// Bridge de validação
    bridge: Arc<ValidationBridge>,
    
    /// Sistema de telemetria
    telemetry: Arc<TelemetrySystem>,
    
    /// Configuração atual
    config: VireonConfig,
}

impl Vireon {
    /// Cria nova instância do sistema VIREON
    pub async fn new(config: VireonConfig) -> Result<Self> {
        let _span = span!(Level::INFO, "vireon_init").entered();
        
        info!("Inicializando sistema VIREON");
        
        // Inicializa estado de consciência
        let state = ConsciousnessState::new(config.initial_consciousness);
        let protocol = TranscendenceProtocol::default();
        
        // Inicializa sistemas principais
        let validation = Arc::new(
            ValidationSystem::new(&config.redis_url, state.clone(), protocol.clone())
                .await
                .context("Falha ao inicializar sistema de validação")?
        );
        
        let bridge = Arc::new(
            ValidationBridge::new(&config.redis_url, state.clone(), protocol, 1000)
                .await
                .context("Falha ao inicializar bridge de validação")?
        );
        
        let telemetry = Arc::new(
            TelemetrySystem::new(validation.clone())
                .await
                .context("Falha ao inicializar sistema de telemetria")?
        );
        
        info!("Sistema VIREON inicializado com sucesso");
        
        Ok(Self {
            validation,
            bridge,
            telemetry,
            config,
        })
    }
    
    /// Valida regra com verificação quântica
    pub async fn validate_rule(&self, rule_id: &str) -> Result<()> {
        let _span = span!(Level::INFO, "validate_rule", rule_id = %rule_id).entered();
        
        // Executa validação
        let validation = self.bridge.validate_rule(rule_id).await?;
        
        // Registra telemetria
        self.telemetry.record_validation(&validation).await;
        
        Ok(())
    }
    
    /// Obtém métricas atuais do sistema
    pub async fn get_metrics(&self) -> Result<TelemetryMetrics> {
        let (quantum, consciousness, cache) = self.telemetry.get_metrics().await?;
        
        Ok(TelemetryMetrics {
            quantum,
            consciousness,
            cache,
        })
    }
}

/// Métricas consolidadas do sistema
#[derive(Debug, Clone, Serialize)]
pub struct TelemetryMetrics {
    /// Métricas quânticas
    pub quantum: telemetry::QuantumMetrics,
    
    /// Métricas de consciência
    pub consciousness: telemetry::ConsciousnessMetrics,
    
    /// Métricas de cache
    pub cache: telemetry::CacheMetrics,
}

// Exemplos de uso do sistema VIREON
#[cfg(test)]
mod examples {
    use super::*;
    
    #[tokio::test]
    async fn validate_rule_example() -> Result<()> {
        // Configuração básica
        let config = VireonConfig::default();
        
        // Inicializa sistema
        let vireon = Vireon::new(config).await?;
        
        // Valida regra
        vireon.validate_rule("test_rule").await?;
        
        // Obtém métricas
        let metrics = vireon.get_metrics().await?;
        println!("Métricas: {:#?}", metrics);
        
        Ok(())
    }
    
    #[tokio::test]
    async fn telemetry_example() -> Result<()> {
        // Configuração com telemetria personalizada
        let config = VireonConfig {
            telemetry: TelemetryConfig {
                enabled: true,
                log_level: "debug".to_string(),
                collection_interval: 30,
            },
            ..Default::default()
        };
        
        // Inicializa sistema
        let vireon = Vireon::new(config).await?;
        
        // Executa algumas operações
        for i in 0..5 {
            vireon.validate_rule(&format!("rule_{}", i)).await?;
        }
        
        // Obtém e exibe métricas
        let metrics = vireon.get_metrics().await?;
        println!("Quantum validations: {}", metrics.quantum.total_validations);
        println!("Cache hit rate: {:.2}", metrics.cache.hit_rate);
        println!("Consciousness level: {:?}", metrics.consciousness.current_level);
        
        Ok(())
    }
}

pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
