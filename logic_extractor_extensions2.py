# Create expanded RESOURCE_PATTERNS based on the 371 Minds ecosystem
expanded_resource_patterns = {
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

# Count new patterns
total_new_resource_patterns = 0
for category, patterns in expanded_resource_patterns.items():
    total_new_resource_patterns += len(patterns)

# Count original patterns  
total_original_resource_patterns = 0
for category, patterns in current_resource_patterns.items():
    total_original_resource_patterns += len(patterns)

print("EXPANDED RESOURCE_PATTERNS:")
print(f"Categories: {len(expanded_resource_patterns)} (was {len(current_resource_patterns)})")
print(f"Total patterns: {total_new_resource_patterns} (was {total_original_resource_patterns})")
print(f"Added: {total_new_resource_patterns - total_original_resource_patterns} new resource patterns")
print(f"Added: {len(expanded_resource_patterns) - len(current_resource_patterns)} new categories")
print()

# Display the new categories
new_categories = ['development', 'legacy_systems', 'tech_stack', 'enterprise_tools', 'ai_ml', 'content_marketing', 'deployment']

print("NEW RESOURCE CATEGORIES:")
for category in new_categories:
    patterns = expanded_resource_patterns[category]
    print(f"\n{category.upper().replace('_', ' ')} ({len(patterns)} patterns):")
    for pattern, resource in patterns[:6]:  # Show first 6 patterns
        # Extract key words from regex pattern for display
        clean_pattern = pattern.replace(r'(?:', '').replace(r')', '').replace('|', ', ').replace('\\', '')
        print(f"  {resource}: {clean_pattern}")
    if len(patterns) > 6:
        print(f"  ... and {len(patterns) - 6} more")