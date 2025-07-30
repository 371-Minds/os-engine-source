# Create a comprehensive implementation guide
implementation_guide = '''
# 371 Minds OS: Repository Intake Engine Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the Repository Intake Engine with PostHog analytics integration for the 371 Minds Operating System. The system combines repository-style bundling (inspired by repomix) with comprehensive analytics tracking.

## Architecture Components

### 1. Repository Intake Engine
- **Purpose**: Clone, analyze, and bundle git repositories
- **Features**: Language detection, security scanning, complexity analysis
- **Output**: RepositoryContext with comprehensive metadata

### 2. PostHog Analytics Integration
- **Purpose**: Track all agent executions and repository processing
- **Features**: Task tracking, execution time monitoring, error reporting
- **Output**: Real-time analytics and performance metrics

### 3. Intelligent Routing System
- **Purpose**: Route requests to appropriate agents with analytics
- **Features**: Request parsing, agent selection, result tracking
- **Output**: TaskResult with comprehensive metadata

## Installation & Setup

### Prerequisites
```bash
pip install posthog
pip install gitpython
pip install tree-sitter
pip install tree-sitter-python
pip install pathlib
pip install dataclasses
```

### PostHog Configuration
```python
import posthog

# Initialize PostHog
posthog.project_api_key = 'your-posthog-api-key'
posthog.host = 'https://us.i.posthog.com'  # or EU endpoint
```

## Implementation Steps

### Step 1: Set Up Repository Context Data Structure

The RepositoryContext dataclass captures comprehensive repository metadata:

```python
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
```

### Step 2: Implement Repository Analysis

Key analysis features based on research:

1. **Language Detection** (similar to repomix approach)
2. **Security Scanning** (inspired by GitHub secret scanning)
3. **Complexity Analysis** (using AST parsing)
4. **Dependency Extraction** (package.json, requirements.txt, etc.)

```python
def _analyze_repository(self, repo_path: Path, repo_url: str) -> RepositoryContext:
    """Comprehensive repository analysis"""
    context = RepositoryContext(repo_url=repo_url)
    
    # File analysis
    source_files = self._get_source_files(repo_path)
    context.total_files = len(source_files)
    
    # Language detection using file extensions
    context.languages = self._detect_languages(source_files)
    
    # Security scanning for secrets/vulnerabilities
    context.security_findings = self._scan_for_secrets(source_files)
    
    # Complexity analysis using AST parsing
    context.complexity_score = self._calculate_complexity(source_files)
    
    return context
```

### Step 3: Implement Repository Bundling

Based on repomix methodology:

```python
def _bundle_repository(self, repo_path: Path) -> str:
    """Bundle repository content for AI processing"""
    bundled_content = []
    
    # Respect .gitignore patterns
    gitignore_patterns = self._read_gitignore(repo_path)
    
    # Process files with security filtering
    for file_path in repo_path.rglob("*"):
        if self._should_include_file(file_path, gitignore_patterns):
            content = self._read_file_safely(file_path)
            if content:
                bundled_content.append(f"--- {file_path.relative_to(repo_path)} ---")
                bundled_content.append(content)
    
    return "\\n".join(bundled_content)
```

### Step 4: PostHog Analytics Integration

Track comprehensive metrics for each operation:

```python
def _track_repository_analysis(self, context: RepositoryContext, execution_time: float):
    """Track detailed repository analysis metrics"""
    properties = {
        "task_id": self.current_task_id,
        "agent_type": "REPOSITORY_INTAKE",
        "execution_time": execution_time,
        "repo_url": context.repo_url,
        "total_files": context.total_files,
        "total_lines": context.total_lines,  
        "languages": context.languages,
        "repo_size_mb": context.repo_size_mb,
        "complexity_score": context.complexity_score,
        "security_findings_count": len(context.security_findings),
        "timestamp": datetime.now().isoformat()
    }
    
    self.posthog_client.capture(
        distinct_id=self.user_id,
        event="repository_analyzed",
        properties=properties
    )
```

## Performance Optimizations

Based on research findings:

### 1. Repository Processing Optimizations
- **Parallel file processing** for large repositories
- **Streaming analysis** to avoid memory issues
- **Caching** for repeated repository analysis
- **Incremental processing** for repository updates

### 2. PostHog Analytics Optimizations
- **Batch event sending** to reduce API calls
- **Async event tracking** to avoid blocking operations
- **Error handling** with retry logic
- **Local buffering** during network issues

### 3. Security Best Practices
- **Secret detection** using regex patterns
- **File size limits** to prevent DoS attacks
- **Path traversal protection** during file processing
- **Sandboxed execution** for untrusted repositories

## Usage Examples

### Basic Repository Analysis
```python
# Initialize the system
router = IntelligentRoutingSystem()

# Process a repository
request = "Analyze the repository at https://github.com/microsoft/vscode"
result = router.route_request(request, user_id="developer123")

print(f"Analysis completed in {result.execution_time:.2f}s")
print(f"Repository has {result.output.total_files} files")
print(f"Languages detected: {result.output.languages}")
```

### Advanced Analytics Tracking
```python
# Initialize analytics with custom configuration
analytics = Analytics371("your-api-key")

# Track with context manager for automatic timing
with TrackExecution(analytics, "task123", "REPOSITORY_INTAKE") as tracker:
    context = process_repository("https://github.com/example/repo")
    
    # Additional specific tracking
    analytics.track_repository_analysis(
        tracker.task_id, 
        "https://github.com/example/repo",
        context,
        tracker.execution_time
    )
```

## Monitoring & Observability

### Key Metrics to Track

1. **Performance Metrics**
   - Repository processing time
   - Files processed per second
   - Memory usage during analysis
   - Token generation for AI processing

2. **Quality Metrics**
   - Security findings per repository
   - Complexity scores over time
   - Language distribution trends
   - Documentation coverage

3. **Operational Metrics**
   - Success/failure rates
   - Error types and frequencies
   - System resource utilization
   - User engagement patterns

### PostHog Dashboard Setup

Create dashboards to monitor:
- **Repository Processing Pipeline**: Track intake → analysis → generation flow
- **Agent Performance**: Compare execution times across different agent types
- **Quality Trends**: Monitor security findings and complexity over time
- **User Behavior**: Understand how different users interact with the system

## Error Handling & Recovery

### Robust Error Handling
```python
try:
    result = self.repository_engine.process_repository(repo_url, task_id, user_id)
    
    # Track success
    self._track_success(task_id, result, execution_time)
    
except subprocess.CalledProcessError as e:
    # Git operation failed
    self._track_git_error(task_id, repo_url, str(e), execution_time)
    
except MemoryError as e:
    # Repository too large
    self._track_resource_error(task_id, "memory", execution_time)
    
except Exception as e:
    # General error
    self._track_general_error(task_id, str(e), execution_time)
```

### Recovery Strategies
- **Automatic retry** with exponential backoff
- **Fallback processing** for large repositories
- **Graceful degradation** when external services fail
- **Circuit breaker** pattern for unreliable dependencies

## Testing Strategy

### Unit Tests
- Repository analysis functions
- PostHog event tracking
- Error handling scenarios
- Security scanning accuracy

### Integration Tests
- End-to-end repository processing
- PostHog analytics pipeline
- Multi-repository batch processing
- Performance under load

### Performance Tests
- Large repository handling (1GB+)
- Concurrent processing
- Memory usage profiling
- Analytics throughput

## Deployment Considerations

### Environment Configuration
```bash
# Required environment variables
POSTHOG_API_KEY=your_api_key_here
POSTHOG_HOST=https://us.i.posthog.com
REPO_TEMP_DIR=/tmp/repo_intake
MAX_REPO_SIZE_MB=1000
MAX_PROCESSING_TIME_SECONDS=300
```

### Resource Requirements
- **CPU**: Multi-core for parallel file processing
- **Memory**: 8GB+ for large repository analysis
- **Storage**: Temporary space for repository cloning
- **Network**: Reliable connection for git operations and PostHog

### Security Hardening
- **Sandboxed execution** environment
- **Resource limits** to prevent DoS
- **Network isolation** for untrusted repositories
- **Regular security updates** for dependencies

## Next Steps

1. **Implement the core engine** using provided code templates
2. **Set up PostHog analytics** with your API key
3. **Configure security scanning** with custom patterns
4. **Deploy with monitoring** and alerting
5. **Iterate based on analytics** and user feedback

This implementation provides a solid foundation for the 371 Minds OS Repository Intake Engine with comprehensive analytics and monitoring capabilities.
'''

