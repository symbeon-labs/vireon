from pathlib import Path
from core.terminology_governance import (
    TerminologyViolation,
    TerminologyViolationLevel,
)
from core.terminology_governance.rules import RuleManager
from core.terminology_governance.analyzer import TerminologyAnalyzer
from core.terminology_governance.integration import IntegrationManager
from core.terminology_governance.corrector import TerminologyCorrector

async def main():
    # Inicializa os componentes
    from core.cognitive_engine import CognitiveEngine
    from core.evolution import EvolutionarySystem
    
    cognitive_engine = CognitiveEngine()
    evolution_system = EvolutionarySystem()
    
    rule_manager = RuleManager()
    analyzer = TerminologyAnalyzer(rule_manager.rules)
    corrector = TerminologyCorrector(rule_manager)
    integration_manager = IntegrationManager(
        rule_manager,
        analyzer,
        corrector,
        cognitive_state=cognitive_engine.state,
        evolution_pattern=evolution_system.pattern
    )

    # Define o caminho do projeto
    project_path = Path(__file__).parent.parent

    # Executa análise
    report = await integration_manager.integrate_project(project_path, auto_correct=False)
    
    # Gera relatório
    print(integration_manager.generate_report(report))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

