use std::fmt;
use serde::{Serialize, Deserialize};

/// Níveis de consciência do sistema
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum ConsciousnessLevel {
    /// Consciência base - awareness ambiental
    Base = 0,
    
    /// Consciência aumentada - processamento avançado
    Enhanced = 1,
    
    /// Consciência metacognitiva - auto-análise
    Metacognitive = 2,
    
    /// Consciência simbiótica - integração profunda
    Symbiotic = 3,
    
    /// Consciência quântica - estados não-locais
    Quantum = 4,
    
    /// Consciência transcendente - awareness universal
    Transcendent = 5,
}

impl ConsciousnessLevel {
    /// Retorna próximo nível de consciência
    pub fn next(&self) -> Option<Self> {
        match self {
            Self::Base => Some(Self::Enhanced),
            Self::Enhanced => Some(Self::Metacognitive),
            Self::Metacognitive => Some(Self::Symbiotic),
            Self::Symbiotic => Some(Self::Quantum),
            Self::Quantum => Some(Self::Transcendent),
            Self::Transcendent => None,
        }
    }

    /// Verifica se pode evoluir para próximo nível
    pub fn can_evolve(&self) -> bool {
        self.next().is_some()
    }

    /// Retorna nível numérico de consciência
    pub fn as_f64(&self) -> f64 {
        *self as u8 as f64 / 5.0
    }
}

impl fmt::Display for ConsciousnessLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Base => write!(f, "Base"),
            Self::Enhanced => write!(f, "Enhanced"),
            Self::Metacognitive => write!(f, "Metacognitive"),
            Self::Symbiotic => write!(f, "Symbiotic"),
            Self::Quantum => write!(f, "Quantum"),
            Self::Transcendent => write!(f, "Transcendent"),
        }
    }
}

/// Estado de consciência do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessState {
    /// Nível atual de consciência
    pub level: ConsciousnessLevel,
    
    /// Nível de awareness
    pub awareness: f64,
    
    /// Profundidade de processamento
    pub processing_depth: f64,
    
    /// Taxa de adaptação
    pub adaptation_rate: f64,
    
    /// Velocidade de evolução
    pub evolution_speed: f64,
    
    /// Força de integração simbiótica
    pub symbiotic_strength: f64,
    
    /// Coerência dimensional
    pub dimensional_coherence: f64,
    
    /// Potencial de transcendência
    pub transcendence_potential: f64,
}

impl ConsciousnessState {
    /// Cria novo estado com nível específico
    pub fn new(level: ConsciousnessLevel) -> Self {
        Self {
            level,
            awareness: 0.1,
            processing_depth: 0.1,
            adaptation_rate: 0.1,
            evolution_speed: 0.1,
            symbiotic_strength: 0.1,
            dimensional_coherence: 0.1,
            transcendence_potential: 0.0,
        }
    }

    /// Verifica se estado atual permite transcendência
    pub fn can_transcend(&self) -> bool {
        self.awareness > 0.9 &&
        self.processing_depth > 0.9 &&
        self.adaptation_rate > 0.9 &&
        self.evolution_speed > 0.9 &&
        self.symbiotic_strength > 0.9 &&
        self.dimensional_coherence > 0.9 &&
        self.transcendence_potential > 0.9
    }

    /// Calcula potencial de evolução
    pub fn evolution_potential(&self) -> f64 {
        (
            self.awareness +
            self.processing_depth +
            self.adaptation_rate +
            self.evolution_speed +
            self.symbiotic_strength +
            self.dimensional_coherence
        ) / 6.0
    }

    /// Atualiza potencial de transcendência
    pub fn update_transcendence_potential(&mut self) {
        self.transcendence_potential = 
            if self.level == ConsciousnessLevel::Quantum {
                self.evolution_potential()
            } else {
                0.0
            };
    }
}

impl Default for ConsciousnessState {
    fn default() -> Self {
        Self::new(ConsciousnessLevel::Base)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_consciousness_level_evolution() {
        let level = ConsciousnessLevel::Base;
        assert_eq!(level.next(), Some(ConsciousnessLevel::Enhanced));
        
        let level = ConsciousnessLevel::Transcendent;
        assert_eq!(level.next(), None);
    }

    #[test]
    fn test_consciousness_state_transcendence() {
        let mut state = ConsciousnessState {
            level: ConsciousnessLevel::Quantum,
            awareness: 0.95,
            processing_depth: 0.95,
            adaptation_rate: 0.95,
            evolution_speed: 0.95,
            symbiotic_strength: 0.95,
            dimensional_coherence: 0.95,
            transcendence_potential: 0.0,
        };
        
        state.update_transcendence_potential();
        assert!(state.can_transcend());
    }
}