# Save the implementation guide
with open('implementation_guide.md', 'w') as f:
    f.write(implementation_guide)

print("✅ Implementation guide created: implementation_guide.md")

# Create a quick start script
quick_start = '''#!/usr/bin/env python3
"""
371 Minds OS - Repository Intake Engine Quick Start
Run this script to test the basic functionality
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from repository_intake_engine import IntelligentRoutingSystem
    from analytics_371 import Analytics371
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all files are in the same directory")
    sys.exit(1)

def main():
    print("🚀 371 Minds OS - Repository Intake Engine")
    print("=" * 50)
    
    # Check environment
    api_key = os.getenv('POSTHOG_API_KEY', 'demo_key_12345')
    if api_key == 'demo_key_12345':
        print("⚠️  Using demo PostHog API key. Set POSTHOG_API_KEY environment variable for real tracking.")
    
    # Initialize system
    print("\\n🔧 Initializing system...")
    analytics = Analytics371(api_key)
    router = IntelligentRoutingSystem(posthog_client=analytics.client)
    print("✅ System initialized")
    
    # Test repository analysis
    print("\\n📊 Testing repository analysis...")
    test_requests = [
        "Analyze the repository at https://github.com/microsoft/vscode",
        "Modernize the legacy COBOL code to React",
        "Extract the API endpoints from https://github.com/fastapi/fastapi"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\\n{i}. Processing: {request}")
        
        try:
            result = router.route_request(request, user_id=f"test_user_{i}")
            
            print(f"   ✅ Status: {result.status}")
            print(f"   ⏱️  Execution time: {result.execution_time:.2f}s")
            print(f"   🤖 Agent: {result.agent_type}")
            
            if result.metadata:
                print(f"   📝 Metadata: {result.metadata}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\\n📈 Analytics Events Tracked:")
    print("   - request_routed")
    print("   - repository_intake_started") 
    print("   - repository_intake_completed")
    print("   - agent_execution")
    
    print("\\n✅ Quick start test completed!")
    print("\\nNext steps:")
    print("1. Set your real PostHog API key: export POSTHOG_API_KEY='your_key'")
    print("2. Implement actual repository cloning and analysis")
    print("3. Add security scanning and complexity analysis")
    print("4. Set up monitoring dashboards in PostHog")

if __name__ == "__main__":
    main()
'''

