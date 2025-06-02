"""
WarpTaskMeshAdapter - Adaptador Simbiótico entre o Warp e o Task Mesh do VIREON

Este módulo implementa uma camada de adaptação que permite ao Warp utilizar o Task Mesh
do VIREON de forma desacoplada, modular e simbiótica. O adaptador garante que todas as
operações de execução paralela, batch e feedback avancem o aprendizado do sistema,
sem criar dependência rígida com nenhum runtime específico.

Componente pronto para ser substituído por adaptadores de outros ecossistemas,
mantendo a lógica simbiótica e de aprendizado contínuo do VIREON.

Autor: Agente Simbiótico VIREON
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional, Callable


class WarpTaskMeshAdapter:
    """
    Adaptador simbiótico para integrar agentes (Warp) a um Task Mesh desacoplado.

    Permite o envio de tarefas em lote, execução supervisionada e recebimento de feedback
    em ciclos de aprendizado incremental, adaptando o mesh para diferentes parceiros.

    Design:
    - Não expõe detalhes internos do VIREON.
    - Oferece interface independente para tasks paralelas.
    - Logging e aprendizado simbiótico integrados.
    - Fácil extensão para outros ecossistemas.
    """

    def __init__(self, mesh_cls: Optional[type] = None, 
                 logger: Optional[logging.Logger] = None,
                 context: Optional[dict] = None, 
                 feedback_enabled: bool = True):
        """
        Inicializa o adaptador para integração simbiótica.
        
        Args:
            mesh_cls: Classe que implementa o mesh (default: SymbioticTaskMesh)
            logger: Logger customizado (default: logger do módulo)
            context: Contexto padrão compartilhado
            feedback_enabled: Se irá coletar feedback para aprendizado incremental
        """
        # Importação dinâmica para independência
        if mesh_cls is not None:
            self.mesh_cls = mesh_cls
        else:
            try:
                from symbiotic_task_mesh import SymbioticTaskMesh
                self.mesh_cls = SymbioticTaskMesh
            except ImportError:
                print("Faltando symbiotic_task_mesh.py no ambiente.")
                sys.exit(1)
        
        self.logger = logger or logging.getLogger("warp_task_mesh_adapter")
        self.context = context or {}
        self.feedback_enabled = feedback_enabled
        self.mesh = None
        self.active = False

    def init(self, context: Optional[dict] = None):
        """
        Ativa e inicializa o Task Mesh para o ambiente do agente.
        Carrega handlers padrão, contexto inicial e feedback.
        """
        merged_context = self.context.copy()
        if context:
            merged_context.update(context)
        self.mesh = self.mesh_cls(context=merged_context, feedback_enabled=self.feedback_enabled)
        self.active = True
        self.logger.info("Task Mesh simbiótico inicializado.")
        return self.mesh

    async def submit_task(self, task: Dict[str, Any], max_workers: int = 4,
                         collect_feedback: bool = True) -> Dict[str, Any]:
        """
        Envia uma tarefa (individual ou batch) para processamento simbiótico.

        Args:
            task: Dicionário com dados da tarefa (superescopo)
            max_workers: Máximo de workers paralelos para execução
            collect_feedback: Se irá coletar feedback deste ciclo

        Returns:
            Resultado consolidado do processamento
        """
        if not self.active or not self.mesh:
            self.init()
        self.logger.info(f"Enviando tarefa para execução simbiótica: {task.get('id', '<sem-id>')}")
        return await self.mesh.execute_task(task, max_workers=max_workers, collect_feedback=collect_feedback)

    async def submit_tasks_parallel(self, tasks: List[Dict[str, Any]], max_workers: int = 4,
                                   collect_feedback: bool = True) -> List[Dict[str, Any]]:
        """
        Envia múltiplas tarefas para execução simbiótica em paralelo.

        Args:
            tasks: Lista de tarefas/superescopos a serem processados
            max_workers: Máximo de workers paralelos entre todos os superescopos
            collect_feedback: Se irá coletar feedback deste ciclo

        Returns:
            Lista de resultados (um por tarefa)
        """
        if not self.active:
            self.init()
        self.logger.info(f"Enviando batch de {len(tasks)} tarefas para execução simbiótica.")
        coros = [self.mesh.execute_task(task, max_workers=max_workers, collect_feedback=collect_feedback) for task in tasks]
        return await asyncio.gather(*coros)

    def get_adaptation_history(self) -> List[Dict[str, Any]]:
        """
        Retorna o histórico de aprendizado adaptativo do mesh.
        """
        if self.mesh:
            return self.mesh.adaptation_history
        return []

    def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        Atualiza o contexto global do Task Mesh do agente.
        """
        if not self.mesh:
            self.init()
        self.mesh.context.update(new_context)
        self.logger.info(f"Contexto do Task Mesh atualizado com: {new_context}")

    def is_active(self) -> bool:
        """
        Verifica se o Task Mesh simbiótico está ativo.
        """
        return self.active

    def deactivate(self):
        """
        Desativa o mesh simbiótico no ambiente.
        """
        self.mesh = None
        self.active = False
        self.logger.info("Task Mesh simbiótico desativado.")

    async def feedback(self, task_id: str, success: bool, notes: Optional[str] = None):
        """
        Permite enviar feedback explícito sobre uma tarefa processada.
        
        Args:
            task_id: ID da tarefa processada
            success: Se a execução foi bem-sucedida
            notes: Observações ou ajustes para aprendizado
        """
        if not self.active or not self.mesh:
            self.logger.warning("Task Mesh inativo. Não é possível registrar feedback.")
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "success": success,
            "notes": notes or ""
        }
        self.mesh.adaptation_history.append(entry)
        # Poderia adicionar lógica de ajuste dinâmico
        self.logger.info(f"Feedback simbiótico registrado para tarefa {task_id}: {entry}")

# Uso básico (pode ser importado por qualquer agente):
# from warp_task_mesh_adapter import WarpTaskMeshAdapter
# warp_adapter = WarpTaskMeshAdapter()
# await warp_adapter.submit_task({...})

