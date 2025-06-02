"""
Testes de integração para o WarpBridge.
"""
import json
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock

from ..warp_bridge import WarpBridge
from ..models import ConsciousnessLevel, Rule, RuleType, WarpRule

@pytest.mark.asyncio
async def test_bridge_initialization(bridge):
    """Testa inicialização básica do bridge."""
    assert isinstance(bridge, WarpBridge)
    assert bridge.redis_client is not None
    assert not bridge.auto_sync

@pytest.mark.asyncio
async def test_rule_conversion(bridge):
    """Testa conversão bidirecional de regras."""
    # Cria regra de teste
    vireon_rule = Rule(
        rule_type=RuleType.SYMBIOTIC,
        content="Test rule",
        language="pt-BR",
        priority=1
    )
    
    # Converte para WarpRule
    warp_rule = bridge._convert_to_warp_rule(vireon_rule)
    assert isinstance(warp_rule, WarpRule)
    assert warp_rule.content["rule"] == vireon_rule.content
    
    # Converte de volta
    converted_rule = bridge._convert_from_warp_rule(warp_rule)
    assert isinstance(converted_rule, Rule)
    assert converted_rule.content == vireon_rule.content

@pytest.mark.asyncio
async def test_quantum_validation(bridge):
    """Testa validação quântica de regras."""
    test_rule = WarpRule(
        rule_id="test_quantum",
        content={"rule": "Quantum test"},
        consciousness_level=ConsciousnessLevel.QUANTUM
    )
    
    # Valida regra
    is_valid = await bridge.validate_rule(test_rule)
    assert is_valid is True
    
    # Verifica cache da validação
    validation_key = f"quantum_validation:{test_rule.rule_id}"
    validation = await bridge.redis_client.get(validation_key)
    assert validation is not None

@pytest.mark.asyncio
async def test_redis_caching(bridge):
    """Testa cache Redis."""
    # Prepara regra para teste
    test_rule = WarpRule(
        rule_id="test_cache",
        content={"rule": "Cache test"},
        consciousness_level=ConsciousnessLevel.BASE
    )
    
    # Configura mock do Redis
    cache_data = {
        "valid": True,
        "consciousness_level": ConsciousnessLevel.METACOGNITIVE.value
    }
    bridge.redis_client.get = AsyncMock(
        return_value=json.dumps(cache_data)
    )
    
    # Testa recuperação do cache
    is_valid = await bridge.validate_rule(test_rule)
    assert is_valid is True
    
    # Verifica uso do cache
    bridge.redis_client.get.assert_called_once()

@pytest.mark.asyncio
async def test_rule_sync(bridge):
    """Testa sincronização de regras."""
    # Prepara regras para teste
    rules = [
        Rule(
            rule_type=RuleType.SYMBIOTIC,
            content=f"Test {i}",
            language="pt-BR",
            priority=i
        ) for i in range(3)
    ]
    
    # Exporta regras
    await bridge.export_vireon_rules(rules)
    
    # Importa regras
    imported = await bridge.import_warp_rules()
    assert len(imported) == len(rules)
    
    # Verifica conteúdo
    for orig, imp in zip(rules, imported):
        assert imp.content == orig.content

@pytest.mark.asyncio
async def test_consciousness_evolution(bridge):
    """Testa evolução de consciência das regras."""
    # Cria regra inicial
    initial_rule = WarpRule(
        rule_id="test_evolution",
        content={"rule": "Evolution test"},
        consciousness_level=ConsciousnessLevel.BASE
    )
    
    # Primeira validação
    is_valid = await bridge.validate_rule(initial_rule)
    assert is_valid is True
    
    # Segunda validação - deve evoluir
    is_valid = await bridge.validate_rule(initial_rule)
    assert is_valid is True
    
    # Verifica evolução
    validation_key = f"quantum_validation:{initial_rule.rule_id}"
    validation = await bridge.redis_client.get(validation_key)
    validation_data = json.loads(validation)
    
    assert validation_data["consciousness_level"] > ConsciousnessLevel.BASE.value

@pytest.mark.asyncio
async def test_error_handling(bridge):
    """Testa tratamento de erros."""
    # Força erro no Redis
    bridge.redis_client.get = AsyncMock(
        side_effect=Exception("Test error")
    )
    
    # Tenta operação - não deve quebrar
    result = await bridge._load_warp_rules()
    assert isinstance(result, list)
    assert len(result) == 0
    
    # Verifica métricas de erro
    stats = bridge.stats
    assert stats.get("errors", 0) > 0

@pytest.mark.asyncio
async def test_performance_metrics(bridge):
    """Testa métricas de performance."""
    initial_stats = bridge.stats.copy()
    
    # Executa algumas operações
    rules = [
        Rule(
            rule_type=RuleType.SYMBIOTIC,
            content=f"Metric {i}",
            language="pt-BR",
            priority=i
        ) for i in range(5)
    ]
    
    await bridge.export_vireon_rules(rules)
    await bridge.import_warp_rules()
    
    # Verifica métricas
    final_stats = bridge.stats
    assert final_stats["operations"] > initial_stats.get("operations", 0)
    assert final_stats["syncs_performed"] > initial_stats.get("syncs_performed", 0)

