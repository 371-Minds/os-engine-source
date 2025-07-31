# 371 Minds OS

The `os-engine-source` repository contains the core logic for the **371 Minds Operating System**, a sophisticated, agent-based system designed to automate complex software development and marketing workflows.

## Overview

371 Minds OS is a framework for orchestrating specialized AI agents. It can analyze and process user requests, activate the appropriate systems, and manage their parallel execution. The architecture is designed for scalability, efficiency, and seamless human-computer collaboration, ensuring that human intervention is only requested for critical decisions.

## Core Architectural Principles

The system is built on a set of powerful architectural patterns:

*   **Intelligent Routing System**: A central orchestrator that analyzes incoming requests and routes them to the appropriate specialized agent or system. This eliminates wasted resources on unnecessary agent interactions.
*   **Specialized Execution Systems**: A suite of independent, containerized agents, each an expert in a specific domain (e.g., code generation, marketing, business logic).
*   **Secure Credential Warehouse**: A centralized and secure vault for managing API keys, tokens, and other sensitive credentials.
*   **Human-in-the-Loop Alerts**: A smart notification system that prompts for human input only at critical decision points, such as approvals or final reviews.
*   **Event-Driven Communication**: Asynchronous, message-based communication between components, allowing for scalable and resilient orchestration.

## Key Features

*   **Efficiency**: Avoids token waste and coordination overhead by activating only the necessary agents.
*   **Parallel Execution**: Capable of running multiple agents concurrently to accelerate complex workflows.
*   **Scalability**: Infinitely scalable by design; new capabilities can be added by simply creating new specialized agents.
*   **Human-in-the-Loop**: Integrates human oversight for crucial decisions without micromanagement.

## System Components

The OS is composed of several core components and specialized systems.

### Core Components

*   **Intelligent Routing System**: The brain of the operation. It parses requests and orchestrates the workflow.
*   **Secure Credential Warehouse**: Manages access to external services like GitHub, AWS, and social media platforms.

### Specialized Execution Systems (Examples)

#### 1. Repository Intake Engine

This system is responsible for ingesting and analyzing code repositories.

*   **Capabilities**:
    *   Clones and bundles Git repositories.
    *   Performs language detection, complexity analysis, and security scanning.
    *   Extracts dependencies and other metadata.
*   **Analytics**: Integrates with PostHog to provide detailed analytics on repository processing, execution times, and quality metrics.

#### 2. Integrated Content & Marketing Automation System

This system turns any 371 Minds agent into its own "CMO" (Chief Marketing Officer).

*   **Capabilities**:
    *   **Content Generation**: Generates on-brand copy and creative content.
    *   **Email Marketing**: Manages segmentation, A/B testing, and personalized email campaigns.
    *   **Social Media Management**: Optimizes and schedules posts for various platforms.
    *   **Analytics & Optimization**: Learns from engagement data to automatically optimize future campaigns.

## Getting Started

A quick start script is provided to test the basic functionality of the Repository Intake Engine.

### 1. Prerequisites

The project has several Python dependencies. While a `requirements.txt` file is not checked in, the necessary dependencies are listed in `repo_intake_build_guide.py`. You can install them using pip:

```bash
pip install posthog gitpython tree-sitter
```
*(Note: A complete list of dependencies for development and analysis can be found in the `repo_intake_build_guide.py` file.)*

### 2. Configuration

The system uses PostHog for analytics. You need to set your PostHog API key as an environment variable.

```bash
export POSTHOG_API_KEY='your_key_here'
```

If this is not set, the system will run with a demo key.

### 3. Run the Quick Start Script

Execute the `quick_start.py` script to see the Intelligent Routing System in action.

```bash
python quick_start.py
```

You should see output showing the system processing several test requests and routing them to the appropriate agent.

```
🚀 371 Minds OS - Repository Intake Engine
==================================================
⚠️  Using demo PostHog API key. Set POSTHOG_API_KEY environment variable for real tracking.

🔧 Initializing system...
✅ System initialized

📊 Testing repository analysis...

1. Processing: Analyze the repository at https://github.com/microsoft/vscode
   ✅ Status: COMPLETED
   ⏱️  Execution time: 0.00s
   🤖 Agent: REPOSITORY_INTAKE
   📝 Metadata: {'url': 'https://github.com/microsoft/vscode'}

...
```

This README provides a comprehensive overview of the 371 Minds OS. For more detailed information on specific components, please refer to the corresponding source files and documentation within this repository.
