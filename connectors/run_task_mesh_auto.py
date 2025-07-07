"""
Automated Task Mesh Execution Script
Executes the task mesh without requiring user interaction
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.run_task_mesh import TaskMeshVisualizer

async def main():
    """Main execution function"""
    visualizer = TaskMeshVisualizer()
    
    # Print initial info
    visualizer.print_header()
    visualizer.print_execution_plan()
    
    print("\n🚀 Starting automatic execution...")
    
    # Start execution with monitoring
    try:
        summary = await visualizer.monitor_execution()
        
        # Check if all tasks completed successfully
        if summary['failed'] == 0 and summary['blocked'] == 0:
            print("\n✅ All tasks completed successfully!")
            return 0
        else:
            print(f"\n⚠️  Execution completed with {summary['failed']} failures and {summary['blocked']} blocked tasks.")
            
            # Show failed tasks details
            if summary['failed'] > 0:
                print("\nFailed Tasks Details:")
                for task_id in visualizer.orchestrator.state.failed_tasks:
                    task = visualizer.orchestrator.state.tasks[task_id]
                    print(f"  - {task.name}: {task.error}")
            return 1
    
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
        return 2
    except Exception as e:
        print(f"\n\nError during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