with open('quick_start.py', 'w') as f:
    f.write(quick_start)

# Make it executable
os.chmod('quick_start.py', 0o755)

print("✅ Quick start script created: quick_start.py")

print("\\n🎯 All files created successfully!")
print("\\nGenerated files:")
print("1. repository_intake_engine.py - Core implementation")
print("2. analytics_371.py - PostHog integration helper") 
print("3. integration_example.py - Usage example")
print("4. implementation_guide.md - Comprehensive guide")
print("5. quick_start.py - Test script")

# Create a requirements.txt file
requirements = '''# 371 Minds OS - Repository Intake Engine Requirements

# Core dependencies
posthog>=3.0.0
gitpython>=3.1.0
pathlib2>=2.3.0  # For Python < 3.4 compatibility

# Repository analysis
tree-sitter>=0.20.0
tree-sitter-python>=0.20.0
tree-sitter-javascript>=0.20.0
tree-sitter-typescript>=0.20.0

# Security scanning
detect-secrets>=1.4.0
bandit>=1.7.0
safety>=2.0.0

# Performance optimization
psutil>=5.9.0
memory-profiler>=0.60.0

# Development and testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.910

# Optional: For enhanced analysis
radon>=5.1.0  # Code complexity analysis
lizard>=1.17.0  # Cyclomatic complexity
semgrep>=1.0.0  # Static analysis
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("6. requirements.txt - Dependency list")

print("\\n📚 To get started:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Set PostHog API key: export POSTHOG_API_KEY='your_key'")
print("3. Run quick test: python quick_start.py")
print("4. Read the implementation guide for detailed setup")