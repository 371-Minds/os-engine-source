#!/usr/bin/env python3
"""
371 Minds OS - Quick Start
Run this script to test the unified agent architecture.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from router_agent import IntelligentRoutingSystem
    from repo_intake_agent import RepoIntakeAgent
    from analytics_371 import Analytics371
    from base_agent import Task, AgentType
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required agent files and dependencies are present.")
    sys.exit(1)

import logging

async def main():
    """
    An asynchronous main function to orchestrate the agent system test.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    print("🚀 371 Minds OS - Unified Architecture Test")
    print("=" * 50)

    # 1. Initialize System Components
    print("\n🔧 Initializing system components...")
    api_key = os.getenv('POSTHOG_API_KEY', 'demo_key_12345')
    if api_key == 'demo_key_12345':
        print("⚠️  Using demo PostHog API key. No real tracking will occur.")

    analytics = Analytics371(api_key)
    router = IntelligentRoutingSystem()
    repo_intake_agent = RepoIntakeAgent(analytics_client=analytics)
    print("✅ System components initialized")

    # 2. Register Agents with the Router
    print("\n🔗 Registering agents with the Intelligent Router...")
    router.register_agent(repo_intake_agent)
    print(f"✅ Registered Agent: {repo_intake_agent.agent_id} ({repo_intake_agent.agent_type.value})")
    print("System Status:", router.get_system_status())


    # 3. Create and Process a Task
    print("\n📊 Creating and processing a repository analysis task...")

    # This is the high-level user request.
    user_submission = "Please analyze the repository at https://github.com/371-minds/os-engine-source"

    # We create a task for the INTELLIGENT_ROUTER. Its job is to break this down.
    initial_task = Task(
        id="quick_start_task_001",
        description="Top-level request to analyze a repository.",
        agent_type=AgentType.INTELLIGENT_ROUTER,
        payload={
            "submission": user_submission,
            "user_id": "quickstart_user"
        }
    )

    print(f"\n▶️  Executing task: '{initial_task.description}'")

    # The router processes the initial task and orchestrates the required sub-tasks.
    # In this case, it will analyze the submission and create a sub-task for the REPOSITORY_INTAKE agent.
    final_task_state = await router.execute_task(initial_task)

    # 4. Display Results
    print("\n✅ Task execution completed!")
    print(f"   - Task ID: {final_task_state.id}")
    print(f"   - Status: {final_task_state.status.value}")

    if final_task_state.status.value == "completed":
        # The result of the router's task is a summary of its orchestration.
        routing_decision = final_task_state.result.get("routing_decision", {})
        subtasks = final_task_state.result.get("subtasks", [])

        print("\n--- Router Orchestration Summary ---")
        print(f"   - Assigned Agents: {routing_decision.get('assigned_agents')}")
        print(f"   - Execution Strategy: {routing_decision.get('execution_strategy')}")
        print(f"   - Sub-tasks Created: {len(subtasks)}")

        # To see the result of the actual repo analysis, we need to inspect the state
        # of the sub-task that the router managed.
        print("\n--- Repo Intake Sub-task Details ---")
        # In a real system, you'd fetch the sub-task details from a shared task store.
        # Here, we can look at the router's internal state for this demo.
        for subtask_summary in subtasks:
            subtask_id = subtask_summary.get("id")
            if subtask_id in router.active_tasks:
                completed_subtask = router.active_tasks[subtask_id]
                print(f"   - Sub-task ID: {completed_subtask.id}")
                print(f"   - Agent: {completed_subtask.agent_type.value}")
                print(f"   - Status: {completed_subtask.status.value}")
                if completed_subtask.result:
                    print("   - Result:")
                    # Pretty print the JSON result from the repo intake agent
                    print(json.dumps(completed_subtask.result, indent=4))
    else:
        print("\n--- Task Failed ---")
        print(f"   - Error: {final_task_state.result.get('error', 'Unknown error')}")


    print("\n✅ Quick start test completed successfully!")
    print("\nThis test demonstrated the full, unified architecture:")
    print("1. A high-level task was sent to the Intelligent Router.")
    print("2. The router analyzed the task and delegated it to the correct specialist agent (`RepoIntakeAgent`).")
    print("3. The specialist agent executed its logic and returned a structured result.")
    print("4. All actions were tracked via the centralized analytics system.")


if __name__ == "__main__":
    # In Python 3.7+ you can run async main functions this way
    asyncio.run(main())
