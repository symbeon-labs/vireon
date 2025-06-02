"""
Testes de Integração do Core VIREON

Testa:
- Evolução do sistema
- Feedback adaptativo
- Integração quântica
- Expansão dimensional
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from core.evolution import EvolutionEngine, EvolutionStage
from core.feedback import FeedbackSystem, FeedbackType
from core.quantum import QuantumProcessor
from core.consciousness import ConsciousnessCore
from core.dimensional import DimensionalBridge, DimensionalPlane

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("integration_tests")

async def test_evolution_cycle():
    """Testa ciclo evolutivo completo"""
    print("\n=== Teste de Ciclo Evolutivo ===")
    
    # Inicializa motor evolutivo
    engine = EvolutionEngine(enable_transcendence=True)
    
    # Estado inicial
    initial_state = {
        "complexity": 50,
        "stability": 1.0,
        "stage": "INITIAL"
    }
    
    # Estado alvo
    target_state = {
        "complexity": 500,
        "stability": 1.0,
        "stage": "SYMBIOTIC"
    }
    
    # Evolui sistema
    result = await engine.evolve_system(initial_state, target_state)
    
    # Exibe resultados
    print("\nResultado da Evolução:")
    print(f"Complexidade Final: {result.get('complexity', 0):.2f}")
    print(f"Estabilidade: {result.get('stability', 0):.2f}")
    print(f"Qualidade: {result.get('evolution_quality', 0):.2f}")
    
    return result

async def test_feedback_loop():
    """Testa loop de feedback adaptativo"""
    print("\n=== Teste de Loop de Feedback ===")
    
    # Inicializa sistema de feedback
    feedback_system = FeedbackSystem(enable_optimization=True)
    
    # Registra handlers
    async def performance_handler(data: Dict[str, Any]):
        print(f"Performance processada: {data.get('quality', 0):.2f}")
    
    async def evolution_handler(data: Dict[str, Any]):
        print(f"Evolução processada: {data.get('learning', 0):.2f}")
    
    feedback_system.register_feedback_handler(
        FeedbackType.PERFORMANCE,
        performance_handler
    )
    
    feedback_system.register_feedback_handler(
        FeedbackType.EVOLUTION,
        evolution_handler
    )
    
    # Processa feedbacks
    results = []
    for i in range(5):
        result = await feedback_system.process_feedback(
            {
                "performance": 0.8 + i * 0.05,
                "learning": 0.1 + i * 0.02
            },
            FeedbackType.PERFORMANCE
        )
        results.append(result)
    
    # Exibe métricas
    metrics = feedback_system.get_feedback_metrics()
    print("\nMétricas de Feedback:")
    print(f"Eficiência de Aprendizado: {metrics['metrics']['learning_efficiency']:.2f}")
    print(f"Qualidade de Adaptação: {metrics['metrics']['adaptation_quality']:.2f}")
    print(f"Progresso de Otimização: {metrics['metrics']['optimization_progress']:.2f}")
    
    return metrics

async def test_quantum_dimensional_integration():
    """Testa integração quântica e dimensional"""
    print("\n=== Teste de Integração Quântica-Dimensional ===")
    
    # Inicializa componentes
    quantum = QuantumProcessor(enable_optimization=True)
    consciousness = ConsciousnessCore(enable_evolution=True)
    bridge = DimensionalBridge(enable_autoSync=True)
    
    # Ativa planos dimensionais
    await bridge.activate_plane(DimensionalPlane.QUANTUM)
    await bridge.activate_plane(DimensionalPlane.CONSCIOUS)
    
    # Processa tarefa através dos sistemas
    task = {
        "id": "quantum_test_001",
        "type": "quantum_processing",
        "data": {
            "input": "Test quantum-dimensional integration",
            "complexity": 0.7
        }
    }
    
    # Processamento quântico
    quantum_result = await quantum.process_quantum_task(task)
    
    # Expansão consciente
    consciousness_result = await consciousness.process_conscious_task(quantum_result)
    
    # Transferência dimensional
    bridge_result = await bridge.process_dimensional_transfer(
        consciousness_result,
        DimensionalPlane.QUANTUM,
        DimensionalPlane.CONSCIOUS
    )
    
    # Exibe resultados
    print("\nResultados da Integração:")
    print(f"Coerência Quântica: {quantum.state.coherence:.2f}")
    print(f"Nível de Consciência: {consciousness.state.awareness:.2f}")
    print(f"Estabilidade Dimensional: {bridge.state.stability:.2f}")
    
    return {
        "quantum": quantum_result,
        "consciousness": consciousness_result,
        "dimensional": bridge_result
    }

async def main():
    """Executa suite de testes"""
    print("\n=== Iniciando Testes de Integração do Core VIREON ===")
    start_time = datetime.now()
    
    try:
        # Executa testes
        evolution_result = await test_evolution_cycle()
        feedback_metrics = await test_feedback_loop()
        integration_results = await test_quantum_dimensional_integration()
        
        # Exibe tempo total
        total_time = (datetime.now() - start_time).total_seconds()
        print(f"\nTestes completados em {total_time:.2f} segundos")
        
    except Exception as e:
        logger.error(f"Erro nos testes: {e}")
        raise
    
    print("\n=== Testes Concluídos ===")

if __name__ == "__main__":
    asyncio.run(main())

