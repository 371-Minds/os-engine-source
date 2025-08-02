import os
import sys
import asyncio
import json
from pathlib import Path
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

# Add current directory to path for local imports
sys.path.append(str(Path(__file__).parent))

try:
    # Core system components
    from router_agent import IntelligentRoutingSystem
    from repo_intake_agent import RepoIntakeAgent
    from analytics_371 import Analytics371
    from base_agent import Task, AgentType
except ImportError as e:
    print(f"Error: Failed to import necessary modules. {e}")
    print("Please ensure all required agent files and their dependencies are present in the same directory.")
    sys.exit(1)

# --- System Initialization ---
# This section sets up the core components of the 371 Minds OS.
# In a production environment, this might be handled more dynamically.
print("Initializing 371 Minds OS components...")
try:
    # Initialize Analytics (using a demo key if not set)
    api_key = os.getenv('POSTHOG_API_KEY', 'demo_key_12345')
    analytics = Analytics371(api_key)

    # Initialize the main router
    router = IntelligentRoutingSystem()

    # Initialize and register specialist agents
    repo_intake_agent = RepoIntakeAgent(analytics_client=analytics)
    router.register_agent(repo_intake_agent)

    print("System components initialized successfully.")
    print("Registered Agents:", router.get_system_status().get("registered_agents"))
except Exception as e:
    print(f"Critical Error during system initialization: {e}")
    sys.exit(1)


# --- Flask Web Server ---
app = Flask(__name__)

@app.route('/api/execute', methods=['POST'])
def execute_task():
    """
    API endpoint to receive and process a task.
    Expects a JSON payload with a 'submission' field.
    e.g., {"submission": "Analyze the repository at https://github.com/user/repo"}
    """
    # Basic input validation
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 400
    
    data = request.get_json()
    submission_text = data.get('submission')

    if not submission_text:
        return jsonify({"error": "Invalid payload: 'submission' field is required"}), 400

    print(f"Received task via API: '{submission_text}'")

    try:
        # Create the initial task for the router
        # The user_id could be passed from the Electron app in a real scenario
        initial_task = Task(
            id="api_task_001",
            description="Top-level API request",
            agent_type=AgentType.INTELLIGENT_ROUTER,
            payload={
                "submission": submission_text,
                "user_id": "electron_user"
            }
        )

        # The agent system uses asyncio, so we run the async execute_task
        # function in a new event loop for this request.
        final_task_state = asyncio.run(router.execute_task(initial_task))
        
        # We need to serialize the result to be JSON-friendly
        # The Task object itself is not directly serializable.
        if final_task_state.status.value == "completed":
            response_data = {
                "status": "success",
                "taskId": final_task_state.id,
                "result": final_task_state.result
            }
            return jsonify(response_data), 200
        else:
            response_data = {
                "status": "error",
                "taskId": final_task_state.id,
                "error": final_task_state.result.get('error', 'An unknown error occurred')
            }
            return jsonify(response_data), 500

    except Exception as e:
        print(f"An error occurred during task execution: {e}")
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    A simple health check endpoint to confirm the server is running.
    """
    return jsonify({"status": "ok", "timestamp": os.path.getmtime(__file__)}), 200

if __name__ == '__main__':
    # Running the app on 0.0.0.0 makes it accessible from the network,
    # which is useful for development and containerization.
    # For a desktop app, 127.0.0.1 is often preferred for security.
    app.run(host='127.0.0.1', port=5000, debug=True)
