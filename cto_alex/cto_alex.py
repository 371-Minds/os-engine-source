import sys
import os
import asyncio

# Add the parent directory to the system path to import the main agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cto_alex import CtoAlexAgent
from base_agent import Task, AgentType

async def main():
    """
    Main function to run the benchmark test for CtoAlexAgent.
    """
    print("--- Starting CTO Alex Agent Benchmark ---")

    # Instantiate the CTO agent
    cto_agent = CtoAlexAgent()

    # The current CtoAlexAgent is a placeholder.
    # This test suite verifies its current behavior and can be expanded
    # when the agent's delegation logic is implemented.

    benchmark_tasks = [
        Task(id="1", description="Design technical architecture for new microservice", agent_type=AgentType.CTO, payload={"service_name": "AuthService"}),
        Task(id="2", description="Evaluate and select a new database technology", agent_type=AgentType.CTO, payload={"requirements": ["scalability", "low_latency"]}),
        Task(id="3", description="Create a plan for reducing technical debt in the legacy system", agent_type=AgentType.CTO, payload={"system": "LegacyMonolith"}),
        Task(id="4", description="Oversee the response to a critical security vulnerability", agent_type=AgentType.CTO, payload={"vulnerability_id": "CVE-2024-12345"}),
        Task(id="5", description="Plan infrastructure scaling for anticipated holiday traffic", agent_type=AgentType.CTO, payload={"event": "Black Friday"}),
    ]

    print("\n--- Testing Task Processing ---")
    for task in benchmark_tasks:
        print(f"\nProcessing Task: {task.description}")
        result = await cto_agent.process_task(task)
        print(f"Result: {result}")
        # Assert the current placeholder behavior
        expected_message = f"Technical task '{task.description}' is being processed."
        assert result["status"] == "success"
        assert result["message"] == expected_message
        print("Assertion passed: Agent returned the expected placeholder message.")

    print("\n--- Testing Health Check ---")
    is_healthy = await cto_agent.health_check()
    print(f"Health Check Passed: {is_healthy}")
    assert is_healthy is True

    print("\n--- CTO Alex Agent Benchmark Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
