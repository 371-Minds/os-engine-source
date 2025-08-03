# Repository Intake Engine Implementation
# Aligned with the BaseAgent architecture

import os
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
import yaml
import requests

from base_agent import BaseAgent, AgentType, Task, AgentCapability
from analytics_371 import Analytics371

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
    structured_data: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        if self.languages is None:
            self.languages = {}
        if self.security_findings is None:
            self.security_findings = []
        if self.dependencies is None:
            self.dependencies = []
        if not self.processed_at:
            self.processed_at = datetime.now().isoformat()

class RepoIntakeAgent(BaseAgent):
    """
    An agent specialized in cloning, analyzing, and bundling Git repositories.
    """

    def __init__(self, agent_id: str = "repo_intake_agent_001", analytics_client: Optional[Analytics371] = None):
        capabilities = [
            AgentCapability(
                name="process_repository",
                description="Clone, analyze, and bundle a Git repository."
            )
        ]
        super().__init__(agent_id, AgentType.REPOSITORY_INTAKE, capabilities)
        self.analytics = analytics_client
        self.temp_dir = Path("/tmp/repo_intake")
        self.temp_dir.mkdir(exist_ok=True)

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Main entry point for repository processing.
        The payload should contain 'repo_url'.
        """
        start_time = time.time()
        repo_url = task.payload.get("repo_url")
        user_id = task.payload.get("user_id", "system")

        if not repo_url:
            raise ValueError("repo_url not found in task payload.")

        if self.analytics:
            self.analytics.track_agent_execution(task.id, self.agent_type.value, 0, "started", user_id=user_id)

        try:
            self.logger.info("DEBUG: Cloning repository...")
            local_path = self._clone_repository(repo_url, task.id)
            self.logger.info("DEBUG: Analyzing repository...")
            context = self._analyze_repository(local_path, repo_url)
            self.logger.info("DEBUG: Fetching structured.yaml...")
            context.structured_data = self._get_structured_yaml(repo_url)
            self.logger.info("DEBUG: Bundling repository...")
            self._bundle_repository(local_path)

            execution_time = time.time() - start_time
            result_context = asdict(context)

            if self.analytics:
                self.logger.info("DEBUG: Tracking repository analysis...")
                self.analytics.track_repository_analysis(task.id, repo_url, result_context, execution_time, user_id=user_id)
                self.logger.info("DEBUG: Tracking agent execution completion...")
                self.analytics.track_agent_execution(task.id, self.agent_type.value, execution_time, "completed", user_id=user_id)

            self.logger.info("DEBUG: Process task finished successfully.")
            return result_context

        except Exception as e:
            self.logger.error(f"DEBUG: Exception caught in process_task: {e}", exc_info=True)
            execution_time = time.time() - start_time
            if self.analytics:
                self.analytics.track_error(task.id, self.agent_type.value, str(e), execution_time, user_id=user_id)
            raise e

        finally:
            self._cleanup_temp_files(task.id)

    def _clone_repository(self, repo_url: str, task_id: str) -> Path:
        """Clone repository to a temporary location."""
        clone_path = self.temp_dir / f"repo_{task_id}"
        cmd = ["git", "clone", "--depth", "1", repo_url, str(clone_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Failed to clone repository: {result.stderr}")
        return clone_path

    def _analyze_repository(self, repo_path: Path, repo_url: str) -> RepositoryContext:
        """Analyze repository structure and metadata."""
        context = RepositoryContext(repo_url=repo_url)
        all_files = list(repo_path.rglob("*"))
        source_files = [f for f in all_files if f.is_file() and not self._is_binary(f) and ".git" not in str(f)]
        context.total_files = len(source_files)

        language_counts = {}
        total_lines = 0
        for file_path in source_files:
            try:
                ext = file_path.suffix.lower()
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    lang = self._extension_to_language(ext)
                    language_counts[lang] = language_counts.get(lang, 0) + lines
            except Exception:
                continue
        context.total_lines = total_lines
        context.languages = language_counts

        total_size = sum(f.stat().st_size for f in source_files if f.exists())
        context.repo_size_mb = total_size / (1024 * 1024)

        try:
            cmd = ["git", "-C", str(repo_path), "rev-parse", "HEAD"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                context.last_commit_hash = result.stdout.strip()
        except Exception:
            pass

        return context

    def _get_structured_yaml(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse structured.yaml from a repository."""
        # Note: This is a simplified approach that assumes a public GitHub repo
        # and a common branch name. A more robust solution would use the
        # GitHub API and handle different branches.
        if not repo_url.startswith("https://github.com/"):
            return None

        # Convert git URL to raw content URL
        base_url = repo_url.replace(".git", "").replace("github.com", "raw.githubusercontent.com")

        for branch in ["main", "master"]:
            yaml_url = f"{base_url}/{branch}/structured.yaml"
            try:
                response = requests.get(yaml_url)
                if response.status_code == 200:
                    return yaml.safe_load(response.text)
            except requests.RequestException as e:
                self.logger.warning(f"Could not fetch structured.yaml from {yaml_url}: {e}")
                continue

        self.logger.info(f"No structured.yaml found for {repo_url}")
        return None

    def _is_binary(self, file_path: Path) -> bool:
        """Check if a file is likely binary."""
        try:
            with open(file_path, 'rb') as f:
                # Read the first 1024 bytes
                chunk = f.read(1024)
                # If it contains a null byte, it's probably binary
                return b'\x00' in chunk
        except Exception:
            return True # If we can't read it, assume it's binary

    def _bundle_repository(self, repo_path: Path) -> str:
        """Bundle repository content into a single string."""
        bundled_content = []
        gitignore_patterns = self._read_gitignore(repo_path)

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
        """Read .gitignore patterns."""
        gitignore_path = repo_path / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception:
                pass
        return []

    def _should_include_file(self, file_path: Path, gitignore_patterns: List[str]) -> bool:
        """Check if a file should be included."""
        if any(part.startswith('.') for part in file_path.parts):
            return False

        # This is a simplified gitignore check
        if any(pattern in str(file_path) for pattern in gitignore_patterns):
            return False

        if self._is_binary(file_path):
            return False

        try:
            if file_path.stat().st_size > 1024 * 1024: # 1MB limit
                return False
        except Exception:
            return False

        return True

    def _extension_to_language(self, ext: str) -> str:
        """Map file extension to language name."""
        mapping = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.go': 'Go',
            '.rs': 'Rust', '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown'
        }
        return mapping.get(ext, 'Other')

    def _cleanup_temp_files(self, task_id: str):
        """Clean up temporary files."""
        import shutil
        clone_path = self.temp_dir / f"repo_{task_id}"
        if clone_path.exists():
            try:
                shutil.rmtree(clone_path)
            except Exception as e:
                self.logger.error(f"Failed to clean up temp directory {clone_path}: {e}")

    async def health_check(self) -> bool:
        """Health check for the repo intake agent."""
        return self.temp_dir.exists() and os.access(self.temp_dir, os.W_OK)
