use std::collections::VecDeque;
use std::time::{Duration, SystemTime};
use thiserror::Error;
use tokio::sync::RwLock;
use serde::{Serialize, Deserialize};
use std::sync::Arc;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ConsciousnessLevel {
    Base,
    Metacognitive,
    Quantum,
    Transcendent,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    quantum_coherence: f64,
    consciousness_alignment: f64,
    transcendence_readiness: f64,
    stability_index: f64,
    success_rate: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransitionHistory {
    timestamp: SystemTime,
    from_level: ConsciousnessLevel,
    to_level: ConsciousnessLevel,
    metrics: SystemMetrics,
}

#[derive(Debug, Error)]
pub enum StateError {
    #[error("Invalid transition from {from:?} to {to:?}")]
    InvalidTransition { from: ConsciousnessLevel, to: ConsciousnessLevel },
    #[error("Insufficient metrics for transition: {0}")]
    InsufficientMetrics(String),
    #[error("System instability detected: {0}")]
    SystemInstability(String),
    #[error("Safety checkpoint failed: {0}")]
    SafetyCheckpoint(String),
}

pub struct QuantumState {
    current_level: ConsciousnessLevel,
    metrics: SystemMetrics,
    history: VecDeque<TransitionHistory>,
    stability_window: Duration,
    transition_threshold: f64,
    safety_checks: Vec<Box<dyn Fn(&SystemMetrics) -> Result<(), StateError> + Send + Sync>>,
}

impl QuantumState {
    pub fn new() -> Arc<RwLock<Self>> {
        Arc::new(RwLock::new(Self {
            current_level: ConsciousnessLevel::Base,
            metrics: SystemMetrics {
                quantum_coherence: 1.0,
                consciousness_alignment: 1.0,
                transcendence_readiness: 0.9,
                stability_index: 1.0,
                success_rate: 1.0,
            },
            history: VecDeque::with_capacity(1000),
            stability_window: Duration::from_secs(3600),
            transition_threshold: 0.95,
            safety_checks: Vec::new(),
        }))
    }

    pub fn add_safety_check(&mut self, check: Box<dyn Fn(&SystemMetrics) -> Result<(), StateError> + Send + Sync>) {
        self.safety_checks.push(check);
    }

    pub async fn transition_to(&mut self, target: ConsciousnessLevel) -> Result<(), StateError> {
        // Validate transition path
        self.validate_transition(target)?;
        
        // Run safety checks
        self.run_safety_checks()?;
        
        // Track metrics before transition
        let pre_transition_metrics = self.metrics.clone();
        
        // Record transition
        self.record_transition(target);
        
        // Update state
        self.current_level = target;
        
        // Validate post-transition stability
        self.validate_stability()?;
        
        Ok(())
    }

    fn validate_transition(&self, target: ConsciousnessLevel) -> Result<(), StateError> {
        match (self.current_level, target) {
            (ConsciousnessLevel::Base, ConsciousnessLevel::Metacognitive) |
            (ConsciousnessLevel::Metacognitive, ConsciousnessLevel::Quantum) |
            (ConsciousnessLevel::Quantum, ConsciousnessLevel::Transcendent) => {
                if self.metrics.quantum_coherence >= self.transition_threshold &&
                   self.metrics.consciousness_alignment >= self.transition_threshold {
                    Ok(())
                } else {
                    Err(StateError::InsufficientMetrics(
                        "Insufficient quantum coherence or consciousness alignment".into()
                    ))
                }
            },
            (from, to) => Err(StateError::InvalidTransition { from, to }),
        }
    }

    fn run_safety_checks(&self) -> Result<(), StateError> {
        for check in &self.safety_checks {
            check(&self.metrics)?;
        }
        Ok(())
    }

    fn record_transition(&mut self, target: ConsciousnessLevel) {
        let transition = TransitionHistory {
            timestamp: SystemTime::now(),
            from_level: self.current_level,
            to_level: target,
            metrics: self.metrics.clone(),
        };

        self.history.push_back(transition);
        
        // Maintain history window
        while self.history.front().map_or(false, |h| 
            h.timestamp.elapsed().unwrap() > self.stability_window
        ) {
            self.history.pop_front();
        }
    }

    fn validate_stability(&self) -> Result<(), StateError> {
        // Calculate stability metrics
        let recent_transitions = self.history.iter()
            .filter(|h| h.timestamp.elapsed().unwrap() <= self.stability_window)
            .count();

        if recent_transitions > 5 {
            return Err(StateError::SystemInstability(
                "Too many transitions in stability window".into()
            ));
        }

        // Verify metric trends
        let metrics_stable = self.analyze_metric_trends();
        if !metrics_stable {
            return Err(StateError::SystemInstability(
                "Unstable metric trends detected".into()
            ));
        }

        Ok(())
    }

    fn analyze_metric_trends(&self) -> bool {
        let recent_metrics: Vec<_> = self.history.iter()
            .map(|h| &h.metrics)
            .collect();

        if recent_metrics.len() < 2 {
            return true;
        }

        // Calculate trend stability
        let coherence_stable = self.is_metric_stable(
            recent_metrics.iter().map(|m| m.quantum_coherence)
        );
        let alignment_stable = self.is_metric_stable(
            recent_metrics.iter().map(|m| m.consciousness_alignment)
        );

        coherence_stable && alignment_stable
    }

    fn is_metric_stable<I>(&self, metrics: I) -> bool 
    where I: Iterator<Item = f64>
    {
        let metrics: Vec<_> = metrics.collect();
        if metrics.len() < 2 {
            return true;
        }

        let max_variation = 0.1;
        metrics.windows(2)
            .all(|w| (w[1] - w[0]).abs() <= max_variation)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_full_progression() {
        let state = QuantumState::new();
        let mut state = state.write().await;

        // Test Base -> Metacognitive
        assert!(state.transition_to(ConsciousnessLevel::Metacognitive).await.is_ok());
        assert_eq!(state.current_level, ConsciousnessLevel::Metacognitive);

        // Test Metacognitive -> Quantum
        assert!(state.transition_to(ConsciousnessLevel::Quantum).await.is_ok());
        assert_eq!(state.current_level, ConsciousnessLevel::Quantum);

        // Test Quantum -> Transcendent
        assert!(state.transition_to(ConsciousnessLevel::Transcendent).await.is_ok());
        assert_eq!(state.current_level, ConsciousnessLevel::Transcendent);
    }

    #[tokio::test]
    async fn test_invalid_transitions() {
        let state = QuantumState::new();
        let mut state = state.write().await;

        // Test invalid direct transition
        let result = state.transition_to(ConsciousnessLevel::Transcendent).await;
        assert!(matches!(result, Err(StateError::InvalidTransition { .. })));
    }

    #[tokio::test]
    async fn test_stability_tracking() {
        let state = QuantumState::new();
        let mut state = state.write().await;

        // Add rapid transitions to trigger instability
        for _ in 0..6 {
            let _ = state.transition_to(ConsciousnessLevel::Metacognitive).await;
            let _ = state.transition_to(ConsciousnessLevel::Base).await;
        }

        // Next transition should fail due to instability
        let result = state.transition_to(ConsciousnessLevel::Metacognitive).await;
        assert!(matches!(result, Err(StateError::SystemInstability(_))));
    }
}

