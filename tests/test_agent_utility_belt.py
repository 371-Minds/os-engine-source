import pytest
from unittest.mock import Mock, patch
from repo_intake_agent import RepoIntakeAgent, RepositoryContext
from agent_utility_belt import AgentUtilityBelt
from mindscript_agent import LogicExtractorAgent
from base_agent import Task, AgentType

@pytest.fixture
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

def test_find_services_by_tag(mock_service_catalog):
    """Test that the AgentUtilityBelt can find services by tag."""
    belt = AgentUtilityBelt(service_catalog=mock_service_catalog)

    # Test finding services with the 'json' tag
    json_services = belt._find_services_by_tag("json")
    assert len(json_services) == 1
    assert json_services[0]["service"] == "ipinfo.io"

    # Test finding services with the 'curl' tag
    curl_services = belt._find_services_by_tag("curl")
    assert len(curl_services) == 3

    # Test finding a tag that doesn't exist
    non_existent_services = belt._find_services_by_tag("non-existent-tag")
    assert len(non_existent_services) == 0

@patch('requests.get')
def test_get_structured_yaml(mock_get):
    """Test that the RepoIntakeAgent can fetch and parse structured.yaml."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
by_category:
  - ip:
      l2.io:
        tags: [curl, plain]
"""
    mock_get.return_value = mock_response

    agent = RepoIntakeAgent()
    repo_url = "https://github.com/test/repo.git"
    data = agent._get_structured_yaml(repo_url)

    assert data is not None
    assert "by_category" in data
    assert len(data["by_category"]) == 1

def test_mindscript_agent_parsing():
    """Test that the LogicExtractorAgent can parse utility belt commands."""
    agent = LogicExtractorAgent()

    command = "find services with tag json"
    parse_result = agent.parse_command(command)

    assert parse_result.action == "search"
    assert parse_result.category == "utility_belt"
    assert parse_result.resource == "catalog_services"
    assert parse_result.parameters["tag"] == "json"

@pytest.mark.asyncio
async def test_mindscript_agent_process_task():
    """Test the full processing of a utility belt command."""
    agent = LogicExtractorAgent()
    task = Task(
        id="test_task",
        description="Find services with tag json",
        agent_type=AgentType.BUSINESS_LOGIC,
        payload={"command": "find services with tag json"}
    )

    result = await agent.process_task(task)

    structured_payload = result["structured_payload"]
    assert structured_payload["action"] == "find_services_by_tag"
    assert structured_payload["category"] == "utility_belt"
    assert structured_payload["resource"] == "catalog_services"
    assert structured_payload["parameters"]["tag"] == "json"
