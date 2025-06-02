"""
VIREON Task Mesh - Correção Temporária do Planner
------------------------------------------------

Este arquivo corrige a função plan_and_execute para aguardar corretamente
a chamada assíncrona para reduce_results.
"""

import asyncio
from typing import Dict, List, Any, Callable, Optional
from core.symbiotic_core.task_mesh.worker import execute_subtask
from core.symbiotic_core.task_mesh.reducer import reduce_results

async def plan_and_execute(
    task: Dict[str, Any],
    context: Dict[str, Any],
    max_workers: Optional[int] = None,
    task_division_strategy: Optional[Callable] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Planeja e executa uma tarefa complexa dividindo-a em sub-tarefas paralelas.
    
    Args:
        task: Descrição completa da tarefa a ser executada
        context: Contexto global da tarefa (super-escopo)
        max_workers: Número máximo de workers paralelos (None = auto)
        task_division_strategy: Função personalizada para dividir a tarefa
                               (None = usar estratégia padrão)
        **kwargs: Parâmetros adicionais para configuração do processo
        
    Returns:
        Resultado final após a redução dos resultados das sub-tarefas
    """
    # Divisão da tarefa em sub-tarefas
    subtasks = _divide_task(task, context, task_division_strategy)
    
    # Determinar número de workers
    if max_workers is None:
        # Implementação futura: integração com resource_sentinel para determinar
        # o número ideal de workers com base na disponibilidade de recursos
        max_workers = min(len(subtasks), 4)  # Valor padrão temporário
    
    # Execução paralela das sub-tarefas
    subtask_results = await _execute_subtasks_parallel(subtasks, context, max_workers)
    
    # Redução dos resultados - CORREÇÃO: adicionado await
    final_result = await reduce_results(subtask_results, task)
    
    return final_result


async def _execute_subtasks_parallel(
    subtasks: List[Dict[str, Any]],
    context: Dict[str, Any],
    max_workers: int
) -> List[Dict[str, Any]]:
    """
    Executa sub-tarefas em paralelo utilizando um pool de workers.
    
    Args:
        subtasks: Lista de sub-tarefas a serem executadas
        context: Contexto global compartilhado
        max_workers: Número máximo de workers
        
    Returns:
        Lista com os resultados de todas as sub-tarefas
    """
    # Criar um semáforo para limitar o número de tarefas concorrentes
    semaphore = asyncio.Semaphore(max_workers)
    
    async def _execute_with_semaphore(subtask):
        async with semaphore:
            return await execute_subtask(subtask, context)
    
    # Criar e executar tasks assíncronas para cada sub-tarefa
    tasks = [_execute_with_semaphore(subtask) for subtask in subtasks]
    results = await asyncio.gather(*tasks)
    
    return results


def _divide_task(
    task: Dict[str, Any],
    context: Dict[str, Any],
    division_strategy: Optional[Callable] = None
) -> List[Dict[str, Any]]:
    """
    Divide uma tarefa complexa em sub-tarefas menores.
    
    Args:
        task: Tarefa a ser dividida
        context: Contexto global
        division_strategy: Estratégia de divisão personalizada
        
    Returns:
        Lista de sub-tarefas
    """
    if division_strategy is not None:
        return division_strategy(task, context)
    
    # Implementação padrão de divisão (a ser expandida conforme necessidades)
    # Esta é uma versão simplificada para iniciar
    subtasks = []
    
    # Exemplo de lógica de divisão (será substituída por implementação real)
    if "components" in task:
        # Dividir por componentes explícitos
        for i, component in enumerate(task["components"]):
            subtasks.append({
                "id": f"subtask_{i}",
                "parent_task_id": task.get("id", "root"),
                "component": component,
                "type": "component_execution",
                "parameters": task.get("parameters", {})
            })
    else:
        # Se não há divisão explícita, retorna a tarefa como uma única sub-tarefa
        subtasks.append({
            "id": "subtask_single",
            "parent_task_id": task.get("id", "root"),
            "type": "full_execution",
            "parameters": task.get("parameters", {}),
            "content": task.get("content", {})
        })
    
    return subtasks

