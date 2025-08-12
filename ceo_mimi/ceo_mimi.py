import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock

# Add the parent directory to the system path to import the main agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ceo_mimi import CeoMimiAgent
from base_agent import Task, AgentType

# Mock other agents for testing purposes
class MockAgent:
    def __init__(self, agent_id, agent_type):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.process_task = AsyncMock(return_value={"status": "success", "message": f"Mock task processed by {self.agent_type}"})

async def main():
    """
    Main function to run the benchmark test for CeoMimiAgent.
    """
    print("--- Starting CEO Mimi Agent Benchmark ---")

    # Instantiate the CEO agent
    ceo_agent = CeoMimiAgent()

    # Mock other agents that the CEO might delegate to
    mock_cto = MockAgent("cto_001", "CTO")
    mock_cfo = MockAgent("cfo_001", "CFO")
    mock_cmo = MockAgent("cmo_001", "CMO")

    # A list of benchmark tasks to simulate various scenarios
    benchmark_tasks = [
        Task(id="1", description="Develop a new feature for the main application.", agent_type=AgentType.CEO, payload={}),
        Task(id="2", description="Analyze the quarterly financial results.", agent_type=AgentType.CEO, payload={}),
        Task(id="3", description="Launch a new marketing campaign.", agent_type=AgentType.CEO, payload={}),
        Task(id="4", description="Review and approve the new infrastructure budget.", agent_type=AgentType.CEO, payload={}),
        Task(id="5", description="Coordinate a response to a major security vulnerability.", agent_type=AgentType.CEO, payload={}),
    ]

    # In a real scenario, the CEO agent would have a more complex mechanism
    # for delegating tasks. For this benchmark, we'll simulate the delegation
    # by calling the mock agents' process_task methods based on the task description.

    # This is a simplified simulation of the CEO's decision-making process.
    # A more advanced version would involve a router or a more sophisticated
    # delegation strategy.

    for task in benchmark_tasks:
        print(f"\nProcessing Task: {task.description}")

        # Simulate CEO's decision-making and delegation
        if "feature" in task.description or "security" in task.description:
            # Delegate to CTO
            print("CEO delegates to CTO.")
            result = await mock_cto.process_task(task)
        elif "financial" in task.description or "budget" in task.description:
            # Delegate to CFO
            print("CEO delegates to CFO.")
            result = await mock_cfo.process_task(task)
        elif "marketing" in task.description:
            # Delegate to CMO
            print("CEO delegates to CMO.")
            result = await mock_cmo.process_task(task)
        else:
            # CEO handles the task directly
            print("CEO handles task directly.")
            result = await ceo_agent.process_task(task)

        print(f"Result: {result}")

    print("\n--- CEO Mimi Agent Benchmark Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
