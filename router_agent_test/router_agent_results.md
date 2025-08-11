--- Initializing Router Agent Test Suite ---
Registered Mock Agent: mock_intelligent_router_01 of type intelligent_router
Registered Mock Agent: mock_code_generation_01 of type code_generation
Registered Mock Agent: mock_marketing_asset_01 of type marketing_asset
Registered Mock Agent: mock_business_logic_01 of type business_logic
Registered Mock Agent: mock_deployment_agent_01 of type deployment_agent
Registered Mock Agent: mock_credential_manager_01 of type credential_manager
Registered Mock Agent: mock_marketing_automation_01 of type marketing_automation
Registered Mock Agent: mock_repository_intake_01 of type repository_intake
Registered Mock Agent: mock_qa_automation_01 of type qa_automation
Registered Mock Agent: mock_tech_stack_specialist_01 of type tech_stack_specialist
Registered Mock Agent: mock_agent_utility_belt_01 of type agent_utility_belt
Registered Mock Agent: mock_ceo_01 of type ceo
Registered Mock Agent: mock_cto_01 of type cto
Registered Mock Agent: mock_cmo_01 of type cmo
Registered Mock Agent: mock_cfo_01 of type cfo
Registered Mock Agent: mock_clo_01 of type clo
Registered Mock Agent: mock_financial_01 of type financial

--- Starting Test Submissions ---

--- Test Case #1 ---
Submission: "Please deploy my new application from the repo github.com/user/my-app."

Routing Decision:
  - Task ID: task_1_721
  - Assigned Agents: ['code_generation', 'repository_intake', 'deployment_agent', 'business_logic', 'credential_manager']
  - Execution Strategy: parallel
  - Estimated Completion Time: 360s

Orchestration Log:
  - Mock Agent mock_code_generation_01 (code_generation) received task: task_1_721_subtask_1
    - Description: Execute code_generation for task_1_721
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_repository_intake_01 (repository_intake) received task: task_1_721_subtask_2
    - Description: Execute repository_intake for task_1_721
    - Payload: {'repo_url': 'https://github.com/example/repo', 'user_id': 'test_user_01'}
  - Mock Agent mock_deployment_agent_01 (deployment_agent) received task: task_1_721_subtask_3
    - Description: Execute deployment_agent for task_1_721
    - Payload: {'task_id': 'task_1_721_subtask_3', 'repo_url': 'https://github.com/example/repo', 'repo_branch': 'main', 'target_environment': 'staging', 'cloud_provider': 'digitalocean', 'infra_spec': {'size': 's-1vcpu-1gb', 'region': 'nyc3', 'replicas': 1}, 'domain': 'app.example.com', 'ssl': False, 'build_commands': 'npm install && npm run build', 'container_registry': 'registry.digitalocean.com/myapp', 'environment_vars': {'NODE_ENV': 'production'}}
  - Mock Agent mock_business_logic_01 (business_logic) received task: task_1_721_subtask_4
    - Description: Execute business_logic for task_1_721
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_credential_manager_01 (credential_manager) received task: task_1_721_subtask_5
    - Description: Execute credential_manager for task_1_721
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #2 ---
Submission: "We need to create a new marketing campaign for our summer sale."

Routing Decision:
  - Task ID: task_6_4250
  - Assigned Agents: ['marketing_asset']
  - Execution Strategy: sequential
  - Estimated Completion Time: 180s

Orchestration Log:
  - Mock Agent mock_marketing_asset_01 (marketing_asset) received task: task_6_4250_subtask_1
    - Description: Execute marketing_asset for task_6_4250
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #3 ---
Submission: "I have an idea for a SaaS application. It needs a database, user authentication, and a payment gateway. Let's launch it on AWS."

Routing Decision:
  - Task ID: task_7_6328
  - Assigned Agents: ['financial', 'code_generation', 'cfo', 'deployment_agent', 'business_logic', 'credential_manager']
  - Execution Strategy: parallel
  - Estimated Completion Time: 360s

