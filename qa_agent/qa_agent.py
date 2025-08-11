"""
QA Agent for testing the Adaptive LLM Router.
"""

from typing import Dict, Any

from base_agent import BaseAgent, AgentType, Task, AgentCapability

class QAAgent(BaseAgent):
    """
    A simple agent for asking questions to test the LLM router.
    """
    def __init__(self, agent_id: str = "qa_agent_001"):
        capabilities = [
            AgentCapability(
                name="ask_question",
                description="Ask a question to an LLM and get an answer."
            )
        ]
        super().__init__(agent_id, AgentType.QA_AUTOMATION, capabilities)

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Processes a QA task by calling the LLM invoke method.
        """
        prompt = task.payload.get("prompt")
        if not prompt:
            raise ValueError("Prompt not found in task payload.")

        # Set metadata for the policy engine
        meta = task.payload.get("meta", {"quality": "normal"})

        self.logger.info(f"Asking question: {prompt}")
        
        # Call the llm_invoke method from the base class
        llm_response = await self.llm_invoke(prompt, meta)

        self.logger.info(f"Got response: {llm_response}")

        return {"answer": llm_response}

    async def health_check(self) -> bool:
        """Health check for the QA agent."""
        return True
