# PostHog Analytics Helper for 371 Minds OS
# Provides unified tracking across all agents and systems

import time
from datetime import datetime
from typing import Dict, Optional, Any

import posthog

# Forward declaration for type hinting
class Analytics371:
    pass

class TrackExecution:
    """Context manager to automatically track execution time"""

    def __init__(self, analytics: Analytics371, task_id: str, agent_type: str, user_id: str = "system"):
        self.analytics = analytics
        self.task_id = task_id
        self.agent_type = agent_type
        self.user_id = user_id
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time

        if exc_type is None:
            # Success
            self.analytics.track_agent_execution(
                self.task_id,
                self.agent_type,
                execution_time,
                "completed",
                user_id=self.user_id
            )
        else:
            # Error occurred
            self.analytics.track_error(
                self.task_id,
                self.agent_type,
                str(exc_val),
                execution_time,
                user_id=self.user_id
            )

class Analytics371:
    """Centralized analytics system for 371 Minds OS"""

    def __init__(self, api_key: str, host: str = "https://us.i.posthog.com"):
        posthog.project_api_key = api_key
        posthog.host = host
        self.client = posthog

    def track_agent_execution(self,
                            task_id: str,
                            agent_type: str,
                            execution_time: float,
                            status: str = "completed",
                            metadata: Optional[Dict[str, Any]] = None,
                            user_id: str = "system"):
        """Track agent execution with standard properties"""

        properties = {
            "task_id": task_id,
            "agent_type": agent_type,
            "execution_time": execution_time,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "platform": "371_minds_os"
        }

        if metadata:
            properties.update(metadata)

        self.client.capture(
            distinct_id=user_id,
            event="agent_execution",
            properties=properties
        )

    def track_repository_analysis(self,
                                task_id: str,
                                repo_url: str,
                                context: Dict[str, Any], # Changed from 'RepositoryContext'
                                execution_time: float,
                                user_id: str = "system"):
        """Track repository analysis with detailed metrics"""

        properties = {
            "task_id": task_id,
            "agent_type": "REPOSITORY_INTAKE",
            "execution_time": execution_time,
            "repo_url": repo_url,
            "timestamp": datetime.now().isoformat()
        }

        # Merge context dictionary into properties
        properties.update(context)

        self.client.capture(
            distinct_id=user_id,
            event="repository_analyzed",
            properties=properties
        )

    def track_code_generation(self,
                            task_id: str,
                            tech_stack: str,
                            generated_files: int,
                            execution_time: float,
                            user_id: str = "system"):
        """Track code generation activities"""

        properties = {
            "task_id": task_id,
            "agent_type": "CODE_GENERATION",
            "execution_time": execution_time,
            "tech_stack": tech_stack,
            "generated_files": generated_files,
            "timestamp": datetime.now().isoformat()
        }

        self.client.capture(
            distinct_id=user_id,
            event="code_generated",
            properties=properties
        )

    def track_error(self,
                   task_id: str,
                   agent_type: str,
                   error_message: str,
                   execution_time: float,
                   user_id: str = "system"):
        """Track errors across all agents"""

        properties = {
            "task_id": task_id,
            "agent_type": agent_type,
            "execution_time": execution_time,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }

        self.client.capture(
            distinct_id=user_id,
            event="agent_error",
            properties=properties
        )
