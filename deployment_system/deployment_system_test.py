import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Mock the external dependencies
mock_credential_warehouse = MagicMock()

modules_to_mock = {
    "credential_warehouse_agent": mock_credential_warehouse,
    "digitalocean": MagicMock(),
    "boto3": MagicMock(),
    "CloudFlare": MagicMock(),
    "posthog": MagicMock(),
    "subprocess": MagicMock(),
}

patcher = patch.dict("sys.modules", modules_to_mock)
patcher.start()

# Now we can import the class we want to test
from deployment_system import DeploymentAgent
from base_agent import DeploymentRequest, Task, DeploymentContext, TaskStatus, AgentType

def tearDownModule():
    """Tear down the module-level patches."""
    patcher.stop()

class TestDeploymentAgent(unittest.TestCase):

    def setUp(self):
        """Set up the test case."""
        for mock_module in modules_to_mock.values():
            mock_module.reset_mock()

        self.agent = DeploymentAgent()
        self.agent.cred_store.get_secret = AsyncMock(return_value="dummy_secret")
        # also mock the tracking methods to avoid posthog calls
        self.agent._track_event = MagicMock()
        self.agent._track_final_event = MagicMock()


    @patch('deployment_system.DeploymentAgent.finalize')
    @patch('deployment_system.DeploymentAgent.configure_dns_and_ssl', new_callable=AsyncMock)
    @patch('deployment_system.DeploymentAgent.provision_and_deploy', new_callable=AsyncMock)
    @patch('deployment_system.DeploymentAgent.clone_and_build', new_callable=AsyncMock)
    def test_digitalocean_deployment_with_ssl(self, mock_clone_build, mock_provision_deploy, mock_configure_ssl, mock_finalize):
        """Test a full deployment to DigitalOcean with SSL."""
        print("--- Running Test: DigitalOcean Deployment with SSL ---")

        # --- Arrange ---
        def finalize_side_effect(request, ctx):
            ctx.status = "success"
            ctx.end_time = ctx.start_time + 120 # mock 2 minute duration
        mock_finalize.side_effect = finalize_side_effect

        request = DeploymentRequest(
            task_id="task123",
            repo_url="https://github.com/test/repo.git",
            repo_branch="main",
            container_registry="test_registry",
            cloud_provider="digitalocean",
            infra_spec={"size": "s-2vcpu-2gb", "region": "sfo3", "replicas": 2},
            domain="test.example.com",
            ssl=True,
            target_environment="production",
            build_commands=[],
            environment_vars={}
        )
        task = Task(id="task123", description="test task", agent_type=AgentType.DEPLOYMENT, payload=vars(request))

        # --- Act ---
        result = asyncio.run(self.agent.process_task(task))

        # --- Assert ---
        mock_clone_build.assert_called_once()
        mock_provision_deploy.assert_called_once()
        mock_configure_ssl.assert_called_once()
        mock_finalize.assert_called_once()

        # Check that events were tracked
        self.agent._track_event.assert_any_call("task123", TaskStatus.PROVISIONING)
        self.agent._track_event.assert_any_call("task123", TaskStatus.DEPLOYING)
        self.agent._track_event.assert_any_call("task123", TaskStatus.CONFIGURING)
        self.agent._track_event.assert_any_call("task123", TaskStatus.FINALIZING)

        print("Result:", result)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['domain'], 'test.example.com')
        self.assertAlmostEqual(result['duration_seconds'], 120, delta=1)
        print("--- Test Finished: DigitalOcean Deployment with SSL ---\n")


    @patch('deployment_system.DeploymentAgent.finalize')
    @patch('deployment_system.DeploymentAgent.configure_dns_and_ssl', new_callable=AsyncMock)
    @patch('deployment_system.DeploymentAgent.provision_and_deploy', new_callable=AsyncMock)
    @patch('deployment_system.DeploymentAgent.clone_and_build', new_callable=AsyncMock)
    def test_aws_deployment_no_ssl(self, mock_clone_build, mock_provision_deploy, mock_configure_ssl, mock_finalize):
        """Test a deployment to AWS without SSL."""
        print("--- Running Test: AWS Deployment without SSL ---")

        # --- Arrange ---
        def finalize_side_effect(request, ctx):
            ctx.status = "success"
            ctx.end_time = ctx.start_time + 180 # mock 3 minute duration
        mock_finalize.side_effect = finalize_side_effect

        request = DeploymentRequest(
            task_id="task456",
            repo_url="https://github.com/test/aws_repo.git",
            repo_branch="develop",
            container_registry="aws_ecr",
            cloud_provider="aws",
            infra_spec={"cluster": "test-cluster"},
            domain="",
            ssl=False,
            target_environment="staging",
            build_commands=[],
            environment_vars={}
        )
        task = Task(id="task456", description="test task", agent_type=AgentType.DEPLOYMENT, payload=vars(request))

        # --- Act ---
        result = asyncio.run(self.agent.process_task(task))

        # --- Assert ---
        mock_clone_build.assert_called_once()
        mock_provision_deploy.assert_called_once()
        # Since ssl=False, configure_dns_and_ssl should still be called, but it should return early.
        mock_configure_ssl.assert_called_once()
        mock_finalize.assert_called_once()

        print("Result:", result)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['domain'], '')
        self.assertAlmostEqual(result['duration_seconds'], 180, delta=1)
        print("--- Test Finished: AWS Deployment without SSL ---\n")


def main():
    """Main function to run the tests."""
    unittest.main()

if __name__ == "__main__":
    main()
