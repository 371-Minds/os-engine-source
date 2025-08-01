"""
Integration example for the Adaptive LLM Router.
"""

import asyncio
import os
import json
from unittest.mock import MagicMock, AsyncMock, patch

from dotenv import load_dotenv

from qa_agent import QAAgent
from base_agent import Task, AgentType
from adaptive_llm_router.usage_ledger import usage_ledger

async def main():
    """
    An example of how to use the QAAgent to test the Adaptive LLM Router.
    """
    # Load environment variables from .env file
    load_dotenv()

    # --- Mocking litellm.acompletion ---
    # We mock the litellm.acompletion call to avoid needing real API keys.
    # The mock will return a response that looks like a real LiteLLM response.
    mock_response = MagicMock()
    mock_response.usage = MagicMock()
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a mocked response from the LLM."

    # Patch litellm.acompletion to return our mock response
    with patch('litellm.acompletion', new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = mock_response

        # --- Test Scenario 1: Normal Quality Request ---
        print("--- Running Scenario 1: Normal Quality Request ---")

        # Initialize the QA Agent
        qa_agent = QAAgent()

        # Create a task for the agent
        task1 = Task(
            id="qa_task_1",
            description="Ask a simple question.",
            agent_type=AgentType.QA_AUTOMATION,
            payload={
                "prompt": "What is the capital of France?",
                "meta": {"quality": "normal"}
            }
        )

        # Execute the task
        result1 = await qa_agent.execute_task(task1)

        # Print the result
        print("Task Result 1:", result1.result)

        # --- Test Scenario 2: High Quality Request ---
        print("\n--- Running Scenario 2: High Quality Request ---")

        task2 = Task(
            id="qa_task_2",
            description="Ask a complex question requiring a high-quality model.",
            agent_type=AgentType.QA_AUTOMATION,
            payload={
                "prompt": "Explain the theory of relativity in simple terms.",
                "meta": {"quality": "high"}
            }
        )

        result2 = await qa_agent.execute_task(task2)
        print("Task Result 2:", result2.result)

        # --- Test Scenario 3: Confidential Request ---
        print("\n--- Running Scenario 3: Confidential Request ---")

        task3 = Task(
            id="qa_task_3",
            description="Ask a question that should be handled by a local model.",
            agent_type=AgentType.QA_AUTOMATION,
            payload={
                "prompt": "What are the company's Q3 financial projections?",
                "meta": {"confidential": True}
            }
        )

        result3 = await qa_agent.execute_task(task3)
        print("Task Result 3:", result3.result)

    # --- Verify Usage Tracking ---
    print("\n--- Verifying Usage Tracking ---")
    if os.path.exists(usage_ledger.usage_file):
        with open(usage_ledger.usage_file, 'r') as f:
            usage_data = json.load(f)
            print("LLM Usage Ledger:")
            print(json.dumps(usage_data, indent=2))

            # Clean up the usage file for the next run
            os.remove(usage_ledger.usage_file)
            print("\nCleaned up usage ledger file.")
    else:
        print("Usage ledger file not found.")

if __name__ == "__main__":
    # Setup basic logging
    import logging
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
