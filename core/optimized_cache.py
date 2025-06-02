import asyncio
import json
import logging
import time
from typing import Any, Dict, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import redis.asyncio as redis
import psutil

@dataclass
class CacheStats:
    """Estatísticas detalhadas do cache"""
    hits: int = 0
    misses: int = 0
    memory_hits: int = 0
    redis_hits: int = 0
    evictions: int = 0
    total_requests: int = 0
    avg_latency: float = 0.0
    memory_usage: float = 0.0
    access_patterns: Dict[str, int] = field(default_factory=dict)
    ttl_stats: Dict[str, float] = field(default_factory=dict)

    def update_latency(self, latency: float):
        """Atualiza a latência média"""
        self.avg_latency = (self.avg_latency * self.total_requests + latency) / (self.total_requests + 1)
        self.total_requests += 1

    def update_memory_usage(self):
        """Atualiza estatísticas de uso de memória"""
        self.memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB

    def update_access_pattern(self, key: str):
        """Registra padrão de acesso"""
        self.access_patterns[key] = self.access_patterns.get(key, 0) + 1

    def update_ttl_stats(self, key: str, ttl: float):
        """Atualiza estatísticas de TTL"""
        self.ttl_stats[key] = ttl

    def to_dict(self) -> Dict[str, Any]:
        """Converte estatísticas para dicionário"""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "memory_hits": self.memory_hits,
            "redis_hits": self.redis_hits,
            "hit_ratio": self.hits / max(self.total_requests, 1),
            "avg_latency": self.avg_latency,
            "evictions": self.evictions,
            "memory_usage_mb": self.memory_usage,
            "total_requests": self.total_requests,
            "access_patterns": self.access_patterns,
            "ttl_stats": self.ttl_stats
        }

@dataclass
class CacheItem:
    """Item armazenado no cache com metadados"""
    value: Any
    expiry: datetime
    access_count: int = 0
    last_access: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

