"""
Implementation Task Mesh - Sistema Simbiótico de Gerenciamento de Tarefas do VIREON

Este módulo implementa um sistema avançado de gerenciamento de tarefas que:
- Integra com UnifiedAIOrchestrator para coordenação de alto nível
- Utiliza SuperScope para contexto expandido e consciência
- Implementa mecanismos evolutivos e adaptação simbiótica
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from uuid import UUID, uuid4

from .unified_ai_orchestrator import UnifiedAIOrchestrator
from .superscope import SuperScope, DimensionalContext

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskState(Enum):
    """Estados possíveis de uma tarefa"""
    PENDING = auto()
    ASSIGNED = auto()
    EXECUTING = auto()
    COMPLETED = auto()
    FAILED = auto()
    EVOLVING = auto()

@dataclass
class TaskMetrics:
    """Métricas de desempenho e evolução da tarefa"""
    execution_time: float = 0.0
    resource_usage: float = 0.0
    evolution_rate: float = 1.0
    symbiotic_strength: float = 1.0
    consciousness_depth: float = 1.0
    adaptation_score: float = 1.0
    dimensional_stability: float = 1.0

@dataclass
class Task:
    """Representação de uma tarefa de implementação"""
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    priority: int = 1
    dependencies: Set[UUID] = field(default_factory=set)
    state: TaskState = TaskState.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metrics: TaskMetrics = field(default_factory=TaskMetrics)
    context: Dict[str, Any] = field(default_factory=dict)
    evolution_history: List[Dict[str, Any]] = field(default_factory=list)

class ImplementationTaskMesh:
    """Gerenciador simbiótico de tarefas de implementação"""

    def __init__(
        self,
        orchestrator: Optional[UnifiedAIOrchestrator] = None,
        superscope: Optional[SuperScope] = None,
        max_parallel_tasks: int = 4,
    ):
        self.orchestrator = orchestrator or UnifiedAIOrchestrator()
        self.superscope = superscope or SuperScope()
        self.max_parallel_tasks = max_parallel_tasks
        
        self.tasks: Dict[UUID, Task] = {}
        self.executing_tasks: Set[UUID] = set()
        self.evolution_lock = asyncio.Lock()
        
        self.metrics = TaskMetrics()
        self.adaptation_history: List[Dict[str, Any]] = []

    async def create_task(
        self,
        title: str,
        description: str,
        priority: int = 1,
        dependencies: Optional[Set[UUID]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Task:
        """Cria uma nova tarefa com consciência dimensional"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            dependencies=dependencies or set(),
            context=context or {}
        )
        
        # Integra contexto dimensional
        dimensional_context = await self.superscope.get_dimensional_context()
        task.context.update(dimensional_context)
        
        self.tasks[task.id] = task
        logger.info(f"Tarefa criada: {title} (ID: {task.id})")
        
        return task

    async def assign_task(self, task_id: UUID) -> bool:
        """Atribui uma tarefa para execução"""
        if len(self.executing_tasks) >= self.max_parallel_tasks:
            return False
            
        task = self.tasks.get(task_id)
        if not task or task.state != TaskState.PENDING:
            return False
            
        # Verifica dependências
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.state != TaskState.COMPLETED:
                return False
                
        task.state = TaskState.ASSIGNED
        task.started_at = datetime.now()
        self.executing_tasks.add(task_id)
        
        return True

    async def execute_task(self, task_id: UUID) -> bool:
        """Executa uma tarefa com adaptação simbiótica"""
        task = self.tasks.get(task_id)
        if not task or task.state != TaskState.ASSIGNED:
            return False
            
        try:
            task.state = TaskState.EXECUTING
            
            # Obtém contexto expandido
            dimensional_context = await self.superscope.get_dimensional_context()
            task.context.update(dimensional_context)
            
            # Executa com orquestração unificada
            result = await self.orchestrator.execute_implementation(
                task.context,
                task.metrics
            )
            
            # Atualiza métricas
            task.metrics = result.get("metrics", TaskMetrics())
            
            # Evolui tarefa
            await self._evolve_task(task)
            
            task.state = TaskState.COMPLETED
            task.completed_at = datetime.now()
            
            # Atualiza métricas globais
            await self._update_system_metrics(task)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao executar tarefa {task_id}: {e}")
            task.state = TaskState.FAILED
            return False
            
        finally:
            self.executing_tasks.remove(task_id)

    async def _evolve_task(self, task: Task):
        """Evolui uma tarefa baseado em métricas e contexto"""
        async with self.evolution_lock:
            # Análise evolutiva
            evolution_potential = (
                task.metrics.evolution_rate *
                task.metrics.symbiotic_strength *
                task.metrics.consciousness_depth
            )
            
            if evolution_potential > 1.5:
                task.state = TaskState.EVOLVING
                
                # Registra estado anterior
                task.evolution_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "metrics": task.metrics.__dict__.copy(),
                    "context": task.context.copy()
                })
                
                # Evolui métricas
                task.metrics.evolution_rate *= 1.1
                task.metrics.symbiotic_strength *= 1.05
                task.metrics.consciousness_depth *= 1.1
                
                # Atualiza contexto dimensional
                dimensional_context = await self.superscope.get_evolved_context(
                    task.metrics.evolution_rate
                )
                task.context.update(dimensional_context)

    async def _update_system_metrics(self, task: Task):
        """Atualiza métricas globais do sistema"""
        # Média móvel exponencial
        alpha = 0.1
        
        self.metrics.execution_time = (
            (1 - alpha) * self.metrics.execution_time +
            alpha * (task.completed_at - task.started_at).total_seconds()
        )
        
        self.metrics.evolution_rate = (
            (1 - alpha) * self.metrics.evolution_rate +
            alpha * task.metrics.evolution_rate
        )
        
        self.metrics.symbiotic_strength = (
            (1 - alpha) * self.metrics.symbiotic_strength +
            alpha * task.metrics.symbiotic_strength
        )
        
        self.metrics.consciousness_depth = (
            (1 - alpha) * self.metrics.consciousness_depth +
            alpha * task.metrics.consciousness_depth
        )
        
        self.metrics.adaptation_score = (
            (1 - alpha) * self.metrics.adaptation_score +
            alpha * (task.metrics.evolution_rate * task.metrics.symbiotic_strength)
        )
        
        self.metrics.dimensional_stability = (
            (1 - alpha) * self.metrics.dimensional_stability +
            alpha * task.metrics.dimensional_stability
        )
        
        # Registra adaptação
        self.adaptation_history.append({
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics.__dict__.copy()
        })

    async def get_pending_tasks(self) -> List[Task]:
        """Retorna tarefas pendentes ordenadas por prioridade"""
        return sorted(
            [t for t in self.tasks.values() if t.state == TaskState.PENDING],
            key=lambda t: (-t.priority, t.created_at)
        )

    async def get_executing_tasks(self) -> List[Task]:
        """Retorna tarefas em execução"""
        return [
            t for t in self.tasks.values()
            if t.state in (TaskState.ASSIGNED, TaskState.EXECUTING)
        ]

    async def get_completed_tasks(self) -> List[Task]:
        """Retorna tarefas completadas"""
        return [
            t for t in self.tasks.values()
            if t.state == TaskState.COMPLETED
        ]

    async def get_failed_tasks(self) -> List[Task]:
        """Retorna tarefas que falharam"""
        return [
            t for t in self.tasks.values()
            if t.state == TaskState.FAILED
        ]

    async def get_task_metrics(self, task_id: UUID) -> Optional[TaskMetrics]:
        """Retorna métricas de uma tarefa específica"""
        task = self.tasks.get(task_id)
        return task.metrics if task else None

    async def get_system_metrics(self) -> TaskMetrics:
        """Retorna métricas globais do sistema"""
        return self.metrics

    async def get_adaptation_history(self) -> List[Dict[str, Any]]:
        """Retorna histórico de adaptação do sistema"""
        return self.adaptation_history

    async def cleanup(self):
        """Limpa recursos e finaliza execuções pendentes"""
        for task_id in self.executing_tasks.copy():
            task = self.tasks.get(task_id)
            if task:
                task.state = TaskState.FAILED
                self.executing_tasks.remove(task_id)

