"""
Persists every request's cost, latency, success, and response quality score.
"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import posthog

from .data_models import LLMUsage

class UsageLedger:
    """
    Tracks LLM usage by writing to a JSON file and sending events to PostHog.
    """
    def __init__(self, usage_file: Path, posthog_client: Optional[posthog.Posthog] = None):
        self.usage_file = usage_file
        self.posthog_client = posthog_client

    def record_usage(self, usage_data: LLMUsage):
        """
        Records a single usage event to the ledger and PostHog.
        """
        self._write_to_ledger(usage_data)
        self._capture_posthog_event(usage_data)

    def _write_to_ledger(self, usage_data: LLMUsage):
        """Appends a usage record to the JSON file."""
        records = []
        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                try:
                    records = json.load(f)
                except json.JSONDecodeError:
                    records = []

        records.append(usage_data.model_dump(mode='json'))

        with open(self.usage_file, 'w') as f:
            json.dump(records, f, indent=2)

    def _capture_posthog_event(self, usage_data: LLMUsage):
        """Sends a 'llm_usage' event to PostHog."""
        if self.posthog_client:
            self.posthog_client.capture(
                "llm_usage",
                properties={
                    "provider": usage_data.provider,
                    "model": usage_data.model,
                    "cost": usage_data.cost,
                    "agent": usage_data.agent,
                    "tokens_in": usage_data.tokens_in,
                    "tokens_out": usage_data.tokens_out,
                    "status": usage_data.status,
                    "task_id": usage_data.task_id,
                }
            )

    def get_total_cost_for_current_month(self) -> float:
        """
        Calculates the total cost of LLM usage for the current calendar month.
        """
        if not self.usage_file.exists():
            return 0.0

        with open(self.usage_file, 'r') as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                return 0.0

        total_cost = 0.0
        current_month = datetime.now().month
        current_year = datetime.now().year

        for record in records:
            # record['ts'] is a string, so we need to parse it
            record_ts = datetime.fromisoformat(record['ts'])
            if record_ts.month == current_month and record_ts.year == current_year:
                total_cost += record.get('cost', 0.0)

        return total_cost

# Initialize a default ledger instance
usage_path = Path(__file__).parent / "llm_usage.json"
# The PostHog client will be set later during the integration.
usage_ledger = UsageLedger(usage_path)
