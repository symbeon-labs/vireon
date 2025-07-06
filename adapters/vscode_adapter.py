"""
VS Code Adapter for VIREON Universal Meta-Governance System

This adapter enables VIREON to integrate with Visual Studio Code,
translating VIREON rules to VS Code settings and extensions configuration.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from base_adapter import (
    UniversalAdapter, 
    AdapterMetadata, 
    AdapterCapability,
    TranslationContext,
    RuleTranslator,
    FeedbackCollector,
    EvolutionEngine
)

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Rule, ConsciousnessLevel, RuleType


class VSCodeAdapter(UniversalAdapter):
    """
    Adapter for Visual Studio Code integration.
    
    This adapter translates VIREON rules to VS Code settings.json format
    and manages workspace-specific configurations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("vscode", config)
        self.workspace_path = None
        self.settings_path = None
        self.extensions_path = None
        self.translator = VSCodeRuleTranslator()
        self.feedback_collector = VSCodeFeedbackCollector("vscode")
        self.evolution_engine = VSCodeEvolutionEngine("vscode")
        
    def _create_metadata(self) -> AdapterMetadata:
        """Create VS Code adapter metadata"""
        return AdapterMetadata(
            name="Visual Studio Code Adapter",
            version="1.0.0",
            supported_environments=["vscode", "code-server", "vscode-insiders"],
            capabilities=[
                AdapterCapability.REAL_TIME_SYNC,
                AdapterCapability.BIDIRECTIONAL_FEEDBACK,
                AdapterCapability.RULE_TRANSLATION,
                AdapterCapability.STATE_PERSISTENCE,
                AdapterCapability.PLUGIN_SYSTEM
            ],
            author="VIREON Team",
            description="Enables VIREON integration with VS Code environments",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    async def connect(self, environment_config: Dict[str, Any]) -> bool:
        """
        Connect to VS Code workspace.
        
        Args:
            environment_config: Must contain 'workspace_path'
        """
        try:
            self.workspace_path = Path(environment_config.get('workspace_path', '.'))
            
            # Setup VS Code paths
            vscode_dir = self.workspace_path / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            self.settings_path = vscode_dir / 'settings.json'
            self.extensions_path = vscode_dir / 'extensions.json'
            
            # Initialize settings file if it doesn't exist
            if not self.settings_path.exists():
                self.settings_path.write_text('{}')
                
            self.connected = True
            self.logger.info(f"Connected to VS Code workspace: {self.workspace_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to VS Code: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from VS Code workspace"""
        self.connected = False
        self.workspace_path = None
        self.settings_path = None
        self.extensions_path = None
        return True
    
    async def apply_rules(self, rules: List[Rule]) -> Dict[str, Any]:
        """
        Apply VIREON rules to VS Code settings.
        
        Translates rules to VS Code format and updates settings.json
        """
        if not self.connected:
            raise RuntimeError("Not connected to VS Code workspace")
            
        results = {
            'applied': [],
            'failed': [],
            'settings_updated': {}
        }
        
        # Load current settings
        current_settings = {}
        if self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                current_settings = json.load(f)
        
        # Apply each rule
        for rule in rules:
            try:
                # Translate rule to VS Code format
                context = TranslationContext(
                    source_format="vireon",
                    target_format="vscode_json",
                    environment_specifics={"workspace": str(self.workspace_path)}
                )
                
                vscode_settings = self.translate_rule(rule, context)
                
                # Merge with current settings
                for key, value in vscode_settings.items():
                    current_settings[key] = value
                    results['settings_updated'][key] = value
                
                results['applied'].append({
                    'rule_id': rule.id,
                    'rule_name': rule.content.get('name', 'Unknown'),
                    'settings_applied': list(vscode_settings.keys())
                })
                
            except Exception as e:
                results['failed'].append({
                    'rule_id': rule.id,
                    'error': str(e)
                })
        
        # Save updated settings
        with open(self.settings_path, 'w') as f:
            json.dump(current_settings, f, indent=2)
            
        self.logger.info(f"Applied {len(results['applied'])} rules to VS Code")
        return results
    
    async def collect_feedback(self) -> Dict[str, Any]:
        """
        Collect feedback from VS Code environment.
        
        This could include:
        - User acceptance of settings
        - Performance metrics
        - Error rates
        - Extension compatibility
        """
        feedback = await self.feedback_collector.collect(self.workspace_path)
        
        # Add VS Code specific feedback
        if self.settings_path and self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                current_settings = json.load(f)
                feedback['data']['current_settings_count'] = len(current_settings)
                
        # Check for problems/issues
        problems_file = self.workspace_path / '.vscode' / 'problems.json'
        if problems_file.exists():
            with open(problems_file, 'r') as f:
                problems = json.load(f)
                feedback['data']['problems'] = problems
                
        self.log_feedback(feedback)
        return feedback
    
    async def get_environment_state(self) -> Dict[str, Any]:
        """Get current VS Code workspace state"""
        if not self.connected:
            return {'connected': False}
            
        state = {
            'connected': True,
            'workspace': str(self.workspace_path),
            'settings': {},
            'extensions': [],
            'workspace_files': []
        }
        
        # Load current settings
        if self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                state['settings'] = json.load(f)
                
        # Load extensions
        if self.extensions_path and self.extensions_path.exists():
            with open(self.extensions_path, 'r') as f:
                extensions_data = json.load(f)
                state['extensions'] = extensions_data.get('recommendations', [])
                
        # Get workspace structure (limited to avoid large outputs)
        try:
            for item in self.workspace_path.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    state['workspace_files'].append(item.name)
                if len(state['workspace_files']) > 20:
                    state['workspace_files'].append('...')
                    break
        except Exception:
            pass
            
        return state
    
    def translate_rule(self, rule: Rule, context: TranslationContext) -> Dict[str, Any]:
        """Translate VIREON rule to VS Code settings format"""
        return self.translator.translate(rule, "vscode", "json")
    
    def validate_rule(self, rule: Rule) -> Tuple[bool, Optional[str]]:
        """Validate if rule can be applied to VS Code"""
        # Check if rule type is supported
        supported_types = [
            RuleType.LANGUAGE,
            RuleType.FRAMEWORK,
            RuleType.WORKFLOW,
            RuleType.TEXT_PATTERN
        ]
        
        if rule.rule_type not in supported_types:
            return False, f"Rule type {rule.rule_type} not supported by VS Code adapter"
            
        # Check if rule has required content
        if 'content' not in rule.content and 'settings' not in rule.content:
            return False, "Rule must contain 'content' or 'settings' field"
            
        return True, None


class VSCodeRuleTranslator(RuleTranslator):
    """Translates VIREON rules to VS Code settings format"""
    
    def __init__(self):
        super().__init__()
        self._setup_mappings()
        self._setup_handlers()
        
    def _setup_mappings(self):
        """Setup concept mappings from VIREON to VS Code"""
        # Language preferences
        self.register_concept_mapping("language", "vscode", "files.defaultLanguage")
        self.register_concept_mapping("file_associations", "vscode", "files.associations")
        
        # Editor preferences
        self.register_concept_mapping("indent_size", "vscode", "editor.tabSize")
        self.register_concept_mapping("line_length", "vscode", "editor.rulers")
        self.register_concept_mapping("format_on_save", "vscode", "editor.formatOnSave")
        
        # Python specific
        self.register_concept_mapping("python_formatter", "vscode", "python.formatting.provider")
        self.register_concept_mapping("python_linter", "vscode", "python.linting.enabled")
        
        # Git preferences
        self.register_concept_mapping("git_autofetch", "vscode", "git.autofetch")
        self.register_concept_mapping("git_confirmSync", "vscode", "git.confirmSync")
        
    def _setup_handlers(self):
        """Setup format handlers"""
        self.register_format_handler("json", self._json_handler)
        
    def _json_handler(self, rule: Rule, content: Dict[str, Any]) -> Dict[str, Any]:
        """Convert rule content to VS Code JSON settings"""
        vscode_settings = {}
        
        # Handle different rule types
        if rule.rule_type == RuleType.LANGUAGE:
            # Language-specific settings
            if 'language' in content:
                vscode_settings['files.defaultLanguage'] = content['language']
            if 'file_extensions' in content:
                vscode_settings['files.associations'] = content['file_extensions']
                
        elif rule.rule_type == RuleType.FRAMEWORK:
            # Framework-specific settings
            if 'framework' in content:
                framework = content['framework']
                if framework.lower() == 'fastapi':
                    vscode_settings.update({
                        'python.linting.enabled': True,
                        'python.linting.pylintEnabled': False,
                        'python.linting.flake8Enabled': True,
                        'python.formatting.provider': 'black'
                    })
                elif framework.lower() == 'django':
                    vscode_settings.update({
                        'python.linting.pylintArgs': ['--load-plugins', 'pylint_django'],
                        'files.associations': {'*.html': 'django-html'}
                    })
                    
        elif rule.rule_type == RuleType.WORKFLOW:
            # Workflow settings
            if 'editor_config' in content:
                editor_config = content['editor_config']
                if 'indent' in editor_config:
                    vscode_settings['editor.tabSize'] = editor_config['indent']
                if 'line_length' in editor_config:
                    vscode_settings['editor.rulers'] = [editor_config['line_length']]
                if 'format_on_save' in editor_config:
                    vscode_settings['editor.formatOnSave'] = editor_config['format_on_save']
                    
        # Handle direct settings if provided
        if 'vscode_settings' in content:
            vscode_settings.update(content['vscode_settings'])
            
        return vscode_settings


class VSCodeFeedbackCollector(FeedbackCollector):
    """Collects feedback specific to VS Code environment"""
    
    async def collect(self, source: Any) -> Dict[str, Any]:
        """Collect VS Code specific feedback"""
        feedback = await super().collect(source)
        
        # Add VS Code specific data
        feedback['data'] = {
            'timestamp': datetime.now().isoformat(),
            'workspace': str(source) if source else None,
            'editor_info': {
                'name': 'vscode',
                'platform': os.platform.system() if hasattr(os.platform, 'system') else 'unknown'
            }
        }
        
        return feedback


class VSCodeEvolutionEngine(EvolutionEngine):
    """Evolution engine specific to VS Code adapter"""
    
    def _calculate_evolution_metrics(self, feedback: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate VS Code specific evolution metrics"""
        metrics = super()._calculate_evolution_metrics(feedback)
        
        # Add VS Code specific metrics
        problem_count = sum(
            len(f.get('data', {}).get('problems', []))
            for f in feedback
        )
        
        # Adjust effectiveness based on problems
        if problem_count > 0:
            metrics['effectiveness'] *= 0.8
            
        return metrics
