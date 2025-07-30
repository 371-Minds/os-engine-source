# Let's create expanded ACTION/RESOURCE pattern tables based on the 371 Minds ecosystem
import json
import re
from typing import Dict, List, Tuple

# Current ACTION_PATTERNS from the logic_extractor.py file
current_action_patterns = [
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

# Current RESOURCE_PATTERNS from the logic_extractor.py file
current_resource_patterns = {
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

print("Current ACTION_PATTERNS:", len(current_action_patterns))
print("Current RESOURCE_PATTERNS categories:", len(current_resource_patterns))
print()

# Let's count total current patterns
total_current = len(current_action_patterns)
for category, patterns in current_resource_patterns.items():
    total_current += len(patterns)
    
print(f"Total current patterns: {total_current}")