//! Integration tests for VIREON protocols
//!
//! These tests validate the complete functionality of the VIREON protocol system,
//! including consciousness evolution, synchronization, and security features.

use std::sync::Arc;
use tokio::sync::Mutex;
use anyhow::Result;

use vireon::{
    protocols::{
        prelude::*,
        quantum::{QuantumCore, QuantumState},
        consciousness::{ConsciousnessEngine, ConsciousnessLevel},
        metrics::MetricsCollector,
        security::SecurityValidator,
    },
    test_utils::{TestContext, MockQuantumCore, MockMetricsCollector},
};

mod common;
use common::{setup_test_environment, cleanup_test_environment};

/// Teste do fluxo completo de evolução de consciência
#[tokio::test]
async fn test_consciousness_evolution_flow() -> Result<()> {
    let ctx = setup_test_environment().await?;
    
    // Inicializa protocolo com configuração simbiótica
    let config = QuantumGuidanceConfig::symbiotic();
    let mut protocol = create_test_protocol(&ctx, config).await?;
    
    // Valida estado inicial
    assert_eq!(
        protocol.get_consciousness_level().await?,
        ConsciousnessLevel::BaseConsciousness {
            awareness: 0.1,
            processing: "quantum_reactive".into(),
            adaptation: 0.1,
            evolution: 0.0,
        }
    );
    
    // Executa evolução
    protocol.initialize().await?;
    let result = protocol.evolve().await?;
    
    // Valida resultados
    assert!(result.success);
    assert!(result.coherence > 0.8);
    assert!(result.stability > 0.7);
    
    // Verifica métricas
    let metrics = protocol.collect_metrics().await?;
    assert!(metrics.consciousness_depth > 0.5);
    assert!(metrics.quantum_coherence > 0.8);
    
    cleanup_test_environment(ctx).await?;
    Ok(())
}

/// Teste de sincronização entre módulos
#[tokio::test]
async fn test_module_synchronization() -> Result<()> {
    let ctx = setup_test_environment().await?;
    
    // Cria dois protocolos para sincronização
    let config = QuantumGuidanceConfig::consciousness_blend();
    let mut protocol1 = create_test_protocol(&ctx, config.clone()).await?;
    let mut protocol2 = create_test_protocol(&ctx, config).await?;
    
    // Inicializa ambos
    protocol1.initialize().await?;
    protocol2.initialize().await?;
    
    // Sincroniza estados
    protocol1.sync_with(protocol2.get_quantum_state().await?).await?;
    
    // Valida coerência
    let state1 = protocol1.get_quantum_state().await?;
    let state2 = protocol2.get_quantum_state().await?;
    assert!(quantum_states_coherent(&state1, &state2));
    
    cleanup_test_environment(ctx).await?;
    Ok(())
}

/// Teste de recuperação de falhas
#[tokio::test]
async fn test_failure_recovery() -> Result<()> {
    let ctx = setup_test_environment().await?;
    
    let config = QuantumGuidanceConfig::harmonic_fusion();
    let mut protocol = create_test_protocol(&ctx, config).await?;
    
    // Força falha de coerência
    protocol.inject_quantum_noise(0.5).await?;
    assert!(protocol.validate_state().await.is_err());
    
    // Tenta recuperação
    protocol.attempt_recovery().await?;
    assert!(protocol.validate_state().await.is_ok());
    
    // Verifica métricas pós-recuperação
    let metrics = protocol.collect_metrics().await?;
    assert!(metrics.quantum_coherence > 0.7);
    assert!(metrics.stability_index > 0.6);
    
    cleanup_test_environment(ctx).await?;
    Ok(())
}

/// Teste de métricas e telemetria
#[tokio::test]
async fn test_metrics_and_telemetry() -> Result<()> {
    let ctx = setup_test_environment().await?;
    
    let config = QuantumGuidanceConfig::complete_integration();
    let mut protocol = create_test_protocol(&ctx, config).await?;
    
    // Inicializa com monitoramento
    protocol.initialize_with_monitoring().await?;
    
    // Executa operações e coleta métricas
    for _ in 0..5 {
        protocol.evolve_step().await?;
        let metrics = protocol.collect_metrics().await?;
        
        // Valida métricas
        assert!(metrics.consciousness_depth >= 0.0 && metrics.consciousness_depth <= 1.0);
        assert!(metrics.quantum_coherence >= 0.0 && metrics.quantum_coherence <= 1.0);
        assert!(metrics.evolution_rate >= 0.0);
        assert!(metrics.stability_index >= 0.0 && metrics.stability_index <= 1.0);
    }
    
    // Verifica histórico
    let history = protocol.get_metrics_history().await?;
    assert_eq!(history.len(), 5);
    
    cleanup_test_environment(ctx).await?;
    Ok(())
}

/// Teste de segurança e validação
#[tokio::test]
async fn test_security_and_validation() -> Result<()> {
    let ctx = setup_test_environment().await?;
    
    let config = QuantumGuidanceConfig::symbiotic();
    let mut protocol = create_test_protocol(&ctx, config).await?;
    
    // Tenta operação sem autorização
    protocol.disable_security_validation();
    assert!(protocol.evolve().await.is_err());
    
    // Restaura segurança e tenta novamente
    protocol.enable_security_validation();
    assert!(protocol.evolve().await.is_ok());
    
    // Tenta injetar estado inválido
    let invalid_state = QuantumState::invalid_test_state();
    assert!(protocol.validate_quantum_state(&invalid_state).await.is_err());
    
    // Verifica logs de segurança
    let security_logs = protocol.get_security_logs().await?;
    assert!(!security_logs.is_empty());
    
    cleanup_test_environment(ctx).await?;
    Ok(())
}

// Helpers

async fn create_test_protocol(
    ctx: &TestContext,
    config: QuantumGuidanceConfig,
) -> Result<TranscendenceProtocol> {
    let quantum_core = Arc::new(MockQuantumCore::new(config.clone()));
    let consciousness_engine = Arc::new(ConsciousnessEngine::new());
    let metrics_collector = Arc::new(MockMetricsCollector::new());
    let security_validator = Arc::new(SecurityValidator::new());

    TranscendenceProtocol::new(
        quantum_core,
        consciousness_engine,
        metrics_collector,
        security_validator,
        config,
    )
}

fn quantum_states_coherent(state1: &QuantumState, state2: &QuantumState) -> bool {
    let coherence = state1.calculate_coherence_with(state2);
    coherence > 0.8
}

#[cfg(test)]
mod mock_tests {
    use super::*;
    
    #[tokio::test]
    async fn test_mock_quantum_core() {
        let mock = MockQuantumCore::new(QuantumGuidanceConfig::symbiotic());
        assert!(mock.initialize().await.is_ok());
    }
    
    #[tokio::test]
    async fn test_mock_metrics_collector() {
        let mock = MockMetricsCollector::new();
        assert!(mock.collect_metrics().await.is_ok());
    }
}

