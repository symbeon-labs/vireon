import re
from pathlib import Path
from typing import Dict, List, Tuple

from . import TerminologyViolation
from .rules import RuleManager

class TerminologyCorrector:
    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager
        self.replacements = rule_manager.get_replacements()

    def correct_file(self, file_path: Path, violations: List[TerminologyViolation]) -> Tuple[str, List[str]]:
        """Corrige violações em um arquivo"""
        if not violations:
            return "", []

        content = file_path.read_text(encoding='utf-8')
        changes = []
        new_content = content

        # Agrupa violações por linha
        violations_by_line = {}
        for v in violations:
            if v.line_number not in violations_by_line:
                violations_by_line[v.line_number] = []
            violations_by_line[v.line_number].append(v)

        # Aplica correções linha por linha
        lines = content.splitlines()
        for line_num in sorted(violations_by_line.keys()):
            line_violations = violations_by_line[line_num]
            original_line = lines[line_num - 1]
            new_line = original_line

            for violation in line_violations:
                if violation.term in self.replacements:
                    replacement = self.replacements[violation.term]
                    new_line = re.sub(
                        rf'\b{violation.term}\b',
                        replacement,
                        new_line,
                        flags=re.IGNORECASE
                    )
                    changes.append(
                        f"Line {line_num}: '{violation.term}' -> '{replacement}'"
                    )

            lines[line_num - 1] = new_line

        return '\n'.join(lines), changes

    def suggest_corrections(self, violations: List[TerminologyViolation]) -> Dict[str, List[str]]:
        """Sugere correções para violações encontradas"""
        suggestions = {}
        for violation in violations:
            if violation.term in self.replacements:
                file_key = str(violation.file_path)
                if file_key not in suggestions:
                    suggestions[file_key] = []
                
                suggestion = (
                    f"Line {violation.line_number}: Replace '{violation.term}' "
                    f"with '{self.replacements[violation.term]}' "
                    f"(context: {violation.context})"
                )
                suggestions[file_key].append(suggestion)
        
        return suggestions

    def apply_corrections(self, project_path: Path, violations: List[TerminologyViolation]) -> Dict[str, List[str]]:
        """Aplica correções em todo o projeto"""
        changes_by_file = {}
        
        # Agrupa violações por arquivo
        violations_by_file = {}
        for violation in violations:
            if violation.file_path not in violations_by_file:
                violations_by_file[violation.file_path] = []
            violations_by_file[violation.file_path].append(violation)
        
        # Aplica correções em cada arquivo
        for file_path, file_violations in violations_by_file.items():
            new_content, changes = self.correct_file(file_path, file_violations)
            if changes:
                file_path.write_text(new_content, encoding='utf-8')
                changes_by_file[str(file_path)] = changes
        
        return changes_by_file

