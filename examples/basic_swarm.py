"""
VIREON Basic Swarm Example
===========================

Demonstrates multi-agent coordination using VIREON Core.

This example matches EXACTLY the code shown in README.md to prove
that the API works as documented.

Usage:
    python examples/basic_swarm.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from vireon import VireonCore


async def main():
    """Main execution function."""
    
    print("=" * 60)
    print("VIREON: Basic Swarm Coordination Example")
    print("=" * 60)
    
    # Initialize the Orchestrator
    vireon = VireonCore(config="./vireon.yaml")
    
    print("\n" + "-" * 60)
    print("SCENARIO: Multi-Agent Code Refactoring")
    print("-" * 60)
    
    # Coordinate a complex task across models
    result = await vireon.swarm_execute(
        task="Refactor authentication module",
        agents=[
            "claude-3-5-sonnet",  # For Architecture
            "github-copilot",     # For Implementation
            "gpt-4-turbo"         # For Security Audit
        ]
    )
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(f"\nConsensus: {result.consensus}")
    print(f"Confidence: {result.confidence_score:.2%}")
    print(f"Agents Participated: {len(result.agent_results)}")
    
    # Show individual agent contributions
    print("\n" + "-" * 60)
    print("INDIVIDUAL AGENT RESULTS")
    print("-" * 60)
    for i, agent_result in enumerate(result.agent_results, 1):
        print(f"\n{i}. {agent_result.agent_id}")
        print(f"   Output: {agent_result.output}")
        print(f"   Confidence: {agent_result.confidence:.2%}")
    
    # Show governance applied
    print("\n" + "-" * 60)
    print("GOVERNANCE RULES APPLIED")
    print("-" * 60)
    for rule in result.governance_applied:
        print(f"  ✓ {rule.get('rule', 'unknown')}")
    
    print("\n" + "=" * 60)
    print("✅ Swarm execution completed successfully!")
    print("=" * 60)
    
    # Show execution history
    print("\nExecution History:")
    for record in vireon.get_history():
        print(f"  - [{record['timestamp']}] {record['task']}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
