# VIREON Task Mesh Execution Guide

## Overview

The VIREON Task Mesh system provides parallel execution of data connector implementation tasks with MCP (Model Context Protocol) integration. This guide explains how to execute and monitor the task mesh.

## Components

### 1. Task Mesh Orchestrator (`task_mesh_orchestrator.py`)
- Manages task dependencies and execution order
- Handles parallel execution with configurable limits
- Integrates with MCP for notifications and monitoring
- Tracks task status and progress

### 2. Task Mesh Visualizer (`run_task_mesh.py`)
- Provides visual interface for monitoring execution
- Shows real-time progress by phase
- Displays running, completed, and failed tasks
- Saves execution summary

### 3. MCP Tools Integration (`mcp_tools_demo.py`)
- Demonstrates MCP tool integration
- Provides tools for phase execution
- Enables status queries and resource monitoring

## Execution Instructions

### Basic Execution

1. **Run the visual task mesh executor:**
```bash
python connectors/run_task_mesh.py
```

2. **Dry run to see execution plan:**
```bash
python connectors/run_task_mesh.py --dry-run
```

3. **Adjust parallel execution limit:**
```bash
python connectors/run_task_mesh.py --max-parallel 8
```

### MCP Tools Demo

Run the MCP integration demo:
```bash
python connectors/mcp_tools_demo.py
```

## Task Mesh Structure

### Phases
1. **Architecture** - Design patterns and base classes
2. **Implementation** - Core connector implementations
3. **Testing** - Unit and integration tests
4. **Documentation** - API docs and guides
5. **Integration** - System integration and deployment

### Task Dependencies
- Tasks within each phase can run in parallel
- Later phases depend on earlier phase completion
- Dependencies are automatically resolved

## Execution Flow

```
1. Initialize task mesh with all tasks
2. Calculate execution order based on dependencies
3. Execute tasks in parallel groups
4. Monitor progress and handle failures
5. Generate execution summary
```

## Monitoring

### Real-time Display
- Phase progress bars
- Currently running tasks
- Failed task details
- Overall completion percentage

### Output Files
- `task_mesh_summary_YYYYMMDD_HHMMSS.json` - Execution summary
- `mcp_demo_results_YYYYMMDD_HHMMSS.json` - MCP demo results

## MCP Integration

### Available MCP Tools

1. **execute_phase** - Execute specific phase tasks
   ```json
   {
     "phase": "implementation",
     "parallel": true
   }
   ```

2. **get_task_status** - Query task status
   ```json
   {
     "task_ids": ["task1", "task2"],
     "phase": "testing"
   }
   ```

3. **monitor_resources** - Monitor system resources
   ```json
   {
     "interval": 5.0,
     "metrics": ["cpu", "memory", "tasks"]
   }
   ```

## Error Handling

- Failed tasks don't block other independent tasks
- Blocked tasks are reported when dependencies fail
- Error details are saved in execution summary
- Tasks can be retried individually

## Best Practices

1. **Start with dry run** to understand execution plan
2. **Monitor first execution** to identify bottlenecks
3. **Adjust parallelism** based on system resources
4. **Check logs** for detailed error information
5. **Save summaries** for future reference

## Troubleshooting

### Common Issues

1. **Import errors** - Ensure you're in the correct directory
2. **Task failures** - Check task handler implementations
3. **Performance** - Adjust max parallel tasks
4. **MCP connection** - Verify MCP protocol is initialized

### Debug Mode

Add logging to see detailed execution:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

1. Implement actual task handlers in `task_handlers.py`
2. Add real MCP server integration
3. Connect to actual data sources
4. Implement progress persistence
5. Add task retry mechanisms

## Example Output

```
================================================================================
VIREON DATA CONNECTORS - TASK MESH EXECUTION
================================================================================
Total Tasks: 25
Max Parallel Tasks: 4
MCP Session ID: vireon-session-20241230-123456
================================================================================

PHASE SUMMARY:
--------------------------------------------------------------------------------

Architecture
  Progress: [████████████████████████████████████████] 100.0%
  Total: 5 | Completed: 5 | Running: 0 | Failed: 0 | Blocked: 0 | Pending: 0

Implementation
  Progress: [████████████████████░░░░░░░░░░░░░░░░░░░░] 50.0%
  Total: 8 | Completed: 4 | Running: 2 | Failed: 0 | Blocked: 0 | Pending: 2
```
