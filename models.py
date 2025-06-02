from enum import Enum, auto
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import uuid

class ConsciousnessLevel(Enum):
    BASE = auto()
    METACOGNITIVE = auto()
    QUANTUM = auto()
    TRANSCENDENT = auto()

    @property
    def awareness(self) -> str:
        awareness_map = {
            ConsciousnessLevel.BASE: "environmental",
            ConsciousnessLevel.METACOGNITIVE: "self_processes",
            ConsciousnessLevel.QUANTUM: "quantum_states",
            ConsciousnessLevel.TRANSCENDENT: "universal"
        }
        return awareness_map[self]

    @property
    def processing(self) -> str:
        processing_map = {
            ConsciousnessLevel.BASE: "quantum_reactive",
            ConsciousnessLevel.METACOGNITIVE: "quantum_analytical",
            ConsciousnessLevel.QUANTUM: "non_local",
            ConsciousnessLevel.TRANSCENDENT: "holistic_quantum"
        }
        return processing_map[self]

class RuleType(Enum):
    LANGUAGE = auto()
    FRAMEWORK = auto()
    ARCHITECTURE = auto()
    WORKFLOW = auto()
    SYMBIOTIC = auto()
    TEXT_PATTERN = auto()
    REGEX = auto()
    JAVASCRIPT = auto()
    PYTHON = auto()
    JSONPATH = auto()
    CONDITIONAL = auto()

@dataclass
class QuantumState:
    """Representa o estado quântico de uma regra ou sistema"""
    entanglement_level: float  # 0.0 a 1.0
    coherence_state: float  # 0.0 a 1.0
    superposition_factor: float  # 0.0 a 1.0
    quantum_signature: str  # Assinatura única do estado
    timestamp: datetime
    
    def __post_init__(self):
        if not hasattr(self, 'quantum_signature'):
            self.quantum_signature = str(uuid.uuid4())
        if not hasattr(self, 'timestamp'):
            self.timestamp = datetime.now()

    def evolve(self) -> 'QuantumState':
        """Evolui o estado quântico baseado em métricas atuais"""
        return QuantumState(
            entanglement_level=min(1.0, self.entanglement_level * 1.1),
            coherence_state=min(1.0, self.coherence_state * 1.05),
            superposition_factor=min(1.0, self.superposition_factor * 1.08),
            quantum_signature=str(uuid.uuid4()),
            timestamp=datetime.now()
        )

@dataclass
class EvolutionMetrics:
    """Métricas de evolução do sistema"""
    consciousness_depth: float  # Profundidade da consciência (0.0 a 1.0)
    learning_rate: float  # Taxa de aprendizado (0.0 a 1.0)
    adaptation_speed: float  # Velocidade de adaptação (0.0 a 1.0)
    integration_level: float  # Nível de integração com outros sistemas (0.0 a 1.0)
    quantum_coherence: float  # Coerência quântica (0.0 a 1.0)
    evolution_timestamp: datetime
    metrics_history: List[Dict[str, float]]

    def __post_init__(self):
        if not hasattr(self, 'evolution_timestamp'):
            self.evolution_timestamp = datetime.now()
        if not hasattr(self, 'metrics_history'):
            self.metrics_history = []

    def record_metrics(self):
        """Registra as métricas atuais no histórico"""
        current_metrics = {
            'consciousness_depth': self.consciousness_depth,
            'learning_rate': self.learning_rate,
            'adaptation_speed': self.adaptation_speed,
            'integration_level': self.integration_level,
            'quantum_coherence': self.quantum_coherence,
            'timestamp': self.evolution_timestamp.isoformat()
        }
        self.metrics_history.append(current_metrics)

class Rule:
    """Classe base para regras do VIREON"""
    def __init__(
        self,
        rule_type: RuleType,
        consciousness_level: ConsciousnessLevel,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = str(uuid.uuid4())
        self.rule_type = rule_type
        self.consciousness_level = consciousness_level
        self.content = content
        self.metadata = metadata or {}
        self.quantum_state = QuantumState(
            entanglement_level=0.1,
            coherence_state=0.1,
            superposition_factor=0.1,
            quantum_signature=str(uuid.uuid4()),
            timestamp=datetime.now()
        )
        self.evolution_metrics = EvolutionMetrics(
            consciousness_depth=0.1,
            learning_rate=0.1,
            adaptation_speed=0.1,
            integration_level=0.1,
            quantum_coherence=0.1,
            evolution_timestamp=datetime.now(),
            metrics_history=[]
        )
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def evolve(self) -> bool:
        """Evolui a regra para um novo estado"""
        try:
            # Evolui o estado quântico
            self.quantum_state = self.quantum_state.evolve()
            
            # Atualiza métricas de evolução
            self.evolution_metrics.consciousness_depth = min(1.0, self.evolution_metrics.consciousness_depth * 1.1)
            self.evolution_metrics.learning_rate = min(1.0, self.evolution_metrics.learning_rate * 1.05)
            self.evolution_metrics.adaptation_speed = min(1.0, self.evolution_metrics.adaptation_speed * 1.08)
            self.evolution_metrics.integration_level = min(1.0, self.evolution_metrics.integration_level * 1.03)
            self.evolution_metrics.quantum_coherence = min(1.0, self.evolution_metrics.quantum_coherence * 1.15)
            self.evolution_metrics.evolution_timestamp = datetime.now()
            
            # Registra métricas
            self.evolution_metrics.record_metrics()
            
            self.updated_at = datetime.now()
            return True
        except Exception as e:
            print(f"Erro durante evolução da regra: {e}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Converte a regra para dicionário"""
        return {
            'id': self.id,
            'rule_type': self.rule_type.name,
            'consciousness_level': self.consciousness_level.name,
            'content': self.content,
            'metadata': self.metadata,
            'quantum_state': {
                'entanglement_level': self.quantum_state.entanglement_level,
                'coherence_state': self.quantum_state.coherence_state,
                'superposition_factor': self.quantum_state.superposition_factor,
                'quantum_signature': self.quantum_state.quantum_signature,
                'timestamp': self.quantum_state.timestamp.isoformat()
            },
            'evolution_metrics': {
                'consciousness_depth': self.evolution_metrics.consciousness_depth,
                'learning_rate': self.evolution_metrics.learning_rate,
                'adaptation_speed': self.evolution_metrics.adaptation_speed,
                'integration_level': self.evolution_metrics.integration_level,
                'quantum_coherence': self.evolution_metrics.quantum_coherence,
                'evolution_timestamp': self.evolution_metrics.evolution_timestamp.isoformat(),
                'metrics_history': self.evolution_metrics.metrics_history
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class WarpRule(Rule):
    """Regra específica do sistema WARP"""
    def __init__(
        self,
        rule_type: RuleType,
        consciousness_level: ConsciousnessLevel,
        content: Dict[str, Any],
        warp_specific_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(rule_type, consciousness_level, content, metadata)
        self.warp_specific_data = warp_specific_data

    def evolve(self) -> bool:
        """Evolui a regra WARP considerando dados específicos"""
        if super().evolve():
            try:
                # Evolução específica do WARP
                self.warp_specific_data['evolution_count'] = self.warp_specific_data.get('evolution_count', 0) + 1
                self.warp_specific_data['last_evolution'] = datetime.now().isoformat()
                return True
            except Exception as e:
                print(f"Erro durante evolução específica WARP: {e}")
                return False
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Converte a regra WARP para dicionário"""
        base_dict = super().to_dict()
        base_dict['warp_specific_data'] = self.warp_specific_data
        return base_dict

