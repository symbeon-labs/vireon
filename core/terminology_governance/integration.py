from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

from . import TerminologyViolation
from .analyzer import TerminologyAnalyzer
from .corrector import TerminologyCorrector
from .rules import RuleManager

@dataclass
class IntegrationReport:
    violations: List[TerminologyViolation]
    corrections: Dict[str, List[str]]
    summary: Dict
    status: str

class IntegrationManager:
    def __init__(self, 
                 rule_manager: RuleManager,
                 analyzer: TerminologyAnalyzer,
                 corrector: TerminologyCorrector):
        self.rule_manager = rule_manager
        self.analyzer = analyzer
        self.corrector = corrector

    async def analyze_project(self, project_path: Path) -> List[TerminologyViolation]:
        """Analisa todo o projeto em busca de violações"""
        violations = []
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and self._should_analyze_file(file_path):
                violations.extend(self.analyzer.analyze_file(file_path))
        return violations

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determina se um arquivo deve ser analisado"""
        excluded = {'.git', '__pycache__', 'node_modules', 'target'}
        if any(part in excluded for part in file_path.parts):
            return False

        analyzable_extensions = {
            '.py', '.rs', '.ts', '.js', '.md', '.txt',
            '.yaml', '.yml', '.json', '.toml'
        }
        return file_path.suffix in analyzable_extensions

    async def integrate_project(self, project_path: Path, auto_correct: bool = False) -> IntegrationReport:
        """Integra um projeto, aplicando regras de terminologia"""
        # Analisa o projeto
        violations = await self.analyze_project(project_path)

        # Gera sugestões de correção
        corrections = {}
        if violations:
            if auto_correct:
                corrections = self.corrector.apply_corrections(project_path, violations)
            else:
                corrections = self.corrector.suggest_corrections(violations)

        # Gera sumário
        summary = self.analyzer.get_context_summary(violations)

        # Define status
        status = 'success' if not violations else 'needs_correction'

        return IntegrationReport(
            violations=violations,
            corrections=corrections,
            summary=summary,
            status=status
        )

    async def validate_pr(self, pr_files: List[Path]) -> IntegrationReport:
        """Valida arquivos de um PR"""
        violations = []
        for file_path in pr_files:
            if self._should_analyze_file(file_path):
                violations.extend(self.analyzer.analyze_file(file_path))

        corrections = self.corrector.suggest_corrections(violations)
        summary = self.analyzer.get_context_summary(violations)
        status = 'success' if not violations else 'needs_correction'

        return IntegrationReport(
            violations=violations,
            corrections=corrections,
            summary=summary,
            status=status
        )

    def generate_report(self, report: IntegrationReport) -> str:
        """Gera relatório formatado das violações e correções"""
        output = []
        
        # Cabeçalho
        output.append("=== Relatório de Conformidade Terminológica ===")
        output.append(f"Status: {report.status}\n")

        # Sumário
        output.append("Sumário por Contexto:")
        for context, data in report.summary.items():
            output.append(f"\nContexto: {context}")
            output.append(f"Total de violações: {data['total']}")
            output.append(f"Termos problemáticos: {', '.join(data['terms'])}")
            output.append(f"Arquivos afetados: {len(data['files'])}")

        # Violações e Correções
        if report.violations:
            output.append("\nDetalhes das Violações:")
            for violation in report.violations:
                output.append(
                    f"\n{violation.file_path}:{violation.line_number} - "
                    f"Termo: '{violation.term}' (Contexto: {violation.context})"
                )

        if report.corrections:
            output.append("\nCorreções Sugeridas:")
            for file, changes in report.corrections.items():
                output.append(f"\n{file}:")
                for change in changes:
                    output.append(f"  {change}")

        return '\n'.join(output)

