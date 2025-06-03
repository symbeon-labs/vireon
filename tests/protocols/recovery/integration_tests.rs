use std::time::Duration;
use tokio::time::sleep;
use anyhow::Result;
use futures::StreamExt;
use metrics::{counter, gauge};

use crate::{
    protocols::{
        recovery::{RecoverySystem, RecoveryConfig, RecoveryState},
        monitoring::{ContinuousMonitor, MonitorConfig, AlertLevel},
        quantum::{QuantumState, StateValidator},
    },
    core::{MetricsCollector, SystemState},
};

const TEST_TIMEOUT: Duration = Duration::from_secs(5);

async fn setup_test_environment() -> Result<(RecoverySystem, ContinuousMonitor)> {
    let recovery_config = RecoveryConfig {
        validation_interval: Duration::from_millis(100),
        retry_limit: 3,
        coherence_threshold: 0.9,
    };

    let monitor_config = MonitorConfig {
        check_interval: Duration::from_millis(50),
        alert_threshold: 0.7,
        metrics_buffer_size: 100,
    };

    let recovery = RecoverySystem::new(recovery_config)?;
    let monitor = ContinuousMonitor::new(monitor_config)?;

    Ok((recovery, monitor))
}

#[tokio::test]
async fn test_recovery_system_initialization() -> Result<()> {
    let (recovery, _) = setup_test_environment().await?;
    
    assert!(recovery.is_initialized());
    assert_eq!(recovery.current_state(), RecoveryState::Ready);
    assert!(recovery.get_metrics().is_empty());

    Ok(())
}

#[tokio::test]
async fn test_recovery_cycle() -> Result<()> {
    let (mut recovery, _) = setup_test_environment().await?;
    
    // Simular estado inválido
    let invalid_state = QuantumState {
        coherence: 0.5,
        entanglement: 0.3,
        stability: 0.4,
    };

    recovery.handle_invalid_state(invalid_state).await?;
    assert_eq!(recovery.current_state(), RecoveryState::Recovering);

    // Aguardar ciclo de recuperação
    sleep(Duration::from_millis(200)).await;
    
    assert_eq!(recovery.current_state(), RecoveryState::Ready);
    assert!(recovery.get_metrics()["recovery_attempts"].unwrap() > 0.0);

    Ok(())
}

#[tokio::test]
async fn test_continuous_monitoring() -> Result<()> {
    let (_, mut monitor) = setup_test_environment().await?;
    
    monitor.start_monitoring().await?;
    
    // Gerar algumas métricas
    gauge!("quantum_coherence", 0.95);
    gauge!("system_stability", 0.85);
    counter!("recovery_attempts", 1);

    sleep(Duration::from_millis(100)).await;

    let metrics = monitor.get_current_metrics();
    assert!(!metrics.is_empty());
    assert!(metrics.contains_key("quantum_coherence"));
    assert!(metrics.contains_key("system_stability"));

    Ok(())
}

#[tokio::test]
async fn test_alert_generation() -> Result<()> {
    let (_, mut monitor) = setup_test_environment().await?;
    
    let mut alert_stream = monitor.subscribe_alerts();
    monitor.start_monitoring().await?;

    // Simular condição de alerta
    gauge!("quantum_coherence", 0.5); // Abaixo do threshold
    
    if let Some(alert) = alert_stream.next().await {
        assert_eq!(alert.level, AlertLevel::Warning);
        assert!(alert.message.contains("quantum_coherence"));
    }

    Ok(())
}

#[tokio::test]
async fn test_recovery_monitor_integration() -> Result<()> {
    let (mut recovery, mut monitor) = setup_test_environment().await?;
    
    monitor.start_monitoring().await?;
    let mut alert_stream = monitor.subscribe_alerts();

    // Simular falha que requer recuperação
    let invalid_state = QuantumState {
        coherence: 0.3,
        entanglement: 0.4,
        stability: 0.3,
    };

    recovery.handle_invalid_state(invalid_state).await?;

    // Verificar se o monitor detectou a recuperação
    if let Some(alert) = alert_stream.next().await {
        assert_eq!(alert.level, AlertLevel::Critical);
        assert!(alert.message.contains("recovery"));
    }

    // Aguardar recuperação
    sleep(Duration::from_millis(300)).await;

    // Verificar métricas pós-recuperação
    let metrics = monitor.get_current_metrics();
    assert!(metrics["recovery_success_rate"].unwrap() > 0.0);

    Ok(())
}

#[tokio::test]
async fn test_metrics_collection() -> Result<()> {
    let (recovery, mut monitor) = setup_test_environment().await?;
    
    monitor.start_monitoring().await?;

    // Gerar métricas de vários tipos
    gauge!("quantum_coherence", 0.95);
    gauge!("entanglement_strength", 0.85);
    counter!("recovery_attempts", 1);
    counter!("successful_recoveries", 1);

    sleep(Duration::from_millis(100)).await;

    let metrics = monitor.get_current_metrics();
    assert!(metrics.len() >= 4);
    assert!(metrics["quantum_coherence"].unwrap() > 0.9);
    assert!(metrics["recovery_attempts"].unwrap() >= 1.0);

    Ok(())
}

#[tokio::test]
async fn test_error_handling() -> Result<()> {
    let (mut recovery, mut monitor) = setup_test_environment().await?;
    
    // Simular erro de validação
    let result = recovery.validate_state(QuantumState {
        coherence: -1.0, // Valor inválido
        entanglement: 0.5,
        stability: 0.5,
    }).await;

    assert!(result.is_err());

    // Verificar se o monitor registrou o erro
    let metrics = monitor.get_current_metrics();
    assert!(metrics["validation_errors"].unwrap() > 0.0);

    Ok(())
}

#[tokio::test]
async fn test_performance_under_load() -> Result<()> {
    let (mut recovery, mut monitor) = setup_test_environment().await?;
    
    // Simular carga alta
    for _ in 0..100 {
        gauge!("quantum_coherence", 0.95);
        gauge!("system_stability", 0.85);
        counter!("operations", 1);
        
        recovery.validate_state(QuantumState {
            coherence: 0.9,
            entanglement: 0.8,
            stability: 0.9,
        }).await?;
    }

    let metrics = monitor.get_current_metrics();
    assert!(metrics["system_load"].unwrap() > 0.0);
    assert!(metrics["operation_latency"].unwrap() >= 0.0);

    Ok(())
}

#[tokio::test]
async fn test_system_recovery_persistence() -> Result<()> {
    let (mut recovery, monitor) = setup_test_environment().await?;
    
    // Simular múltiplas recuperações
    for _ in 0..3 {
        recovery.handle_invalid_state(QuantumState {
            coherence: 0.5,
            entanglement: 0.4,
            stability: 0.5,
        }).await?;

        sleep(Duration::from_millis(200)).await;
    }

    let metrics = monitor.get_current_metrics();
    assert!(metrics["total_recoveries"].unwrap() >= 3.0);
    assert!(metrics["recovery_success_rate"].unwrap() > 0.0);

    Ok(())
}

