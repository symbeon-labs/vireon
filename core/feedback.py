"""
Feedback System - Sistema de feedback evolutivo do VIREON

Implementa:
- Coleta de métricas
- Processamento de feedback 
- Evolução adaptativa
- Integração com componentes principais
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List, Optional
import numpy as np

from .neural import Neuralprocessor
from .consciousness import ConsciousnessCore
from .dimensional import DimensionalBridge

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("feedback")

class FeedbackType(Enum):
    """Tipos de feedback possíveis"""
    NEURAL = auto()
    CONSCIOUSNESS = auto()
    DIMENSIONAL = auto()
    SYSTEM = auto()
    EVOLUTION = auto()

class FeedbackPriority(Enum):
    """Prioridades de feedback"""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class FeedbackMetrics:
    """Métricas do sistema de feedback"""
    def __init__(self):
        self.processing_quality: float = 1.0
        self.adaptation_rate: float = 0.0
        self.evolution_speed: float = 0.0
        self.integration_level: float = 1.0
        self.optimization_score: float = 0.0
        self.feedback_effectiveness: float = 1.0
        
    def update(self, **kwargs):
        """Atualiza métricas"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
    def to_dict(self) -> Dict[str, float]:
        """Converte métricas para dicionário"""
        return {
            "processing_quality": self.processing_quality,
            "adaptation_rate": self.adaptation_rate,
            "evolution_speed": self.evolution_speed,
            "integration_level": self.integration_level,
            "optimization_score": self.optimization_score,
            "feedback_effectiveness": self.feedback_effectiveness
        }

