"""
Módulo de modelos para o SDK VIREON.

Define as classes de dados utilizadas para representar entidades
e resultados da API VIREON.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union


class RuleType(str, Enum):
    """Tipos de regras suportados."""
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    ARCHITECTURE = "architecture"
    WORKFLOW = "workflow"
    SYMBIOTIC = "symbiotic"


@dataclass
class Rule:
    """Representa uma regra simbiótica."""
    
    id: Optional[str] = None
    rule_type: Union[str, RuleType] = RuleType.LANGUAGE
    content: str = ""
    priority: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __str__(self) -> str:
        """Representação de string da regra."""
        return f"Rule({self.id}, {self.rule_type}, priority={self.priority})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a regra para dicionário."""
        rule_type = self.rule_type
        if not isinstance(rule_type, str):
            rule_type = rule_type.value
            
        return {
            "id": self.id,
            "rule_type": rule_type,
            "content": self.content,
            "priority": self.priority,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class EvaluationResult:
    """Resultado da avaliação de uma regra."""
    
    success: bool = False
    result: str = ""
    error_message: Optional[str] = None
    duration_ms: float = 0.0
    engine_type: str = "unknown"
    rule_id: str = ""
    rule_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Representação de string do resultado."""
        status = "Sucesso" if self.success else "Falha"
        return f"EvaluationResult({status}, engine={self.engine_type}, duration={self.duration_ms}ms)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o resultado para dicionário."""
        return {
            "success": self.success,
            "result": self.result,
            "error_message": self.error_message,
            "duration_ms": self.duration_ms,
            "engine_type": self.engine_type,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class SimulationResult:
    """Resultado da simulação (dry-run) de uma regra."""
    
    success: bool = False
    confidence: float = 0.0
    action: str = ""
    message: Optional[str] = None
    
    def __str__(self) -> str:
        """Representação de string do resultado da simulação."""
        status = "Sucesso" if self.success else "Falha"
        return f"SimulationResult({status}, confidence={self.confidence:.2f})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o resultado da simulação para dicionário."""
        return {
            "success": self.success,
            "confidence": self.confidence,
            "action": self.action,
            "message": self.message
        }


@dataclass
class Metrics:
    """Métricas do sistema VIREON."""
    
    engine_type: str = "unknown"
    sage_x_available: bool = False
    sage_x_initialized: bool = False
    cache_hits: Optional[int] = None
    cache_misses: Optional[int] = None
    rules_evaluated: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Representação de string das métricas."""
        engine_status = "inicializado" if self.sage_x_initialized else "não inicializado"
        return f"Metrics({self.engine_type}, {engine_status}, hits={self.cache_hits})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte as métricas para dicionário."""
        return {
            "engine_type": self.engine_type,
            "sage_x_available": self.sage_x_available,
            "sage_x_initialized": self.sage_x_initialized,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "rules_evaluated": self.rules_evaluated,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    @property
    def cache_hit_rate(self) -> float:
        """Taxa de acertos de cache."""
        if self.cache_hits is None or self.cache_misses is None:
            return 0.0
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

