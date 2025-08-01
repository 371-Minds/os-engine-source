"""
371 Minds Operating System - CASH (CFO) Agent Implementation
"""

from base_agent import BaseAgent, AgentType, Task, AgentCapability
from financial_system import FinancialAgent

class CfoCashAgent(BaseAgent):
    """
    CASH (CFO): Handles financial planning, analysis, and forecasting.

    @cfo-cash - Chief Financial Officer

    Primary Responsibilities:
    - Financial planning, analysis, and forecasting
    - Revenue optimization and cost management
    - Investment strategy and resource allocation
    - Financial reporting and compliance oversight
    - Risk management and operational efficiency

    Key Performance Indicators:
    - Revenue growth targets and profitability margins
    - Cost optimization and operational efficiency ratios
    - Cash flow management and financial stability
    - Investment ROI and resource allocation effectiveness
    - Financial reporting accuracy and compliance rates

    Reporting Structure: Reports to @ceo-agent

    Collaboration Protocols: Financial reviews with all departments, budget planning session
    """

    def __init__(self, agent_id: str = "cfo_cash_001"):
        capabilities = [
            AgentCapability(name="financial_planning", description="Manage financial planning, analysis, and forecasting."),
            AgentCapability(name="revenue_optimization", description="Optimize revenue and manage costs."),
            AgentCapability(name="investment_strategy", description="Develop and manage investment strategy."),
        ]
        super().__init__(agent_id, AgentType.CFO, capabilities)
        self.financial_agent = FinancialAgent()

    async def process_task(self, task: Task) -> dict:
        """Process a financial task by delegating to the FinancialAgent."""
        self.logger.info(f"CFO CASH delegating task '{task.description}' to FinancialAgent.")

        # Here, CfoCashAgent can add strategic oversight, validation, or enrichment
        # before and after delegating to the specialized financial agent.

        # For now, we delegate directly.
        # The financial agent expects a task of type FINANCIAL, but CfoCashAgent receives a CFO task.
        # We can either create a new task or just pass the relevant details.
        # Let's assume for now that the operational agent can handle a CFO task,
        # or in a more robust system, we would translate this.

        result = await self.financial_agent.process_task(task)

        return result

    async def health_check(self) -> bool:
        """Check if the agent and its sub-agents are healthy."""
        return await self.financial_agent.health_check()
