
"""
371 Minds Operating System - Base Agent Implementation
"""

import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

class AgentType(Enum):
    """Types of agents in the 371 Minds OS"""
    INTELLIGENT_ROUTER = "intelligent_router"
    CODE_GENERATION = "code_generation"
    MARKETING_ASSET = "marketing_asset"
    BUSINESS_LOGIC = "business_logic"
    DEPLOYMENT = "deployment"
    CREDENTIAL_MANAGER = "credential_manager"
    MARKETING_AUTOMATION = "marketing_automation"
    REPOSITORY_INTAKE = "repository_intake"
    QA_AUTOMATION = "qa_automation"
    TECH_STACK_SPECIALIST = "tech_stack_specialist"
    CEO = "ceo"
    CTO = "cto"

class TaskStatus(Enum):
    """Status of tasks in the system"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_HUMAN_APPROVAL = "requires_human_approval"

@dataclass
class Task:
    """Represents a task in the 371 Minds OS"""
    id: str
    description: str
    agent_type: AgentType
    payload: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    requires_human_approval: bool = False
    human_approval_message: Optional[str] = None

@dataclass
class AgentCapability:
    """Represents a capability of an agent"""
    name: str
    description: str
    required_credentials: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # in seconds

class BaseAgent(ABC):
    """Base class for all agents in the 371 Minds OS"""

    def __init__(self, agent_id: str, agent_type: AgentType, capabilities: List[AgentCapability]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.logger = logging.getLogger(f"{agent_type.value}_{agent_id}")
        self.is_busy = False
        self.current_task: Optional[Task] = None

    @abstractmethod
    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a task and return the result"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the agent is healthy and ready to process tasks"""
        pass

    def get_capabilities(self) -> List[AgentCapability]:
        """Return the capabilities of this agent"""
        return self.capabilities

    async def execute_task(self, task: Task) -> Task:
        """Execute a task and update its status"""
        self.is_busy = True
        self.current_task = task
        task.status = TaskStatus.IN_PROGRESS

        try:
            self.logger.info(f"Starting task {task.id}: {task.description}")
            result = await self.process_task(task)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()

            self.logger.info(f"Completed task {task.id}")

        except Exception as e:
            self.logger.error(f"Failed to process task {task.id}: {str(e)}")
            task.status = TaskStatus.FAILED
            task.result = {"error": str(e)}

        finally:
            self.is_busy = False
            self.current_task = None

        return task
