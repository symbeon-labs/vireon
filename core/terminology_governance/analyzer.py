import re
from typing import Dict, List, Set, Tuple
from pathlib import Path

from . import TerminologyViolation, TerminologyViolationLevel

class TerminologyAnalyzer:
    def __init__(self, rules: Dict):
        self.rules = rules
        self.context_patterns = self._compile_context_patterns()

    def _compile_context_patterns(self) -> Dict[str, re.Pattern]:
        """Compila padrões de contexto para análise eficiente"""
        patterns = {}
        for context, terms in self.rules.get('contexts', {}).items():
            pattern = '|'.join(map(re.escape, terms))
            patterns[context] = re.compile(pattern)
        return patterns

    def analyze_file(self, file_path: Path) -> List[TerminologyViolation]:
        """Analisa um arquivo em busca de violações de terminologia"""
        violations = []
        content = file_path.read_text(encoding='utf-8')
        
        for line_num, line in enumerate(content.splitlines(), 1):
            context = self._determine_context(line)
            if context:
                violations.extend(self._check_line(line, line_num, file_path, context))
        
        return violations

    def _determine_context(self, line: str) -> str:
        """Determina o contexto da linha baseado nos padrões"""
        for context, pattern in self.context_patterns.items():
            if pattern.search(line):
                return context
        return 'default'

    def _check_line(self, line: str, line_num: int, file_path: Path, context: str) -> List[TerminologyViolation]:
        """Verifica uma linha em busca de violações"""
        violations = []
        
        # Verifica termos proibidos
        for term, replacement in self.rules.get('replacements', {}).items():
            if re.search(rf'\b{term}\b', line, re.IGNORECASE):
                violations.append(
                    TerminologyViolation(
                        term=term,
                        context=context,
                        suggestion=replacement,
                        level=TerminologyViolationLevel.ERROR,
                        file_path=file_path,
                        line_number=line_num
                    )
                )
        
        return violations

    def get_context_summary(self, violations: List[TerminologyViolation]) -> Dict:
        """Gera um sumário de violações por contexto"""
        summary = {}
        for violation in violations:
            if violation.context not in summary:
                summary[violation.context] = {
                    'total': 0,
                    'terms': set(),
                    'files': set()
                }
            
            ctx = summary[violation.context]
            ctx['total'] += 1
            ctx['terms'].add(violation.term)
            ctx['files'].add(str(violation.file_path))
        
        return summary