Orchestration Log:
  - Mock Agent mock_financial_01 (financial) received task: task_7_6328_subtask_1
    - Description: Execute financial for task_7_6328
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_code_generation_01 (code_generation) received task: task_7_6328_subtask_2
    - Description: Execute code_generation for task_7_6328
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_cfo_01 (cfo) received task: task_7_6328_subtask_3
    - Description: Execute cfo for task_7_6328
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_deployment_agent_01 (deployment_agent) received task: task_7_6328_subtask_4
    - Description: Execute deployment_agent for task_7_6328
    - Payload: {'task_id': 'task_7_6328_subtask_4', 'repo_url': 'https://github.com/example/repo', 'repo_branch': 'main', 'target_environment': 'staging', 'cloud_provider': 'aws', 'infra_spec': {'size': 's-1vcpu-1gb', 'region': 'nyc3', 'replicas': 1}, 'domain': 'app.example.com', 'ssl': False, 'build_commands': 'npm install && npm run build', 'container_registry': 'registry.digitalocean.com/myapp', 'environment_vars': {'NODE_ENV': 'production'}}
  - Mock Agent mock_business_logic_01 (business_logic) received task: task_7_6328_subtask_5
    - Description: Execute business_logic for task_7_6328
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_credential_manager_01 (credential_manager) received task: task_7_6328_subtask_6
    - Description: Execute credential_manager for task_7_6328
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #4 ---
Submission: "Set up the infrastructure for our new service on DigitalOcean."

Routing Decision:
  - Task ID: task_13_7951
  - Assigned Agents: ['business_logic']
  - Execution Strategy: sequential
  - Estimated Completion Time: 120s

Orchestration Log:
  - Mock Agent mock_business_logic_01 (business_logic) received task: task_13_7951_subtask_1
    - Description: Execute business_logic for task_13_7951
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #5 ---
Submission: "Can I get a P&L report for the last quarter? Also, project our revenue for the next year."

Routing Decision:
  - Task ID: task_14_2027
  - Assigned Agents: ['financial', 'repository_intake', 'cfo']
  - Execution Strategy: sequential
  - Estimated Completion Time: 180s

Orchestration Log:
  - Mock Agent mock_financial_01 (financial) received task: task_14_2027_subtask_1
    - Description: Execute financial for task_14_2027
    - Payload: {'user_id': 'test_user_01'}
  - Mock Agent mock_repository_intake_01 (repository_intake) received task: task_14_2027_subtask_2
    - Description: Execute repository_intake for task_14_2027
    - Payload: {'repo_url': 'https://github.com/example/repo', 'user_id': 'test_user_01'}
  - Mock Agent mock_cfo_01 (cfo) received task: task_14_2027_subtask_3
    - Description: Execute cfo for task_14_2027
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #6 ---
Submission: "What is the best way to structure our customer support team?"

Routing Decision:
  - Task ID: task_17_2293
  - Assigned Agents: ['business_logic']
  - Execution Strategy: sequential
  - Estimated Completion Time: 120s

Orchestration Log:
  - Mock Agent mock_business_logic_01 (business_logic) received task: task_17_2293_subtask_1
    - Description: Execute business_logic for task_17_2293
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #7 ---
Submission: "Help me with my business."

Routing Decision:
  - Task ID: task_18_8741
  - Assigned Agents: ['business_logic']
  - Execution Strategy: sequential
  - Estimated Completion Time: 120s

Orchestration Log:
  - Mock Agent mock_business_logic_01 (business_logic) received task: task_18_8741_subtask_1
    - Description: Execute business_logic for task_18_8741
    - Payload: {'user_id': 'test_user_01'}

--- Test Case #8 ---
Submission: "Analyze the repository at https://github.com/371-minds/mock-repo and suggest improvements."

Routing Decision:
  - Task ID: task_19_9903
  - Assigned Agents: ['repository_intake']
  - Execution Strategy: sequential
  - Estimated Completion Time: 120s

Orchestration Log:
  - Mock Agent mock_repository_intake_01 (repository_intake) received task: task_19_9903_subtask_1
    - Description: Execute repository_intake for task_19_9903
    - Payload: {'repo_url': 'https://github.com/371-minds/mock-repo', 'user_id': 'test_user_01'}

--- Router Agent Test Suite Finished ---
