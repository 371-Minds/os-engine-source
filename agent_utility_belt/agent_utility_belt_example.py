import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_utility_belt import AgentUtilityBelt
from base_agent import Task

def mock_service_catalog():
    """A mock service catalog for testing."""
    return {
        "by_category": [
            {
                "ip": {
                    "l2.io": {"tags": ["curl", "plain"]},
                    "echoip.de": {"tags": ["curl", "plain"]},
                }
            },
            {
                "geo": {
                    "ipinfo.io": {"tags": ["curl", "json"]},
                }
            }
        ]
    }

async def main():
    """Main function to run the example."""
    print("Agent Utility Belt Example")
    print("==========================")

    # Initialize the AgentUtilityBelt with a mock service catalog
    service_catalog = mock_service_catalog()
    belt = AgentUtilityBelt(service_catalog=service_catalog)
    print("Initialized AgentUtilityBelt with mock service catalog.")
    print(f"Service Catalog: {service_catalog}")
    print("")

    # Test Case 1: Find services by tag 'json'
    print("Test Case 1: Find services by tag 'json'")
    task_payload_1 = {"action": "find_services_by_tag", "tag": "json"}
    task_1 = Task(id="1", description="Find services by tag 'json'", agent_type=belt.agent_type, payload=task_payload_1)
    result_1 = await belt.process_task(task_1)
    print(f"Task: {task_payload_1}")
    print(f"Result: {result_1}")
    print("")

    # Test Case 2: Find services by tag 'curl'
    print("Test Case 2: Find services by tag 'curl'")
    task_payload_2 = {"action": "find_services_by_tag", "tag": "curl"}
    task_2 = Task(id="2", description="Find services by tag 'curl'", agent_type=belt.agent_type, payload=task_payload_2)
    result_2 = await belt.process_task(task_2)
    print(f"Task: {task_payload_2}")
    print(f"Result: {result_2}")
    print("")

    # Test Case 3: Get repository details for 'ipinfo.io'
    print("Test Case 3: Get repository details for 'ipinfo.io'")
    service_catalog_with_repo = mock_service_catalog()
    service_catalog_with_repo["by_category"][1]["geo"]["ipinfo.io"]["repository"] = "https://github.com/ipinfo/ipinfo"
    belt.update_catalog(service_catalog_with_repo)
    task_payload_3 = {"action": "get_repository_details", "service_name": "ipinfo.io"}
    task_3 = Task(id="3", description="Get repository details for 'ipinfo.io'", agent_type=belt.agent_type, payload=task_payload_3)
    result_3 = await belt.process_task(task_3)
    print(f"Task: {task_payload_3}")
    print(f"Result: {result_3}")
    print("")

    # Test Case 4: Try to find a service that doesn't exist
    print("Test Case 4: Try to find a service that doesn't exist")
    task_payload_4 = {"action": "get_repository_details", "service_name": "non_existent_service"}
    task_4 = Task(id="4", description="Try to find a service that doesn't exist", agent_type=belt.agent_type, payload=task_payload_4)
    result_4 = await belt.process_task(task_4)
    print(f"Task: {task_payload_4}")
    print(f"Result: {result_4}")
    print("")

if __name__ == "__main__":
    asyncio.run(main())
