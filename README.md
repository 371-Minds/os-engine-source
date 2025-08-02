# 371 Minds OS

The 371 Minds OS is a framework for building and orchestrating specialized AI agents to automate complex software development, marketing, and business logic tasks. It is designed as a microservices-based, event-driven "operating system" that routes tasks to the most appropriate agent, enabling parallel execution and human-in-the-loop decision-making.

## Core Concepts

The OS is built around a few core concepts:

*   **Intelligent Routing System**: This is the central orchestrator of the OS. It analyzes incoming requests and routes them to the appropriate specialized agent or system. This ensures that tasks are handled by the most qualified agent, without wasting resources.
*   **Specialized Execution Systems (Agents)**: These are individual components, or "agents," that are experts in a specific domain. Examples include the `RepoIntakeAgent` for analyzing code repositories and the `QAAgent` for handling question-answering tasks. Each agent operates independently, allowing for parallel execution and scalability.
*   **Secure Credential Warehouse**: A centralized and secure vault for managing API keys, tokens, and other sensitive credentials. This allows agents to access the resources they need without exposing sensitive information in the codebase.
*   -**Human-in-the-Loop-Alerts**: The system is designed to automate as much as possible, but it also includes checkpoints for human approval. This ensures that critical decisions are reviewed by a human before proceeding.

## Features

*   **Extensible Agent Architecture**: Easily add new agents with specialized skills.
*   **Parallel Execution**: Agents can run in parallel, significantly speeding up complex workflows.
*   **Event-Driven Communication**: A flexible and scalable architecture based on asynchronous messaging.
*   **Analytics and Monitoring**: Integrated analytics with PostHog to track agent performance and system metrics.
*   **Secure by Design**: A secure credential warehouse and other security best practices are built into the architecture.

## System Architecture

The 371 Minds OS uses a microservices-based architecture where each agent is an independent, containerized service. Communication is handled through an event-driven system using message queues and REST APIs.

The high-level architecture is represented by the following JSON structure:

```json
{
    "371_minds_os": {
        "user_interface": {
            "desktop_application": {
                "technology": "Electron.js",
                "purpose": "Provides an IDE-like experience for interacting with the OS."
            }
        },
        "core_orchestration": {
            "intelligent_routing_system": {
                "description": "Analyzes submissions and delegates tasks to specialist agents."
            }
        },
        "specialized_agents": {
            "repo_intake_agent": { "purpose": "Clones and analyzes Git repositories." },
            "qa_agent": { "purpose": "Answers questions using the Adaptive LLM Router." },
            "code_generation_agent": { "status": "In Development" },
            "deployment_agent": { "status": "In Development" }
        },
        "supporting_services": {
            "adaptive_llm_router": {
                "description": "Dynamically selects LLMs and manages costs."
            },
            "secure_credential_warehouse": {
                "description": "Manages API keys and other secrets."
            },
            "analytics": {
                "technology": "PostHog",
                "purpose": "Tracks system performance and agent execution."
            }
        },
        "architectural_patterns": [
            "Microservices-based",
            "Event-driven Communication",
            "Asynchronous Task Processing"
        ]
    }
}
```

## Getting Started

Follow these steps to get the 371 Minds OS up and running on your local machine.

### Prerequisites

*   Python 3.7+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/os-engine-source.git
    cd os-engine-source
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The system uses PostHog for analytics. You will need to set your PostHog API key as an environment variable.

```bash
export POSTHOG_API_KEY='your_key'
```

If you don't have a PostHog account, you can still run the system using a demo key, but no events will be tracked.

### Running the Quick Start

To see the system in action, run the `repo_intake_quick_start.py` script:

```bash
python repo_intake_quick_start.py
```

This script demonstrates the full, unified architecture by sending a high-level task to the `IntelligentRoutingSystem`, which then delegates it to the appropriate specialist agent.

## Usage

The following is a basic example of how to use the `IntelligentRoutingSystem` and a specialist agent. This example is adapted from the `repo_intake_quick_start.py` script.

