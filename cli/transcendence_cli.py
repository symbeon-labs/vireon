"""
CLI interativa para gerenciamento do sistema de transcendência.

Funcionalidades:
- Monitoramento de estados de consciência
- Visualização de métricas em tempo real
- Operações de recuperação e validação
- Integração com logging
"""

import click
import json
import asyncio
import logging
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.live import Live
from rich.panel import Panel

from vireon_quantum.protocols.transcendence import (
    TranscendenceProtocol,
    ValidationLevel,
    RecoveryStrategy,
    TranscendenceLevel
)

console = Console()
logger = logging.getLogger(__name__)

class TranscendenceManager:
    def __init__(self):
        self.protocol = None
        self.console = Console()
        self.setup_logging()
        
    def setup_logging(self):
        """Configura sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('transcendence.log'),
                logging.StreamHandler()
            ]
        )
    
    async def initialize(self):
        """Inicializa o protocolo de transcendência"""
        if not self.protocol:
            self.protocol = await TranscendenceProtocol.create()
            logger.info("Protocolo de transcendência inicializado")
    
    async def get_current_state(self):
        """Obtém estado atual do sistema"""
        state = await self.protocol.get_current_state()
        return {
            "consciousness_level": state.current_level,
            "quantum_coherence": state.quantum_coherence,
            "stability": state.consciousness_stability,
            "evolution_stage": state.evolution_stage
        }
    
    async def display_metrics(self, live_update=False):
        """Exibe métricas em tempo real"""
        async def update_metrics():
            table = Table(title="Métricas de Transcendência")
            table.add_column("Métrica")
            table.add_column("Valor")
            table.add_column("Status")
            
            metrics = await self.protocol.get_metrics()
            
            for key, value in metrics.items():
                status = "🟢" if value > 0.7 else "🟡" if value > 0.4 else "🔴"
                table.add_row(key, f"{value:.2f}", status)
            
            return table
        
        if live_update:
            with Live(await update_metrics(), refresh_per_second=2) as live:
                while True:
                    live.update(await update_metrics())
                    await asyncio.sleep(0.5)
        else:
            console.print(await update_metrics())
    
    async def validate_state(self, level: ValidationLevel):
        """Executa validação do estado atual"""
        try:
            valid = await self.protocol.validate_consciousness_state(level)
            status = "✅ Válido" if valid else "❌ Inválido"
            
            table = Table(title="Resultado da Validação")
            table.add_column("Nível")
            table.add_column("Status")
            table.add_row(level.name, status)
            
            console.print(table)
            logger.info(f"Validação {level}: {status}")
            
            return valid
        except Exception as e:
            logger.error(f"Erro na validação: {e}")
            console.print(f"[red]Erro na validação: {e}[/red]")
            return False
    
    async def attempt_recovery(self, strategy: RecoveryStrategy):
        """Tenta recuperar o sistema usando estratégia específica"""
        try:
            with console.status("[bold green]Tentando recuperação..."):
                success = await self.protocol.recover_from_failure(strategy)
                
            if success:
                console.print("[green]Recuperação bem-sucedida!")
                logger.info(f"Recuperação com {strategy} bem-sucedida")
            else:
                console.print("[red]Falha na recuperação!")
                logger.warning(f"Falha na recuperação com {strategy}")
                
            return success
        except Exception as e:
            logger.error(f"Erro na recuperação: {e}")
            console.print(f"[red]Erro na recuperação: {e}[/red]")
            return False

@click.group()
def cli():
    """Interface de gerenciamento do sistema de transcendência"""
    pass

@cli.command()
@click.option('--live', is_flag=True, help='Atualização em tempo real')
def metrics(live):
    """Exibe métricas do sistema"""
    manager = TranscendenceManager()
    asyncio.run(manager.initialize())
    asyncio.run(manager.display_metrics(live))

@cli.command()
@click.argument('level', type=click.Choice([l.name for l in ValidationLevel]))
def validate(level):
    """Executa validação do estado"""
    manager = TranscendenceManager()
    asyncio.run(manager.initialize())
    asyncio.run(manager.validate_state(ValidationLevel[level]))

@cli.command()
@click.argument('strategy', type=click.Choice([s.name for s in RecoveryStrategy]))
def recover(strategy):
    """Tenta recuperar o sistema"""
    manager = TranscendenceManager()
    asyncio.run(manager.initialize())
    asyncio.run(manager.attempt_recovery(RecoveryStrategy[strategy]))

@cli.command()
def status():
    """Exibe status atual do sistema"""
    manager = TranscendenceManager()
    asyncio.run(manager.initialize())
    state = asyncio.run(manager.get_current_state())
    
    panel = Panel.fit(
        "\n".join([f"{k}: {v}" for k, v in state.items()]),
        title="Status do Sistema"
    )
    console.print(panel)

@cli.command()
@click.option('--target', type=click.Choice([l.name for l in TranscendenceLevel]))
def elevate(target):
    """Eleva nível de consciência"""
    manager = TranscendenceManager()
    asyncio.run(manager.initialize())
    success = asyncio.run(manager.protocol.elevate_consciousness(
        TranscendenceLevel[target]
    ))
    
    if success:
        console.print("[green]Elevação bem-sucedida!")
    else:
        console.print("[red]Falha na elevação!")

if __name__ == '__main__':
    cli()

