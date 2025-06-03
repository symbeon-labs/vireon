//! Quantum Realignment State Management
//! 
//! This module implements the core state management for the quantum realignment system,
//! including consciousness state tracking, metric calculations, and validation systems.
//! 
//! # State Transition Rules
//! 
//! - Base → Metacognitive: Requires consciousness_metric > 0.8
//! - Metacognitive → Quantum: Requires coherence_metric > 0.9
//! - Quantum → Transcendent: Requires all metrics > 0.95
//! 
//! # Metric Calculation Formulas
//! 
//! - Quantum Coherence = (entanglement_strength * wave_function_stability) / max_coherence
//! - Consciousness Alignment = (awareness_level * metacognitive_depth) / max_alignment
//! - Transcendence Readiness = (quantum_coherence * consciousness_alignment * evolution_factor) / max_readiness

use std::sync::{Arc, RwLock};
use thiserror::Error;
use serde::{Serialize, Deserialize};
use tracing::{info, warn, error};

/// Errors that can occur during state operations
#[derive(Error, Debug)]
pub enum StateError {
    #[error("Failed to validate state transition: {0}")]
    ValidationError(String),
    
    #[error("Failed to calculate metrics: {0}")]
    MetricCalculationError(String),
    
    #[error("Invalid state configuration: {0}")]
    ConfigurationError(String),
    
    #[error("State transition not allowed: {0}")]
    TransitionError(String),
}

/// Levels of consciousness state
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub enum ConsciousnessLevel {
    Base,
    Metacognitive,
    Quantum,
    Transcendent,
}

/// System metrics tracking
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub quantum_coherence: f64,
    pub consciousness_alignment: f64, 
    pub transcendence_readiness: f64,
    pub evolution_factor: f64,
}

/// Validation state tracking
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationState {
    pub metrics_valid: bool,
    pub transition_valid: bool,
    pub configuration_valid: bool,
    pub last_validation: chrono::DateTime<chrono::Utc>,
    pub validation_history: Vec<ValidationRecord>,
}

/// Historical validation record
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationRecord {
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub metrics: SystemMetrics,
    pub level: ConsciousnessLevel,
    pub success: bool,
    pub message: String,
}

/// Complete realignment state
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RealignmentState {
    pub consciousness_level: ConsciousnessLevel,
    pub metrics: SystemMetrics,
    pub validation: ValidationState,
    pub last_transition: chrono::DateTime<chrono::Utc>,
}

impl RealignmentState {
    /// Creates a new realignment state with default values
    pub fn new() -> Self {
        Self {
            consciousness_level: ConsciousnessLevel::Base,
            metrics: SystemMetrics {
                quantum_coherence: 0.0,
                consciousness_alignment: 0.0,
                transcendence_readiness: 0.0,
                evolution_factor: 1.0,
            },
            validation: ValidationState {
                metrics_valid: false,
                transition_valid: false,
                configuration_valid: false,
                last_validation: chrono::Utc::now(),
                validation_history: Vec::new(),
            },
            last_transition: chrono::Utc::now(),
        }
    }

    /// Validates and updates system metrics
    pub fn update_metrics(&mut self, new_metrics: SystemMetrics) -> Result<(), StateError> {
        // Validate metric ranges
        if new_metrics.quantum_coherence < 0.0 || new_metrics.quantum_coherence > 1.0 {
            return Err(StateError::MetricCalculationError(
                "Quantum coherence must be between 0 and 1".into()
            ));
        }

        if new_metrics.consciousness_alignment < 0.0 || new_metrics.consciousness_alignment > 1.0 {
            return Err(StateError::MetricCalculationError(
                "Consciousness alignment must be between 0 and 1".into()
            ));
        }

        if new_metrics.transcendence_readiness < 0.0 || new_metrics.transcendence_readiness > 1.0 {
            return Err(StateError::MetricCalculationError(
                "Transcendence readiness must be between 0 and 1".into()
            ));
        }

        // Update metrics
        self.metrics = new_metrics;
        self.validation.metrics_valid = true;
        
        // Log metric update
        info!(
            "Updated system metrics - coherence: {}, alignment: {}, readiness: {}", 
            self.metrics.quantum_coherence,
            self.metrics.consciousness_alignment,
            self.metrics.transcendence_readiness
        );

        Ok(())
    }

