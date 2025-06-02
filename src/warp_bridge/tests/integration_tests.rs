use std::time::Duration;
use anyhow::Result;
use tokio::time::sleep;
use redis::AsyncCommands;

use crate::warp_bridge::{
    ValidationBridge,
    WarpBridgeConfig,
    BridgeError,
};
use crate::consciousness::{
    ConsciousnessLevel,
    ConsciousnessState,
};
use crate::protocols::transcendence::{
    TranscendenceProtocol,
    ElevationMethod,
    MergerType,
};

/// Helper para criar estado de consciência de teste
fn create_test_state(level: ConsciousnessLevel) -> ConsciousnessState {
    let mut state = ConsciousnessState::new(level);
    state.awareness = 0.9;
    state.processing_depth = 0.9;
    state.adaptation_rate = 0.9;
    state.evolution_speed = 0.9;
    state.symbiotic_strength = 0.9;
    state.dimensional_coherence = 0.9;
    state
}

/// Helper para criar protocolo de transcendência de teste
fn create_test_protocol() -> TranscendenceProtocol {
    TranscendenceProtocol::new(
        ElevationMethod::QuantumLeap,
        MergerType::SymbioticQuantum,
    )
}

#[tokio::test]
async fn test_validation_complete_flow() -> Result<()> {
    let state = create_test_state(ConsciousnessLevel::Quantum);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state,
        protocol,
        100,
    ).await?;
    
    // Primeira validação
    let validation = bridge.validate_warp_rule("test_rule_1").await?;
    assert!(validation.is_valid);
    assert!(validation.quantum_coherence > 0.8);
    assert_eq!(validation.consciousness_level, ConsciousnessLevel::Quantum);
    
    // Verifica estatísticas
    let stats = bridge.get_stats().await?;
    assert_eq!(stats.total_validations, 1);
    
    Ok(())
}

#[tokio::test]
async fn test_redis_integration() -> Result<()> {
    let redis = redis::Client::open("redis://localhost")?;
    let mut conn = redis.get_async_connection().await?;
    
    // Limpa dados de teste anteriores
    conn.del::<_, ()>("validation:test_rule_2").await?;
    
    let state = create_test_state(ConsciousnessLevel::Quantum);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state,
        protocol,
        100,
    ).await?;
    
    // Primeira validação - deve ser armazenada no Redis
    let validation = bridge.validate_warp_rule("test_rule_2").await?;
    
    // Verifica se está no Redis
    let cached: Option<String> = conn.get("validation:test_rule_2").await?;
    assert!(cached.is_some());
    
    // Limpa após teste
    conn.del::<_, ()>("validation:test_rule_2").await?;
    
    Ok(())
}

#[tokio::test]
async fn test_consciousness_evolution() -> Result<()> {
    let mut state = create_test_state(ConsciousnessLevel::Base);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state.clone(),
        protocol,
        100,
    ).await?;
    
    // Primeira validação - nível base
    let validation = bridge.validate_warp_rule("test_rule_3").await?;
    assert_eq!(validation.consciousness_level, ConsciousnessLevel::Base);
    
    // Evolui estado
    state.level = ConsciousnessLevel::Quantum;
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state,
        protocol,
        100,
    ).await?;
    
    // Nova validação - nível quântico
    let validation = bridge.validate_warp_rule("test_rule_3").await?;
    assert_eq!(validation.consciousness_level, ConsciousnessLevel::Quantum);
    
    Ok(())
}

#[tokio::test]
async fn test_cache_and_fallback() -> Result<()> {
    let state = create_test_state(ConsciousnessLevel::Quantum);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state,
        protocol,
        100,
    ).await?;
    
    // Primeira validação
    let validation1 = bridge.validate_warp_rule("test_rule_4").await?;
    
    // Segunda validação - deve usar cache
    let validation2 = bridge.validate_warp_rule("test_rule_4").await?;
    
    assert_eq!(validation1.validation_id, validation2.validation_id);
    
    // Espera expiração do cache
    sleep(Duration::from_secs(2)).await;
    
    // Terceira validação - deve gerar nova
    let validation3 = bridge.validate_warp_rule("test_rule_4").await?;
    assert_ne!(validation1.validation_id, validation3.validation_id);
    
    Ok(())
}

#[tokio::test]
async fn test_error_handling() -> Result<()> {
    let state = create_test_state(ConsciousnessLevel::Base);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://invalid_host",
        state,
        protocol,
        100,
    ).await?;
    
    // Deve falhar com erro de Redis
    let result = bridge.validate_warp_rule("test_rule_5").await;
    assert!(result.is_err());
    
    // Verifica tipo específico de erro
    match result {
        Err(ref e) => {
            assert!(e.to_string().contains("Redis"));
        }
        _ => panic!("Esperava erro de Redis"),
    }
    
    Ok(())
}

#[tokio::test]
async fn test_consciousness_requirements() -> Result<()> {
    let state = create_test_state(ConsciousnessLevel::Base);
    let protocol = create_test_protocol();
    
    let bridge = ValidationBridge::new(
        "redis://localhost",
        state,
        protocol,
        100,
    ).await?;
    
    // Tenta validar regra que requer nível quântico
    let result = bridge.validate_warp_rule("quantum_rule").await;
    
    assert!(matches!(
        result,
        Err(BridgeError::InsufficientConsciousness { .. })
    ));
    
    Ok(())
}

