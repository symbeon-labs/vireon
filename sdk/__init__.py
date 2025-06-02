"""
VIREON SDK - Cliente Python para interação com a API VIREON.

Este módulo fornece uma interface de programação para interação
com o sistema VIREON de meta-governança simbiótica para agentes de IA.
"""

from .client import VireonClient, RuleClient, EvaluationClient
from .models import Rule, RuleType, EvaluationResult, SimulationResult, Metrics

__version__ = "0.1.0"
__all__ = [
    "VireonClient",
    "RuleClient",
    "EvaluationClient",
    "Rule",
    "RuleType",
    "EvaluationResult",
    "SimulationResult",
    "Metrics"
]

