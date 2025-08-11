# file: financial_system/financial_system_example_agent.py

import asyncio
import time
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path to find the financial_system module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from financial_system import FinancialAgent, Task, RDExpenseEntry
from base_agent import AgentType

# Mock PostHog for local testing
class MockPostHog:
    def capture(self, *args, **kwargs):
        print(f"PostHog Capture: {args}, {kwargs}")

# Replace the real PostHog with our mock
import financial_system
financial_system.posthog = MockPostHog()

async def run_financial_agent_benchmark():
    """
    Runs a series of simulated tasks for the FinancialAgent to benchmark
    its performance and decision-making capabilities.
    """
    print("--- Starting Financial Agent Benchmark ---")
    agent = FinancialAgent()

    # --- Task 1: P&L Analysis ---
    print("\n--- Task 1: P&L Analysis ---")
    pnl_task = Task(id="task_pnl_001", description="Analyze P&L for Q2 2025", agent_type=AgentType.FINANCIAL, payload={})
    result = await agent.process_task(pnl_task)
    print(f"P&L Analysis Result: {result}")

    # --- Task 2: R&D Tax Optimization ---
    print("\n--- Task 2: R&D Tax Optimization ---")
    rd_expenses = [
        RDExpenseEntry(
            expense_id="rd_exp_001", amount=50000, date=datetime(2025, 4, 15),
            description="Software development for new AI feature",
            employee_allocation={"dev1": 0.5, "dev2": 0.5}, project_code="AI-FEATURE-X",
            qualifying_activities=["software development"], tax_year=2025
        ),
        RDExpenseEntry(
            expense_id="rd_exp_002", amount=120000, date=datetime(2023, 8, 20),
            description="Algorithm research for core product",
            employee_allocation={"researcher1": 1.0}, project_code="CORE-ALG-IMP",
            qualifying_activities=["algorithm research"], tax_year=2023, retroactive_claim=True
        )
    ]
    # In a real scenario, the agent would fetch this data. We inject it for the test.
    # We will mock the output of analyze_rd_expenses directly to avoid recursion
    analysis_result = {
        'immediate_deductions_2025_plus': 50000.0,
        'retroactive_amendments_available': [rd_expenses[1]],
        'projected_tax_savings': (50000.0 + 120000.0) * 0.21,
        'compliance_documentation': 'Generated compliance documentation for 2 R&D expense entries.'
    }
    agent.rd_tax_optimizer.analyze_rd_expenses = lambda expenses: analysis_result
    rd_task = Task(id="task_rd_001", description="Optimize R&D tax credits", agent_type=AgentType.FINANCIAL, payload={})
    result = await agent.process_task(rd_task)
    print(f"R&D Tax Optimization Result: {result}")


    # --- Task 3: Billing Orchestration (Stripe) ---
    print("\n--- Task 3: Billing Orchestration (Stripe) ---")
    stripe_event = {
        "platform": "stripe",
        "type": "subscription_created",
        "subscription_id": "sub_abc123",
        "amount": 4900,  # $49.00 in cents
        "created": time.time(),
        "plan_name": "Pro Tier"
    }
    billing_task_stripe = Task(id="task_billing_stripe_001", description="Process new Stripe subscription", agent_type=AgentType.FINANCIAL, payload=stripe_event)
    result = await agent.process_task(billing_task_stripe)
    print(f"Stripe Billing Event Result: {result}")

    # --- Task 4: Billing Orchestration (Creem.io) ---
    print("\n--- Task 4: Billing Orchestration (Creem.io) ---")
    creemio_event = {
        "platform": "creemio",
        "type": "subscription_created",
        "subscription_id": "sub_def456",
        "amount": 9900,  # $99.00 in cents
        "created": time.time(),
        "plan_name": "Enterprise Plan"
    }
    billing_task_creemio = Task(id="task_billing_creemio_001", description="Handle Creem.io subscription event", agent_type=AgentType.FINANCIAL, payload=creemio_event)
    result = await agent.process_task(billing_task_creemio)
    print(f"Creem.io Billing Event Result: {result}")

    # --- Task 5: Banking Synchronization ---
    print("\n--- Task 5: Banking Synchronization ---")
    # Mocking the banking APIs to return some transactions
    async def mock_get_transactions():
        return [{"id": "merc_tx_1", "amount": -150.0, "description": "AWS Services"}]
    agent.banking_integration.mercury_api.get_transactions = mock_get_transactions

    banking_task = Task(id="task_banking_sync_001", description="Sync all banking transactions", agent_type=AgentType.FINANCIAL, payload={})
    result = await agent.process_task(banking_task)
    print(f"Banking Sync Result: {result}")

    print("\n--- Financial Agent Benchmark Complete ---")

if __name__ == "__main__":
    asyncio.run(run_financial_agent_benchmark())
