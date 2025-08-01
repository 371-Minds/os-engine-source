"""
Pydantic models for the Adaptive LLM Router, mocking a Convex DB schema.
"""

from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime

class LLMProvider(BaseModel):
    """
    Represents an LLM provider and model, mirroring the `llm_providers` table.
    """
    name: str  # e.g., "openrouter"
    model: str  # e.g., "gpt-4o"
    cost_in: float = Field(..., description="Cost per 1k input tokens in USD")
    cost_out: float = Field(..., description="Cost per 1k output tokens in USD")
    max_context: int = Field(..., description="Maximum context window size in tokens")
    latency_ms: int = Field(..., description="Expected latency in milliseconds")
    endpoint_env: str = Field(..., description="Environment variable for the API key")

class LLMUsage(BaseModel):
    """
    Represents a single usage event, mirroring the `llm_usage` table.
    """
    ts: datetime = Field(default_factory=datetime.now)
    provider: str
    model: str
    tokens_in: int
    tokens_out: int
    cost: float
    task_id: Optional[str] = None
    agent: Optional[str] = None
    status: Union[str, None] = "ok" # "ok", "fallback", "error"

class Settings(BaseModel):
    """
    Represents system settings, mirroring the `settings` table.
    """
    monthly_cap: float = 20.00
