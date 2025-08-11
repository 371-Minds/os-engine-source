import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from credential_warehouse_agent import SecureCredentialWarehouse

async def run_credential_warehouse_benchmark():
    """
    An extensive benchmark and test suite for the SecureCredentialWarehouse agent.
    This script runs a variety of submissions using mock agents to simulate
    the behavior of the full agent system.
    """
    print("--- Starting Credential Warehouse Benchmark ---")

    # 1. Initialize the SecureCredentialWarehouse
    print("\n[1. INITIALIZATION]")
    # Use a fixed master key for reproducibility
    master_key = "test-master-key-32-bytes-long-for-testing"
    warehouse = SecureCredentialWarehouse(master_key=master_key)

    # Verify health check passes
    is_healthy = await warehouse.health_check()
    print(f"Warehouse health check: {'OK' if is_healthy else 'Failed'}")

    # Mock agent IDs
    admin_agent = "admin_agent_001"
    finance_agent = "finance_agent_002"
    devops_agent = "devops_agent_003"
    marketing_agent = "marketing_agent_004"

    print(f"Mock agents created: {admin_agent}, {finance_agent}, {devops_agent}, {marketing_agent}")

    # 2. Store a variety of credentials
    print("\n[2. STORING CREDENTIALS]")

    try:
        # DevOps agent stores a Digital Ocean API key
        do_api_key_data = {"api_token": "do_tok_1234567890abcdef"}
        do_cred_id = await warehouse.store_credential(
            name="DigitalOcean API Key",
            credential_type="digital_ocean_api",
            credential_data=do_api_key_data,
            agent_id=devops_agent,
            tags=["cloud", "production"]
        )
        print(f"  - Stored DigitalOcean API key with ID: {do_cred_id}")

        # Finance agent stores payment processor credentials
        payment_data = {"public_key": "pk_test_123", "private_key": "sk_test_456", "webhook_secret": "wh_secret_789"}
        payment_cred_id = await warehouse.store_credential(
            name="Stripe API Credentials",
            credential_type="payment_processor",
            credential_data=payment_data,
            agent_id=finance_agent
        )
        print(f"  - Stored Stripe credentials with ID: {payment_cred_id}")

        # Admin agent stores a database password
        db_data = {"host": "db.example.com", "username": "admin", "password": "db_password_abc", "database": "main_db"}
        db_cred_id = await warehouse.store_credential(
            name="Production Database Password",
            credential_type="database_connection",
            credential_data=db_data,
            agent_id=admin_agent,
            rotation_days=15 # Custom rotation
        )
        print(f"  - Stored database password with ID: {db_cred_id}")

        # Storing a credential with missing fields (should fail)
        print("  - Attempting to store credential with missing fields (expected to fail)...")
        await warehouse.store_credential(
            name="Incomplete GitHub Token",
            credential_type="github_deploy_token",
            credential_data={"token": "ghp_abcdef"}, # Missing 'repository'
            agent_id=devops_agent
        )
    except ValueError as e:
        print(f"  - SUCCESS: Caught expected error: {e}")

    # 3. Listing and Access Control
    print("\n[3. LISTING & ACCESS CONTROL]")

    # DevOps agent lists its credentials
    devops_creds = await warehouse.list_credentials(agent_id=devops_agent)
    print(f"  - DevOps agent can see {len(devops_creds)} credential(s).")
    # for cred in devops_creds:
    #     print(f"    * {cred['name']} ({cred['id']})")

    # Finance agent lists cloud credentials (should be empty)
    finance_cloud_creds = await warehouse.list_credentials(agent_id=finance_agent, tags=["cloud"])
    print(f"  - Finance agent can see {len(finance_cloud_creds)} credentials with 'cloud' tag.")

    # 4. Retrieving Credentials
    print("\n[4. RETRIEVING CREDENTIALS]")

    # DevOps agent retrieves its own credential (should succeed)
    print("  - DevOps agent retrieving its own DO key...")
    retrieved_do_key = await warehouse.retrieve_credential(do_cred_id, agent_id=devops_agent)
    if retrieved_do_key['data']['api_token'] == do_api_key_data['api_token']:
        print("  - SUCCESS: Retrieved and decrypted DigitalOcean key correctly.")

    # Finance agent tries to retrieve DevOps credential (should fail)
    print("  - Finance agent attempting to retrieve DO key (expected to fail)...")
    try:
        await warehouse.retrieve_credential(do_cred_id, agent_id=finance_agent)
    except PermissionError as e:
        print(f"  - SUCCESS: Caught expected permission error: {e}")

    # Use the convenience `get_secret` method
    print("  - DevOps agent using get_secret for DO key...")
    secret_token = await warehouse.get_secret("DigitalOcean API Key", agent_id=devops_agent)
    if secret_token == do_api_key_data['api_token']:
         print("  - SUCCESS: get_secret returned the correct token.")

    # 5. Granting Access
    print("\n[5. GRANTING ACCESS]")

    # DevOps agent grants admin agent access to the DO key (should fail as not creator)
    # This is a bit of a misinterpretation of the code, let's correct the test logic
    # The creator of the credential is the one who can grant access.
    print("  - Admin agent attempting to grant access to finance agent (not creator, should fail)...")
    try:
        await warehouse.grant_access(finance_agent, do_cred_id, grantor_agent_id=admin_agent)
    except PermissionError as e:
         print(f"  - SUCCESS: Caught expected error: {e}")

    # DevOps agent (creator) grants admin agent access
    print("  - DevOps agent grants admin access to DO key...")
    await warehouse.grant_access(admin_agent, do_cred_id, grantor_agent_id=devops_agent)

    # Admin agent now tries to retrieve the DO key (should succeed)
    print("  - Admin agent retrieving DO key after being granted access...")
    retrieved_by_admin = await warehouse.retrieve_credential(do_cred_id, agent_id=admin_agent)
    if retrieved_by_admin['id'] == do_cred_id:
        print("  - SUCCESS: Admin agent retrieved the key successfully.")

    # 6. Auditing
    print("\n[6. AUDITING]")

    # Get all logs for the Digital Ocean credential
    audit_logs = await warehouse.get_audit_logs(credential_id=do_cred_id)
    print(f"  - Found {len(audit_logs)} audit log entries for the DO credential.")
    # for log in audit_logs:
    #     print(f"    * {log['timestamp']}: Agent {log['agent_id']} performed '{log['action']}' (Success: {log['success']})")

    # 7. Credential Rotation
    print("\n[7. CREDENTIAL ROTATION]")

    # Rotate the database password
    print("  - Admin agent rotating the database password...")
    new_db_password = {"host": "db.example.com", "username": "admin", "password": "new_db_password_xyz", "database": "main_db"}
    rotation_success = await warehouse.rotate_credential(db_cred_id, new_db_password, agent_id=admin_agent)
    print(f"  - Database password rotation status: {'Success' if rotation_success else 'Failure'}")

    # Verify the new password
    retrieved_new_db_pass = await warehouse.retrieve_credential(db_cred_id, agent_id=admin_agent)
    if retrieved_new_db_pass['data']['password'] == "new_db_password_xyz":
        print("  - SUCCESS: Retrieved new database password correctly after rotation.")

    # 8. Checking for Expiring Credentials
    print("\n[8. EXPIRATION & DELETION]")

    # Check for credentials expiring in the next 20 days (the DB cred should be there)
    expiring_creds = await warehouse.check_expiring_credentials(days_ahead=20)
    print(f"  - Found {len(expiring_creds)} credential(s) expiring in the next 20 days.")
    # for cred in expiring_creds:
    #     print(f"    * {cred['name']} expires on {cred['expires_at']}")

    # Deleting a credential
    print(f"  - Finance agent attempting to delete DO key (not creator, should fail)...")
    try:
        await warehouse.delete_credential(do_cred_id, agent_id=finance_agent)
    except PermissionError as e:
        print(f"  - SUCCESS: Caught expected permission error: {e}")

    print(f"  - DevOps agent deleting the DO key...")
    delete_success = await warehouse.delete_credential(do_cred_id, agent_id=devops_agent)
    print(f"  - Deletion status: {'Success' if delete_success else 'Failure'}")

    # Verify deletion
    print("  - Verifying deletion by attempting to retrieve the key...")
    try:
        await warehouse.retrieve_credential(do_cred_id, agent_id=admin_agent)
    except ValueError as e:
        print(f"  - SUCCESS: Caught expected error, credential not found: {e}")

    # 9. Vault Statistics
    print("\n[9. VAULT STATISTICS]")
    stats = warehouse.get_vault_statistics()
    print(f"  - Total credentials remaining: {stats['total_credentials']}")
    print(f"  - Credentials by type: {stats['credentials_by_type']}")
    print(f"  - Total access logs: {stats['total_access_logs']}")

    print("\n--- Credential Warehouse Benchmark Finished ---")

if __name__ == "__main__":
    # To run this from the command line:
    # python credential_warehouse_agent/credential_warehouse_example_agent.py
    asyncio.run(run_credential_warehouse_benchmark())
