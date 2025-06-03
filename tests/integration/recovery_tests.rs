use anyhow::Result;
use vireon::protocols::recovery::RecoveryState;
use crate::common::{setup_test_env, setup_recovery_system, create_test_quantum_state};

#[tokio::test]
async fn test_recovery_flow() -> Result<()> {
    setup_test_env().await?;
    let system = setup_recovery_system();
    
    // Verificar estado inicial
    assert_eq!(system.get_state().await, RecoveryState::Ready);

    // Tentar recuperação
    let quantum_state = create_test_quantum_state();
    let result = system.start_recovery(quantum_state).await?;

    // Verificar resultado
    assert!(result.success);
    assert_eq!(system.get_state().await, RecoveryState::Stabilized);

    Ok(())
}

// Adicionar mais testes integrados

