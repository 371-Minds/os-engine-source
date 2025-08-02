
"""
371 Minds Operating System - Secure Credential Warehouse
CyberArk-style vault for secure credential management
"""

import asyncio
import json
import logging
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

from base_agent import BaseAgent, AgentType, Task, TaskStatus, AgentCapability

@dataclass
class CredentialEntry:
    """Represents a credential stored in the vault"""
    id: str
    name: str
    credential_type: str  # "api_key", "oauth_token", "database_connection", etc.
    encrypted_value: bytes
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    rotation_interval_days: Optional[int] = None
    access_count: int = 0
    tags: List[str] = field(default_factory=list)

@dataclass
class AccessLog:
    """Log entry for credential access"""
    credential_id: str
    agent_id: str
    action: str  # "read", "write", "delete", "rotate"
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class SecureCredentialWarehouse(BaseAgent):
    """
    Secure credential management system similar to CyberArk
    Handles encryption, access control, rotation, and auditing
    """

    def __init__(self, agent_id: str = "credential_manager_001", master_key: Optional[str] = None):
        capabilities = [
            AgentCapability(
                name="store_credentials",
                description="Securely store encrypted credentials"
            ),
            AgentCapability(
                name="retrieve_credentials", 
                description="Retrieve credentials with access control"
            ),
            AgentCapability(
                name="rotate_credentials",
                description="Automatically rotate expiring credentials"
            ),
            AgentCapability(
                name="audit_access",
                description="Comprehensive logging and auditing"
            ),
            AgentCapability(
                name="access_control",
                description="Role-based access control management"
            )
        ]

        super().__init__(agent_id, AgentType.CREDENTIAL_MANAGER, capabilities)

        # Initialize encryption
        self.master_key = master_key or os.environ.get("VAULT_MASTER_KEY", self._generate_master_key())
        self.cipher_suite = self._initialize_encryption(self.master_key)

        # Storage
        self.credentials: Dict[str, CredentialEntry] = {}
        self.access_logs: List[AccessLog] = []
        self.access_policies: Dict[str, List[str]] = {}  # agent_id -> [credential_ids]

        # Predefined credential types for the 371 Minds OS
        self.credential_templates = {
            "digital_ocean_api": {
                "required_fields": ["api_token"],
                "rotation_interval_days": 90,
                "tags": ["cloud", "infrastructure"]
            },
            "github_deploy_token": {
                "required_fields": ["token", "repository"],
                "rotation_interval_days": 180,
                "tags": ["code", "deployment"]
            },
            "domain_registrar": {
                "required_fields": ["api_key", "api_secret"],
                "rotation_interval_days": 365,
                "tags": ["dns", "domain"]
            },
            "email_service_api": {
                "required_fields": ["api_key", "sender_domain"],
                "rotation_interval_days": 90,
                "tags": ["email", "communication"]
            },
            "database_connection": {
                "required_fields": ["host", "username", "password", "database"],
                "rotation_interval_days": 30,
                "tags": ["database", "storage"]
            },
            "payment_processor": {
                "required_fields": ["public_key", "private_key", "webhook_secret"],
                "rotation_interval_days": 60,
                "tags": ["payment", "financial"]
            },
            "social_media_api": {
                "required_fields": ["access_token", "refresh_token", "platform"],
                "rotation_interval_days": 30,
                "tags": ["social", "marketing"]
            }
        }

    def _generate_master_key(self) -> str:
        """Generate a secure master key"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()

    def _initialize_encryption(self, master_key: str) -> Fernet:
        """Initialize encryption cipher with master key"""
        key = base64.urlsafe_b64encode(master_key.encode()[:32].ljust(32, b'\0'))
        return Fernet(key)

    async def store_credential(self, name: str, credential_type: str, 
                             credential_data: Dict[str, Any], agent_id: str,
                             tags: List[str] = None, rotation_days: int = None) -> str:
        """
        Store a credential securely in the vault
        """
        # Validate credential type
        if credential_type in self.credential_templates:
            template = self.credential_templates[credential_type]
            required_fields = template["required_fields"]

            # Check if all required fields are present
            missing_fields = [field for field in required_fields if field not in credential_data]
            if missing_fields:
                raise ValueError(f"Missing required fields for {credential_type}: {missing_fields}")

        # Generate credential ID
        credential_id = f"cred_{credential_type}_{int(time.time())}_{secrets.token_hex(8)}"

        # Encrypt the credential data
        credential_json = json.dumps(credential_data)
        encrypted_data = self.cipher_suite.encrypt(credential_json.encode())

        # Set expiration and rotation
        rotation_interval = rotation_days or (
            self.credential_templates.get(credential_type, {}).get("rotation_interval_days", 90)
        )
        expires_at = datetime.now() + timedelta(days=rotation_interval)

        # Create credential entry
        credential_entry = CredentialEntry(
            id=credential_id,
            name=name,
            credential_type=credential_type,
            encrypted_value=encrypted_data,
            metadata={
                "created_by": agent_id,
                "size_bytes": len(encrypted_data),
                "template_used": credential_type in self.credential_templates
            },
            expires_at=expires_at,
            rotation_interval_days=rotation_interval,
            tags=tags or self.credential_templates.get(credential_type, {}).get("tags", [])
        )

        # Store credential
        self.credentials[credential_id] = credential_entry

        # Log the action
        self._log_access(credential_id, agent_id, "write")

        self.logger.info(f"Stored credential {credential_id} of type {credential_type}")

        return credential_id

    async def retrieve_credential(self, credential_id: str, agent_id: str) -> Dict[str, Any]:
        """
        Retrieve and decrypt a credential
        """
        # Check if credential exists
        if credential_id not in self.credentials:
            self._log_access(credential_id, agent_id, "read", success=False)
            raise ValueError(f"Credential {credential_id} not found")

        # Check access policy
        if not self._check_access_permission(agent_id, credential_id):
            self._log_access(credential_id, agent_id, "read", success=False)
            raise PermissionError(f"Agent {agent_id} does not have access to credential {credential_id}")

        credential = self.credentials[credential_id]

        # Check if credential has expired
        if credential.expires_at and datetime.now() > credential.expires_at:
            self._log_access(credential_id, agent_id, "read", success=False)
            raise ValueError(f"Credential {credential_id} has expired")

        # Decrypt credential data
        try:
            decrypted_data = self.cipher_suite.decrypt(credential.encrypted_value)
            credential_data = json.loads(decrypted_data.decode())
        except Exception as e:
            self._log_access(credential_id, agent_id, "read", success=False)
            raise ValueError(f"Failed to decrypt credential: {str(e)}")

        # Update access tracking
        credential.last_accessed = datetime.now()
        credential.access_count += 1

        # Log successful access
        self._log_access(credential_id, agent_id, "read")

        return {
            "id": credential_id,
            "name": credential.name,
            "type": credential.credential_type,
            "data": credential_data,
            "metadata": credential.metadata,
            "expires_at": credential.expires_at.isoformat() if credential.expires_at else None
        }

    async def get_secret(self, name: str, agent_id: str) -> Any:
        """
        Finds a credential by name and returns its decrypted value.
        This is a convenience method for agents.
        If the credential data has a single field, its value is returned.
        Otherwise, the entire data dictionary is returned.
        """
        found_id = None
        for cred_id, cred_entry in self.credentials.items():
            if cred_entry.name == name:
                found_id = cred_id
                break

        if not found_id:
            raise ValueError(f"Secret with name '{name}' not found.")

        credential_data = await self.retrieve_credential(found_id, agent_id)

        secret_payload = credential_data.get("data", {})
        if isinstance(secret_payload, dict) and len(secret_payload) == 1:
            return next(iter(secret_payload.values()))

        return secret_payload

    async def rotate_credential(self, credential_id: str, new_credential_data: Dict[str, Any], 
                               agent_id: str) -> bool:
        """
        Rotate an existing credential with new values
        """
        if credential_id not in self.credentials:
            return False

        # Check access permission
        if not self._check_access_permission(agent_id, credential_id):
            self._log_access(credential_id, agent_id, "rotate", success=False)
            raise PermissionError(f"Agent {agent_id} cannot rotate credential {credential_id}")

        credential = self.credentials[credential_id]

        # Encrypt new credential data
        credential_json = json.dumps(new_credential_data)
        encrypted_data = self.cipher_suite.encrypt(credential_json.encode())

        # Update credential
        credential.encrypted_value = encrypted_data
        credential.expires_at = datetime.now() + timedelta(days=credential.rotation_interval_days or 90)
        credential.metadata["last_rotated"] = datetime.now().isoformat()
        credential.metadata["rotated_by"] = agent_id

        # Log the rotation
        self._log_access(credential_id, agent_id, "rotate")

        self.logger.info(f"Rotated credential {credential_id}")

        return True

    async def delete_credential(self, credential_id: str, agent_id: str) -> bool:
        """
        Securely delete a credential
        """
        if credential_id not in self.credentials:
            return False

        # Check access permission (typically only the creator or admin can delete)
        credential = self.credentials[credential_id]
        if credential.metadata.get("created_by") != agent_id:
            self._log_access(credential_id, agent_id, "delete", success=False)
            raise PermissionError(f"Agent {agent_id} cannot delete credential {credential_id}")

        # Remove credential
        del self.credentials[credential_id]

        # Log the deletion
        self._log_access(credential_id, agent_id, "delete")

        self.logger.info(f"Deleted credential {credential_id}")

        return True

    async def list_credentials(self, agent_id: str, tags: List[str] = None) -> List[Dict[str, Any]]:
        """
        List credentials accessible to an agent
        """
        accessible_credentials = []

        for credential_id, credential in self.credentials.items():
            # Check access permission
            if not self._check_access_permission(agent_id, credential_id):
                continue

            # Filter by tags if specified
            if tags and not any(tag in credential.tags for tag in tags):
                continue

            # Return metadata only (no sensitive data)
            accessible_credentials.append({
                "id": credential_id,
                "name": credential.name,
                "type": credential.credential_type,
                "created_at": credential.created_at.isoformat(),
                "expires_at": credential.expires_at.isoformat() if credential.expires_at else None,
                "tags": credential.tags,
                "access_count": credential.access_count
            })

        return accessible_credentials

    async def grant_access(self, agent_id: str, credential_id: str, grantor_agent_id: str) -> bool:
        """
        Grant access to a credential for a specific agent
        """
        # Only the creator or admin can grant access
        if credential_id in self.credentials:
            credential = self.credentials[credential_id]
            if credential.metadata.get("created_by") != grantor_agent_id:
                raise PermissionError("Only credential creator can grant access")

        if agent_id not in self.access_policies:
            self.access_policies[agent_id] = []

        if credential_id not in self.access_policies[agent_id]:
            self.access_policies[agent_id].append(credential_id)
            self.logger.info(f"Granted access to credential {credential_id} for agent {agent_id}")
            return True

        return False

    def _check_access_permission(self, agent_id: str, credential_id: str) -> bool:
        """
        Check if an agent has permission to access a credential
        """
        # Creator always has access
        if credential_id in self.credentials:
            credential = self.credentials[credential_id]
            if credential.metadata.get("created_by") == agent_id:
                return True

        # Check explicit access policies
        agent_permissions = self.access_policies.get(agent_id, [])
        return credential_id in agent_permissions

    def _log_access(self, credential_id: str, agent_id: str, action: str, 
                   success: bool = True, ip_address: str = None):
        """
        Log credential access for auditing
        """
        log_entry = AccessLog(
            credential_id=credential_id,
            agent_id=agent_id,
            action=action,
            success=success,
            ip_address=ip_address
        )

        self.access_logs.append(log_entry)

        # Keep only last 10000 log entries to prevent memory issues
        if len(self.access_logs) > 10000:
            self.access_logs = self.access_logs[-5000:]

    async def get_audit_logs(self, agent_id: str = None, 
                           credential_id: str = None, 
                           hours: int = 24) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs for specified criteria
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        filtered_logs = []
        for log in self.access_logs:
            if log.timestamp < cutoff_time:
                continue

            if agent_id and log.agent_id != agent_id:
                continue

            if credential_id and log.credential_id != credential_id:
                continue

            filtered_logs.append({
                "credential_id": log.credential_id,
                "agent_id": log.agent_id,
                "action": log.action,
                "timestamp": log.timestamp.isoformat(),
                "success": log.success,
                "ip_address": log.ip_address
            })

        return filtered_logs

    async def check_expiring_credentials(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Check for credentials that will expire soon
        """
        expiring_soon = []
        cutoff_date = datetime.now() + timedelta(days=days_ahead)

        for credential_id, credential in self.credentials.items():
            if credential.expires_at and credential.expires_at <= cutoff_date:
                expiring_soon.append({
                    "id": credential_id,
                    "name": credential.name,
                    "type": credential.credential_type,
                    "expires_at": credential.expires_at.isoformat(),
                    "days_until_expiry": (credential.expires_at - datetime.now()).days
                })

        return expiring_soon

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process credential management tasks"""
        action = task.payload.get("action")
        agent_id = task.payload.get("agent_id", "system")

        if action == "store":
            credential_id = await self.store_credential(
                name=task.payload["name"],
                credential_type=task.payload["type"],
                credential_data=task.payload["data"],
                agent_id=agent_id,
                tags=task.payload.get("tags"),
                rotation_days=task.payload.get("rotation_days")
            )
            return {"credential_id": credential_id, "status": "stored"}

        elif action == "retrieve":
            credential = await self.retrieve_credential(
                task.payload["credential_id"], 
                agent_id
            )
            return {"credential": credential, "status": "retrieved"}

        elif action == "list":
            credentials = await self.list_credentials(
                agent_id,
                tags=task.payload.get("tags")
            )
            return {"credentials": credentials, "count": len(credentials)}

        elif action == "audit":
            logs = await self.get_audit_logs(
                agent_id=task.payload.get("target_agent_id"),
                credential_id=task.payload.get("credential_id"),
                hours=task.payload.get("hours", 24)
            )
            return {"audit_logs": logs, "count": len(logs)}

        else:
            raise ValueError(f"Unknown action: {action}")

    async def health_check(self) -> bool:
        """Check if the credential warehouse is healthy"""
        try:
            # Test encryption/decryption
            test_data = {"test": "data"}
            encrypted = self.cipher_suite.encrypt(json.dumps(test_data).encode())
            decrypted = json.loads(self.cipher_suite.decrypt(encrypted).decode())

            return decrypted == test_data
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

    def get_vault_statistics(self) -> Dict[str, Any]:
        """Get statistics about the credential vault"""
        total_credentials = len(self.credentials)
        credentials_by_type = {}
        expiring_soon = 0

        cutoff_date = datetime.now() + timedelta(days=30)

        for credential in self.credentials.values():
            # Count by type
            cred_type = credential.credential_type
            credentials_by_type[cred_type] = credentials_by_type.get(cred_type, 0) + 1

            # Count expiring soon
            if credential.expires_at and credential.expires_at <= cutoff_date:
                expiring_soon += 1

        return {
            "total_credentials": total_credentials,
            "credentials_by_type": credentials_by_type,
            "expiring_soon_30_days": expiring_soon,
            "total_access_logs": len(self.access_logs),
            "agents_with_access": len(self.access_policies)
        }
