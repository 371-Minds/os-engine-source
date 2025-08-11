"""
Mock BrokkAi Client for simulating semantic code analysis.

This module provides a mock client that mimics the behavior of the BrokkAi
semantic analysis engine. It is designed to be used for development and
testing purposes when the real BrokkAi service is not available.
"""

import json
from typing import Dict, Any

class BrokkAiClient:
    """
    A mock client that simulates the BrokkAi semantic analysis API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the mock BrokkAi client.

        Args:
            api_key: The API key for the BrokkAi service (not used in mock).
        """
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key

    def analyze_code(self, code_snippet: str) -> Dict[str, Any]:
        """
        Simulates the analysis of a code snippet.

        Args:
            code_snippet: A string containing the code to be analyzed.

        Returns:
            A dictionary with the simulated analysis results.
        """
        # In a real implementation, this would make an API call to BrokkAi.
        # For this mock, we perform a basic analysis of the code snippet.
        import re

        functions = []
        classes = []
        libraries = []

        # Find imported libraries
        for line in code_snippet.splitlines():
            line = line.strip()
            if line.startswith("import"):
                # e.g., "import os, sys"
                libs = line.split("import")[1].strip()
                libraries.extend([lib.strip() for lib in libs.split(',')])
            elif line.startswith("from"):
                # e.g., "from os import path"
                lib = line.split("import")[0].split("from")[1].strip()
                libraries.append(lib)

        # Find function definitions
        func_matches = re.findall(r"def\s+([a-zA-Z0-9_]+)", code_snippet)
        for func_name in func_matches:
            functions.append({
                "name": func_name,
                "signature": f"def {func_name}(...)",
                "dependencies": []
            })

        # Find class definitions
        class_matches = re.findall(r"class\s+([a-zA-Z0-9_]+)", code_snippet)
        for class_name in class_matches:
            classes.append({
                "name": class_name,
                "methods": [] # simplified for now
            })

        mock_analysis = {
            "semantic_analysis": {
                "language": "python",
                "libraries": sorted(list(set([lib for lib in libraries if lib]))),
                "functions": functions,
                "classes": classes,
            },
            "confidence_score": 0.95,
        }
        return mock_analysis
