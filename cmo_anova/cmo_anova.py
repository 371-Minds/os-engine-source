import sys
import os
import asyncio

# Add the parent directory to the system path to import the main agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cmo_anova import CmoAnovaAgent
from base_agent import Task, AgentType

async def main():
    """
    Main function to run the benchmark test for CmoAnovaAgent.
    """
    print("--- Starting CMO Anova Agent Benchmark ---")

    # Instantiate the CMO agent
    cmo_agent = CmoAnovaAgent()

    # The current CmoAnovaAgent is a placeholder.
    # This test suite verifies its current behavior and can be expanded
    # when the agent's delegation logic to MarketingAutomationAgent is implemented.

    benchmark_tasks = [
        Task(id="1", description="Develop market strategy for new product launch", agent_type=AgentType.CMO, payload={"product": "ProductX"}),
        Task(id="2", description="Analyze customer acquisition cost for Q3", agent_type=AgentType.CMO, payload={"quarter": "Q3 2024"}),
        Task(id="3", description="Plan a new social media campaign for brand awareness", agent_type=AgentType.CMO, payload={"goal": "brand_awareness"}),
        Task(id="4", description="Review competitor marketing and suggest counter-strategies", agent_type=AgentType.CMO, payload={"competitors": ["CompA", "CompB"]}),
        Task(id="5", description="Optimize customer retention programs", agent_type=AgentType.CMO, payload={"focus_area": "retention"}),
    ]

    print("\n--- Testing Task Processing ---")
    for task in benchmark_tasks:
        print(f"\nProcessing Task: {task.description}")
        result = await cmo_agent.process_task(task)
        print(f"Result: {result}")
        # Assert the current placeholder behavior
        expected_message = f"Marketing task '{task.description}' is being processed."
        assert result["status"] == "success"
        assert result["message"] == expected_message
        print("Assertion passed: Agent returned the expected placeholder message.")


    print("\n--- Testing Health Check ---")
    is_healthy = await cmo_agent.health_check()
    print(f"Health Check Passed: {is_healthy}")
    assert is_healthy is True

    print("\n--- CMO Anova Agent Benchmark Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
