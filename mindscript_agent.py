
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
    # Existing patterns (keeping all current ones)
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

    # NEW: Development & Infrastructure Actions
    (r'\b(?:configure|setup|install|build)\b', 'configure'),
    (r'\b(?:fork|clone|branch)\b', 'fork'),
    (r'\b(?:integrate|connect|link)\b', 'integrate'),
    (r'\b(?:customize|modify|adapt)\b', 'customize'),
    (r'\b(?:test|validate|verify)\b', 'test'),
    (r'\b(?:compile|bundle|package)\b', 'compile'),
    (r'\b(?:debug|troubleshoot|fix)\b', 'debug'),
    (r'\b(?:optimize|improve|enhance)\b', 'optimize'),

    # NEW: Business Operations Actions
    (r'\b(?:modernize|migrate|convert)\b', 'modernize'),
    (r'\b(?:process|handle|manage)\b', 'process'),
    (r'\b(?:coordinate|orchestrate|organize)\b', 'coordinate'),
    (r'\b(?:automate|streamline|systematize)\b', 'automate'),
    (r'\b(?:schedule|plan|organize)\b', 'schedule'),
    (r'\b(?:execute|run|perform)\b', 'execute'),
    (r'\b(?:report|document|record)\b', 'report'),
    (r'\b(?:audit|review|inspect)\b', 'audit'),

    # NEW: AI & Agent Actions
    (r'\b(?:train|learn|teach)\b', 'train'),
    (r'\b(?:infer|predict|forecast)\b', 'infer'),
    (r'\b(?:classify|categorize|label)\b', 'classify'),
    (r'\b(?:transform|convert|translate)\b', 'transform'),
    (r'\b(?:embed|encode|vectorize)\b', 'embed'),
    (r'\b(?:retrieve|fetch|get)\b', 'retrieve'),

    # NEW: Security & Authentication Actions
    (r'\b(?:authenticate|login|authorize)\b', 'authenticate'),
    (r'\b(?:secure|protect|encrypt)\b', 'secure'),
    (r'\b(?:rotate|refresh|renew)\b', 'rotate'),
    (r'\b(?:backup|archive|preserve)\b', 'backup'),

    # NEW: Communication & Collaboration Actions
    (r'\b(?:notify|alert|inform)\b', 'notify'),
    (r'\b(?:communicate|broadcast|announce)\b', 'communicate'),
    (r'\b(?:collaborate|cooperate|work together)\b', 'collaborate'),
    (r'\b(?:present|demonstrate|showcase)\b', 'present'),

    # NEW: Data & Analytics Actions
    (r'\b(?:visualize|chart|graph)\b', 'visualize'),
    (r'\b(?:aggregate|summarize|consolidate)\b', 'aggregate'),
    (r'\b(?:filter|sort|organize)\b', 'filter'),
    (r'\b(?:compare|contrast|benchmark)\b', 'compare'),

    # NEW: Deployment & Operations Actions
    (r'\b(?:provision|allocate|assign)\b', 'provision'),
    (r'\b(?:restart|reboot|reload)\b', 'restart'),
    (r'\b(?:rollback|revert|undo)\b', 'rollback'),
    (r'\b(?:maintain|service|support)\b', 'maintain')
]

