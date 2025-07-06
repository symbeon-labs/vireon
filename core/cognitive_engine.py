import asyncio
import logging
from typing import Any, Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass, field

from .optimized_cache import OptimizedCache
from .quantum_lite import QuantumLite

@dataclass
class EngineMetrics:
    """Métricas do motor cognitivo"""
    total_processed: int = 0
    cache_usage: Dict[str, int] = field(default_factory=dict)
    quantum_usage: Dict[str, int] = field(default_factory=dict)
    avg_processing_time: float = 0.0
    operation_history: List[Dict[str, Any]] = field(default_factory=list)

    def update_metrics(self, operation_type: str, processing_time: float, cache_hit: bool):
        """Atualiza métricas de operação"""
        self.total_processed += 1
        
        # Atualiza métricas de cache
        cache_status = "hit" if cache_hit else "miss"
        self.cache_usage[cache_status] = self.cache_usage.get(cache_status, 0) + 1
        
        # Atualiza métricas de tipo de operação
        self.quantum_usage[operation_type] = self.quantum_usage.get(operation_type, 0) + 1
        
        # Atualiza tempo médio
        self.avg_processing_time = (
            (self.avg_processing_time * (self.total_processed - 1) + processing_time)
            / self.total_processed
        )
        
        # Registra operação no histórico
        self.operation_history.append({
            "type": operation_type,
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time,
            "cache_hit": cache_hit
        })
        
        # Mantém histórico limitado
        if len(self.operation_history) > 1000:
            self.operation_history = self.operation_history[-1000:]

class CognitiveEngine:
    """Motor cognitivo otimizado com cache e processamento quântico simplificado"""
    
    def __init__(
        self,
        redis_url: str = "redis://localhost",
        cache_size: int = 1000,
        cache_ttl: int = 3600
    ):
        self.cache = OptimizedCache(
            redis_url=redis_url,
            memory_max_size=cache_size,
            default_ttl=cache_ttl
        )
        self.neural = QuantumLite()
        self.metrics = EngineMetrics()
        self.logger = logging.getLogger("CognitiveEngine")
        
        # Configuração de logging
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(handler)

    async def process(
        self,
        input_data: Dict[str, Any],
        operation_type: str = "default",
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Processa input usando cache e camada quântica otimizada"""
        start_time = datetime.now()
        cache_hit = False

        try:
            # Gera chave de cache
            cache_key = self._generate_cache_key(input_data, operation_type)
            
            # Verifica cache se habilitado
            if use_cache:
                cached_result = await self.cache.get(cache_key)
                if cached_result:
                    cache_hit = True
                    self.logger.info(f"Cache hit para operação {operation_type}")
                    return cached_result

            # Processamento quântico simplificado
            processed_state = await self.neural.process_state(
                input_data,
                operation_type
            )
            
            if not processed_state:
                self.logger.error("Falha no processamento quântico")
                return None

            # Valida coerência
            if not await self.neural.validate_coherence(processed_state):
                self.logger.warning("Estado quântico incoerente detectado")
                return None

            # Armazena em cache se habilitado
            if use_cache:
                await self.cache.set(cache_key, processed_state)

            return processed_state

        except Exception as e:
            self.logger.error(f"Erro no processamento cognitivo: {e}")
            return None
            
        finally:
            # Atualiza métricas
            processing_time = (datetime.now() - start_time).total_seconds()
            self.metrics.update_metrics(operation_type, processing_time, cache_hit)

    def _generate_cache_key(self, input_data: Dict[str, Any], operation_type: str) -> str:
        """Gera chave única para cache"""
        # Simplificado - pode ser expandido para melhor unicidade
        return f"{operation_type}:{hash(str(input_data))}"

    async def cleanup(self):
        """Limpa recursos do motor"""
        try:
            await asyncio.gather(
                self.cache.clear(),
                self.neural.cleanup()
            )
            self.logger.info("Limpeza do motor cognitivo concluída")
            return True
        except Exception as e:
            self.logger.error(f"Erro na limpeza do motor: {e}")
            return False

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas consolidadas"""
        return {
            "engine": {
                "total_processed": self.metrics.total_processed,
                "avg_processing_time": self.metrics.avg_processing_time,
                "cache_usage": self.metrics.cache_usage,
                "quantum_usage": self.metrics.quantum_usage
            },
            "cache": self.cache.get_metrics(),
            "neural": self.neural.get_metrics()
        }

    async def optimize_performance(self):
        """Otimiza performance do motor"""
        self.logger.info("Iniciando otimização de performance")
        
        try:
            # Limpa cache expirado
            await self.cache.cleanup_expired()
            
            # Análise de métricas para ajustes
            metrics = self.get_metrics()
            cache_hit_rate = metrics["cache"]["hits"] / max(metrics["cache"]["total_requests"], 1)
            
            # Ajusta parâmetros baseado nas métricas
            if cache_hit_rate < 0.5:
                self.logger.warning("Taxa de cache hit baixa - considerar ajustes")
            
            return True
        except Exception as e:
            self.logger.error(f"Erro na otimização: {e}")
            return False