class OptimizedCache:
    """Cache multicamada com gerenciamento adaptativo e métricas detalhadas"""
    
    def __init__(
        self,
        redis_url: str = "redis://localhost",
        memory_max_size: int = 1000,
        default_ttl: int = 3600,
        min_ttl: int = 60,
        max_ttl: int = 86400
    ):
        self.redis_client = redis.from_url(redis_url)
        self.memory_cache: Dict[str, CacheItem] = {}
        self.memory_max_size = memory_max_size
        self.default_ttl = default_ttl
        self.min_ttl = min_ttl
        self.max_ttl = max_ttl
        self.stats = CacheStats()
        self.logger = logging.getLogger("OptimizedCache")

        # Configuração de logging
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(handler)

        # Inicia tarefas de manutenção
        asyncio.create_task(self._maintenance_loop())

    async def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache com fallback automático"""
        start_time = time.time()

        try:
            # Tenta memória primeiro
            if key in self.memory_cache:
                item = self.memory_cache[key]
                if item.expiry > datetime.now():
                    # Atualiza estatísticas de acesso
                    item.access_count += 1
                    item.last_access = datetime.now()
                    self.stats.hits += 1
                    self.stats.memory_hits += 1
                    self.stats.update_access_pattern(key)
                    self.stats.update_latency(time.time() - start_time)
                    return item.value
                else:
                    # Remove item expirado
                    del self.memory_cache[key]
                    self.stats.evictions += 1

            # Fallback para Redis
            value = await self.redis_client.get(key)
            if value:
                value = json.loads(value)
                # Atualiza cache em memória com TTL adaptativo
                ttl = await self.redis_client.ttl(key)
                if ttl > 0:
                    await self._update_memory_cache(key, value, ttl=ttl)
                self.stats.hits += 1
                self.stats.redis_hits += 1
                self.stats.update_access_pattern(key)
                self.stats.update_latency(time.time() - start_time)
                return value

            self.stats.misses += 1
            self.stats.update_latency(time.time() - start_time)
            return None

        except Exception as e:
            self.logger.error(f"Erro ao recuperar do cache: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Armazena valor no cache com TTL adaptativo"""
        try:
            # Calcula TTL adaptativo
            adaptive_ttl = self._calculate_adaptive_ttl(key, ttl)
            expiry = datetime.now() + timedelta(seconds=adaptive_ttl)

            # Armazena em memória
            await self._update_memory_cache(key, value, ttl=adaptive_ttl)
            
            # Armazena no Redis
            await self.redis_client.setex(
                key,
                adaptive_ttl,
                json.dumps(value)
            )

            self.stats.update_ttl_stats(key, adaptive_ttl)
            return True

        except Exception as e:
            self.logger.error(f"Erro ao armazenar no cache: {e}")
            return False

    def _calculate_adaptive_ttl(self, key: str, requested_ttl: Optional[int] = None) -> int:
        """Calcula TTL adaptativo baseado em padrões de uso"""
        base_ttl = requested_ttl or self.default_ttl
        
        # Ajusta TTL baseado em frequência de acesso
        access_count = self.stats.access_patterns.get(key, 0)
        if access_count > 0:
            # Aumenta TTL para itens frequentemente acessados
            adaptive_ttl = base_ttl * (1 + (access_count / 100))
            return min(max(int(adaptive_ttl), self.min_ttl), self.max_ttl)
        
        return base_ttl

    async def _update_memory_cache(
        self,
        key: str,
        value: Any,
        ttl: int
    ):
        """Atualiza cache em memória com política de priorização"""
        if len(self.memory_cache) >= self.memory_max_size:
            # Remove itens baseado em política de priorização
            await self._evict_items()

        expiry = datetime.now() + timedelta(seconds=ttl)
        self.memory_cache[key] = CacheItem(
            value=value,
            expiry=expiry
        )
        self.stats.update_memory_usage()

    async def _evict_items(self):
        """Remove itens do cache baseado em política de priorização"""
        now = datetime.now()
        
        # Remove itens expirados primeiro
        expired = [k for k, v in self.memory_cache.items() if v.expiry <= now]
        for key in expired:
            del self.memory_cache[key]
            self.stats.evictions += 1

        # Se ainda precisa de espaço, remove itens menos acessados
        if len(self.memory_cache) >= self.memory_max_size:
            sorted_items = sorted(
                self.memory_cache.items(),
                key=lambda x: (x[1].access_count, x[1].last_access)
            )
            for key, _ in sorted_items[:int(self.memory_max_size * 0.1)]:  # Remove 10% menos acessados
                del self.memory_cache[key]
                self.stats.evictions += 1

    async def _maintenance_loop(self):
        """Loop de manutenção periódica"""
        while True:
            try:
                await asyncio.sleep(60)  # Executa a cada minuto
                await self._perform_maintenance()
            except Exception as e:
                self.logger.error(f"Erro na manutenção: {e}")

    async def _perform_maintenance(self):
        """Executa tarefas de manutenção"""
        try:
            # Limpa itens expirados
            now = datetime.now()
            expired = [k for k, v in self.memory_cache.items() if v.expiry <= now]
            for key in expired:
                del self.memory_cache[key]
                self.stats.evictions += 1

            # Atualiza estatísticas
            self.stats.update_memory_usage()

            # Log de status
            self.logger.info(
                f"Manutenção: {len(expired)} itens removidos, "
                f"Uso de memória: {self.stats.memory_usage:.2f}MB"
            )

        except Exception as e:
            self.logger.error(f"Erro durante manutenção: {e}")

    async def clear(self):
        """Limpa todo o cache"""
        try:
            self.memory_cache.clear()
            await self.redis_client.flushdb()
            self.stats = CacheStats()  # Reseta estatísticas
            return True
        except Exception as e:
            self.logger.error(f"Erro ao limpar cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas do cache"""
        return self.stats.to_dict()

