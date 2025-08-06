from flask import Flask, request, jsonify
import sys
from pathlib import Path

# Add current directory to path for local imports
sys.path.append(str(Path(__file__).parent))

from qa_agent import QAAgent
from analytics_371 import Analytics371

app = Flask(__name__)

# Initialize the QA Agent
analytics = Analytics371()
qa_agent = QAAgent(analytics_client=analytics)

@app.route('/api/agent', methods=['POST'])
def handle_agent_request():
    data = request.get_json()
    task = data.get('task')

    if not task:
        return jsonify({"error": "No task provided"}), 400

    # This is where we call the QA agent.
    # The QAAgent expects a Task object.
    from base_agent import Task, AgentType
    import asyncio

    task_obj = Task(
        id="convex_task_001",
        description="Question from Convex",
        agent_type=AgentType.QA_AGENT,
        payload={"question": task}
    )

    # The answer_question method is async, so we need to run it in an event loop.
    result = asyncio.run(qa_agent.answer_question(task_obj))

    return jsonify({"result": result.result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