# Resource patterns for categories
RESOURCE_PATTERNS: Dict[str, List[Tuple[str, str]]] = {
    # Existing categories (keeping all current ones)
    'knowledge': [
        (r'knowledge base', 'knowledge_base'),
        (r'(?:conversation|chat)', 'chat_history'),
        (r'agent memory', 'agent_memory'),
        # NEW additions to knowledge
        (r'logic schemas?', 'logic_schema'),
        (r'business canvas', 'business_canvas'),
        (r'documentation', 'documentation'),
        (r'training data', 'training_data'),
        (r'prompts?', 'prompts'),
        (r'templates?', 'templates')
    ],

    'infrastructure': [
        (r'infrastructure', 'infrastructure'),
        (r'services?', 'services'),
        (r'security', 'security'),
        (r'resources', 'resources'),
        # NEW additions to infrastructure
        (r'servers?', 'servers'),
        (r'containers?', 'containers'),
        (r'networks?', 'networks'),
        (r'storage', 'storage'),
        (r'databases?', 'databases'),
        (r'apis?', 'apis'),
        (r'endpoints?', 'endpoints'),
        (r'pipelines?', 'pipelines')
    ],

    'agent': [
        (r'MiMI|CEO agent', 'mimi_ceo_agent'),
        (r'ALEX|CTO agent', 'alex_cto_agent'),
        (r'CASH|CFO agent', 'cash_cfo_agent'),
        (r'NOVA|CMO agent', 'nova_cmo_agent'),
        (r'SAGE|CLO agent', 'sage_clo_agent'),
        (r'agent', 'generic_agent'),
        # NEW agent types
        (r'logic extractor', 'logic_extractor_agent'),
        (r'repository intake', 'repository_intake_agent'),
        (r'tech stack specialist', 'tech_stack_specialist_agent'),
        (r'intelligent router', 'intelligent_router_agent'),
        (r'credential manager', 'credential_manager_agent')
    ],

    'business': [
        (r'revenue', 'revenue'),
        (r'competitive positioning', 'competitive_positioning'),
        (r'progress', 'progress'),
        (r'forecast', 'forecast'),
        # NEW business resources
        (r'business model', 'business_model'),
        (r'pricing strategy', 'pricing_strategy'),
        (r'go.to.market', 'go_to_market_plan'),
        (r'financial projections?', 'financial_projections'),
        (r'marketing campaigns?', 'marketing_campaigns'),
        (r'customer segments?', 'customer_segments'),
        (r'value propositions?', 'value_propositions'),
        (r'metrics', 'metrics'),
        (r'kpis?', 'kpis'),
        (r'analytics', 'analytics')
    ],

    # NEW CATEGORIES
    'development': [
        (r'(?:vs code|vscode)', 'vscode'),
        (r'ide', 'ide'),
        (r'git(?:\s+tower)?', 'git_repository'),
        (r'repositories?', 'repositories'),
        (r'codebases?', 'codebases'),
        (r'source code', 'source_code'),
        (r'branches?', 'branches'),
        (r'commits?', 'commits'),
        (r'pull requests?', 'pull_requests'),
        (r'devpod', 'devpod_workspace'),
        (r'workspaces?', 'workspaces'),
        (r'environments?', 'environments')
    ],

    'legacy_systems': [
        (r'(?:cobol|COBOL)', 'cobol_code'),
        (r'(?:fortran|FORTRAN)', 'fortran_code'),
        (r'mainframe', 'mainframe_systems'),
        (r'copybooks?', 'cobol_copybooks'),
        (r'jcl|job control language', 'jcl_scripts'),
        (r'legacy (?:code|systems?)', 'legacy_systems'),
        (r'(?:pl\/i|PLI)', 'pli_code'),
        (r'assembler', 'assembler_code'),
        (r'rpg', 'rpg_code'),
        (r'(?:visual basic|vb6)', 'visual_basic_code')
    ],

    'tech_stack': [
        (r'(?:mern|MERN)', 'mern_stack'),
        (r'(?:mean|MEAN)', 'mean_stack'),
        (r'react', 'react'),
        (r'(?:node\.?js|nodejs)', 'nodejs'),
        (r'express', 'express'),
        (r'mongodb', 'mongodb'),
        (r'typescript', 'typescript'),
        (r'javascript', 'javascript'),
        (r'python', 'python'),
        (r'django', 'django'),
        (r'flask', 'flask'),
        (r'fastapi', 'fastapi'),
        (r'next\.?js|nextjs', 'nextjs'),
        (r'convex', 'convex_backend')
    ],

    'enterprise_tools': [
        (r'cyberark', 'cyberark'),
        (r'posthog', 'posthog_analytics'),
        (r'logto', 'logto_auth'),
        (r'secretless broker', 'secretless_broker'),
        (r'credentials?', 'credentials'),
        (r'api keys?', 'api_keys'),
        (r'tokens?', 'tokens'),
        (r'certificates?', 'certificates'),
        (r'compliance', 'compliance'),
        (r'gdpr', 'gdpr_compliance'),
        (r'hipaa', 'hipaa_compliance'),
        (r'sox', 'sox_compliance')
    ],

    'ai_ml': [
        (r'(?:llm|large language model)', 'llm_models'),
        (r'(?:gpt|GPT)', 'gpt_models'),
        (r'claude', 'claude_models'),
        (r'embeddings?', 'embeddings'),
        (r'vectors?', 'vectors'),
        (r'models?', 'ai_models'),
        (r'neural networks?', 'neural_networks'),
        (r'machine learning', 'machine_learning'),
        (r'training sets?', 'training_sets'),
        (r'datasets?', 'datasets'),
        (r'mem0', 'mem0_memory'),
        (r'mindsdb', 'mindsdb_analytics'),
        (r'context windows?', 'context_windows')
    ],

    'content_marketing': [
        (r'marketing assets?', 'marketing_assets'),
        (r'social media', 'social_media'),
        (r'campaigns?', 'campaigns'),
        (r'content', 'content'),
        (r'blog posts?', 'blog_posts'),
        (r'newsletters?', 'newsletters'),
        (r'landing pages?', 'landing_pages'),
        (r'copywriting', 'copywriting'),
        (r'branding', 'branding'),
        (r'logos?', 'logos'),
        (r'themes?', 'themes'),
        (r'assets?', 'assets')
    ],

    'deployment': [
        (r'cloud', 'cloud_infrastructure'),
        (r'aws', 'aws'),
        (r'azure', 'azure'),
        (r'gcp|google cloud', 'gcp'),
        (r'digital ocean', 'digital_ocean'),
        (r'docker', 'docker'),
        (r'kubernetes', 'kubernetes'),
        (r'ci\/cd', 'cicd_pipeline'),
        (r'deployments?', 'deployments'),
        (r'staging', 'staging_environment'),
        (r'production', 'production_environment'),
        (r'byoc|bring your own cloud', 'byoc')
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
