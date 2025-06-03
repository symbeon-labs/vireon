//! Common test utilities for protocol testing

use std::sync::Arc;
use tokio::sync::Mutex;
use anyhow::Result;

use vireon::test_utils::TestContext;

/// Setup test environment with necessary resources
pub async fn setup_test_environment() -> Result<TestContext> {
    let ctx = TestContext::new();
    
    // Initialize test database
    ctx.init_test_database().await?;
    
    // Setup mock services
    ctx.start_mock_quantum_service().await?;
    ctx.start_mock_metrics_service().await?;
    
    // Create test directories
    ctx.create_test_directories()?;
    
    Ok(ctx)
}

/// Cleanup test environment and resources
pub async fn cleanup_test_environment(ctx: TestContext) -> Result<()> {
    // Stop mock services
    ctx.stop_mock_services().await?;
    
    // Cleanup database
    ctx.cleanup_test_database().await?;
    
    // Remove test directories
    ctx.cleanup_test_directories()?;
    
    Ok(())
}

/// Test utilities
pub mod utils {
    use super::*;
    
    /// Creates test quantum state
    pub fn create_test_quantum_state() -> QuantumState {
        QuantumState {
            coherence: 0.9,
            entanglement: 0.8,
            stability: 0.85,
        }
    }
    
    /// Creates test consciousness state
    pub fn create_test_consciousness_state() -> ConsciousnessState {
        ConsciousnessState {
            level: ConsciousnessLevel::BaseConsciousness {
                awareness: 0.5,
                processing: "quantum_reactive".into(),
                adaptation: 0.6,
                evolution: 0.3,
            },
            stability: 0.8,
        }
    }
    
    /// Validates test metrics
    pub fn validate_test_metrics(metrics: &QuantumMetrics) -> bool {
        metrics.consciousness_depth >= 0.0
            && metrics.consciousness_depth <= 1.0
            && metrics.quantum_coherence >= 0.0
            && metrics.quantum_coherence <= 1.0
            && metrics.evolution_rate >= 0.0
            && metrics.stability_index >= 0.0
            && metrics.stability_index <= 1.0
    }
}

