
# Repository Intake Engine Implementation
# Based on repomix approach with PostHog analytics integration

import os
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import uuid

# PostHog integration (would be imported in real implementation)
# import posthog

@dataclass
class RepositoryContext:
    repo_url: str
    branch: str = "main"
    total_files: int = 0
    total_lines: int = 0
    languages: Dict[str, int] = None
    complexity_score: float = 0.0
    security_findings: List[str] = None
    documentation_score: float = 0.0
    test_coverage: float = 0.0
    dependencies: List[str] = None
    repo_size_mb: float = 0.0
    last_commit_hash: str = ""
    last_commit_date: str = ""
    processed_at: str = ""

    def __post_init__(self):
        if self.languages is None:
            self.languages = {}
        if self.security_findings is None:
            self.security_findings = []
        if self.dependencies is None:
            self.dependencies = []
        if not self.processed_at:
            self.processed_at = datetime.now().isoformat()

class RepositoryIntakeEngine:
    """Repository bundling engine inspired by repomix with analytics tracking"""

    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client
        self.temp_dir = Path("/tmp/repo_intake")
        self.temp_dir.mkdir(exist_ok=True)

    def process_repository(self, repo_url: str, task_id: str, user_id: str = "system") -> RepositoryContext:
        """Main entry point for repository processing with analytics"""
        start_time = time.time()

        # Track the start of repository processing
        self._track_event("repository_intake_started", {
            "task_id": task_id,
            "repo_url": repo_url,
            "agent_type": "REPOSITORY_INTAKE",
            "timestamp": datetime.now().isoformat()
        }, user_id)

        try:
            # Clone repository
            local_path = self._clone_repository(repo_url, task_id)

            # Analyze repository structure
            context = self._analyze_repository(local_path, repo_url)

            # Bundle repository content
            bundled_content = self._bundle_repository(local_path)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Track successful completion
            self._track_event("repository_intake_completed", {
                "task_id": task_id,
                "repo_url": repo_url,
                "agent_type": "REPOSITORY_INTAKE",
                "execution_time": execution_time,
                "total_files": context.total_files,
                "total_lines": context.total_lines,
                "repo_size_mb": context.repo_size_mb,
                "languages": context.languages,
                "timestamp": datetime.now().isoformat()
            }, user_id)

            return context

        except Exception as e:
            execution_time = time.time() - start_time

            # Track failure
            self._track_event("repository_intake_failed", {
                "task_id": task_id,
                "repo_url": repo_url,
                "agent_type": "REPOSITORY_INTAKE",
                "execution_time": execution_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }, user_id)

            raise

        finally:
            # Cleanup
            self._cleanup_temp_files(task_id)

    def _track_event(self, event_name: str, properties: Dict[str, Any], user_id: str):
        """Track event to PostHog with error handling"""
        try:
            if self.posthog_client:
                self.posthog_client.capture(
                    distinct_id=user_id,
                    event=event_name,
                    properties=properties
                )
        except Exception as e:
            print(f"Failed to track event {event_name}: {e}")

    def _clone_repository(self, repo_url: str, task_id: str) -> Path:
        """Clone repository to temporary location"""
        clone_path = self.temp_dir / f"repo_{task_id}"
        # Implementation would use subprocess to clone
        return clone_path

    def _analyze_repository(self, repo_path: Path, repo_url: str) -> RepositoryContext:
        """Analyze repository structure and metadata"""
        return RepositoryContext(repo_url=repo_url)

    def _bundle_repository(self, repo_path: Path) -> str:
        """Bundle repository content similar to repomix"""
        return "bundled content"

    def _cleanup_temp_files(self, task_id: str):
        """Clean up temporary files"""
        pass

@dataclass 
class TaskResult:
    task_id: str
    agent_type: str
    status: str
    execution_time: float
    output: Any = None
    error: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class IntelligentRoutingSystem:
    """Enhanced routing system with PostHog analytics integration"""

    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client
        self.repository_engine = RepositoryIntakeEngine(posthog_client)

    def route_request(self, request: str, user_id: str = "system") -> TaskResult:
        """Route request and track analytics"""
        task_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Determine agent type and action
        agent_type, action = self._parse_request(request)

        # Track routing decision
        self._track_event("request_routed", {
            "task_id": task_id,
            "agent_type": agent_type,
            "action": action,
            "request_length": len(request),
            "timestamp": datetime.now().isoformat()
        }, user_id)

        try:
            if agent_type == "REPOSITORY_INTAKE":
                repo_url = self._extract_repo_url(request)
                result = self.repository_engine.process_repository(repo_url, task_id, user_id)

                execution_time = time.time() - start_time

                return TaskResult(
                    task_id=task_id,
                    agent_type=agent_type,
                    status="completed",
                    execution_time=execution_time,
                    output=result,
                    metadata={
                        "repo_url": repo_url,
                        "total_files": result.total_files,
                        "languages": result.languages
                    }
                )
            else:
                execution_time = time.time() - start_time
                return TaskResult(
                    task_id=task_id,
                    agent_type=agent_type,
                    status="completed", 
                    execution_time=execution_time,
                    output="Task completed"
                )

        except Exception as e:
            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task_id,
                agent_type=agent_type,
                status="failed",
                execution_time=execution_time,
                error=str(e)
            )

    def _parse_request(self, request: str) -> tuple:
        """Parse request to determine agent type and action"""
        request_lower = request.lower()

        if "repository" in request_lower or "repo" in request_lower:
            return "REPOSITORY_INTAKE", "analyze"
        elif "modernize" in request_lower:
            return "TECH_STACK_SPECIALIST", "modernize"
        else:
            return "GENERAL", "process"

    def _extract_repo_url(self, request: str) -> str:
        """Extract repository URL from request"""
        import re
        github_pattern = r'https://github\.com/[\w.-]+/[\w.-]+'
        match = re.search(github_pattern, request)
        return match.group(0) if match else "https://github.com/example/repo"

    def _track_event(self, event_name: str, properties: Dict[str, Any], user_id: str):
        """Track event to PostHog"""
        try:
            if self.posthog_client:
                self.posthog_client.capture(
                    distinct_id=user_id,
                    event=event_name,
                    properties=properties
                )
        except Exception as e:
            print(f"Failed to track event {event_name}: {e}")
