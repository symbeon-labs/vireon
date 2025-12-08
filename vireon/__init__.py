"""
VIREON Core - Universal Agentic Orchestration
==============================================

Main entry point for the VIREON orchestration system.
"""

__version__ = "0.2.0-alpha"
__author__ = "JX (SH1W4)"

from .core import VireonCore
from .models import AgentResult, SwarmConsensus

__all__ = ["VireonCore", "AgentResult", "SwarmConsensus"]
