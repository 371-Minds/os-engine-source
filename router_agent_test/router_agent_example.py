import asyncio
import sys
import os
from typing import List, Dict, Any

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from router_agent import IntelligentRoutingSystem, RoutingDecision
from base_agent import BaseAgent, AgentType, Task

class MockAgent(BaseAgent):
    """A mock agent for testing purposes."""
    def __init__(self, agent_id: str, agent_type: AgentType):
        super().__init__(agent_id, agent_type, capabilities=[])
        self.is_busy = False

    async def execute_task(self, task: Task) -> Dict[str, Any]:
        print(f"  - Mock Agent {self.agent_id} ({self.agent_type.value}) received task: {task.id}")
        print(f"    - Description: {task.description}")
        if task.payload:
            # Don't print the whole submission payload, just the relevant parts
            payload_summary = {k: v for k, v in task.payload.items() if k != 'submission'}
            if not payload_summary and 'submission' in task.payload:
                 payload_summary = {'submission': task.payload['submission'][:80] + '...'} # truncate long submissions
            print(f"    - Payload: {payload_summary}")
        await asyncio.sleep(0.1) # Simulate async work
        return {"status": "completed", "result": f"Mock result for task {task.id}"}

    async def process_task(self, task: Task) -> Dict[str, Any]:
        return await self.execute_task(task)

    async def health_check(self) -> bool:
        """Mock health check. Always returns True."""
        return True


async def main():
    """Main function to run the router agent test suite."""
    print("--- Initializing Router Agent Test Suite ---")

    router = IntelligentRoutingSystem()

    # Create and register mock agents for all agent types
    mock_agents = {}
    for agent_type in AgentType:
        # Create a unique ID for each mock agent
        agent_id = f"mock_{agent_type.value.lower().replace(' ', '_')}_01"
        agent = MockAgent(agent_id=agent_id, agent_type=agent_type)
        mock_agents[agent_type] = agent
        router.register_agent(agent)
        print(f"Registered Mock Agent: {agent.agent_id} of type {agent_type.value}")

    print("\n--- Starting Test Submissions ---")

    # A diverse list of submissions to test different routing scenarios
    submissions = [
        # Scenario 1: Simple deployment request
        "Please deploy my new application from the repo github.com/user/my-app.",

        # Scenario 2: Marketing campaign
        "We need to create a new marketing campaign for our summer sale.",

        # Scenario 3: Full SaaS product build
        "I have an idea for a SaaS application. It needs a database, user authentication, and a payment gateway. Let's launch it on AWS.",

        # Scenario 4: Infrastructure setup
        "Set up the infrastructure for our new service on DigitalOcean.",

        # Scenario 5: Financial analysis request
        "Can I get a P&L report for the last quarter? Also, project our revenue for the next year.",

        # Scenario 6: Simple business logic query
        "What is the best way to structure our customer support team?",

        # Scenario 7: Vague request that should default to business logic
        "Help me with my business.",

        # Scenario 8: Repository intake specific task
        "Analyze the repository at https://github.com/371-minds/mock-repo and suggest improvements."
    ]

    for i, submission_text in enumerate(submissions):
        print(f"\n--- Test Case #{i+1} ---")
        print(f"Submission: \"{submission_text}\"")

        # 1. Analyze the submission to get a routing decision
        routing_decision = await router.analyze_submission(submission_text)

        print("\nRouting Decision:")
        print(f"  - Task ID: {routing_decision.task_id}")
        print(f"  - Assigned Agents: {[agent.value for agent in routing_decision.assigned_agents]}")
        print(f"  - Execution Strategy: {routing_decision.execution_strategy}")
        print(f"  - Estimated Completion Time: {routing_decision.estimated_completion_time}s")

        # 2. Orchestrate the execution based on the decision
        print("\nOrchestration Log:")
        task_payload = {"submission": submission_text, "user_id": "test_user_01"}
        await router.orchestrate_execution(routing_decision, task_payload)

    print("\n--- Router Agent Test Suite Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
