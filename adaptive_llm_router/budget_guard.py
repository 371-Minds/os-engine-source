"""
Hard-stop gate that returns BudgetExceededError or forces downgrade when the monthly cap is reached.
"""

from .config import MONTHLY_BUDGET_CAP
from .usage_ledger import UsageLedger, usage_ledger

class BudgetExceededError(Exception):
    """Custom exception for when the budget is exceeded."""
    pass

class BudgetManager:
    """
    Manages the LLM budget by checking usage against a monthly cap.
    """
    def __init__(self, monthly_cap: float, ledger: UsageLedger):
        self.monthly_cap = monthly_cap
        self.ledger = ledger

    def get_remaining_budget_percentage(self) -> float:
        """
        Calculates the percentage of the budget that remains.
        """
        if self.monthly_cap <= 0:
            return 0.0

        current_spend = self.ledger.get_total_cost_for_current_month()
        remaining = self.monthly_cap - current_spend

        if remaining <= 0:
            return 0.0

        return (remaining / self.monthly_cap)

    def is_budget_exceeded(self) -> bool:
        """
        Checks if the current spend has exceeded the monthly cap.
        """
        return self.get_remaining_budget_percentage() <= 0

    def check_budget(self):
        """
        Raises a BudgetExceededError if the budget is exhausted.
        """
        if self.is_budget_exceeded():
            raise BudgetExceededError(f"Monthly budget of ${self.monthly_cap} has been exceeded.")

# Initialize a default budget manager instance
budget_manager = BudgetManager(MONTHLY_BUDGET_CAP, usage_ledger)
