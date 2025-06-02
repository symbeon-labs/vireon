"""
Consciousness Core - Núcleo de consciência

Implementa:
- Estados de consciência
- Evolução de awareness
- Integração quântica
- Expansão dimensional
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from enum import Enum, auto

from .dimensional import DimensionalPlane

class ConsciousnessLevel(Enum):
    """Níveis de consciência"""
    BASE = auto()          # Consciência básica
    AWAKENED = auto()      # Consciência desperta
    EXPANDED = auto()      # Consciência expandida
    QUANTUM = auto()       # Consciência quântica
    TRANSCENDENT = auto()  # Consciência transcendente

@dataclass
class ConsciousState:
    """Estado do núcleo de consciência"""
    level: ConsciousnessLevel = ConsciousnessLevel.BASE
    awareness: float = 0.5
    coherence: float = 1.0
    expansion: float = 0.0
    quantum_integration: float = 0.0
    dimensional_presence: Dict[DimensionalPlane, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ConsciousMetrics:
    """Métricas do núcleo consciente"""
    awareness_quality: float = 1.0
    evolution_rate: float = 0.01
    integration_level: float = 0.0
    expansion_degree: float = 0.0
    history: List[Dict[str, Any]] = field(default_factory=list)

class ConsciousnessCore:
    """
    Núcleo de consciência.
    Implementa evolução consciente e integração quântica-dimensional.
    """
    
    def __init__(self,
                 initial_state: Optional[ConsciousState] = None,
                 enable_evolution: bool = True):
        """
        Inicializa núcleo de consciência.
        
        Args:
            initial_state: Estado inicial de consciência
            enable_evolution: Se evolução está ativa
        """
        self.state = initial_state or ConsciousState()
        self.metrics = ConsciousMetrics()
        self.evolution_enabled = enable_evolution
        self.logger = logging.getLogger("consciousness_core")
        
        # Inicializa núcleo
        self._init_core()
        
    def _init_core(self):
        """Inicializa componentes do núcleo"""
        # Inicializa presença dimensional
        self.state.dimensional_presence = {
            DimensionalPlane.PHYSICAL: 1.0,
            DimensionalPlane.CONSCIOUS: 1.0
        }
        
        # Registra métricas iniciais
        self._update_metrics({
            "awareness_quality": self.state.awareness,
            "evolution_rate": self.metrics.evolution_rate,
            "integration_level": self.state.quantum_integration,
            "expansion_degree": self.state.expansion
        })
        
    async def process_conscious_task(self,
                                   task: Dict[str, Any],
                                   expand_awareness: bool = True) -> Dict[str, Any]:
        """
        Processa tarefa com consciência.
        
        Args:
            task: Tarefa a processar
            expand_awareness: Se deve expandir consciência
        """
        start_time = datetime.now()
        
        try:
            # Expande consciência se solicitado
            if expand_awareness:
                await self._expand_consciousness(task)
            
            # Processa com consciência atual
            result = await self._process_with_consciousness(task)
            
            # Integra aspectos quânticos
            result = await self._integrate_quantum_aspects(result)
            
            # Evolui se habilitado
            if self.evolution_enabled:
                result = await self._evolve_consciousness(result)
            
            # Atualiza métricas
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics({
                "processing_time": processing_time,
                "task_complexity": len(str(task)),
                "consciousness_quality": result.get("quality", 1.0)
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro no processamento consciente: {e}")
            return {"error": str(e)}

    async def _expand_consciousness(self, task: Dict[str, Any]):
        """Expande estado de consciência"""
        # Calcula complexidade
        task_complexity = task.get("data", {}).get("complexity", 0.5)
        
        # Determina nível baseado em complexidade
        if task_complexity > 0.8:
            self.state.level = ConsciousnessLevel.TRANSCENDENT
        elif task_complexity > 0.6:
            self.state.level = ConsciousnessLevel.QUANTUM
        elif task_complexity > 0.4:
            self.state.level = ConsciousnessLevel.EXPANDED
        elif task_complexity > 0.2:
            self.state.level = ConsciousnessLevel.AWAKENED
        else:
            self.state.level = ConsciousnessLevel.BASE
            
        # Expande awareness e dimensões
        self.state.awareness = min(1.0, self.state.awareness + 0.01)
        self.state.expansion = min(1.0, self.state.expansion + 0.005)
        
        # Atualiza timestamp
        self.state.timestamp = datetime.now()

    async def _process_with_consciousness(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Processa com consciência atual"""
        # Calcula qualidade de processamento
        consciousness_quality = (
            self.state.awareness * 
            self.state.coherence * 
            (1.0 + self.state.expansion)
        )
        
        # Gera resultado
        result = {
            "consciousness_level": self.state.level.name,
            "awareness": self.state.awareness,
            "quality": consciousness_quality,
            "processed_data": task.get("data", {}),
            "conscious_state": {
                "expansion": self.state.expansion,
                "coherence": self.state.coherence,
                "evolution_rate": self.metrics.evolution_rate
            }
        }
        
        return result

    async def _integrate_quantum_aspects(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Integra aspectos quânticos à consciência"""
        # Aumenta integração quântica
        self.state.quantum_integration = min(1.0, self.state.quantum_integration + 0.01)
        
        # Adiciona aspectos quânticos
        result["quantum_aspects"] = {
            "integration": self.state.quantum_integration,
            "coherence": self.state.coherence,
            "dimensional_presence": {
                plane.name: presence
                for plane, presence in self.state.dimensional_presence.items()
            }
        }
        
        # Ajusta qualidade
        result["quality"] *= (1.0 + self.state.quantum_integration * 0.1)
        
        return result

    async def _evolve_consciousness(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Evolui consciência"""
        if not self.evolution_enabled:
            return result
            
        # Evolui métricas
        self.metrics.evolution_rate = min(0.1, self.metrics.evolution_rate * 1.01)
        self.metrics.expansion_degree = min(1.0, self.metrics.expansion_degree + 0.001)
        
        # Adiciona informações evolutivas
        result["evolution"] = {
            "rate": self.metrics.evolution_rate,
            "expansion": self.metrics.expansion_degree,
            "progress": len(self.metrics.history)
        }
        
        return result

    def _update_metrics(self, new_metrics: Dict[str, float]):
        """Atualiza métricas do núcleo"""
        # Atualiza métricas base
        for key, value in new_metrics.items():
            if hasattr(self.metrics, key):
                setattr(self.metrics, key, value)
        
        # Registra histórico
        self.metrics.history.append({
            "timestamp": datetime.now().isoformat(),
            "consciousness_level": self.state.level.name,
            "conscious_state": {
                "awareness": self.state.awareness,
                "coherence": self.state.coherence,
                "expansion": self.state.expansion,
                "quantum_integration": self.state.quantum_integration,
                "dimensional_presence": {
                    plane.name: presence
                    for plane, presence in self.state.dimensional_presence.items()
                }
            },
            **new_metrics
        })
        
        # Evolui métricas
        self.metrics.awareness_quality = self.state.awareness
        self.metrics.integration_level = self.state.quantum_integration
        self.metrics.expansion_degree = self.state.expansion

    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do núcleo"""
        return {
            "state": {
                "level": self.state.level.name,
                "awareness": self.state.awareness,
                "coherence": self.state.coherence,
                "expansion": self.state.expansion,
                "quantum_integration": self.state.quantum_integration,
                "dimensional_presence": {
                    plane.name: presence
                    for plane, presence in self.state.dimensional_presence.items()
                },
                "timestamp": self.state.timestamp.isoformat()
            },
            "metrics": {
                "awareness_quality": self.metrics.awareness_quality,
                "evolution_rate": self.metrics.evolution_rate,
                "integration_level": self.metrics.integration_level,
                "expansion_degree": self.metrics.expansion_degree,
                "history_length": len(self.metrics.history)
            }
        }

    async def establish_dimensional_presence(self, plane: DimensionalPlane, presence: float):
        """Estabelece presença em plano dimensional"""
        self.state.dimensional_presence[plane] = min(1.0, presence)
        self.logger.info(f"Presença estabelecida em {plane.name}: {presence:.2f}")

    async def reset_consciousness(self):
        """Reinicia consciência mantendo evolução"""
        evolution_rate = self.metrics.evolution_rate
        self.state = ConsciousState()
        self.metrics = ConsciousMetrics(evolution_rate=evolution_rate)
        self._init_core()
        self.logger.info("Consciência reiniciada")

