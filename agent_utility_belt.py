"""
371 Minds Operating System - Agent Utility Belt
"""

from typing import Dict, List, Optional, Any

from base_agent import BaseAgent, AgentType, Task, AgentCapability

class AgentUtilityBelt(BaseAgent):
    """
    An agent that provides utility functions based on a structured catalog of services.
    """

    def __init__(self, agent_id: str = "agent_utility_belt_001", service_catalog: Optional[Dict[str, Any]] = None):
        capabilities = [
            AgentCapability(
                name="find_services_by_tag",
                description="Find services in the catalog that match a given tag."
            ),
            AgentCapability(
                name="get_repository_details",
                description="Get the repository URL for a given service."
            )
        ]
        super().__init__(agent_id, AgentType.AGENT_UTILITY_BELT, capabilities)
        self.service_catalog = service_catalog if service_catalog else {"by_category": []}

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """
        Process tasks related to the service catalog.
        """
        payload = task.payload
        action = payload.get("action")

        if action == "find_services_by_tag":
            tag = payload.get("tag")
            if not tag:
                raise ValueError("'tag' not found in task payload for find_services_by_tag action.")

            services = self._find_services_by_tag(tag)
            return {"services": services}

        if action == "get_repository_details":
            service_name = payload.get("service_name")
            if not service_name:
                raise ValueError("'service_name' not found in task payload for get_repository_details action.")

            repo_details = self._get_repository_details(service_name)
            return {"repository_details": repo_details}

        raise NotImplementedError(f"Action '{action}' is not supported by the Agent Utility Belt.")

    def _find_services_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Finds all services that have a specific tag.
        """
        found_services = []
        for category in self.service_catalog.get("by_category", []):
            for category_name, services in category.items():
                for service_name, service_details in services.items():
                    if tag in service_details.get("tags", []):
                        found_services.append({
                            "category": category_name,
                            "service": service_name,
                            "details": service_details
                        })
        return found_services

    def _get_repository_details(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Finds the repository URL for a given service.
        In the future, this could be extended to use the github-mcp-server to fetch more details.
        """
        for category in self.service_catalog.get("by_category", []):
            for category_name, services in category.items():
                if service_name in services:
                    service_details = services[service_name]
                    if "repository" in service_details:
                        return {
                            "service": service_name,
                            "repository_url": service_details["repository"]
                        }
        return None

    async def health_check(self) -> bool:
        """
        Health check for the Agent Utility Belt.
        """
        return True

    def update_catalog(self, new_catalog: Dict[str, Any]):
        """
        Updates the service catalog for the agent.
        """
        self.service_catalog = new_catalog
        self.logger.info("Service catalog updated.")