```python
import asyncio
import os
from router_agent import IntelligentRoutingSystem
from repo_intake_agent import RepoIntakeAgent
from analytics_371 import Analytics371
from base_agent import Task, AgentType

async def main():
    # 1. Initialize System Components
    analytics = Analytics371(os.getenv('POSTHOG_API_KEY', 'demo_key_12345'))
    router = IntelligentRoutingSystem()
    repo_intake_agent = RepoIntakeAgent(analytics_client=analytics)

    # 2. Register Agents with the Router
    router.register_agent(repo_intake_agent)

    # 3. Create and Process a Task
    # This is a high-level user request.
    user_submission = "Please analyze the repository at https://github.com/371-minds/os-engine-source"

    # We create a task for the INTELLIGENT_ROUTER. Its job is to break this down.
    initial_task = Task(
        id="quick_start_task_001",
        description="Top-level request to analyze a repository.",
        agent_type=AgentType.INTELLIGENT_ROUTER,
        payload={
            "submission": user_submission,
            "user_id": "quickstart_user"
        }
    )

    # The router processes the initial task and orchestrates the required sub-tasks.
    final_task_state = await router.execute_task(initial_task)

    # 4. Display Results
    print(f"Task execution completed with status: {final_task_state.status.value}")
    if final_task_state.status.value == "completed":
        print("--- Router Orchestration Summary ---")
        print(final_task_state.result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Components

The 371 Minds OS is composed of several key components that work together to automate complex tasks.

### Intelligent Routing System

The `IntelligentRoutingSystem` (found in `router_agent.py`) is the brain of the OS. It acts as a central orchestrator that analyzes high-level user requests and delegates them to the appropriate specialist agents. Its key responsibilities include:
*   **Task Analysis**: Parsing user submissions to identify the required skills and agents.
*   **Orchestration**: Creating and managing sub-tasks for specialist agents. It can execute tasks sequentially or in parallel.
*   **Agent Registry**: Maintaining a registry of all available agents in the system.

### RepoIntakeAgent

The `RepoIntakeAgent` (found in `repo_intake_agent.py`) is a specialist agent responsible for fetching and analyzing source code from Git repositories. Its capabilities include:
*   Cloning public Git repositories.
*   Analyzing repository content to determine file counts, lines of code, and programming languages.
*   Extracting metadata such as the last commit hash.
*   Bundling the repository content for further processing by other agents.

### QAAgent

The `QAAgent` (found in `qa_agent.py`) is a specialist agent designed for question-answering tasks. It leverages the `Adaptive LLM Router` to select the most appropriate language model for a given query, balancing cost, quality, and confidentiality.

For more details on the specific components and their capabilities, please refer to the source files in this repository.

## Adaptive LLM Router

The `Adaptive LLM Router` (located in the `adaptive_llm_router` directory) is a sophisticated component for managing calls to large language models (LLMs). Instead of being tied to a single LLM provider, the router dynamically selects the best provider for a given task based on a set of policies.

Key features include:
*   **Dynamic Provider Selection**: Chooses the optimal LLM provider (e.g., OpenAI, Anthropic, a local model) based on metadata such as desired quality, confidentiality requirements, and budget constraints.
*   **Cost Management**: Tracks token usage and cost per request, helping to manage and enforce budgets.
*   **Centralized Usage Ledger**: Records all LLM interactions, providing a clear overview of usage and spending.
*   **Extensible Provider Registry**: Easily add new LLM providers by defining them in the `providers.json` file.

This component allows agents like the `QAAgent` to leverage LLMs without being tightly coupled to a specific implementation, making the system more flexible and cost-effective.

## Desktop Application

This repository includes an Electron-based desktop application that provides a rich user interface for the 371 Minds OS. It is designed to feel like a dedicated IDE for working with the agent system.

The application is architected as follows:
*   **Frontend**: An Electron.js application provides the user interface, which includes features like a text editor (`monaco-editor`) and a terminal (`xterm`).
*   **Backend**: The core Python-based agent system is packaged into a single, standalone executable using PyInstaller.
*   **Communication**: The Electron frontend launches the Python executable as a background process on startup. It then communicates with the backend via a local Flask web server.

This setup allows for a seamless user experience, combining the power of the Python backend with a modern, web-based frontend.

For detailed instructions on how to set up and run the desktop application, please refer to the **[Electron Integration Guide](electron/ELECTRON_GUIDE.md)**.