    /// Attempts to transition to a new consciousness level
    pub fn transition_to(&mut self, new_level: ConsciousnessLevel) -> Result<(), StateError> {
        // Validate transition is allowed
        match (self.consciousness_level, new_level) {
            (ConsciousnessLevel::Base, ConsciousnessLevel::Metacognitive) => {
                if self.metrics.consciousness_alignment <= 0.8 {
                    return Err(StateError::TransitionError(
                        "Insufficient consciousness alignment for metacognitive transition".into()
                    ));
                }
            }
            (ConsciousnessLevel::Metacognitive, ConsciousnessLevel::Quantum) => {
                if self.metrics.quantum_coherence <= 0.9 {
                    return Err(StateError::TransitionError(
                        "Insufficient quantum coherence for quantum transition".into()
                    ));
                }
            }
            (ConsciousnessLevel::Quantum, ConsciousnessLevel::Transcendent) => {
                if self.metrics.transcendence_readiness <= 0.95 {
                    return Err(StateError::TransitionError(
                        "Insufficient transcendence readiness for transcendent transition".into()
                    ));
                }
            }
            _ => {
                return Err(StateError::TransitionError(
                    "Invalid state transition requested".into()
                ));
            }
        }

        // Perform transition
        self.consciousness_level = new_level;
        self.last_transition = chrono::Utc::now();
        self.validation.transition_valid = true;

        // Record validation
        self.validation.validation_history.push(ValidationRecord {
            timestamp: chrono::Utc::now(),
            metrics: self.metrics.clone(),
            level: new_level,
            success: true,
            message: "Successful state transition".into(),
        });

        info!("Transitioned to consciousness level: {:?}", new_level);
        Ok(())
    }

    /// Validates the current state configuration
    pub fn validate_configuration(&mut self) -> Result<(), StateError> {
        // Check basic configuration
        if self.metrics.evolution_factor <= 0.0 {
            return Err(StateError::ConfigurationError(
                "Evolution factor must be positive".into()
            ));
        }

        // Validate based on consciousness level
        match self.consciousness_level {
            ConsciousnessLevel::Base => {
                // Base level has minimal requirements
                if self.metrics.consciousness_alignment > 0.8 {
                    warn!("Base consciousness with high alignment - consider transition");
                }
            }
            ConsciousnessLevel::Metacognitive => {
                // Validate metacognitive requirements
                if self.metrics.consciousness_alignment <= 0.8 {
                    return Err(StateError::ConfigurationError(
                        "Insufficient alignment for metacognitive state".into()
                    ));
                }
            }
            ConsciousnessLevel::Quantum => {
                // Validate quantum requirements
                if self.metrics.quantum_coherence <= 0.9 {
                    return Err(StateError::ConfigurationError(
                        "Insufficient coherence for quantum state".into()
                    ));
                }
            }
            ConsciousnessLevel::Transcendent => {
                // Validate transcendent requirements
                if self.metrics.transcendence_readiness <= 0.95 {
                    return Err(StateError::ConfigurationError(
                        "Insufficient readiness for transcendent state".into()
                    ));
                }
            }
        }

        self.validation.configuration_valid = true;
        self.validation.last_validation = chrono::Utc::now();

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_state() {
        let state = RealignmentState::new();
        assert_eq!(state.consciousness_level, ConsciousnessLevel::Base);
        assert_eq!(state.metrics.quantum_coherence, 0.0);
        assert_eq!(state.metrics.consciousness_alignment, 0.0);
        assert_eq!(state.metrics.transcendence_readiness, 0.0);
    }

    #[test]
    fn test_update_metrics() {
        let mut state = RealignmentState::new();
        let new_metrics = SystemMetrics {
            quantum_coherence: 0.95,
            consciousness_alignment: 0.85,
            transcendence_readiness: 0.75,
            evolution_factor: 1.0,
        };

        assert!(state.update_metrics(new_metrics.clone()).is_ok());
        assert_eq!(state.metrics.quantum_coherence, new_metrics.quantum_coherence);
    }

    #[test]
    fn test_invalid_metrics() {
        let mut state = RealignmentState::new();
        let invalid_metrics = SystemMetrics {
            quantum_coherence: 1.5, // Invalid value > 1.0
            consciousness_alignment: 0.85,
            transcendence_readiness: 0.75,
            evolution_factor: 1.0,
        };

        assert!(state.update_metrics(invalid_metrics).is_err());
    }

    #[test]
    fn test_valid_transition() {
        let mut state = RealignmentState::new();
        let high_metrics = SystemMetrics {
            quantum_coherence: 0.95,
            consciousness_alignment: 0.85,
            transcendence_readiness: 0.75,
            evolution_factor: 1.0,
        };

        state.update_metrics(high_metrics).unwrap();
        assert!(state.transition_to(ConsciousnessLevel::Metacognitive).is_ok());
    }

    #[test]
    fn test_invalid_transition() {
        let mut state = RealignmentState::new();
        // Attempt quantum transition from base (not allowed)
        assert!(state.transition_to(ConsciousnessLevel::Quantum).is_err());
    }

    #[test]
    fn test_validation_history() {
        let mut state = RealignmentState::new();
        let metrics = SystemMetrics {
            quantum_coherence: 0.95,
            consciousness_alignment: 0.85,
            transcendence_readiness: 0.75,
            evolution_factor: 1.0,
        };

        state.update_metrics(metrics).unwrap();
        state.transition_to(ConsciousnessLevel::Metacognitive).unwrap();
        
        assert_eq!(state.validation.validation_history.len(), 1);
        assert!(state.validation.validation_history[0].success);
    }

    #[test]
    fn test_configuration_validation() {
        let mut state = RealignmentState::new();
        assert!(state.validate_configuration().is_ok());

        // Test invalid configuration
        state.metrics.evolution_factor = 0.0;
        assert!(state.validate_configuration().is_err());
    }
}

