import asyncio
import os
from adaptive_llm_router.llm import invoke

# Mock litellm because we don't have API keys in the test environment
# and we are not testing litellm itself, but the router logic.
class MockLiteLLMResponse:
    class MockChoice:
        class MockMessage:
            def __init__(self, content):
                self.content = content

        def __init__(self, content):
            self.message = self.MockMessage(content)

    class MockUsage:
        def __init__(self, prompt_tokens, completion_tokens):
            self.prompt_tokens = prompt_tokens
            self.completion_tokens = completion_tokens

    def __init__(self, content, prompt_tokens=10, completion_tokens=20):
        self.choices = [self.MockChoice(content)]
        self.usage = self.MockUsage(prompt_tokens, completion_tokens)

async def mock_acompletion(model, messages):
    # The model string is 'provider/model', we return it for verification
    return MockLiteLLMResponse(f"Mock response from {model}")

# Patch litellm.acompletion
import litellm
litellm.acompletion = mock_acompletion


async def main():
    """
    An example script to demonstrate the functionality of the Adaptive LLM Router.
    """
    print("--- Running Adaptive LLM Router Example ---")

    # Test Case 1: Balanced Default
    print("\n--- Test Case 1: Balanced Default ---")
    prompt1 = "This is a standard request."
    meta1 = {"agent_name": "test_agent"}
    response1 = await invoke(prompt1, meta1)
    print(f"Response: {response1}")

    # Test Case 2: High Quality
    print("\n--- Test Case 2: High Quality ---")
    prompt2 = "This is a high-quality request."
    meta2 = {"quality": "high", "agent_name": "test_agent"}
    response2 = await invoke(prompt2, meta2)
    print(f"Response: {response2}")

    # Test Case 3: Confidential
    print("\n--- Test Case 3: Confidential ---")
    prompt3 = "This is a confidential request."
    meta3 = {"confidential": True, "agent_name": "test_agent"}
    response3 = await invoke(prompt3, meta3)
    print(f"Response: {response3}")

    # Test Case 4: Long Context
    print("\n--- Test Case 4: Long Context ---")
    prompt4 = "This is a very long prompt... " * 1000  # Approx 8000 tokens
    meta4 = {"agent_name": "test_agent"}
    response4 = await invoke(prompt4, meta4)
    print(f"Response: {response4}")

    print("\n--- Adaptive LLM Router Example Complete ---")

if __name__ == "__main__":
    # Set a dummy API key to satisfy litellm's checks, even with mocking
    os.environ["OPENAI_API_KEY"] = "dummy_key"
    asyncio.run(main())
