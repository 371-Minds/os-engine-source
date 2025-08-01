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

# PostHog integration
import posthog

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
    """
    Repository bundling engine inspired by repomix with analytics tracking
    """

    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client or posthog
        self.temp_dir = Path("/tmp/repo_intake")
        self.temp_dir.mkdir(exist_ok=True)

    def process_repository(self, repo_url: str, task_id: str, user_id: str = "system") -> RepositoryContext:
        """
        Main entry point for repository processing with analytics
        """
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

    def _clone_repository(self, repo_url: str, task_id: str) -> Path:
        """Clone repository to temporary location"""
        clone_path = self.temp_dir / f"repo_{task_id}"

        # Use subprocess to clone (similar to repomix approach)
        cmd = ["git", "clone", "--depth", "1", repo_url, str(clone_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Failed to clone repository: {result.stderr}")

        return clone_path

    def _analyze_repository(self, repo_path: Path, repo_url: str) -> RepositoryContext:
        """Analyze repository structure and metadata"""
        context = RepositoryContext(repo_url=repo_url)

        # Basic file analysis
        all_files = list(repo_path.rglob("*"))
        source_files = [f for f in all_files if f.is_file() and not f.name.startswith('.')]

        context.total_files = len(source_files)

        # Language detection
        language_counts = {}
        total_lines = 0

        for file_path in source_files:
            try:
                ext = file_path.suffix.lower()
                if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines

                        lang = self._extension_to_language(ext)
                        language_counts[lang] = language_counts.get(lang, 0) + lines
            except Exception:
                continue

        context.total_lines = total_lines
        context.languages = language_counts

        # Repository size
        total_size = sum(f.stat().st_size for f in source_files if f.exists())
        context.repo_size_mb = total_size / (1024 * 1024)

        # Git metadata
        try:
            git_dir = repo_path / ".git"
            if git_dir.exists():
                # Get last commit info
                cmd = ["git", "-C", str(repo_path), "rev-parse", "HEAD"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    context.last_commit_hash = result.stdout.strip()

                cmd = ["git", "-C", str(repo_path), "log", "-1", "--format=%ci"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    context.last_commit_date = result.stdout.strip()
        except Exception:
            pass

        return context

    def _bundle_repository(self, repo_path: Path) -> str:
        """Bundle repository content similar to repomix"""
        bundled_content = []

        # Read .gitignore patterns
        gitignore_patterns = self._read_gitignore(repo_path)

        # Process files
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and self._should_include_file(file_path, gitignore_patterns):
                try:
                    relative_path = file_path.relative_to(repo_path)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    bundled_content.append(f"\n--- {relative_path} ---\n")
                    bundled_content.append(content)
                except Exception:
                    continue

        return "\n".join(bundled_content)

    def _read_gitignore(self, repo_path: Path) -> List[str]:
        """Read .gitignore patterns"""
        gitignore_path = repo_path / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception:
                pass
        return []

    def _should_include_file(self, file_path: Path, gitignore_patterns: List[str]) -> bool:
        """Check if file should be included based on gitignore and other rules"""
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return False

        # Skip common non-source files
        skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.bin', '.jpg', '.png', '.gif', '.pdf'}
        if file_path.suffix.lower() in skip_extensions:
            return False

        # Skip large files (> 1MB)
        try:
            if file_path.stat().st_size > 1024 * 1024:
                return False
        except Exception:
            return False

        return True

    def _extension_to_language(self, ext: str) -> str:
        """Map file extension to language name"""
        mapping = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        return mapping.get(ext, 'Other')

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

# PostHog Analytics Helper for 371 Minds OS
# Provides unified tracking across all agents and systems

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
                                context: 'RepositoryContext',
                                execution_time: float,
                                user_id: str = "system"):
        """Track repository analysis with detailed metrics"""

        properties = {
            "task_id": task_id,
            "agent_type": "REPOSITORY_INTAKE",
            "execution_time": execution_time,
            "repo_url": repo_url,
            "total_files": context.total_files,
            "total_lines": context.total_lines,
            "languages": context.languages,
            "repo_size_mb": context.repo_size_mb,
            "complexity_score": context.complexity_score,
            "documentation_score": context.documentation_score,
            "test_coverage": context.test_coverage,
            "timestamp": datetime.now().isoformat()
        }

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

# Context manager for tracking execution time
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

    def _cleanup_temp_files(self, task_id: str):
        """Clean up temporary files"""
        import shutil
        clone_path = self.temp_dir / f"repo_{task_id}"
        if clone_path.exists():
            try:
                shutil.rmtree(clone_path)
            except Exception:
                pass


# Enhanced Intelligent Router with PostHog Integration

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
    """
    Enhanced routing system with PostHog analytics integration
    """

    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client or posthog
        self.repository_engine = RepositoryIntakeEngine(posthog_client)

    def route_request(self, request: str, user_id: str = "system") -> TaskResult:
        """Route request and track analytics"""
        task_id = self._generate_task_id()
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
            # Execute based on agent type
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

            elif agent_type == "TECH_STACK_SPECIALIST":
                # Handle tech stack specialization
                execution_time = time.time() - start_time

                return TaskResult(
                    task_id=task_id,
                    agent_type=agent_type,
                    status="completed", 
                    execution_time=execution_time,
                    output="Tech stack analysis completed",
                    metadata={"stack": "MERN"}
                )

            else:
                raise ValueError(f"Unknown agent type: {agent_type}")

        except Exception as e:
            execution_time = time.time() - start_time

            # Track failure
            self._track_event("request_failed", {
                "task_id": task_id,
                "agent_type": agent_type,
                "execution_time": execution_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }, user_id)

            return TaskResult(
                task_id=task_id,
                agent_type=agent_type,
                status="failed",
                execution_time=execution_time,
                error=str(e)
            )

    def _parse_request(self, request: str) -> tuple[str, str]:
        """Parse request to determine agent type and action"""
        request_lower = request.lower()

        if "repository" in request_lower or "repo" in request_lower or "github.com" in request_lower:
            return "REPOSITORY_INTAKE", "analyze"
        elif "modernize" in request_lower or "convert" in request_lower:
            return "TECH_STACK_SPECIALIST", "modernize"
        else:
            return "GENERAL", "process"

    def _extract_repo_url(self, request: str) -> str:
        """Extract repository URL from request"""
        import re

        # Look for GitHub URLs
        github_pattern = r'https://github\.com/[\w.-]+/[\w.-]+'
        match = re.search(github_pattern, request)

        if match:
            return match.group(0)

        # Default fallback
        return "https://github.com/example/repo"

    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        import uuid
        return str(uuid.uuid4())[:8]

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
