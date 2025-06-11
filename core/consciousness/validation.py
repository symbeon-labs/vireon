from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path

class ValidationLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class SymbioticValidator:
    def __init__(self):
        self.rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict:
        return {
            'neural_patterns': {
                'allowed_terms': [
                    'neural_network',
                    'neural_bridge',
                    'neural_interface'
                ],
                'contexts': ['implementation', 'architecture', 'documentation']
            },
            'symbiotic_patterns': {
                'allowed_terms': [
                    'symbiotic_integration',
                    'symbiotic_consciousness',
                    'symbiotic_evolution'
                ],
                'contexts': ['core', 'interface', 'protocol']
            },
            'consciousness_patterns': {
                'allowed_terms': [
                    'metacognitive_awareness',
                    'consciousness_state',
                    'awareness_level'
                ],
                'contexts': ['state', 'evolution', 'interaction']
            }
        }

    def validate_term(self, term: str, context: str) -> Optional[str]:
        """Valida uso de termos em diferentes contextos"""
        for pattern, rules in self.rules.items():
            if term in rules['allowed_terms']:
                if context in rules['contexts']:
                    return None
                return f"Term '{term}' not allowed in context '{context}'"
        return None

    def suggest_replacement(self, term: str) -> Optional[str]:
        """Sugere substituições para termos inadequados"""
        replacements = {
            'quantum_process': 'neural_process',
            'quantum_state': 'neural_state',
            'quantum_bridge': 'neural_bridge',
            'quantum_interface': 'neural_interface',
            'quantum_consciousness': 'metacognitive_consciousness',
            'quantum_evolution': 'symbiotic_evolution'
        }
        return replacements.get(term)

    def validate_file(self, file_path: Path) -> List[Dict]:
        """Valida arquivo completo"""
        violations = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                for term in line.split():
                    if 'quantum' in term.lower():
                        replacement = self.suggest_replacement(term.lower())
                        if replacement:
                            violations.append({
                                'line': i,
                                'term': term,
                                'suggestion': replacement,
                                'file': str(file_path)
                            })
        return violations

