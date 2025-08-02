"""
The main entry point for the Adaptive LLM Router.
"""

import litellm
import tiktoken
from typing import Dict, Any, Optional

from .policy_engine import select_provider
from .provider_registry import provider_registry
from .usage_ledger import usage_ledger
from .budget_guard import budget_manager, BudgetExceededError
from .data_models import LLMUsage

# Initialize the tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

def estimate_tokens(text: str) -> int:
    """Estimates the number of tokens in a given text."""
    return len(tokenizer.encode(text))

async def invoke(
    prompt: str,
    meta: Dict[str, Any],
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    print("DEBUG: Entering adaptive_llm_router.invoke")
    """
    The main function for the Adaptive LLM Router.
    It selects a provider, makes the LLM call, and records the usage.
    """
    # 1. Estimate input tokens
    est_in = estimate_tokens(prompt)
    # For now, we'll estimate output tokens as a fraction of input, this can be improved.
    est_out = est_in // 2

    # 2. Select the best provider
    selected_model = select_provider(meta, est_in, est_out)
    provider_name, model_name = selected_model.split(":")

    provider_details = provider_registry.get_provider(provider_name, model_name)
    if not provider_details:
        raise ValueError(f"Provider {selected_model} not found in registry.")

    # 3. Check the budget
    try:
        budget_manager.check_budget()
    except BudgetExceededError as e:
        # Here you could implement a fallback to a free model or just raise
        raise e

    # 4. Make the LLM call using litellm
    try:
        response = await litellm.acompletion(
            model=f"{provider_name}/{model_name}",
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract usage details from the response
        usage = response.usage
        tokens_in = usage.prompt_tokens
        tokens_out = usage.completion_tokens
        status = "ok"

    except Exception as e:
        # Handle fallback or error
        tokens_in = est_in
        tokens_out = 0
        status = "error"
        raise e

    # 5. Calculate cost
    cost = (
        (tokens_in / 1000) * provider_details.cost_in +
        (tokens_out / 1000) * provider_details.cost_out
    )

    # 6. Record usage
    usage_data = LLMUsage(
        provider=provider_name,
        model=model_name,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost=cost,
        task_id=meta.get("task_id"),
        agent=meta.get("agent_name"),
        status=status,
    )
    usage_ledger.record_usage(usage_data)

    return response.choices[0].message.content
