#!/usr/bin/env python
"""
Exemplo de uso do SDK VIREON.

Este script demonstra como utilizar o SDK para interagir com a plataforma VIREON,
incluindo autenticação, gerenciamento de regras, avaliação e métricas.
"""

import json
import logging
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("vireon_sdk_example.log", encoding="utf-8")
    ]
)

logger = logging.getLogger("vireon.example")

# Importar SDK
sys.path.insert(0, '..')  # Para execução a partir do diretório sdk
from vireon_sdk import VireonClient, Rule, RuleType


def main():
    """Função principal com exemplos de uso do SDK."""
    # Inicializar cliente
    logger.info("Inicializando cliente VIREON...")
    client = VireonClient(
        base_url="http://localhost:8000",
        username="demo",
        password="vireon_demo"
    )
    
    # Exemplo 1: Listar regras existentes
    logger.info("Exemplo 1: Listar regras existentes")
    try

