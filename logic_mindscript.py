# Implement LogicExtractorAgent to parse MindScript commands into structured tasks

logic_extractor_code = '''
"""
371 Minds Operating System - Logic Extractor Agent (MindScript Interpreter)

Goal: Convert plain English / MindScript commands into structured task payloads to minimize LLM token usage.
"""

import re
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from base_agent import BaseAgent, AgentType, Task, TaskStatus, AgentCapability

# Simple token estimator (approx 4 chars per token assumption)
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

# Define action patterns and mapping
ACTION_PATTERNS: List[Tuple[str, str]] = [
    (r'\b(?:store|upload|save)\b', 'store'),
    (r'\b(?:search|find|lookup)\b', 'search'),
    (r'\b(?:sync|share|propagate)\b', 'sync'),
    (r'\b(?:update|refresh)\b', 'update'),
    (r'\b(?:analyze|analyse|analysis)\b', 'analyze'),
    (r'\b(?:extract)\b', 'extract'),
    (r'\b(?:deploy|launch|release)\b', 'deploy'),
    (r'\b(?:scale)\b', 'scale'),
    (r'\b(?:monitor|check|show)\b', 'monitor'),
    (r'\b(?:activate|start|enable)\b', 'activate'),
    (r'\b(?:generate|create)\b', 'generate'),
    (r'\b(?:track)\b', 'track'),
]

# Resource patterns for categories
RESOURCE_PATTERNS: Dict[str, List[Tuple[str, str]]] = {
    'knowledge': [
        (r'knowledge base', 'knowledge_base'),
        (r'(?:conversation|chat)', 'chat_history'),
        (r'agent memory', 'agent_memory'),
    ],
    'infrastructure': [
        (r'infrastructure', 'infrastructure'),
        (r'services?', 'services'),
        (r'security', 'security'),
        (r'resources', 'resources'),
    ],
    'agent': [
        (r'CEO agent', 'ceo_agent'),
        (r'CTO agent', 'cto_agent'),
        (r'CFO agent', 'cfo_agent'),
        (r'CMO agent', 'cmo_agent'),
        (r'CLO agent', 'clo_agent'),
        (r'agent', 'generic_agent')
    ],
    'business': [
        (r'revenue', 'revenue'),
        (r'competitive positioning', 'competitive_positioning'),
        (r'progress', 'progress'),
        (r'forecast', 'forecast'),
    ]
}

@dataclass
class ParseResult:
    action: str
    category: str
    resource: str
    parameters: Dict[str, Any]

class LogicExtractorAgent(BaseAgent):
    """Agent that parses MindScript (plain English) commands to structured payloads"""

    def __init__(self, agent_id: str = 'logic_extractor_001'):
        capabilities = [
            AgentCapability(
                name='parse_mindscript',
                description='Parse MindScript command into structured JSON payload'
            ),
            AgentCapability(
                name='estimate_token_savings',
                description='Estimate LLM tokens saved by rule-based parsing'
            )
        ]
        super().__init__(agent_id, AgentType.BUSINESS_LOGIC, capabilities)

    def _match_action(self, text: str) -> str:
        for pattern, action in ACTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return action
        return 'unknown'

    def _match_category_resource(self, text: str) -> Tuple[str, str]:
        for category, patterns in RESOURCE_PATTERNS.items():
            for pattern, resource in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return category, resource
        return 'general', 'generic'

    def _extract_parameters(self, text: str) -> Dict[str, Any]:
        # Simple heuristic to capture quoted strings as parameters
        params = {}
        matches = re.findall(r'"([^"]+)"', text)
        if matches:
            params['query'] = matches[0]
        # Extract numbers (e.g., MRR target)
        num_match = re.search(r'\$?[0-9,]+', text)
        if num_match:
            params['value'] = num_match.group().replace(',', '').replace('$', '')
        return params

    def parse_command(self, text: str) -> ParseResult:
        action = self._match_action(text)
        category, resource = self._match_category_resource(text)
        parameters = self._extract_parameters(text)
        return ParseResult(action, category, resource, parameters)

    async def process_task(self, task: Task) -> Dict[str, Any]:
        text = task.payload.get('command', '')
        original_tokens = estimate_tokens(text)

        parse_result = self.parse_command(text)
        structured_payload = {
            'action': parse_result.action,
            'category': parse_result.category,
            'resource': parse_result.resource,
            'parameters': parse_result.parameters,
            'original_text': text
        }

        structured_tokens = estimate_tokens(str(structured_payload))
        tokens_saved = max(0, original_tokens - structured_tokens)

        return {
            'structured_payload': structured_payload,
            'original_tokens': original_tokens,
            'structured_tokens': structured_tokens,
            'tokens_saved': tokens_saved
        }

    async def health_check(self) -> bool:
        # Simple health check always true in this minimal implementation
        return True
'''

print("Logic Extractor Agent Implementation:")
print("=" * 60)
print(logic_extractor_code)

with open('logic_extractor.py', 'w') as f:
    f.write(logic_extractor_code)

print("\n✓ Logic Extractor Agent saved to logic_extractor.py")