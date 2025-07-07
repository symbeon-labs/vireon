"""
MCP Tools Integration Demo

This script demonstrates how to use MCP tools with the VIREON task mesh
for parallel execution and monitoring.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List

from mcp_integration.mcp_protocol import (
    mcp_protocol, MCPMessage, MCPMessageType, MCPResource, MCPTool
)
from task_mesh_orchestrator import orchestrator


class MCPTaskMeshIntegration:
    """Integrates MCP tools with task mesh execution"""
    
    def __init__(self):
        self.mcp = mcp_protocol
        self.orchestrator = orchestrator
        self.tool_results = {}
        
    async def register_task_mesh_tools(self):
        """Register task mesh specific tools"""
        
        # Tool for executing specific phases
        phase_tool = MCPTool(
            name="execute_phase",
            description="Execute a specific phase of the task mesh",
            input_schema={
                "type": "object",
                "properties": {
                    "phase": {
                        "type": "string",
                        "enum": ["architecture", "implementation", "testing", "documentation", "integration"],
                        "description": "Phase to execute"
                    },
                    "parallel": {
                        "type": "boolean",
                        "default": True,
                        "description": "Execute tasks in parallel"
                    }
                },
                "required": ["phase"]
            }
        )
        
        # Tool for task status query
        status_tool = MCPTool(
            name="get_task_status",
            description="Get status of specific tasks or all tasks",
            input_schema={
                "type": "object",
                "properties": {
                    "task_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of task IDs to query (empty for all)"
                    },
                    "phase": {
                        "type": "string",
                        "description": "Filter by phase"
                    }
                }
            }
        )
        
        # Tool for resource monitoring
        resource_tool = MCPTool(
            name="monitor_resources",
            description="Monitor resource usage during task execution",
            input_schema={
                "type": "object",
                "properties": {
                    "interval": {
                        "type": "number",
                        "default": 5.0,
                        "description": "Monitoring interval in seconds"
                    },
                    "metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": ["cpu", "memory", "tasks"],
                        "description": "Metrics to monitor"
                    }
                }
            }
        )
        
        # Register tools
        await self.mcp.register_tool(phase_tool)
        await self.mcp.register_tool(status_tool)
        await self.mcp.register_tool(resource_tool)
        
        print("✅ Task mesh MCP tools registered successfully")
    
    async def handle_mcp_requests(self):
        """Handle incoming MCP requests"""
        
        while True:
            # In a real implementation, this would listen for actual MCP messages
            # For demo purposes, we'll simulate processing
            await asyncio.sleep(1)
            
            # Check for pending tool calls
            if hasattr(self.mcp, 'pending_tool_calls'):
                for call in self.mcp.pending_tool_calls:
                    result = await self.execute_tool_call(call)
                    self.tool_results[call['id']] = result
    
    async def execute_tool_call(self, call: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        
        tool_name = call.get('tool')
        params = call.get('params', {})
        
        if tool_name == "execute_phase":
            return await self.execute_phase(params)
        elif tool_name == "get_task_status":
            return await self.get_task_status(params)
        elif tool_name == "monitor_resources":
            return await self.monitor_resources(params)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    async def execute_phase(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific phase"""
        phase = params.get('phase')
        parallel = params.get('parallel', True)
        
        # Filter tasks by phase
        phase_tasks = [
            task_id for task_id, task in self.orchestrator.state.tasks.items()
            if task.phase.value.lower() == phase.lower()
        ]
        
        if not phase_tasks:
            return {"error": f"No tasks found for phase: {phase}"}
        
        # Execute tasks
        results = {
            "phase": phase,
            "total_tasks": len(phase_tasks),
            "completed": 0,
            "failed": 0,
            "results": {}
        }
        
        if parallel:
            # Execute in parallel
            tasks = []
            for task_id in phase_tasks:
                task = self.orchestrator.run_task(task_id)
                tasks.append(task)
            
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for task_id, result in zip(phase_tasks, task_results):
                if isinstance(result, Exception):
                    results["failed"] += 1
                    results["results"][task_id] = {"status": "failed", "error": str(result)}
                else:
                    results["completed"] += 1
                    results["results"][task_id] = {"status": "completed", "result": result}
        else:
            # Execute sequentially
            for task_id in phase_tasks:
                try:
                    result = await self.orchestrator.run_task(task_id)
                    results["completed"] += 1
                    results["results"][task_id] = {"status": "completed", "result": result}
                except Exception as e:
                    results["failed"] += 1
                    results["results"][task_id] = {"status": "failed", "error": str(e)}
        
        return results
    
    async def get_task_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get task status"""
        task_ids = params.get('task_ids', [])
        phase_filter = params.get('phase')
        
        # Get all tasks if no specific IDs provided
        if not task_ids:
            task_ids = list(self.orchestrator.state.tasks.keys())
        
        # Apply phase filter if provided
        if phase_filter:
            task_ids = [
                tid for tid in task_ids
                if self.orchestrator.state.tasks[tid].phase.value.lower() == phase_filter.lower()
            ]
        
        # Collect status
        status = {
            "timestamp": datetime.now().isoformat(),
            "tasks": {}
        }
        
        for task_id in task_ids:
            if task_id in self.orchestrator.state.tasks:
                task = self.orchestrator.state.tasks[task_id]
                status["tasks"][task_id] = {
                    "name": task.name,
                    "phase": task.phase.value,
                    "status": task.status.value,
                    "dependencies": task.dependencies,
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "error": task.error
                }
        
        return status
    
    async def monitor_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor resources during execution"""
        interval = params.get('interval', 5.0)
        metrics = params.get('metrics', ['cpu', 'memory', 'tasks'])
        
        # In a real implementation, this would collect actual system metrics
        # For demo, we'll return simulated data
        monitoring_data = {
            "start_time": datetime.now().isoformat(),
            "interval": interval,
            "metrics": {}
        }
        
        if 'cpu' in metrics:
            monitoring_data['metrics']['cpu'] = {
                "usage_percent": 45.2,
                "cores_used": 2
            }
        
        if 'memory' in metrics:
            monitoring_data['metrics']['memory'] = {
                "usage_percent": 62.8,
                "used_mb": 2048,
                "available_mb": 1220
            }
        
        if 'tasks' in metrics:
            monitoring_data['metrics']['tasks'] = {
                "running": len(self.orchestrator.state.running_tasks),
                "completed": len(self.orchestrator.state.completed_tasks),
                "failed": len(self.orchestrator.state.failed_tasks),
                "pending": len([
                    t for t in self.orchestrator.state.tasks.values()
                    if t.status.value == "pending"
                ])
            }
        
        return monitoring_data
    
    async def demonstrate_mcp_execution(self):
        """Demonstrate MCP-controlled task mesh execution"""
        
        print("\n" + "="*80)
        print("MCP TASK MESH INTEGRATION DEMO")
        print("="*80)
        
        # Register tools
        await self.register_task_mesh_tools()
        
        # Simulate MCP tool calls
        print("\n📋 Simulating MCP Tool Calls...")
        
        # 1. Get initial status
        print("\n1️⃣ Getting initial task status...")
        status = await self.get_task_status({})
        print(f"   Total tasks: {len(status['tasks'])}")
        
        # 2. Execute architecture phase
        print("\n2️⃣ Executing Architecture phase in parallel...")
        arch_result = await self.execute_phase({
            "phase": "architecture",
            "parallel": True
        })
        print(f"   Completed: {arch_result['completed']}/{arch_result['total_tasks']}")
        
        # 3. Monitor resources
        print("\n3️⃣ Monitoring resources...")
        resources = await self.monitor_resources({
            "metrics": ["cpu", "memory", "tasks"]
        })
        print(f"   CPU: {resources['metrics']['cpu']['usage_percent']}%")
        print(f"   Memory: {resources['metrics']['memory']['usage_percent']}%")
        
        # 4. Execute implementation phase
        print("\n4️⃣ Executing Implementation phase...")
        impl_result = await self.execute_phase({
            "phase": "implementation",
            "parallel": True
        })
        print(f"   Completed: {impl_result['completed']}/{impl_result['total_tasks']}")
        
        # 5. Final status
        print("\n5️⃣ Getting final status...")
        final_status = await self.get_task_status({})
        
        # Summary
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        
        completed = sum(1 for t in final_status['tasks'].values() if t['status'] == 'completed')
        failed = sum(1 for t in final_status['tasks'].values() if t['status'] == 'failed')
        
        print(f"Total Tasks: {len(final_status['tasks'])}")
        print(f"Completed: {completed}")
        print(f"Failed: {failed}")
        
        # Save results
        results_file = f"mcp_demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "demo_timestamp": datetime.now().isoformat(),
                "initial_status": status,
                "architecture_result": arch_result,
                "implementation_result": impl_result,
                "final_status": final_status,
                "resources": resources
            }, f, indent=2)
        
        print(f"\nResults saved to: {results_file}")


async def main():
    """Main demo function"""
    integration = MCPTaskMeshIntegration()
    
    try:
        await integration.demonstrate_mcp_execution()
    except Exception as e:
        print(f"\nError during demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting MCP Task Mesh Integration Demo...")
    asyncio.run(main())
