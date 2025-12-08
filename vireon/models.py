"""
VIREON Data Models
------------------

Pydantic models for type safety and validation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """Result from a single agent execution."""
    
    agent_id: str = Field(..., description="Unique identifier for the agent")
    task: str = Field(..., description="Task that was executed")
    output: str = Field(..., description="Agent's response/output")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "claude-3-5-sonnet",
                "task": "Analyze code",
                "output": "Code is secure and follows best practices",
                "confidence": 0.92,
                "metadata": {"tokens": 1500}
            }
        }


class SwarmConsensus(BaseModel):
    """Consensus result from multi-agent execution."""
    
    consensus: str = Field(..., description="Final consensus decision")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    agent_results: List[AgentResult] = Field(default_factory=list, description="Individual agent results")
    governance_applied: List[Dict] = Field(default_factory=list, description="Governance rules applied")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "consensus": "Task completed successfully",
                "confidence_score": 0.89,
                "agent_results": [],
                "governance_applied": [{"rule": "consensus_required"}],
                "metadata": {"agents_count": 3}
            }
        }
    
    def __str__(self) -> str:
        return f"Consensus(confidence={self.confidence_score:.2f}): {self.consensus}"
