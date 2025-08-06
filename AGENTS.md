# 371 Minds OS - Agent Development Guide

This guide is intended for AI developers working on the 371 Minds OS. It provides an overview of the system architecture and instructions for running, testing, and extending the system.

## System Architecture

The 371 Minds OS is a hybrid system that combines a powerful Python-based agent framework with a modern web-based UI built in Electron and a Convex backend.

The system consists of three main parts:

1.  **Python Agent System**: A collection of specialized AI agents responsible for tasks like code analysis, question answering, and more. The agents are built on a common `base_agent` and can be orchestrated by a `router_agent`.
2.  **Convex Backend**: A serverless backend that provides a database and serverless functions. The Convex backend acts as the central hub for communication between the Electron app and the Python agents.
3.  **Electron UI**: A desktop application that provides a user interface for interacting with the system. The Electron app communicates with the Convex backend to send tasks and receive results.

### Communication Flow

1.  The user interacts with the Electron UI, for example, by asking a question.
2.  The Electron app sends a mutation to the Convex backend (e.g., `api.qa.ask`).
3.  The Convex backend runs an action that calls a Python agent via an HTTP request.
4.  The Python agent system, running as a separate Flask server (`convex_api.py`), receives the request, processes it, and returns the result.
5.  The Convex action receives the result and stores it in the database.
6.  The Electron app, which is subscribed to the Convex query, receives the updated data and displays it to the user.

## Running the System

To run the full system for development, you will need to start three separate processes in three separate terminals:

1.  **Start the Python Agent Server:**
    ```bash
    python convex_api.py
    ```
    This will start a Flask server on `http://localhost:8000` that listens for requests from the Convex backend.

2.  **Start the Convex Development Server:**
    ```bash
    npx convex dev
    ```
    This will start the Convex development server and sync your backend functions. You will be prompted to log in if you haven't already.

3.  **Start the Electron Application:**
    ```bash
    cd electron
    npm start
    ```
    This will start the Electron desktop application.

## Extending the System

### Adding a New Agent

1.  Create a new Python file for your agent (e.g., `my_new_agent.py`).
2.  Your agent should inherit from `BaseAgent` and implement the `execute_task` method.
3.  Register your new agent in `convex_api.py` so that it can be called from the Convex backend.
4.  Add a new API endpoint in `convex_api.py` to handle requests for your new agent.
5.  Add new functions to the Convex backend to call your new agent's API endpoint.
6.  Update the Electron app to call the new Convex functions.

### Modifying an Existing Agent

1.  Open the agent's Python file (e.g., `qa_agent.py`).
2.  Make your changes to the agent's logic.
3.  Restart the Python agent server to apply the changes.
