import asyncio
import pytest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qa_agent.qa_agent import QAAgent
from base_agent import Task, AgentType

@pytest.mark.asyncio
async def test_ask_question_with_simple_prompt():
    """
    Tests the QA agent with a simple question.
    """
    print("Running test: test_ask_question_with_simple_prompt")

    with patch('base_agent.alr_invoke', new_callable=MagicMock) as mock_llm_invoke:
        future = asyncio.Future()
        future.set_result({"content": "The capital of France is Paris."})
        mock_llm_invoke.return_value = future

        agent = QAAgent()
        task = Task(
            id="123",
            description="A simple question",
            agent_type=AgentType.QA_AUTOMATION,
            payload={"prompt": "What is the capital of France?"}
        )

        result = await agent.process_task(task)

        expected_meta = {"quality": "normal", "agent_name": "qa_automation"}
        mock_llm_invoke.assert_called_once_with(
            "What is the capital of France?",
            expected_meta,
            user_id="qa_agent_001"
        )

        assert result == {"answer": {"content": "The capital of France is Paris."}}
        print("Test passed.")

@pytest.mark.asyncio
async def test_ask_question_with_custom_metadata():
    """
    Tests the QA agent with custom metadata.
    """
    print("\\nRunning test: test_ask_question_with_custom_metadata")

    with patch('base_agent.alr_invoke', new_callable=MagicMock) as mock_llm_invoke:
        future = asyncio.Future()
        future.set_result({"content": "The answer is 42."})
        mock_llm_invoke.return_value = future

        agent = QAAgent()
        task = Task(
            id="456",
            description="A question with custom metadata",
            agent_type=AgentType.QA_AUTOMATION,
            payload={
                "prompt": "What is the meaning of life?",
                "meta": {"quality": "high", "urgency": "asap"}
            }
        )

        result = await agent.process_task(task)

        expected_meta = {"quality": "high", "urgency": "asap", "agent_name": "qa_automation"}
        mock_llm_invoke.assert_called_once_with(
            "What is the meaning of life?",
            expected_meta,
            user_id="qa_agent_001"
        )
        assert result == {"answer": {"content": "The answer is 42."}}
        print("Test passed.")

def test_missing_prompt_in_payload():
    """
    Tests that a ValueError is raised when the prompt is missing.
    """
    print("\\nRunning test: test_missing_prompt_in_payload")
    agent = QAAgent()
    task = Task(
        id="789",
        description="A task with a missing prompt",
        agent_type=AgentType.QA_AUTOMATION,
        payload={}
    )

    with pytest.raises(ValueError, match="Prompt not found in task payload."):
        asyncio.run(agent.process_task(task))

    print("Test passed.")
