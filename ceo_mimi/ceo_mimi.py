import sys
import os
import asyncio

# Add the parent directory to the system path to import the main agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ceo_mimi import CeoMimiAgent
from base_agent import Task, AgentType

async def main():
    """
    Main function to run the benchmark test for CeoMimiAgent.
    """
    print("--- Starting CEO Mimi Agent Benchmark ---")

    # Instantiate the CEO agent
    ceo_agent = CeoMimiAgent()

    # The current CeoMimiAgent is a placeholder.
    # This test suite verifies its current behavior.

    benchmark_tasks = [
        Task(id="1", description="Develop a new feature for the main application.", agent_type=AgentType.CEO, payload={"priority": 1}),
        Task(id="2", description="Analyze the quarterly financial results.", agent_type=AgentType.CEO, payload={"priority": 1}),
        Task(id="3", description="Launch a new marketing campaign.", agent_type=AgentType.CEO, payload={"priority": 2}),
        Task(id="4", description="Review and approve the new infrastructure budget.", agent_type=AgentType.CEO, payload={"priority": 1}),
        Task(id="5", description="Coordinate a response to a major security vulnerability.", agent_type=AgentType.CEO, payload={"priority": 0}),
    ]

    print("\n--- Testing Task Processing ---")
    for task in benchmark_tasks:
        print(f"\nProcessing Task: {task.description}")
        result = await ceo_agent.process_task(task)
        print(f"Result: {result}")
        # Assert the current placeholder behavior
        expected_message = f"Task '{task.description}' has been noted and will be delegated accordingly."
        assert result["status"] == "success"
        assert result["message"] == expected_message
        print("Assertion passed: Agent returned the expected placeholder message.")


    print("\n--- Testing Health Check ---")
    is_healthy = await ceo_agent.health_check()
    print(f"Health Check Passed: {is_healthy}")
    assert is_healthy is True

    print("\n--- CEO Mimi Agent Benchmark Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
