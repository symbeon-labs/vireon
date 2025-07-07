import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from warp_task_mesh_adapter import WarpTaskMeshAdapter
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExampleAgent:
    """
    Um agente de exemplo que usa o Task Mesh para processar tarefas complexas.
    """

    def __init__(self, name: str = "ExampleAgent", context: Optional[Dict[str, Any]] = None):
        """Inicializa o agente com nome e contexto."""
        self.name = name
        self.context = context or {}
        self.task_mesh_adapter = WarpTaskMeshAdapter()
        self.task_mesh_adapter.init(context=self.context)
        self.running = False
        logger.info(f"Agente '{self.name}' inicializado.")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma tarefa utilizando o Task Mesh.

        Args:
            task_data: Dicionário com os dados da tarefa a ser executada.

        Returns:
            Um dicionário com os resultados do processamento.
        """
        if not self.task_mesh_adapter.is_active():
            logger.warning("Task Mesh não está ativo. Ativando com configurações padrão.")
            self.task_mesh_adapter.init()

        # Define a tarefa com um super-escopo
        super_task = {
            "id": f"task-{hash(task_data)}",
            "type": "complex_processing",
            "description": "Super tarefa para processamento completo",
            "data": task_data,
            "planning_strategy": "adaptive"  # Utilizar estratégia adaptativa
        }
        
        logger.info(f"Submetendo tarefa '{super_task['id']}' para Task Mesh...")
        try:
            # Executar a tarefa através do adaptador
            result = await self.task_mesh_adapter.submit_task(super_task)
            logger.info(f"Tarefa '{super_task['id']}' executada com sucesso.")
            return result
        except Exception as e:
            logger.error(f"Erro ao executar tarefa '{super_task['id']}': {e}")
            return {"status": "error", "message": str(e)}

async def main():
    """Demonstração do uso do Task Mesh por um agente."""
    agent = ExampleAgent(name="Warp Simbiótico", context={"agent_type": "warp_agent"})
    
    # Simular dados da tarefa do Agente
    task_data = {
        "description": "Analisar o sentimento em um conjunto de reviews de clientes",
        "reviews": [
            "Este produto é incrível! Superou minhas expectativas.",
            "O produto é bom, mas o atendimento ao cliente é péssimo.",
            "Não recomendo este produto. Decepcionante.",
            "Amei este produto! Compraria novamente."
        ]
    }
    
    print("\n=== VIREON - Simulação de Agente ===\n")
    print(f"Agente: {agent.name}")
    
    print("\nSubmetendo tarefa para análise de sentimento...")
    result = await agent.process_task(task_data)
    
    if result.get("status") == "completed":
        print(f"\nTarefa concluída com sucesso! Detalhes:")
        print(json.dumps(result, indent=2))
        
        # Processa o resultado em cada subtask
        logger.info(f"As subtarefas obtiveram status 'completed'")
    
    else:
        print(f"Ocorreu um erro ao processar a tarefa: {result.get('error_message', 'Desconhecido')}")
        logger.error(f"Erro ao processar tarefa: {result}")
    
    # Ver histórico do Task Mesh
    print("\n=== Histórico do Task Mesh ===\n")
    history = agent.task_mesh_adapter.get_adaptation_history()
    print(json.dumps(history, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

