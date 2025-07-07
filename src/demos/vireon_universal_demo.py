"""
VIREON Universal Demo

Demonstrates how VIREON can manage rules across multiple environments
using its universal adapter system.
"""

import asyncio
import json
from typing import List, Dict, Any
from datetime import datetime

# Import VIREON core
from models import Rule, ConsciousnessLevel, RuleType, WarpRule

# Import adapters
from adapters.vscode_adapter import VSCodeAdapter
# from adapters.warp_adapter import WarpAdapter  # Would be implemented
# from adapters.vim_adapter import VimAdapter    # Would be implemented


class VIREONUniversal:
    """
    Universal VIREON system that manages multiple adapters
    """
    
    def __init__(self):
        self.adapters = {}
        self.universal_rules = []
        self.feedback_history = []
        
    def register_adapter(self, name: str, adapter):
        """Register an adapter for a specific environment"""
        self.adapters[name] = adapter
        print(f"✅ Registered adapter: {name}")
        
    async def connect_all(self, configs: Dict[str, Dict[str, Any]]):
        """Connect all registered adapters to their environments"""
        for name, adapter in self.adapters.items():
            config = configs.get(name, {})
            success = await adapter.connect(config)
            if success:
                print(f"✅ Connected to {name}")
            else:
                print(f"❌ Failed to connect to {name}")
                
    async def apply_rules_globally(self, rules: List[Rule]):
        """Apply rules to all connected environments"""
        results = {}
        
        for name, adapter in self.adapters.items():
            if adapter.connected:
                print(f"\n📝 Applying rules to {name}...")
                result = await adapter.apply_rules(rules)
                results[name] = result
                
                # Print summary
                applied = len(result.get('applied', []))
                failed = len(result.get('failed', []))
                print(f"  ✅ Applied: {applied} rules")
                if failed > 0:
                    print(f"  ❌ Failed: {failed} rules")
                    
        return results
    
    async def apply_rules_to_targets(self, rules: List[Rule], targets: List[str]):
        """Apply rules only to specific target environments"""
        results = {}
        
        for target in targets:
            if target in self.adapters and self.adapters[target].connected:
                print(f"\n📝 Applying rules to {target}...")
                result = await self.adapters[target].apply_rules(rules)
                results[target] = result
            else:
                print(f"⚠️ Target {target} not found or not connected")
                
        return results
    
    async def collect_global_feedback(self):
        """Collect feedback from all environments"""
        feedback = {}
        
        for name, adapter in self.adapters.items():
            if adapter.connected:
                print(f"📊 Collecting feedback from {name}...")
                env_feedback = await adapter.collect_feedback()
                feedback[name] = env_feedback
                
        self.feedback_history.append({
            'timestamp': datetime.now(),
            'feedback': feedback
        })
        
        return feedback
    
    async def get_all_environments_status(self):
        """Get status of all registered environments"""
        status = {}
        
        for name, adapter in self.adapters.items():
            if adapter.connected:
                env_state = await adapter.get_environment_state()
                status[name] = {
                    'connected': True,
                    'metadata': adapter.to_dict(),
                    'state': env_state
                }
            else:
                status[name] = {
                    'connected': False,
                    'metadata': adapter.to_dict()
                }
                
        return status
    
    def create_universal_rule(self, name: str, content: Dict[str, Any], 
                            rule_type: RuleType = RuleType.WORKFLOW,
                            targets: List[str] = None) -> Rule:
        """Create a universal rule that can be applied to multiple environments"""
        rule = Rule(
            rule_type=rule_type,
            consciousness_level=ConsciousnessLevel.METACOGNITIVE,
            content={
                'name': name,
                'universal': True,
                'targets': targets or list(self.adapters.keys()),
                **content
            }
        )
        
        self.universal_rules.append(rule)
        return rule


async def demo_universal_vireon():
    """
    Demonstrate VIREON universal capabilities
    """
    print("🚀 VIREON Universal Meta-Governance Demo\n")
    
    # Initialize VIREON Universal
    vireon = VIREONUniversal()
    
    # Register adapters
    vireon.register_adapter('vscode', VSCodeAdapter())
    # vireon.register_adapter('warp', WarpAdapter())  # When implemented
    # vireon.register_adapter('vim', VimAdapter())    # When implemented
    
    # Connect to environments
    configs = {
        'vscode': {
            'workspace_path': '.'  # Current directory
        },
        # 'warp': {
        #     'terminal_config': '/path/to/warp/config'
        # },
        # 'vim': {
        #     'vimrc_path': '~/.vimrc'
        # }
    }
    
    await vireon.connect_all(configs)
    
    # Create universal rules
    print("\n📋 Creating universal rules...\n")
    
    # Python development rule
    python_rule = vireon.create_universal_rule(
        name="Python Development Standards",
        content={
            'language': 'python',
            'framework': 'fastapi',
            'editor_config': {
                'indent': 4,
                'line_length': 88,
                'format_on_save': True
            },
            'vscode_settings': {
                'python.formatting.provider': 'black',
                'python.linting.enabled': True,
                'python.linting.flake8Enabled': True
            }
        },
        rule_type=RuleType.LANGUAGE
    )
    
    # Git workflow rule
    git_rule = vireon.create_universal_rule(
        name="Git Workflow",
        content={
            'workflow': 'git',
            'vscode_settings': {
                'git.autofetch': True,
                'git.confirmSync': False,
                'git.enableSmartCommit': True
            }
        },
        rule_type=RuleType.WORKFLOW
    )
    
    # File associations rule
    file_rule = vireon.create_universal_rule(
        name="File Associations",
        content={
            'file_extensions': {
                '*.py': 'python',
                '*.md': 'markdown',
                '*.yaml': 'yaml',
                '*.yml': 'yaml'
            },
            'vscode_settings': {
                'files.associations': {
                    '*.py': 'python',
                    'Dockerfile*': 'dockerfile',
                    '*.env*': 'dotenv'
                }
            }
        },
        rule_type=RuleType.LANGUAGE
    )
    
    # Apply rules globally
    print("\n🌍 Applying rules globally...")
    results = await vireon.apply_rules_globally([python_rule, git_rule, file_rule])
    
    # Collect feedback
    print("\n📊 Collecting feedback from all environments...")
    feedback = await vireon.collect_global_feedback()
    
    # Get status
    print("\n📈 Getting status of all environments...")
    status = await vireon.get_all_environments_status()
    
    # Print summary
    print("\n📋 Summary:")
    print(f"  - Adapters registered: {len(vireon.adapters)}")
    print(f"  - Universal rules created: {len(vireon.universal_rules)}")
    print(f"  - Environments connected: {sum(1 for a in vireon.adapters.values() if a.connected)}")
    
    # Save results
    summary = {
        'timestamp': datetime.now().isoformat(),
        'adapters': list(vireon.adapters.keys()),
        'rules_applied': [r.content.get('name') for r in vireon.universal_rules],
        'results': results,
        'status': status
    }
    
    with open('vireon_universal_demo_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Demo completed! Results saved to vireon_universal_demo_results.json")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_universal_vireon())
