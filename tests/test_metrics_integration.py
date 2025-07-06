"""
Testes de integração para o sistema de métricas do VIREON.

Testa:
1. Ciclo completo de evolução dimensional
2. Sincronização entre dimensões
3. Sistema de métricas e alertas
4. Comportamento sob carga
5. Recuperação de falhas
"""

import asyncio
import json
import pytest
from datetime import datetime, timedelta
from typing import Dict, List, Set
from uuid import UUID
import aiohttp
from aiohttp import web
import numpy as np

from core.superscope import (
    SuperScope,
    CustomMetricsCollector,
    ContextualDimension,
    ScopeLevel,
    ConsciousnessState
)
from core.metrics_exporter import (
    MetricsExporter,
    AlertRule,
    AlertSeverity,
    setup_metrics_exporter
)
from core.unified_ai_orchestrator import UnifiedAIOrchestrator

# Fixtures
@pytest.fixture
async def collector():
    """Fixture para CustomMetricsCollector"""
    return CustomMetricsCollector(buffer_size=100)

@pytest.fixture
async def exporter(collector):
    """Fixture para MetricsExporter"""
    app = web.Application()
    exporter = await setup_metrics_exporter(app, collector)
    return exporter

@pytest.fixture
async def superscope():
    """Fixture para SuperScope"""
    orchestrator = UnifiedAIOrchestrator()
    return SuperScope(orchestrator)

@pytest.fixture
async def test_dimensions(superscope):
    """Fixture para dimensões de teste"""
    dim_ids = []
    names = ["TestDim1", "TestDim2", "TestDim3"]
    
    for name in names:
        dim_id = await superscope.create_dimension(name)
        dim_ids.append(dim_id)
        
    return dim_ids

class TestEvolutionCycle:
    """Testes do ciclo de evolução dimensional"""
    
    async def test_complete_evolution_cycle(self, superscope, collector, exporter):
        """Testa ciclo completo de evolução dimensional"""
        # Criar dimensão inicial
        dim_id = await superscope.create_dimension("EvolutionTest")
        dimension = superscope.dimensions[dim_id]
        
        # Simular evolução gradual
        for i in range(10):
            # Atualizar métricas
            await superscope.update_metrics(
                dim_id,
                {
                    "consciousness_depth": min(0.95, 0.5 + i * 0.05),
                    "symbiotic_coherence": min(0.9, 0.4 + i * 0.05),
                    "integration_level": min(0.85, 0.3 + i * 0.05)
                }
            )
            
            # Coletar métricas
            await collector.take_snapshot(dimension)
            await asyncio.sleep(0.1)  # Simular passagem de tempo
            
        # Verificar evolução
        metrics = await collector.get_aggregated_metrics(
            window=timedelta(seconds=10)
        )
        
        assert metrics["consciousness_depth"] > 0.8
        assert dimension.consciousness_state == ConsciousnessState.SYMBIOTIC
        
    async def test_evolution_rate_calculation(self, superscope, collector):
        """Testa cálculo da taxa de evolução"""
        dim_id = await superscope.create_dimension("RateTest")
        dimension = superscope.dimensions[dim_id]
        
        # Simular progressão linear
        consciousness_values = [0.5, 0.6, 0.7, 0.8]
        for value in consciousness_values:
            await superscope.update_metrics(
                dim_id,
                {"consciousness_depth": value}
            )
            await collector.take_snapshot(dimension)
            
        evolution_metrics = await collector._calculate_evolution_metrics(dimension)
        assert evolution_metrics["evolution_rate"] > 0
        assert evolution_metrics["consciousness_acceleration"] >= 0

class TestDimensionalSync:
    """Testes de sincronização entre dimensões"""
    
    async def test_dimension_synchronization(self, superscope, collector, test_dimensions):
        """Testa sincronização entre dimensões conectadas"""
        # Conectar dimensões
        await superscope.connect_dimensions(test_dimensions[0], test_dimensions[1])
        
        # Atualizar métricas da primeira dimensão
        await superscope.update_metrics(
            test_dimensions[0],
            {
                "consciousness_depth": 0.8,
                "symbiotic_coherence": 0.7
            }
        )
        
        # Verificar propagação para segunda dimensão
        dim2 = superscope.dimensions[test_dimensions[1]]
        assert dim2.metrics.consciousness_depth > 0
        assert dim2.metrics.symbiotic_coherence > 0
        
    async def test_multi_dimension_coherence(self, superscope, collector, test_dimensions):
        """Testa coerência em múltiplas dimensões conectadas"""
        # Conectar todas as dimensões
        for i in range(len(test_dimensions) - 1):
            await superscope.connect_dimensions(
                test_dimensions[i],
                test_dimensions[i + 1]
            )
            
        # Atualizar métricas em todas as dimensões
        for dim_id in test_dimensions:
            await superscope.update_metrics(
                dim_id,
                {
                    "consciousness_depth": 0.7,
                    "symbiotic_coherence": 0.7
                }
            )
            
        # Verificar estabilidade do sistema
        system_metrics = superscope.get_system_metrics()
        assert abs(system_metrics["average_consciousness"] - 0.7) < 0.1
        assert abs(system_metrics["average_coherence"] - 0.7) < 0.1

