import sys
import os
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock

# Add the parent directory to the system path to import the main agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cfo_cash import CfoCashAgent
from base_agent import Task, AgentType

async def main():
    """
    Main function to run the benchmark test for CfoCashAgent.
    """
    print("--- Starting CFO Cash Agent Benchmark ---")

    # To avoid actual financial operations, we'll mock the FinancialAgent
    # that CfoCashAgent depends on.
    with patch('cfo_cash.FinancialAgent') as MockFinancialAgentClass:
        # When FinancialAgent() is called, it returns this instance.
        mock_financial_agent_instance = MockFinancialAgentClass.return_value

        # We need to mock the async methods on the instance.
        async def process_task_side_effect(task):
            await asyncio.sleep(0.01)
            return {
                "status": "success",
                "message": f"Mock financial task '{task.description}' processed.",
                "payload": task.payload
            }

        # Replace the methods with AsyncMocks and configure them.
        mock_financial_agent_instance.process_task = AsyncMock(side_effect=process_task_side_effect)
        mock_financial_agent_instance.health_check = AsyncMock(return_value=True)

        # Instantiate the CFO agent. It will be initialized with the mocked FinancialAgent.
        cfo_agent = CfoCashAgent()

        # A list of benchmark tasks to simulate various financial scenarios
        benchmark_tasks = [
            Task(id="1", description="Analyze quarterly P&L", agent_type=AgentType.CFO, payload={"period": "Q3 2024"}),
            Task(id="2", description="Optimize R&D tax credits for new project", agent_type=AgentType.CFO, payload={"project_id": "proj_123"}),
            Task(id="3", description="Process new Stripe subscription event", agent_type=AgentType.CFO, payload={"platform": "stripe", "type": "subscription_created", "amount": 5000}),
            Task(id="4", description="Sync all banking transactions", agent_type=AgentType.CFO, payload={"sync_type": "full"}),
            Task(id="5", description="Generate revenue forecast for 2025", agent_type=AgentType.CFO, payload={"year": 2025}),
        ]

        print("\n--- Testing Task Processing ---")
        for task in benchmark_tasks:
            print(f"\nProcessing Task: {task.description}")
            result = await cfo_agent.process_task(task)
            print(f"Result: {result}")
            # Verify that the mock financial agent was called
            mock_financial_agent_instance.process_task.assert_called_with(task)

        print("\n--- Testing Health Check ---")
        is_healthy = await cfo_agent.health_check()
        print(f"Health Check Passed: {is_healthy}")
        mock_financial_agent_instance.health_check.assert_called_once()

    print("\n--- CFO Cash Agent Benchmark Complete ---")

if __name__ == "__main__":
    # The actual financial_system.py uses posthog, which may not be configured.
    # We can patch it to avoid errors during the test run.
    with patch('financial_system.posthog', MagicMock()):
        asyncio.run(main())
