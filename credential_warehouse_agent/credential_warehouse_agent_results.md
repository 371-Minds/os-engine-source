--- Starting Credential Warehouse Benchmark ---

[1. INITIALIZATION]
Warehouse health check: OK
Mock agents created: admin_agent_001, finance_agent_002, devops_agent_003, marketing_agent_004

[2. STORING CREDENTIALS]
  - Stored DigitalOcean API key with ID: cred_digital_ocean_api_1754934691_4c48fafb8fde7723
  - Stored Stripe credentials with ID: cred_payment_processor_1754934691_7f808a10f42553a8
  - Stored database password with ID: cred_database_connection_1754934691_d9e2b2fe53ad2e0d
  - Attempting to store credential with missing fields (expected to fail)...
  - SUCCESS: Caught expected error: Missing required fields for github_deploy_token: ['repository']

[3. LISTING & ACCESS CONTROL]
  - DevOps agent can see 1 credential(s).
  - Finance agent can see 0 credentials with 'cloud' tag.

[4. RETRIEVING CREDENTIALS]
  - DevOps agent retrieving its own DO key...
  - SUCCESS: Retrieved and decrypted DigitalOcean key correctly.
  - Finance agent attempting to retrieve DO key (expected to fail)...
  - SUCCESS: Caught expected permission error: Agent finance_agent_002 does not have access to credential cred_digital_ocean_api_1754934691_4c48fafb8fde7723
  - DevOps agent using get_secret for DO key...
  - SUCCESS: get_secret returned the correct token.

[5. GRANTING ACCESS]
  - Admin agent attempting to grant access to finance agent (not creator, should fail)...
  - SUCCESS: Caught expected error: Only credential creator can grant access
  - DevOps agent grants admin access to DO key...
  - Admin agent retrieving DO key after being granted access...
  - SUCCESS: Admin agent retrieved the key successfully.

[6. AUDITING]
  - Found 5 audit log entries for the DO credential.

[7. CREDENTIAL ROTATION]
  - Admin agent rotating the database password...
  - Database password rotation status: Success
  - SUCCESS: Retrieved new database password correctly after rotation.

[8. EXPIRATION & DELETION]
  - Found 1 credential(s) expiring in the next 20 days.
  - Finance agent attempting to delete DO key (not creator, should fail)...
  - SUCCESS: Caught expected permission error: Agent finance_agent_002 cannot delete credential cred_digital_ocean_api_1754934691_4c48fafb8fde7723
  - DevOps agent deleting the DO key...
  - Deletion status: Success
  - Verifying deletion by attempting to retrieve the key...
  - SUCCESS: Caught expected error, credential not found: Credential cred_digital_ocean_api_1754934691_4c48fafb8fde7723 not found

[9. VAULT STATISTICS]
  - Total credentials remaining: 2
  - Credentials by type: {'payment_processor': 1, 'database_connection': 1}
  - Total access logs: 12

--- Credential Warehouse Benchmark Finished ---
