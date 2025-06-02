"""
Utilitários gerais para suporte ao processamento de pesquisas.

Este módulo contém funções auxiliares e utilitários que são usados em
várias partes do pacote research_packager.
"""

from typing import Any, Dict, List
import json
import logging

logger = logging.getLogger(__name__)

def setup_logging(level: int = logging.INFO) -> None:
    """Configura o logging básico para o pacote."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

