"""
Manages the catalog of available LLM providers.
"""

import json
from pathlib import Path
from typing import List, Optional

from .data_models import LLMProvider

class ProviderRegistry:
    """
    Loads and provides access to the list of LLM providers from a JSON file.
    """
    def __init__(self, providers_file: Path):
        self.providers_file = providers_file
        self.providers: List[LLMProvider] = self._load_providers()

    def _load_providers(self) -> List[LLMProvider]:
        """Loads provider data from the JSON file."""
        if not self.providers_file.exists():
            return []
        with open(self.providers_file, 'r') as f:
            data = json.load(f)
        return [LLMProvider(**p) for p in data]

    def get_provider(self, name: str, model: str) -> Optional[LLMProvider]:
        """
        Retrieves a specific provider by name and model.
        """
        for provider in self.providers:
            if provider.name == name and provider.model == model:
                return provider
        return None

    def list_providers(self) -> List[LLMProvider]:
        """
        Returns the list of all available providers.
        """
        return self.providers

# Initialize a default registry instance
providers_path = Path(__file__).parent / "providers.json"
provider_registry = ProviderRegistry(providers_path)
