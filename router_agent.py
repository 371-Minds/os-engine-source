
"""
371 Minds Operating System - Intelligent Routing System
"""

import asyncio
import json
import logging
import re
import uuid
import dataclasses
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from base_agent import BaseAgent, AgentType, Task, TaskStatus, AgentCapability, DeploymentRequest

@dataclass
class RoutingDecision:
    """Represents a routing decision made by the intelligent router"""
    task_id: str
    assigned_agents: List[AgentType]
    execution_strategy: str  # "sequential", "parallel", "conditional"
    dependencies: Dict[str, List[str]] = None
    estimated_completion_time: Optional[int] = None

class IntelligentRoutingSystem(BaseAgent):
    """
    The central orchestrator that analyzes submissions and determines system activation.
    This is the brain of the 371 Minds OS.
    """

    def __init__(self, agent_id: str = "intelligent_router_001"):
        capabilities = [
            AgentCapability(
                name="analyze_submission",
                description="Analyze user submissions to determine required systems"
            ),
            AgentCapability(
                name="orchestrate_parallel_execution", 
                description="Coordinate multiple agents to work in parallel"
            ),
            AgentCapability(
                name="monitor_decision_points",
                description="Track progress and identify when human input is needed"
            ),
            AgentCapability(
                name="optimize_resource_allocation",
                description="Ensure efficient use of system resources"
            )
        ]

        super().__init__(agent_id, AgentType.INTELLIGENT_ROUTER, capabilities)

        # Registry of available agents
        self.available_agents: Dict[AgentType, List[BaseAgent]] = {}
        self.task_queue: List[Task] = []
        self.active_tasks: Dict[str, Task] = {}
        self.routing_rules: Dict[str, List[AgentType]] = self._initialize_routing_rules()

    def _initialize_routing_rules(self) -> Dict[str, List[AgentType]]:
        """Initialize routing rules based on common request patterns"""
        return {
            "deploy_application": [
                AgentType.CODE_GENERATION,
                AgentType.DEPLOYMENT,
                AgentType.CREDENTIAL_MANAGER  
            ],
            "create_marketing_campaign": [
                AgentType.MARKETING_ASSET,
                AgentType.BUSINESS_LOGIC
            ],
            "build_saas_product": [
                AgentType.CODE_GENERATION,
                AgentType.BUSINESS_LOGIC,
                AgentType.MARKETING_ASSET,
                AgentType.DEPLOYMENT,
                AgentType.CREDENTIAL_MANAGER
            ],
            "setup_infrastructure": [
                AgentType.DEPLOYMENT,
                AgentType.CREDENTIAL_MANAGER
            ],
            "financial_analysis": [
                AgentType.FINANCIAL,
                AgentType.CFO
            ]
        }

    def register_agent(self, agent: BaseAgent):
        """Register an agent with the routing system"""
        if agent.agent_type not in self.available_agents:
            self.available_agents[agent.agent_type] = []

        self.available_agents[agent.agent_type].append(agent)
        self.logger.info(f"Registered agent {agent.agent_id} of type {agent.agent_type.value}")

    async def analyze_submission(self, submission: str) -> RoutingDecision:
        """
        Analyze a user submission to determine which systems need to activate
        """
        self.logger.info(f"Analyzing submission: {submission[:100]}...")

        # In a real implementation, this would use NLP/ML to analyze the submission
        # For now, we'll use keyword matching and pattern recognition

        submission_lower = submission.lower()
        required_agents = set()
        execution_strategy = "sequential"

        # Pattern matching logic
        if any(keyword in submission_lower for keyword in ["deploy", "launch", "go live"]):
            required_agents.update([AgentType.CODE_GENERATION, AgentType.DEPLOYMENT])

        if any(keyword in submission_lower for keyword in ["saas", "application", "app"]):
            required_agents.update([
                AgentType.CODE_GENERATION, 
                AgentType.BUSINESS_LOGIC,
                AgentType.DEPLOYMENT,
                AgentType.CREDENTIAL_MANAGER
            ])
            execution_strategy = "parallel"

        if any(keyword in submission_lower for keyword in ["repository", "repo", "github.com"]):
            required_agents.add(AgentType.REPOSITORY_INTAKE)

        if any(keyword in submission_lower for keyword in ["marketing", "campaign", "social media"]):
            required_agents.add(AgentType.MARKETING_ASSET)

        if any(keyword in submission_lower for keyword in ["database", "api", "credentials"]):
            required_agents.add(AgentType.CREDENTIAL_MANAGER)

        if any(keyword in submission_lower for keyword in [
            "financial", "cfo", "cash", "revenue", "expenses", "profit",
            "p&l", "r&d", "tax", "billing", "subscription", "payment"
        ]):
            required_agents.add(AgentType.FINANCIAL)
            required_agents.add(AgentType.CFO)

        # Default to business logic if no specific patterns found
        if not required_agents:
            required_agents.add(AgentType.BUSINESS_LOGIC)

        task_id = f"task_{len(self.active_tasks) + 1}_{hash(submission) % 10000}"

        return RoutingDecision(
            task_id=task_id,
            assigned_agents=list(required_agents),
            execution_strategy=execution_strategy,
            estimated_completion_time=self._estimate_completion_time(required_agents)
        )

    def _estimate_completion_time(self, agents: Set[AgentType]) -> int:
        """Estimate completion time based on agent types and complexity"""
        base_times = {
            AgentType.CODE_GENERATION: 300,  # 5 minutes
            AgentType.MARKETING_ASSET: 180,  # 3 minutes
            AgentType.BUSINESS_LOGIC: 120,   # 2 minutes
            AgentType.DEPLOYMENT: 240,       # 4 minutes
            AgentType.CREDENTIAL_MANAGER: 60 # 1 minute
        }

        if len(agents) <= 2:
            return max(base_times.get(agent, 120) for agent in agents)
        else:
            # Parallel execution, so take the longest agent time + coordination overhead
            return max(base_times.get(agent, 120) for agent in agents) + 60

    def _generate_task_id(self):
        return str(uuid.uuid4())

    def _extract_repo_url(self, user_input: str) -> Optional[str]:
        match = re.search(r'https?://[^\s]+', user_input)
        return match.group(0) if match else "https://github.com/example/repo"

    def _extract_branch(self, user_input: str) -> Optional[str]:
        match = re.search(r'\bbranch\s+([^\s]+)', user_input)
        return match.group(1) if match else "main"

    def _extract_domain(self, user_input: str) -> Optional[str]:
        match = re.search(r'\bdomain\s+([^\s]+)', user_input)
        return match.group(1) if match else "app.example.com"

    def _extract_provider(self, user_input: str) -> Optional[str]:
        if "digitalocean" in user_input.lower():
            return "digitalocean"
        if "aws" in user_input.lower():
            return "aws"
        if "gcp" in user_input.lower():
            return "gcp"
        return "digitalocean"

    def _extract_infra_spec(self, user_input: str) -> Dict:
        # This would be a more complex parsing in a real system
        return {"size": "s-1vcpu-1gb", "region": "nyc3", "replicas": 1}

    def _extract_registry(self, user_input: str) -> str:
        # Placeholder
        return "registry.digitalocean.com/myapp"

    def _extract_env_vars(self, user_input: str) -> Dict[str, str]:
        # Placeholder
        return {"NODE_ENV": "production"}

    def _build_deployment_request(self, user_input: str, task_id: str) -> DeploymentRequest:
        """Constructs a DeploymentRequest from user input."""
        repo_url = self._extract_repo_url(user_input)
        branch = self._extract_branch(user_input)
        env = "production" if "production" in user_input else "staging"
        domain = self._extract_domain(user_input)

        return DeploymentRequest(
            task_id=task_id,
            repo_url=repo_url,
            repo_branch=branch,
            target_environment=env,
            cloud_provider=self._extract_provider(user_input) or "digitalocean",
            infra_spec=self._extract_infra_spec(user_input),
            domain=domain,
            ssl="ssl" in user_input.lower(),
            build_commands="npm install && npm run build",
            container_registry=self._extract_registry(user_input),
            environment_vars=self._extract_env_vars(user_input)
        )

    async def orchestrate_execution(self, routing_decision: RoutingDecision, 
                                   task_payload: Dict) -> List[Task]:
        """
        Orchestrate the execution of multiple agents based on routing decision
        """
        self.logger.info(f"Orchestrating execution for task {routing_decision.task_id}")

        tasks = []
        user_submission = task_payload.get("submission", "")

        # Create tasks for each assigned agent
        for i, agent_type in enumerate(routing_decision.assigned_agents):
            sub_task_id = f"{routing_decision.task_id}_subtask_{i+1}"
            current_payload = task_payload

            # If the agent is a repository intake agent, extract the URL
            if agent_type == AgentType.REPOSITORY_INTAKE:
                repo_url = self._extract_repo_url(user_submission)
                current_payload = {"repo_url": repo_url, "user_id": task_payload.get("user_id")}

            # If the agent is a deployment agent, build a specialized payload
            elif agent_type == AgentType.DEPLOYMENT:
                self.logger.info(f"Building specialized deployment request for sub-task {sub_task_id}")
                deployment_request = self._build_deployment_request(user_submission, sub_task_id)
                current_payload = dataclasses.asdict(deployment_request)

            task = Task(
                id=sub_task_id,
                description=f"Execute {agent_type.value} for {routing_decision.task_id}",
                agent_type=agent_type,
                payload=current_payload
            )
            tasks.append(task)
            self.active_tasks[task.id] = task

        # Execute based on strategy
        if routing_decision.execution_strategy == "parallel":
            await self._execute_parallel(tasks)
        elif routing_decision.execution_strategy == "sequential":
            await self._execute_sequential(tasks)
        else:
            await self._execute_conditional(tasks)

        return tasks

    async def _execute_parallel(self, tasks: List[Task]):
        """Execute tasks in parallel"""
        self.logger.info(f"Executing {len(tasks)} tasks in parallel")

        # Create coroutines for each task
        coroutines = []
        for task in tasks:
            available_agents = self.available_agents.get(task.agent_type, [])
            if available_agents:
                # Get the first available agent (in production, use load balancing)
                agent = next((a for a in available_agents if not a.is_busy), available_agents[0])
                coroutines.append(agent.execute_task(task))

        # Execute all tasks concurrently
        if coroutines:
            await asyncio.gather(*coroutines)

    async def _execute_sequential(self, tasks: List[Task]):
        """Execute tasks sequentially"""
        self.logger.info(f"Executing {len(tasks)} tasks sequentially")

        for task in tasks:
            available_agents = self.available_agents.get(task.agent_type, [])
            if available_agents:
                agent = next((a for a in available_agents if not a.is_busy), available_agents[0])
                await agent.execute_task(task)

    async def _execute_conditional(self, tasks: List[Task]):
        """Execute tasks with conditional logic"""
        # This would implement more complex conditional execution logic
        # For now, default to sequential
        await self._execute_sequential(tasks)

    async def monitor_decision_points(self) -> List[str]:
        """
        Monitor for decision points that require human approval
        """
        alerts = []

        for task_id, task in self.active_tasks.items():
            if task.requires_human_approval and task.status == TaskStatus.REQUIRES_HUMAN_APPROVAL:
                alerts.append(task.human_approval_message or f"Task {task_id} requires approval")

        return alerts

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a routing task"""
        submission = task.payload.get("submission", "")

        # Analyze the submission
        routing_decision = await self.analyze_submission(submission)

        # Orchestrate execution
        subtasks = await self.orchestrate_execution(routing_decision, task.payload)

        return {
            "routing_decision": {
                "task_id": routing_decision.task_id,
                "assigned_agents": [agent.value for agent in routing_decision.assigned_agents],
                "execution_strategy": routing_decision.execution_strategy,
                "estimated_completion_time": routing_decision.estimated_completion_time
            },
            "subtasks_created": len(subtasks),
            "subtasks": [{"id": t.id, "status": t.status.value} for t in subtasks]
        }

    async def health_check(self) -> bool:
        """Check if the routing system is healthy"""
        # Check if we can access agent registry
        if not hasattr(self, 'available_agents'):
            return False

        # Check if we have at least one agent of each critical type
        critical_types = [AgentType.CODE_GENERATION, AgentType.DEPLOYMENT]
        for agent_type in critical_types:
            if agent_type not in self.available_agents or not self.available_agents[agent_type]:
                self.logger.warning(f"No agents available for critical type: {agent_type}")

        return True

    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the entire system"""
        agent_counts = {}
        for agent_type, agents in self.available_agents.items():
            agent_counts[agent_type.value] = {
                "total": len(agents),
                "busy": sum(1 for agent in agents if agent.is_busy),
                "available": sum(1 for agent in agents if not agent.is_busy)
            }

        return {
            "total_agents": sum(len(agents) for agents in self.available_agents.values()),
            "agent_breakdown": agent_counts,
            "active_tasks": len(self.active_tasks),
            "queue_length": len(self.task_queue)
        }
