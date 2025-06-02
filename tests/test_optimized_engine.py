import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List
import matplotlib.pyplot as plt
from pathlib import Path

from core.cognitive_engine import CognitiveEngine
from core.optimized_cache import OptimizedCache
from core.quantum_lite import QuantumLite

class PerformanceTest:
    """Classe para testes de performance do sistema otimizado"""

    def __init__(self, redis_url: str = "redis://localhost"):
        self.engine = CognitiveEngine(
            redis_url=redis_url,
            cache_size=1000,
            cache_ttl=3600
        )
        self.test_data: List[Dict[str, Any]] = []
        self.metrics: Dict[str, List[float]] = {
            "latency": [],
            "memory_usage": [],
            "cache_hits": [],
            "quantum_success": []
        }
        self.logger = logging.getLogger("PerformanceTest")
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

    async def run_cache_test(self):
        """Testa performance do cache multicamada"""
        self.logger.info("Iniciando teste de cache...")
        start_time = time.time()

        # Gera dados de teste
        test_data = self._generate_test_data(1000)
        
        # Teste de escrita
        for item in test_data[:500]:
            await self.engine.cache.set(
                f"key_{item['id']}", 
                item
            )

        # Teste de leitura (com mistura de hits e misses)
        for i in range(1000):
            key = f"key_test_{i % 750}"  # Força alguns misses
            await self.engine.cache.get(key)

        # Coleta métricas
        cache_stats = self.engine.cache.get_stats()
        self.metrics["cache_hits"].append(cache_stats["hit_ratio"])
        self.metrics["memory_usage"].append(cache_stats["memory_usage_mb"])
        self.metrics["latency"].append(time.time() - start_time)

        self.logger.info(f"Teste de cache concluído: {json.dumps(cache_stats, indent=2)}")

    async def run_quantum_test(self):
        """Testa performance das operações quânticas"""
        self.logger.info("Iniciando teste quântico...")
        start_time = time.time()

        # Teste de processamento quântico
        test_data = self._generate_test_data(100)
        success_count = 0

        for item in test_data:
            result = await self.engine.quantum.process_state(
                item,
                operation_type="test"
            )
            if result and await self.engine.quantum.validate_coherence(result):
                success_count += 1

        # Coleta métricas
        quantum_stats = self.engine.quantum.get_metrics()
        success_rate = success_count / len(test_data)
        self.metrics["quantum_success"].append(success_rate)
        self.metrics["latency"].append(time.time() - start_time)

        self.logger.info(f"Teste quântico concluído: {json.dumps(quantum_stats, indent=2)}")

    async def run_full_engine_test(self):
        """Testa o motor cognitivo completo"""
        self.logger.info("Iniciando teste completo do motor...")
        start_time = time.time()

        # Teste de processamento completo
        test_data = self._generate_test_data(200)
        for item in test_data:
            await self.engine.process(
                item,
                operation_type="full_test",
                use_cache=True
            )

        # Coleta métricas consolidadas
        engine_metrics = self.engine.get_metrics()
        self.logger.info(f"Teste completo concluído: {json.dumps(engine_metrics, indent=2)}")

    def generate_report(self, output_dir: str = "test_results"):
        """Gera relatório detalhado com gráficos"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Gera gráficos
        plt.figure(figsize=(15, 10))

        # Cache Hits
        plt.subplot(2, 2, 1)
        plt.plot(self.metrics["cache_hits"])
        plt.title("Taxa de Cache Hits")
        plt.xlabel("Operações")
        plt.ylabel("Hit Ratio")

        # Latência
        plt.subplot(2, 2, 2)
        plt.plot(self.metrics["latency"])
        plt.title("Latência de Operações")
        plt.xlabel("Operações")
        plt.ylabel("Segundos")

        # Uso de Memória
        plt.subplot(2, 2, 3)
        plt.plot(self.metrics["memory_usage"])
        plt.title("Uso de Memória")
        plt.xlabel("Operações")
        plt.ylabel("MB")

        # Sucesso Quântico
        plt.subplot(2, 2, 4)
        plt.plot(self.metrics["quantum_success"])
        plt.title("Taxa de Sucesso Quântico")
        plt.xlabel("Operações")
        plt.ylabel("Taxa de Sucesso")

        plt.tight_layout()
        plt.savefig(output_path / "performance_metrics.png")

        # Gera relatório textual
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "avg_cache_hit_rate": sum(self.metrics["cache_hits"]) / len(self.metrics["cache_hits"]),
                "avg_latency": sum(self.metrics["latency"]) / len(self.metrics["latency"]),
                "max_memory_usage": max(self.metrics["memory_usage"]),
                "avg_quantum_success": sum(self.metrics["quantum_success"]) / len(self.metrics["quantum_success"])
            },
            "detailed_metrics": self.metrics
        }

        with open(output_path / "performance_report.json", "w") as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Relatório gerado em {output_path}")

async def main():
    """Função principal para execução dos testes"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    test = PerformanceTest()
    
    # Executa testes
    await test.run_cache_test()
    await test.run_quantum_test()
    await test.run_full_engine_test()
    
    # Gera relatório
    test.generate_report()

if __name__ == "__main__":
    asyncio.run(main())