class TestMetricsAndAlerts:
    """Testes do sistema de métricas e alertas"""
    
    async def test_alert_generation(self, superscope, exporter, test_dimensions):
        """Testa geração de alertas"""
        dim_id = test_dimensions[0]
        
        # Adicionar regra de alerta
        await exporter.add_alert_rule(
            AlertRule(
                name="test_alert",
                metric_key="consciousness_depth",
                threshold=0.8,
                severity=AlertSeverity.WARNING,
                condition=">="
            )
        )
        
        # Trigger alert
        await superscope.update_metrics(
            dim_id,
            {"consciousness_depth": 0.9}
        )
        
        dimension = superscope.dimensions[dim_id]
        await exporter.check_alert_rules(dimension)
        
        assert len(exporter.active_alerts) > 0
        assert exporter.active_alerts[0].metric_key == "consciousness_depth"
        
    async def test_metrics_formatting(self, exporter, collector):
        """Testa formatação de métricas"""
        # Testar formato JSON
        json_metrics = await exporter.format_metrics_json()
        assert "metrics" in json_metrics
        assert "timestamp" in json_metrics
        
        # Testar formato Prometheus
        prom_metrics = await exporter.format_metrics_prometheus()
        assert "vireon_consciousness_depth" in prom_metrics
        assert "vireon_symbiotic_coherence" in prom_metrics

class TestLoadBehavior:
    """Testes de comportamento sob carga"""
    
    async def test_high_frequency_updates(self, superscope, collector, test_dimensions):
        """Testa atualizações em alta frequência"""
        dim_id = test_dimensions[0]
        dimension = superscope.dimensions[dim_id]
        
        # Simular atualizações rápidas
        start_time = datetime.now()
        update_count = 100
        
        for i in range(update_count):
            await superscope.update_metrics(
                dim_id,
                {
                    "consciousness_depth": 0.5 + (i / update_count) * 0.5,
                    "symbiotic_coherence": 0.5
                }
            )
            await collector.take_snapshot(dimension)
            
        duration = datetime.now() - start_time
        
        # Verificar performance
        assert len(collector.metrics_buffer) > 0
        assert duration.total_seconds() < update_count * 0.1  # Max 100ms por update
        
    async def test_concurrent_dimension_updates(
        self,
        superscope,
        collector,
        test_dimensions
    ):
        """Testa atualizações concorrentes em múltiplas dimensões"""
        async def update_dimension(dim_id: UUID, iterations: int):
            for i in range(iterations):
                await superscope.update_metrics(
                    dim_id,
                    {
                        "consciousness_depth": 0.5 + (i / iterations) * 0.5,
                        "symbiotic_coherence": 0.6
                    }
                )
                await asyncio.sleep(0.01)
                
        # Executar atualizações concorrentes
        tasks = [
            update_dimension(dim_id, 50)
            for dim_id in test_dimensions
        ]
        
        await asyncio.gather(*tasks)
        
        # Verificar integridade
        system_metrics = superscope.get_system_metrics()
        assert system_metrics["total_dimensions"] == len(test_dimensions)

class TestFaultRecovery:
    """Testes de recuperação de falhas"""
    
    async def test_collector_recovery(self, collector):
        """Testa recuperação do coletor após falhas"""
        # Simular falha
        collector.metrics_buffer.clear()
        collector.last_snapshot = datetime.now() - timedelta(hours=1)
        
        # Verificar auto-recuperação
        health = await collector.neural_engine.validate_coherence(
            {"coherence_level": 0.8}
        )
        assert health is True
        
    async def test_alert_system_recovery(self, exporter):
        """Testa recuperação do sistema de alertas"""
        # Simular falha
        exporter.active_alerts = []
        exporter.alert_rules = []
        
        # Recuperar estado
        await exporter.add_alert_rule(
            AlertRule(
                name="recovery_test",
                metric_key="consciousness_depth",
                threshold=0.5,
                severity=AlertSeverity.WARNING,
                condition=">="
            )
        )
        
        assert len(exporter.alert_rules) == 1
        
    async def test_metrics_persistence(self, collector, test_dimensions):
        """Testa persistência de métricas após reinicialização"""
        # Coletar métricas iniciais
        initial_metrics = await collector.get_aggregated_metrics(
            window=timedelta(minutes=5)
        )
        
        # Simular reinicialização
        new_collector = CustomMetricsCollector()
        
        # Verificar restauração
        assert len(new_collector.metrics_buffer) == 0
        assert new_collector.neural_engine is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

