import sys
import os
import json

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brokkai_client import BrokkAiClient

def run_analysis_and_print(client, agent_name, code_snippet):
    """Runs the analysis and prints the results in a formatted way."""
    print(f"--- Analysis for {agent_name} ---")
    try:
        analysis = client.analyze_code(code_snippet)
        print(json.dumps(analysis, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
    print("\\n")

def main():
    """
    Main function to run a variety of submissions using mock agents.
    """
    api_key = "fake-api-key"  # The API key is not used in the mock client
    client = BrokkAiClient(api_key=api_key)

    # Agent 1: A simple function
    agent_1_code = """
def hello_world():
    print("Hello, World!")
"""
    run_analysis_and_print(client, "Agent 1: Simple Function", agent_1_code)

    # Agent 2: A class with a method
    agent_2_code = """
class Greeter:
    def greet(self, name):
        return f"Hello, {name}!"
"""
    run_analysis_and_print(client, "Agent 2: Class with a Method", agent_2_code)

    # Agent 3: A script with imports and a function
    agent_3_code = """
import os
import sys

def list_directory(path):
    return os.listdir(path)
"""
    run_analysis_and_print(client, "Agent 3: Script with Imports", agent_3_code)

    # Agent 4: A more complex class with dependencies
    agent_4_code = """
import logging

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.logger = logging.getLogger(__name__)

    def process(self):
        self.logger.info("Processing data...")
        # Complex processing logic here
        return {"status": "processed"}
"""
    run_analysis_and_print(client, "Agent 4: Complex Class", agent_4_code)

if __name__ == "__main__":
    main()
