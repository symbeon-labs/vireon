"""
Task Mesh Execution and Visualization Script

This script provides a visual interface for monitoring and executing the
VIREON data connector implementation task mesh.
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, List, Any
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.task_mesh_orchestrator import orchestrator, TaskStatus, TaskPhase
from connectors.mcp_integration.mcp_protocol import mcp_protocol, MCPMessage, MCPMessageType

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class TaskMeshVisualizer:
    """Visualizes task mesh execution progress"""
    
    def __init__(self):
        self.orchestrator = orchestrator
        self.start_time = None
        self.update_interval = 2.0  # seconds
        
    def print_header(self):
        """Print header information"""
        print("\n" + "="*80)
        print("VIREON DATA CONNECTORS - TASK MESH EXECUTION")
        print("="*80)
        print(f"Total Tasks: {len(self.orchestrator.state.tasks)}")
        print(f"Max Parallel Tasks: {self.orchestrator.max_parallel_tasks}")
        print(f"MCP Session ID: {self.orchestrator.mcp_session_id}")
        print("="*80 + "\n")
    
    def print_phase_summary(self):
        """Print summary by phase"""
        phase_summary = {}
        
        for task in self.orchestrator.state.tasks.values():
            if task.phase not in phase_summary:
                phase_summary[task.phase] = {
                    'total': 0,
                    'completed': 0,
                    'failed': 0,
                    'running': 0,
                    'pending': 0,
                    'blocked': 0
                }
            
            phase_summary[task.phase]['total'] += 1
            
            if task.status == TaskStatus.COMPLETED:
                phase_summary[task.phase]['completed'] += 1
            elif task.status == TaskStatus.FAILED:
                phase_summary[task.phase]['failed'] += 1
            elif task.status == TaskStatus.RUNNING:
                phase_summary[task.phase]['running'] += 1
            elif task.status == TaskStatus.BLOCKED:
                phase_summary[task.phase]['blocked'] += 1
            else:
                phase_summary[task.phase]['pending'] += 1
        
        print("\nPHASE SUMMARY:")
        print("-" * 80)
        
        for phase in TaskPhase:
            if phase in phase_summary:
                stats = phase_summary[phase]
                progress = stats['completed'] / stats['total'] * 100
                
                print(f"\n{phase.value}")
                print(f"  Progress: [{self._progress_bar(progress)}] {progress:.1f}%")
                print(f"  Total: {stats['total']} | Completed: {stats['completed']} | "
                      f"Running: {stats['running']} | Failed: {stats['failed']} | "
                      f"Blocked: {stats['blocked']} | Pending: {stats['pending']}")
    
    def print_execution_plan(self):
        """Print the execution plan"""
        print("\nEXECUTION PLAN:")
        print("-" * 80)
        
        for idx, group in enumerate(self.orchestrator.state.execution_order):
            print(f"\nGroup {idx + 1} (Parallel Execution):")
            for task_id in group:
                task = self.orchestrator.state.tasks[task_id]
                deps = f" [deps: {', '.join(task.dependencies)}]" if task.dependencies else ""
                print(f"  - {task.name}{deps}")
    
    def print_current_status(self):
        """Print current execution status"""
        if not self.start_time:
            return
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\nCURRENT STATUS (Elapsed: {elapsed:.1f}s):")
        print("-" * 80)
        
        # Running tasks
        if self.orchestrator.state.running_tasks:
            print("\nRunning Tasks:")
            for task_id in self.orchestrator.state.running_tasks:
                task = self.orchestrator.state.tasks[task_id]
                duration = (datetime.now() - task.started_at).total_seconds()
                print(f"  → {task.name} ({duration:.1f}s)")
        
        # Failed tasks
        if self.orchestrator.state.failed_tasks:
            print("\nFailed Tasks:")
            for task_id in self.orchestrator.state.failed_tasks:
                task = self.orchestrator.state.tasks[task_id]
                print(f"  ✗ {task.name}: {task.error}")
        
        # Overall progress
        total = len(self.orchestrator.state.tasks)
        completed = len(self.orchestrator.state.completed_tasks)
        progress = completed / total * 100 if total > 0 else 0
        
        print(f"\nOverall Progress: [{self._progress_bar(progress)}] {progress:.1f}%")
        print(f"Completed: {completed}/{total}")
    
    def _progress_bar(self, percentage: float, width: int = 40) -> str:
        """Generate a progress bar string"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    async def monitor_execution(self):
        """Monitor execution with periodic updates"""
        self.start_time = datetime.now()
        
        # Create monitoring task
        async def update_display():
            while True:
                # Clear screen (cross-platform)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                self.print_header()
                self.print_phase_summary()
                self.print_current_status()
                
                # Check if execution is complete
                if (len(self.orchestrator.state.completed_tasks) + 
                    len(self.orchestrator.state.failed_tasks) + 
                    len([t for t in self.orchestrator.state.tasks.values() 
                         if t.status == TaskStatus.BLOCKED])) == len(self.orchestrator.state.tasks):
                    break
                
                await asyncio.sleep(self.update_interval)
        
        # Start monitoring
        monitor_task = asyncio.create_task(update_display())
        
        # Execute task mesh
        summary = await self.orchestrator.execute()
        
        # Cancel monitoring
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        
        # Final display
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_header()
        self.print_phase_summary()
        self.print_final_summary(summary)
        
        return summary
    
    def print_final_summary(self, summary: Dict[str, Any]):
        """Print final execution summary"""
        print("\n" + "="*80)
        print("EXECUTION COMPLETE")
        print("="*80)
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Completed: {summary['completed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Blocked: {summary['blocked']}")
        print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        print(f"Phases Completed: {', '.join(summary['phases_completed']) if summary['phases_completed'] else 'None'}")
        print("="*80)
        
        # Save summary to file
        summary_file = f"task_mesh_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\nSummary saved to: {summary_file}")


async def main():
    """Main execution function"""
    visualizer = TaskMeshVisualizer()
    
    # Print initial plan
    visualizer.print_header()
    visualizer.print_execution_plan()
    
    print("\nPress Enter to start execution or 'q' to quit...")
    choice = input().strip().lower()
    
    if choice == 'q':
        print("Execution cancelled.")
        return
    
    # Start execution with monitoring
    try:
        summary = await visualizer.monitor_execution()
        
        # Check if all tasks completed successfully
        if summary['failed'] == 0 and summary['blocked'] == 0:
            print("\n✅ All tasks completed successfully!")
        else:
            print(f"\n⚠️  Execution completed with {summary['failed']} failures and {summary['blocked']} blocked tasks.")
            
            # Show failed tasks details
            if summary['failed'] > 0:
                print("\nFailed Tasks Details:")
                for task_id in visualizer.orchestrator.state.failed_tasks:
                    task = visualizer.orchestrator.state.tasks[task_id]
                    print(f"  - {task.name}: {task.error}")
    
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
    except Exception as e:
        print(f"\n\nError during execution: {str(e)}")
        import traceback
        traceback.print_exc()


def dry_run():
    """Perform a dry run to show execution plan without executing"""
    visualizer = TaskMeshVisualizer()
    visualizer.print_header()
    visualizer.print_execution_plan()
    
    # Calculate statistics
    total_tasks = len(orchestrator.state.tasks)
    phases = {}
    for task in orchestrator.state.tasks.values():
        if task.phase not in phases:
            phases[task.phase] = 0
        phases[task.phase] += 1
    
    print("\nDRY RUN STATISTICS:")
    print("-" * 80)
    print(f"Total Tasks: {total_tasks}")
    print(f"Execution Groups: {len(orchestrator.state.execution_order)}")
    print("\nTasks per Phase:")
    for phase, count in phases.items():
        print(f"  {phase.value}: {count} tasks")
    
    # Estimate execution time (assuming 2 seconds per task average)
    estimated_time = len(orchestrator.state.execution_order) * 2 * orchestrator.max_parallel_tasks
    print(f"\nEstimated Execution Time: ~{estimated_time} seconds")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Execute VIREON Task Mesh")
    parser.add_argument('--dry-run', action='store_true', help='Show execution plan without running')
    parser.add_argument('--max-parallel', type=int, default=4, help='Maximum parallel tasks')
    
    args = parser.parse_args()
    
    if args.max_parallel != 4:
        orchestrator.max_parallel_tasks = args.max_parallel
    
    if args.dry_run:
        dry_run()
    else:
        asyncio.run(main())
