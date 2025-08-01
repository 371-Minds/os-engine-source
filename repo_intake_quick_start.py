#!/usr/bin/env python3
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
    from repository_intake_engine import IntelligentRoutingSystem, Analytics371
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
    print("\n🔧 Initializing system...")
    analytics = Analytics371(api_key)
    router = IntelligentRoutingSystem(posthog_client=analytics.client)
    print("✅ System initialized")

    # Test repository analysis
    print("\n📊 Testing repository analysis...")
    test_requests = [
        "Analyze the repository at https://github.com/microsoft/vscode",
        "Modernize the legacy COBOL code to React",
        "Extract the API endpoints from https://github.com/fastapi/fastapi"
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. Processing: {request}")

        try:
            result = router.route_request(request, user_id=f"test_user_{i}")

            print(f"   ✅ Status: {result.status}")
            print(f"   ⏱️  Execution time: {result.execution_time:.2f}s")
            print(f"   🤖 Agent: {result.agent_type}")

            if result.metadata:
                print(f"   📝 Metadata: {result.metadata}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n📈 Analytics Events Tracked:")
    print("   - request_routed")
    print("   - repository_intake_started") 
    print("   - repository_intake_completed")
    print("   - agent_execution")

    print("\n✅ Quick start test completed!")
    print("\nNext steps:")
    print("1. Set your real PostHog API key: export POSTHOG_API_KEY='your_key'")
    print("2. Implement actual repository cloning and analysis")
    print("3. Add security scanning and complexity analysis")
    print("4. Set up monitoring dashboards in PostHog")

if __name__ == "__main__":
    main()
