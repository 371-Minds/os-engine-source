# 371 Minds OS

The 371 Minds OS is a framework for building and orchestrating specialized AI agents to automate complex software development, marketing, and business logic tasks. It is designed as a microservices-based, event-driven "operating system" that routes tasks to the most appropriate agent, enabling parallel execution and human-in-the-loop decision-making.

## Core Concepts

The OS is built around a few core concepts:

*   **Intelligent Routing System**: This is the central orchestrator of the OS. It analyzes incoming requests and routes them to the appropriate specialized agent or system. This ensures that tasks are handled by the most qualified agent, without wasting resources.
*   **Specialized Execution Systems (Agents)**: These are individual components, or "agents," that are experts in a specific domain. Examples include a `CodeGenerationSystem`, a `MarketingAssetSystem`, and a `BusinessLogicSystem`. Each agent operates independently, allowing for parallel execution and scalability.
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
        "core_components": {
            "intelligent_routing_system": {
                "description": "Central orchestrator that analyzes submissions and determines system activation"
            },
            "specialized_execution_systems": {
                "code_generation_system": { "purpose": "Ingests repo, applies tech stack wisdom" },
                "marketing_asset_system": { "purpose": "Brand consistency, asset optimization" },
                "business_logic_system": { "purpose": "PRD creation, requirement analysis" },
                "deployment_system": { "purpose": "Infrastructure, CI/CD pipeline" }
            },
            "secure_credential_warehouse": {
                "description": "CyberArk-style vault for secure credential management"
            },
            "human_in_the_loop_alerts": {
                "description": "Smart notification system for decision points"
            }
        },
        "architectural_patterns": {
            "microservices_based": {
                "description": "Each agent is an independent containerized service"
            },
            "event_driven_communication": {
                "description": "Asynchronous message-based communication"
            }
        }
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

To see the system in action, run the `quick_start.py` script:

```bash
python quick_start.py
```

This will simulate a few requests and show you how the `IntelligentRoutingSystem` processes them.

## Usage

The following is a basic example of how to use the `IntelligentRoutingSystem` from the `quick_start.py` script:

```python
import os
from repository_intake_engine import IntelligentRoutingSystem
from analytics_371 import Analytics371

# Initialize the system
api_key = os.getenv('POSTHOG_API_KEY', 'demo_key_12345')
analytics = Analytics371(api_key)
router = IntelligentRoutingSystem(posthog_client=analytics.client)

# Create a test request
request = "Analyze the repository at https://github.com/microsoft/vscode"

# Route the request
result = router.route_request(request, user_id="test_user_1")

# Print the result
print(f"Status: {result.status}")
print(f"Execution time: {result.execution_time:.2f}s")
print(f"Agent: {result.agent_type}")
if result.metadata:
    print(f"Metadata: {result.metadata}")
```

## Core Components

### Repository Intake Engine

The Repository Intake Engine is responsible for cloning, analyzing, and bundling Git repositories. It can detect languages, scan for security vulnerabilities, analyze code complexity, and extract dependencies.

### Content & Marketing Automation System

This system turns every agent into its own "CMO" (Chief Marketing Officer). It can:
*   Generate on-brand copy and creative content.
*   Launch personalized email sequences and social media posts.
*   Learn from engagement data to optimize future campaigns.
*   Route critical decisions to a human for approval.

For more details on the specific components and their capabilities, please refer to the source files in this repository.
