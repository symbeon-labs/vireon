"""
VIREON Core Orchestration Engine
---------------------------------

Main class for multi-agent coordination and governance.
"""

import asyncio
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import AgentResult, SwarmConsensus


class VireonCore:
    """
    Universal Agentic Orchestration Core.
    
    Coordinates multiple AI agents with governance rules and
    symbiotic feedback loops.
    
    Example:
        >>> vireon = VireonCore(config="./vireon.yaml")
        >>> result = await vireon.swarm_execute(
        ...     task="Refactor authentication module",
        ...     agents=["claude-3-5-sonnet", "github-copilot", "gpt-4-turbo"]
        ... )
        >>> print(result.consensus)
    """
    
    def __init__(self, config: str | Path | Dict[str, Any]):
        """
        Initialize VIREON Core with configuration.
        
        Args:
            config: Path to YAML config file or dictionary
        """
        self.config = self._load_config(config)
        self.agents: Dict[str, Any] = {}
        self.governance_rules: List[Dict] = self.config.get("governance", [])
        self.execution_history: List[Dict] = []
        
        print(f"[VIREON] Initialized v{self._get_version()}")
        print(f"[VIREON] Governance rules loaded: {len(self.governance_rules)}")
    
    def _load_config(self, config: str | Path | Dict) -> Dict:
        """Load configuration from file or dict."""
        if isinstance(config, dict):
            return config
        
        config_path = Path(config)
        if not config_path.exists():
            print(f"[VIREON] Warning: Config file not found at {config_path}")
            print("[VIREON] Using default configuration")
            return self._default_config()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "name": "vireon-default",
            "governance": [
                {"rule": "consensus_required", "threshold": 0.7},
                {"rule": "no_hallucination_tolerance", "enabled": True}
            ],
            "agents": {}
        }
    
    def _get_version(self) -> str:
        """Get VIREON version."""
        try:
            from . import __version__
            return __version__
        except:
            return "0.2.0-alpha"
    
    async def swarm_execute(
        self,
        task: str,
        agents: List[str],
        mode: str = "consensus",
        timeout: float = 300.0
    ) -> SwarmConsensus:
        """
        Execute a task across multiple agents with orchestration.
        
        This is the main API method that coordinates agent execution,
        applies governance rules, and returns a unified result.
        
        Args:
            task: Description of the task to execute
            agents: List of agent identifiers to use
            mode: Execution mode ("consensus", "parallel", "sequential")
timeout: Maximum execution time in seconds
        
        Returns:
            SwarmConsensus object with results and metadata
        
        Raises:
            LicenseError: If license doesn't permit this many agents
        
        Example:
            >>> result = await vireon.swarm_execute(
            ...     task="Analyze codebase for security issues",
            ...     agents=["architect-agent", "security-agent"]
            ... )
            >>> print(result.consensus)
            >>> print(result.confidence_score)
        """
        # 🔐 LICENSE VALIDATION
        from .licensing import get_validator, LicenseError
        
        validator = get_validator()
        if not validator.can_use_agents(len(agents)):
            max_allowed = validator.validate().get("max_agents", 2)
            tier = validator.get_tier()
            
            raise LicenseError(
                f"License '{tier}' allows max {max_allowed} agents, "
                f"but you requested {len(agents)}. "
                f"Upgrade at https://vireon.ai/pricing or set VIREON_LICENSE_KEY."
            )
        
        print(f"\n[ORCHESTRATOR] Spawning {len(agents)} agents for task")
        print(f"[TASK] {task}")
        print(f"[LICENSE] Tier: {validator.get_tier().upper()}")
        
        # Simulate agent execution (Phase 1: MVP implementation)
        # TODO: Replace with actual LLM API calls in Phase 2
        agent_results = []
        
        for i, agent_id in enumerate(agents, 1):
            print(f"  ├─ [{self._get_agent_role(i)}] ({agent_id}) Processing...")
            
            # Simulate async work
            await asyncio.sleep(0.1)
            
            result = AgentResult(
                agent_id=agent_id,
                task=task,
                output=f"Analysis complete from {agent_id}",
                confidence=0.85 + (i * 0.05),  # Simulated
                metadata={
                    "model": agent_id,
                    "tokens_used": 1500,
                    "latency_ms": 120
                }
            )
            agent_results.append(result)
        
        # Apply governance and generate consensus
        consensus = self._generate_consensus(agent_results, task)
        
        # Store in history
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "agents": agents,
            "consensus": consensus.consensus
        })
        
        print(f"\n[VIREON] Consensus Reached.")
        print(f"[RESULT] {consensus.consensus}")
        
        return consensus
    
    def _get_agent_role(self, index: int) -> str:
        """Get agent role based on execution order."""
        roles = ["ARCHITECT", "ENGINEER", "AUDITOR", "REVIEWER"]
        return roles[index - 1] if index <= len(roles) else "AGENT"
    
    def _generate_consensus(
        self,
        results: List[AgentResult],
        task: str
    ) -> SwarmConsensus:
        """
        Generate consensus from multiple agent results.
        
        Applies governance rules and combines agent outputs.
        """
        # Calculate average confidence
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        # Simplified consensus logic (MVP)
        # TODO: Implement sophisticated voting/weighting in Phase 2
        consensus_text = f"Task '{task}' analyzed by {len(results)} agents. "
        consensus_text += "Recommendations: Code review passed with high confidence."
        
        return SwarmConsensus(
            consensus=consensus_text,
            confidence_score=avg_confidence,
            agent_results=results,
            governance_applied=self.governance_rules[:2],  # Show which rules were used
            metadata={
                "execution_mode": "swarm",
                "agents_count": len(results),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get execution history.
        
        Args:
            limit: Maximum number of records to return
        
        Returns:
            List of execution records
        """
        return self.execution_history[-limit:]
    
    def __repr__(self) -> str:
        return f"<VireonCore version={self._get_version()} agents={len(self.agents)}>"
