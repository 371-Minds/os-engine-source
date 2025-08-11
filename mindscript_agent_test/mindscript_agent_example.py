import asyncio
import json
import sys
import os
from uuid import uuid4

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mindscript_agent import LogicExtractorAgent
from base_agent import Task, AgentType, TaskStatus

async def main():
    """
    An extensive test suite for the LogicExtractorAgent.
    """
    agent = LogicExtractorAgent()

    test_commands = [
        # Standard cases
        'Can you please store the latest "customer feedback" document?',
        'Search for the "Q3 financial report" in our knowledge base.',
        'Sync the "marketing campaign" assets with the team.',
        'Update the "user profile" for customer ID "12345".',
        'Analyze the "sales data" from the last quarter.',
        'Extract the key findings from the "research paper".',
        'Deploy the new "authentication service" to production.',
        'Scale the "web server" to handle more traffic.',
        'Monitor the "database performance" for any issues.',
        'Activate the "new feature flag" for beta testers.',
        'Generate a "weekly summary" of the project progress.',
        'Track the "user engagement" metrics for the new feature.',

        # Development & Infrastructure
        'Configure the "staging environment" for the new microservice.',
        'Fork the "main repository" to start working on a new feature.',
        'Integrate the "payment gateway" with our e-commerce site.',
        'Customize the "UI theme" to match our new branding.',
        'Test the "API endpoints" for the new mobile application.',
        'Compile the "source code" into a distributable package.',
        'Debug the "login issue" that users are reporting.',
        'Optimize the "database queries" to improve performance.',

        # Business Operations
        'Modernize the "legacy inventory system" by migrating to a new platform.',
        'Process the "incoming invoices" and categorize them.',
        'Coordinate the "product launch event" with all stakeholders.',
        'Automate the "customer onboarding" process.',
        'Schedule a "meeting" with the marketing team for next week.',
        'Execute the "monthly sales report" generation task.',
        'Report the "key performance indicators" to the management.',
        'Audit the "financial records" for the last fiscal year.',

        # AI & Agent Actions
        'Train the "recommendation model" on the new user data.',
        'Infer the "customer sentiment" from the latest reviews.',
        'Classify the "support tickets" based on their content.',
        'Transform the "raw data" into a structured format.',
        'Embed the "product descriptions" for semantic search.',
        'Retrieve the "user preferences" from the database.',

        # Security & Authentication
        'Authenticate the "user" with their credentials.',
        'Secure the "API keys" by storing them in a vault.',
        'Rotate the "database passwords" as per the security policy.',
        'Backup the "customer data" to a secure location.',

        # Communication & Collaboration
        'Notify the "development team" about the critical bug.',
        'Communicate the "quarterly results" to the entire company.',
        'Collaborate with the "design team" on the new UI mockups.',
        'Present the "project proposal" to the stakeholders.',

        # Data & Analytics
        'Visualize the "user growth" over the last year.',
        'Aggregate the "log files" to identify common errors.',
        'Filter the "customer list" to find users in a specific region.',
        'Compare the "performance" of the two marketing campaigns.',

        # Deployment & Operations
        'Provision a "new server" for the upcoming project.',
        'Restart the "web server" to apply the new configuration.',
        'Rollback the "latest deployment" due to a critical issue.',
        'Maintain the "production environment" by applying security patches.',

        # Edge cases
        'This command has no matching action or resource.',
        'find services in utility belt with tag "beta"',
        'search for services with tag "production-ready"',
        'Show me the money! And the forecast for revenue.',
        'Can you find the business model for our "new venture"?',
        'What is the plan for go-to-market?',
        'I need to see the latest credentials for cyberark',
        'Get the "MERN stack" documentation.',
        'Analyze the "COBOL copybooks" for the "mainframe modernization" project.',
        'Tell me about the "intelligent router" agent.'
    ]

    print("--- Starting MindScript Agent Benchmark ---")
    print(f"Testing {len(test_commands)} commands...\n")

    for i, command in enumerate(test_commands):
        task_id = str(uuid4())
        task = Task(
            id=task_id,
            description=f"Test task {i+1}",
            agent_type=AgentType.BUSINESS_LOGIC,
            payload={'command': command},
            status=TaskStatus.PENDING
        )

        print(f"--- Test Case #{i+1} ---")
        print(f"Command: {command}")

        result = await agent.process_task(task)

        print("Structured Payload:")
        print(json.dumps(result['structured_payload'], indent=2))
        print("\nBrokkAi Analysis:")
        print(json.dumps(result['brokkai_analysis'], indent=2))
        print("\nToken Savings:")
        print(f"  Original: {result['original_tokens']}")
        print(f"  Structured: {result['structured_tokens']}")
        print(f"  Saved: {result['tokens_saved']}")
        print("-" * (len(f"--- Test Case #{i+1} ---")))
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
