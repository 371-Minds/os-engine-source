Agent Utility Belt Example
==========================
Initialized AgentUtilityBelt with mock service catalog.
Service Catalog: {'by_category': [{'ip': {'l2.io': {'tags': ['curl', 'plain']}, 'echoip.de': {'tags': ['curl', 'plain']}}}, {'geo': {'ipinfo.io': {'tags': ['curl', 'json']}}}]}

Test Case 1: Find services by tag 'json'
Task: {'action': 'find_services_by_tag', 'tag': 'json'}
Result: {'services': [{'category': 'geo', 'service': 'ipinfo.io', 'details': {'tags': ['curl', 'json']}}]}

Test Case 2: Find services by tag 'curl'
Task: {'action': 'find_services_by_tag', 'tag': 'curl'}
Result: {'services': [{'category': 'ip', 'service': 'l2.io', 'details': {'tags': ['curl', 'plain']}}, {'category': 'ip', 'service': 'echoip.de', 'details': {'tags': ['curl', 'plain']}}, {'category': 'geo', 'service': 'ipinfo.io', 'details': {'tags': ['curl', 'json']}}]}

Test Case 3: Get repository details for 'ipinfo.io'
Task: {'action': 'get_repository_details', 'service_name': 'ipinfo.io'}
Result: {'repository_details': {'service': 'ipinfo.io', 'repository_url': 'https://github.com/ipinfo/ipinfo'}}

Test Case 4: Try to find a service that doesn't exist
Task: {'action': 'get_repository_details', 'service_name': 'non_existent_service'}
Result: {'repository_details': None}