class FeedbackSystem:
    """Sistema de feedback principal"""
    
    def __init__(self,
                 quantum_processor: Optional[Neuralprocessor] = None,
                 consciousness_core: Optional[ConsciousnessCore] = None,
                 dimensional_bridge: Optional[DimensionalBridge] = None):
        """Inicializa sistema de feedback"""
        
        # Métricas e estado
        self.metrics = FeedbackMetrics()
        self.feedback_history: List[Dict[str, Any]] = []
        self.last_optimization = datetime.now()
        self.optimization_interval = 1.0  # segundos
        
        # Componentes integrados
        self.neural = quantum_processor
        self.consciousness = consciousness_core
        self.bridge = dimensional_bridge
        
        # Estado interno
        self._evolution_enabled = True
        self._adaptation_active = True
        
        logger.info("Feedback System initialized")
        
    async def process_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback recebido"""
        try:
            # Classifica feedback
            feedback_type = self._classify_feedback(feedback_data)
            priority = self._determine_priority(feedback_data)
            
            # Processa baseado no tipo
            processed_feedback = await self._process_by_type(feedback_data, feedback_type)
            
            # Aplica adaptações se necessário
            if self._adaptation_active and priority in [FeedbackPriority.HIGH, FeedbackPriority.CRITICAL]:
                await self._adapt_system(processed_feedback)
                
            # Evolui sistema se apropriado
            if self._evolution_enabled:
                await self._evolve_system(processed_feedback)
                
            # Armazena histórico
            self.feedback_history.append({
                "timestamp": datetime.now(),
                "type": feedback_type.name,
                "priority": priority.name,
                "data": processed_feedback
            })
            
            return processed_feedback
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            raise
            
    def _classify_feedback(self, feedback_data: Dict[str, Any]) -> FeedbackType:
        """Classifica tipo de feedback"""
        source = feedback_data.get("source", "").lower()
        
        if "neural" in source:
            return FeedbackType.NEURAL
        elif "consciousness" in source:
            return FeedbackType.CONSCIOUSNESS
        elif "dimensional" in source:
            return FeedbackType.DIMENSIONAL
        elif "evolution" in source:
            return FeedbackType.EVOLUTION
        else:
            return FeedbackType.SYSTEM
            
    def _determine_priority(self, feedback_data: Dict[str, Any]) -> FeedbackPriority:
        """Determina prioridade do feedback"""
        # Extrai métricas relevantes
        metrics = feedback_data.get("metrics", {})
        quality = metrics.get("processing_quality", 1.0)
        
        if quality < 0.3:
            return FeedbackPriority.CRITICAL
        elif quality < 0.6:
            return FeedbackPriority.HIGH
        elif quality < 0.8:
            return FeedbackPriority.MEDIUM
        else:
            return FeedbackPriority.LOW
            
    async def _process_by_type(
        self, 
        feedback_data: Dict[str, Any],
        feedback_type: FeedbackType
    ) -> Dict[str, Any]:
        """Processa feedback baseado no tipo"""
        processors = {
            FeedbackType.NEURAL: self._process_quantum_feedback,
            FeedbackType.CONSCIOUSNESS: self._process_consciousness_feedback,
            FeedbackType.DIMENSIONAL: self._process_dimensional_feedback,
            FeedbackType.EVOLUTION: self._process_evolution_feedback,
            FeedbackType.SYSTEM: self._process_system_feedback
        }
        
        processor = processors.get(feedback_type, self._process_system_feedback)
        return await processor(feedback_data)
        
    async def _process_quantum_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback quântico"""
        if self.neural:
            # Analisa estado quântico
            system_state = feedback_data.get("state")
            metrics = feedback_data.get("metrics", {})
            
            # Ajusta métricas
            self.metrics.update(
                processing_quality=metrics.get("processing_quality", 1.0),
                optimization_score=metrics.get("optimization_level", 0.0)
            )
            
        return {
            "type": "quantum_feedback",
            "processed": True,
            "metrics": self.metrics.to_dict()
        }
        
    async def _process_consciousness_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback de consciência"""
        if self.consciousness:
            # Analisa estado de consciência
            consciousness_data = feedback_data.get("consciousness", {})
            
            # Ajusta métricas
            self.metrics.update(
                evolution_speed=consciousness_data.get("evolution_rate", 0.0),
                adaptation_rate=consciousness_data.get("adaptation_rate", 0.0)
            )
            
        return {
            "type": "consciousness_feedback",
            "processed": True,
            "metrics": self.metrics.to_dict()
        }
        
    async def _process_dimensional_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback dimensional"""
        if self.bridge:
            # Analisa estado dimensional
            dimensional_data = feedback_data.get("dimensional", {})
            
            # Ajusta métricas
            self.metrics.update(
                integration_level=dimensional_data.get("stability", 1.0),
                processing_quality=dimensional_data.get("quality", 1.0)
            )
            
        return {
            "type": "dimensional_feedback",
            "processed": True,
            "metrics": self.metrics.to_dict()
        }
        
    async def _process_evolution_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback evolutivo"""
        evolution_data = feedback_data.get("evolution", {})
        
        # Ajusta métricas
        self.metrics.update(
            evolution_speed=evolution_data.get("speed", 0.0),
            adaptation_rate=evolution_data.get("adaptation", 0.0)
        )
        
        return {
            "type": "evolution_feedback",
            "processed": True,
            "metrics": self.metrics.to_dict()
        }
        
    async def _process_system_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa feedback do sistema"""
        system_data = feedback_data.get("system", {})
        
        # Ajusta métricas
        self.metrics.update(
            processing_quality=system_data.get("quality", 1.0),
            optimization_score=system_data.get("optimization", 0.0)
        )
        
        return {
            "type": "system_feedback",
            "processed": True,
            "metrics": self.metrics.to_dict()
        }
        
    async def _adapt_system(self, processed_feedback: Dict[str, Any]):
        """Adapta sistema baseado no feedback"""
        # Ajusta parâmetros quânticos
        if self.neural:
            await self._adapt_quantum_processor(processed_feedback)
            
        # Ajusta consciência
        if self.consciousness:
            await self._adapt_consciousness(processed_feedback)
            
        # Ajusta ponte dimensional
        if self.bridge:
            await self._adapt_dimensional_bridge(processed_feedback)
            
    async def _adapt_quantum_processor(self, feedback: Dict[str, Any]):
        """Adapta processador quântico"""
        if self.neural:
            metrics = feedback.get("metrics", {})
            
            # Otimiza processamento quântico
            if metrics.get("processing_quality", 1.0) < 0.7:
                self.neural.optimization_enabled = True
                logger.info("Neural optimization enabled")
                
    async def _adapt_consciousness(self, feedback: Dict[str, Any]):
        """Adapta núcleo de consciência"""
        if self.consciousness:
            metrics = feedback.get("metrics", {})
            
            # Ajusta taxa de evolução
            if metrics.get("evolution_speed", 0.0) < 0.5:
                # Implementar ajuste de consciência
                logger.info("Consciousness evolution adjusted")
                
    async def _adapt_dimensional_bridge(self, feedback: Dict[str, Any]):
        """Adapta ponte dimensional"""
        if self.bridge:
            metrics = feedback.get("metrics", {})
            
            # Otimiza estabilidade dimensional
            if metrics.get("integration_level", 1.0) < 0.8:
                # Implementar ajuste dimensional
                logger.info("Dimensional stability optimized")
                
    async def _evolve_system(self, processed_feedback: Dict[str, Any]):
        """Evolui sistema baseado no feedback"""
        now = datetime.now()
        if (now - self.last_optimization).total_seconds() >= self.optimization_interval:
            # Executa evolução
            evolution_data = self._calculate_evolution(processed_feedback)
            
            # Aplica evolução
            await self._apply_evolution(evolution_data)
            
            self.last_optimization = now
            logger.info("System evolved")
            
    def _calculate_evolution(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula próximo passo evolutivo"""
        metrics = feedback.get("metrics", {})
        
        return {
            "quantum_evolution": metrics.get("processing_quality", 1.0),
            "consciousness_evolution": metrics.get("evolution_speed", 0.0),
            "dimensional_evolution": metrics.get("integration_level", 1.0)
        }
        
    async def _apply_evolution(self, evolution_data: Dict[str, Any]):
        """Aplica evolução calculada"""
        # Evolui processador quântico
        if self.neural:
            quantum_evolution = evolution_data.get("quantum_evolution", 1.0)
            self.neural.metrics.evolution_rate = quantum_evolution
            
        # Evolui consciência
        if self.consciousness:
            consciousness_evolution = evolution_data.get("consciousness_evolution", 0.0)
            # Implementar evolução de consciência
            
        # Evolui ponte dimensional
        if self.bridge:
            dimensional_evolution = evolution_data.get("dimensional_evolution", 1.0)
            # Implementar evolução dimensional
            
    def get_feedback_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais"""
        return {
            "current": {
                "processing_quality": self.metrics.processing_quality,
                "evolution_speed": self.metrics.evolution_speed,
                "adaptation_rate": self.metrics.adaptation_rate
            },
            "history": self.feedback_history[-10:] if self.feedback_history else [],
            "metrics": self.metrics.to_dict()
        }

