# Create expanded ACTION_PATTERNS based on the 371 Minds ecosystem
expanded_action_patterns = [
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

print("EXPANDED ACTION_PATTERNS:")
print(f"Total patterns: {len(expanded_action_patterns)}")
print(f"Added: {len(expanded_action_patterns) - len(current_action_patterns)} new action patterns")
print()

# Display new actions in categories
print("NEW ACTION CATEGORIES:")
categories = {
    "Development & Infrastructure": expanded_action_patterns[12:20],
    "Business Operations": expanded_action_patterns[20:28], 
    "AI & Agent Actions": expanded_action_patterns[28:34],
    "Security & Authentication": expanded_action_patterns[34:38],
    "Communication & Collaboration": expanded_action_patterns[38:42],
    "Data & Analytics": expanded_action_patterns[42:46],
    "Deployment & Operations": expanded_action_patterns[46:50]
}

for category, patterns in categories.items():
    print(f"\n{category}:")
    for pattern, action in patterns:
        # Extract key words from regex pattern for display
        words = pattern.replace(r'\b(?:', '').replace(r')\b', '').replace('|', ', ')
        print(f"  {action}: {words}")