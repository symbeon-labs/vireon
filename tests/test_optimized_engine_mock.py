import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import matplotlib.pyplot as plt
from pathlib import Path

class MockRedis:
    """Implementação mock do Redis para testes"""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._expiry: Dict[str, datetime] = {}

    async def get(self, key: str) -> Optional[bytes]:
        if key not in self._data:
            return None
        if key in self._expiry and datetime.now() > self._expiry[key]:
            del self._data[key]
            del self._expiry[key]
            return None
        return self._data[key].encode() if isinstance(self._data[key], str) else self._data[key]

    async def setex(self, key: str, seconds: int, value: Any) -> bool:
        self._data[key] = value
        self._expiry[key] = datetime.now() + timedelta(seconds=seconds)
        return True

    async def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            if key in self._expiry:
                del self._expiry[key]
            return True
        return False

    async def ttl(self, key: str) -> int:
        if key not in self._expiry:
            return -1
        remaining = (self._expiry[key] - datetime.now()).total_seconds()
        return max(0, int(remaining))

    async def flushdb(self) -> bool:
        self._data.clear()
        self._expiry.clear()
        return True

class TestMetrics:
    """Classe para coleta e análise de métricas de teste"""
    
    def __init__(self):
        self.cache_hits: List[float] = []
        self.cache_misses: List[float] = []
        self.latencies: List[float] = []
        self.memory_usage: List[float] = []
        self.quantum_success: List[float] = []
        self.start_time = time.time()

    def record_cache_operation(self, hit: bool, latency: float):
        if hit:
            self.cache_hits.append(latency)
        else:
            self.cache_misses.append(latency)
        self.latencies.append(latency)

    def record_memory_usage(self, usage: float):
        self.memory_usage.append(usage)

    def record_quantum_operation(self, success: bool):
        self.quantum_success.append(1.0 if success else 0.0)

    def get_summary(self) -> Dict[str, float]:
        total_ops = len(self.cache_hits) + len(self.cache_misses)
        return {
            "total_operations": total_ops,
            "cache_hit_ratio": len(self.cache_hits) / max(total_ops, 1),
            "avg_latency": sum(self.latencies) / max(len(self.latencies), 1),
            "max_memory_usage": max(self.memory_usage) if self.memory_usage else 0,
            "quantum_success_rate": sum(self.quantum_success) / max(len(self.quantum_success), 1),
            "total_runtime": time.time() - self.start_time
        }

class OptimizedSystemTest:
    """Classe de teste para o sistema otimizado"""
    
    def __init__(self):
        self.redis_mock = MockRedis()
        self.metrics = TestMetrics()
        self.logger = logging.getLogger("OptimizedSystemTest")
        self.logger.setLevel(logging.INFO)

    def _generate_test_data(self, size: int = 1000) -> List[Dict[str, Any]]:
        """Gera dados de teste variados"""
        return [
            {
                "id": f"test_{i}",
                "data": f"payload_{i}",
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "complexity": i % 10,
                    "priority": i % 3,
                    "type": f"type_{i % 5}"
                }
            }
            for i in range(size)
        ]

    async def test_cache_operations(self):
        """Testa operações de cache"""
        self.logger.info("Iniciando teste de cache...")
        test_data = self._generate_test_data(500)

        # Teste de escrita
        for item in test_data:
            start_time = time.time()
            await self.redis_mock.setex(f"key_{item['id']}", 3600, json.dumps(item))
            self.metrics.record_cache_operation(True, time.time() - start_time)

        # Teste de leitura
        for i in range(1000):
            start_time = time.time()
            key = f"key_test_{i % 750}"  # Força alguns misses
            result = await self.redis_mock.get(key)
            self.metrics.record_cache_operation(result is not None, time.time() - start_time)

    async def test_quantum_operations(self):
        """Simula operações quânticas"""
        self.logger.info("Iniciando teste quântico...")
        test_data = self._generate_test_data(100)

        for item in test_data:
            # Simula processamento quântico
            success = len(str(item)) % 10 != 0  # Simula taxa de sucesso de 90%
            self.metrics.record_quantum_operation(success)
            await asyncio.sleep(0.01)  # Simula processamento

    def generate_report(self, output_dir: str = "test_results"):
        """Gera relatório detalhado com gráficos"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Gera gráficos
        plt.figure(figsize=(15, 10))

        # Cache Performance
        plt.subplot(2, 2, 1)
        plt.hist(self.metrics.latencies, bins=50)
        plt.title("Distribuição de Latência")
        plt.xlabel("Segundos")
        plt.ylabel("Frequência")

        # Hit/Miss Ratio
        plt.subplot(2, 2, 2)
        hits_misses = [len(self.metrics.cache_hits), len(self.metrics.cache_misses)]
        plt.pie(hits_misses, labels=['Hits', 'Misses'], autopct='%1.1f%%')
        plt.title("Cache Hit/Miss Ratio")

        # Memory Usage
        plt.subplot(2, 2, 3)
        plt.plot(self.metrics.memory_usage)
        plt.title("Uso de Memória")
        plt.xlabel("Operações")
        plt.ylabel("MB")

        # Neural Success
        plt.subplot(2, 2, 4)
        plt.plot(self.metrics.quantum_success)
        plt.title("Taxa de Sucesso Quântico")
        plt.xlabel("Operações")
        plt.ylabel("Taxa de Sucesso")

        plt.tight_layout()
        plt.savefig(output_path / "performance_metrics.png")

        # Gera relatório JSON
        summary = self.metrics.get_summary()
        with open(output_path / "test_report.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": summary,
                "detailed_metrics": {
                    "avg_latency_ms": summary["avg_latency"] * 1000,
                    "cache_hit_ratio": summary["cache_hit_ratio"],
                    "quantum_success_rate": summary["quantum_success_rate"],
                    "total_runtime_seconds": summary["total_runtime"]
                }
            }, f, indent=2)

        self.logger.info(f"Relatório gerado em {output_path}")

async def main():
    """Função principal para execução dos testes"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    test = OptimizedSystemTest()
    
    # Executa testes
    await test.test_cache_operations()
    await test.test_quantum_operations()
    
    # Gera relatório
    test.generate_report()

if __name__ == "__main__":
    asyncio.run(main())

