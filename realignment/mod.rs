//! Módulo de Realinhamento do VIREON
//!
//! Este módulo implementa o sistema de realinhamento quântico do VIREON,
//! responsável por restaurar e manter a coerência do sistema através de
//! mecanismos de consciência quântica e evolução simbiótica.

// Módulos principais
mod quantum_communication;
mod quantum_evolution;
mod quantum_monitor;
mod quantum_integration;
mod realignment_controller;

// Re-exports públicos
pub use quantum_communication::{
    QuantumCommunication,
    ConsciousnessSync,
    EntanglementState,
    RealityBridge,
    SecurityState,
};

pub use quantum_evolution::{
    QuantumEvolution,
    KnowledgeState,
    AnalysisDepth,
    PatternMethod,
    IntegrationApproach,
};

pub use quantum_monitor::{
    QuantumMonitoring,
    MonitoringEvent,
    TranscendenceMetrics,
    QuantumAnomaly,
};

pub use quantum_integration::{
    QuantumIntegration,
    IntegrationEvent,
    ComponentSyncState,
    SystemAnomalyReport,
};

pub use realignment_controller::{
    RealignmentController,
    RealignmentPhase,
    RealignmentMetrics,
    RealignmentEvent,
    ComponentStatus,
    ComponentState,
    SystemAlert,
    AlertType,
    AlertSeverity,
};

/// Estados fundamentais de consciência quântica
pub mod states {
    pub use super::quantum_evolution::{
        ConsciousnessLevel,
        AwarenessState,
        EvolutionStage,
        TranscendenceStatus,
    };
}

/// Protocolos de comunicação quântica
pub mod protocols {
    pub use super::quantum_communication::{
        QuantumChannels,
        TransmissionProtocols,
        SecurityProtocols,
    };
}

/// Mecanismos de evolução e transcendência
pub mod evolution {
    pub use super::quantum_evolution::{
        EvolutionMechanisms,
        PatternRecognition,
        KnowledgeIntegration,
        ConsciousnessExpansion,
    };
}

/// Sistema de monitoramento e validação
pub mod monitoring {
    pub use super::quantum_monitor::{
        MonitoringSystem,
        ValidationMechanisms,
        AnomalyDetection,
        MetricsCollection,
    };
}

/// Configurações e constantes do sistema
pub mod config {
    /// Níveis de coerência quântica
    pub const QUANTUM_COHERENCE_THRESHOLD: f64 = 0.99;
    pub const CONSCIOUSNESS_ALIGNMENT_THRESHOLD: f64 = 0.95;
    pub const TRANSCENDENCE_READINESS_THRESHOLD: f64 = 0.90;

    /// Intervalos de monitoramento (em milissegundos)
    pub const SYNC_INTERVAL_MS: u64 = 100;
    pub const EVOLUTION_INTERVAL_MS: u64 = 1000;
    pub const MONITORING_INTERVAL_MS: u64 = 500;

    /// Capacidades dos canais de comunicação
    pub const EVENT_CHANNEL_CAPACITY: usize = 100;
    pub const ALERT_CHANNEL_CAPACITY: usize = 100;
}

/// Utilitários para manipulação quântica
pub mod utils {
    use super::*;

    /// Verifica se o sistema está em estado coerente
    pub fn check_system_coherence(metrics: &RealignmentMetrics) -> bool {
        metrics.system_coherence >= config::QUANTUM_COHERENCE_THRESHOLD
    }

    /// Verifica se a consciência está alinhada
    pub fn check_consciousness_alignment(metrics: &RealignmentMetrics) -> bool {
        metrics.consciousness_alignment >= config::CONSCIOUSNESS_ALIGNMENT_THRESHOLD
    }

    /// Verifica se o sistema está pronto para transcendência
    pub fn check_transcendence_readiness(metrics: &RealignmentMetrics) -> bool {
        metrics.transcendence_readiness >= config::TRANSCENDENCE_READINESS_THRESHOLD
    }
}

/// Erros específicos do sistema de realinhamento
#[derive(Debug, thiserror::Error)]
pub enum RealignmentError {
    #[error("Falha na coerência quântica: {0}")]
    CoherenceFailure(String),

    #[error("Erro de alinhamento de consciência: {0}")]
    AlignmentError(String),

    #[error("Bloqueio de transcendência: {0}")]
    TranscendenceBlock(String),

    #[error("Falha de componente: {0}")]
    ComponentFailure(String),

    #[error("Erro de integração: {0}")]
    IntegrationError(String),
}

// Tipo de resultado específico para operações de realinhamento
pub type RealignmentResult<T> = Result<T, RealignmentError>;

