
# Complete Integration Example
# Shows how to wire Repository Intake Engine with PostHog analytics

from repository_intake_engine import IntelligentRoutingSystem, RepositoryIntakeEngine
from analytics_371 import Analytics371, TrackExecution
import uuid

def main():
    """Complete example of repository processing with analytics"""

    # Initialize analytics (you'd use your real PostHog API key)
    analytics = Analytics371("ph_your_api_key_here")

    # Initialize routing system with analytics
    router = IntelligentRoutingSystem(posthog_client=analytics.client)

    # Example request
    request = "Analyze the repository at https://github.com/microsoft/vscode and modernize to React"
    user_id = "user_123"

    print(f"Processing request: {request}")

    # Route and process the request
    result = router.route_request(request, user_id)

    print(f"\n--- Results ---")
    print(f"Task ID: {result.task_id}")
    print(f"Agent Type: {result.agent_type}")
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")

    if result.metadata:
        print(f"Metadata: {result.metadata}")

    if result.error:
        print(f"Error: {result.error}")

    # The analytics are automatically tracked within the routing system
    print("\n--- Analytics Tracked ---")
    print("✅ request_routed event")
    print("✅ repository_intake_started event")
    print("✅ repository_intake_completed event") 
    print("✅ agent_execution event")

    return result

if __name__ == "__main__":
    main()
