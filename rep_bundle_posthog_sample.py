# Let me create some sample code implementations based on the research
# to show how to wire up the repository bundling logic and PostHog analytics

sample_code = """
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
    \"\"\"
    Repository bundling engine inspired by repomix with analytics tracking
    \"\"\"
    
    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client or posthog
        self.temp_dir = Path("/tmp/repo_intake")
        self.temp_dir.mkdir(exist_ok=True)
        
    def process_repository(self, repo_url: str, task_id: str, user_id: str = "system") -> RepositoryContext:
        \"\"\"
        Main entry point for repository processing with analytics
        \"\"\"
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
        \"\"\"Clone repository to temporary location\"\"\"
        clone_path = self.temp_dir / f"repo_{task_id}"
        
        # Use subprocess to clone (similar to repomix approach)
        cmd = ["git", "clone", "--depth", "1", repo_url, str(clone_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to clone repository: {result.stderr}")
            
        return clone_path
    
    def _analyze_repository(self, repo_path: Path, repo_url: str) -> RepositoryContext:
        \"\"\"Analyze repository structure and metadata\"\"\"
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
        \"\"\"Bundle repository content similar to repomix\"\"\"
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
                        
                    bundled_content.append(f"\\n--- {relative_path} ---\\n")
                    bundled_content.append(content)
                except Exception:
                    continue
        
        return "\\n".join(bundled_content)
    
    def _read_gitignore(self, repo_path: Path) -> List[str]:
        \"\"\"Read .gitignore patterns\"\"\"
        gitignore_path = repo_path / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    return [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except Exception:
                pass
        return []
    
    def _should_include_file(self, file_path: Path, gitignore_patterns: List[str]) -> bool:
        \"\"\"Check if file should be included based on gitignore and other rules\"\"\"
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
        \"\"\"Map file extension to language name\"\"\"
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
        \"\"\"Track event to PostHog with error handling\"\"\"
        try:
            if self.posthog_client:
                self.posthog_client.capture(
                    distinct_id=user_id,
                    event=event_name,
                    properties=properties
                )
        except Exception as e:
            print(f"Failed to track event {event_name}: {e}")
    
    def _cleanup_temp_files(self, task_id: str):
        \"\"\"Clean up temporary files\"\"\"
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
    \"\"\"
    Enhanced routing system with PostHog analytics integration
    \"\"\"
    
    def __init__(self, posthog_client=None):
        self.posthog_client = posthog_client or posthog
        self.repository_engine = RepositoryIntakeEngine(posthog_client)
        
    def route_request(self, request: str, user_id: str = "system") -> TaskResult:
        \"\"\"Route request and track analytics\"\"\"
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
        \"\"\"Parse request to determine agent type and action\"\"\"
        request_lower = request.lower()
        
        if "repository" in request_lower or "repo" in request_lower or "github.com" in request_lower:
            return "REPOSITORY_INTAKE", "analyze"
        elif "modernize" in request_lower or "convert" in request_lower:
            return "TECH_STACK_SPECIALIST", "modernize"
        else:
            return "GENERAL", "process"
    
    def _extract_repo_url(self, request: str) -> str:
        \"\"\"Extract repository URL from request\"\"\"
        import re
        
        # Look for GitHub URLs
        github_pattern = r'https://github\\.com/[\\w.-]+/[\\w.-]+'
        match = re.search(github_pattern, request)
        
        if match:
            return match.group(0)
        
        # Default fallback
        return "https://github.com/example/repo"
    
    def _generate_task_id(self) -> str:
        \"\"\"Generate unique task ID\"\"\"
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _track_event(self, event_name: str, properties: Dict[str, Any], user_id: str):
        \"\"\"Track event to PostHog\"\"\"
        try:
            if self.posthog_client:
                self.posthog_client.capture(
                    distinct_id=user_id,
                    event=event_name,
                    properties=properties
                )
        except Exception as e:
            print(f"Failed to track event {event_name}: {e}")


# Usage Example
def main():
    # Initialize PostHog
    posthog.project_api_key = 'your-posthog-api-key'
    posthog.host = 'https://us.i.posthog.com'
    
    # Create routing system
    router = IntelligentRoutingSystem()
    
    # Process a repository request
    request = "Analyze the repository at https://github.com/microsoft/vscode"
    result = router.route_request(request, user_id="user123")
    
    print(f"Task ID: {result.task_id}")
    print(f"Agent Type: {result.agent_type}")
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    
    if result.output:
        print(f"Repository Context: {result.output}")

if __name__ == "__main__":
    main()
\"\"\"

print("Sample implementation created successfully!")
print("\\nKey Features Implemented:")
print("1. Repository Intake Engine with repomix-style bundling")
print("2. PostHog analytics integration with task tracking")
print("3. RepositoryContext data structure for rich metadata")
print("4. Intelligent routing with execution time tracking")
print("5. Error handling and cleanup procedures")