import yaml
from pathlib import Path
from typing import Dict, List, Optional

BASE_RULES = {
    'terminology_rules': {
        'neural_symbiotic': {
            'allowed_terms': [
                'neural_network',
                'symbiotic_integration',
                'consciousness_layer',
                'metacognitive_process'
            ],
            'replacements': {
                'neural_process': 'neural_process',
                'symbiotic_enhancement': 'symbiotic_enhancement',
                'adaptive_learning': 'adaptive_learning',
                'system_state': 'system_state',
                'symbiotic_validation': 'symbiotic_validation'
            },
            'contexts': {
                'implementation': [
                    'class',
                    'def',
                    'function',
                    'module'
                ],
                'documentation': [
                    'doc',
                    'comment',
                    'readme',
                    'md'
                ],
                'api': [
                    'api',
                    'endpoint',
                    'interface',
                    'protocol'
                ]
            }
        },
        'consciousness': {
            'allowed_terms': [
                'metacognitive',
                'awareness',
                'self_reflection',
                'cognitive_state'
            ],
            'replacements': {
                'metacognitive_awareness': 'metacognitive_awareness',
                'quantum_mind': 'neural_mind',
                'quantum_thinking': 'symbiotic_processing'
            },
            'contexts': {
                'core': [
                    'consciousness',
                    'awareness',
                    'metacognition'
                ],
                'integration': [
                    'bridge',
                    'connection',
                    'interface'
                ]
            }
        }
    }
}

class RuleManager:
    def __init__(self, rules_path: Optional[Path] = None):
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict:
        """Carrega regras do arquivo ou usa as regras base"""
        if self.rules_path and self.rules_path.exists():
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                custom_rules = yaml.safe_load(f)
                return self._merge_rules(BASE_RULES, custom_rules)
        return BASE_RULES

    def _merge_rules(self, base: Dict, custom: Dict) -> Dict:
        """Mescla regras customizadas com as regras base"""
        merged = base.copy()
        for key, value in custom.items():
            if key in merged and isinstance(merged[key], dict):
                merged[key] = self._merge_rules(merged[key], value)
            else:
                merged[key] = value
        return merged

    def save_rules(self, rules: Dict) -> None:
        """Salva regras em arquivo"""
        if self.rules_path:
            with open(self.rules_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(rules, f, allow_unicode=True)

    def get_replacements(self) -> Dict[str, str]:
        """Retorna todos os termos e suas substituições"""
        replacements = {}
        for category in self.rules['terminology_rules'].values():
            replacements.update(category.get('replacements', {}))
        return replacements

    def get_allowed_terms(self) -> List[str]:
        """Retorna todos os termos permitidos"""
        allowed = []
        for category in self.rules['terminology_rules'].values():
            allowed.extend(category.get('allowed_terms', []))
        return allowed

    def get_contexts(self) -> Dict[str, List[str]]:
        """Retorna todos os contextos e seus padrões"""
        contexts = {}
        for category in self.rules['terminology_rules'].values():
            for context, patterns in category.get('contexts', {}).items():
                if context not in contexts:
                    contexts[context] = []
                contexts[context].extend(patterns)
        return contexts

