"""
VIREON Warp Optimus - Módulo de otimização do consumo de tarefas Warp

Este módulo implementa mecanismos para:
- Cache local de requisições e resultados
- Simulação dry-run antes de executar tarefas
- Detecção de redundância usando hash semântico 
- Monitoramento e controle de quotas
- Promoção automática de padrões frequentes para regras locais
"""

from .cache_manager import CacheManager
from .dry_run import DryRunSimulator
from .resource_sentinel import VireonSentinel
from .semantic_hash import semantic_min_hash, raw_sha256
from .warp_adapter import WarpAdapter, Request, Response, Cost

__version__ = "0.1.0"
