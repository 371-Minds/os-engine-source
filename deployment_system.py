import os
import time
import subprocess
import logging
import asyncio
import tempfile
from typing import Optional, Dict, Any

from base_agent import (
    BaseAgent,
    AgentType,
    Task,
    TaskStatus,
    DeploymentRequest,
    DeploymentContext,
    AgentCapability,
)
from credential_warehouse_agent import SecureCredentialWarehouse
import posthog

# Initialize PostHog
posthog.api_key = os.getenv("POSTHOG_API_KEY")
posthog.host = os.getenv("POSTHOG_HOST", "https://app.posthog.com")

class DeploymentAgent(BaseAgent):
    def __init__(self, agent_id: str = "deployment_agent_001"):
        capabilities = [
            AgentCapability(name="deploy_application", description="Deploy an application from a git repository."),
            AgentCapability(name="clone_and_build", description="Clone a git repository and build a docker container."),
            AgentCapability(name="provision_infrastructure", description="Provision infrastructure on cloud providers (DigitalOcean, AWS)."),
            AgentCapability(name="configure_dns_ssl", description="Configure DNS and SSL for a domain."),
        ]
        super().__init__(agent_id, AgentType.DEPLOYMENT, capabilities)
        self.cred_store = SecureCredentialWarehouse()

    async def health_check(self) -> bool:
        return True

    async def process_task(self, task: Task) -> Dict[str, Any]:
        self.logger.info(f"Processing deployment task {task.id}")

        try:
            request = DeploymentRequest(**task.payload)
        except TypeError as e:
            self.logger.error(f"Failed to create DeploymentRequest from task payload: {e}")
            raise ValueError(f"Invalid payload for DeploymentRequest: {task.payload}") from e

        ctx = DeploymentContext(
            droplet_ids={}, container_image="", dns_record={}, ssl_certificate_id="", start_time=time.time(), end_time=0.0
        )

        self._track_event(request.task_id, TaskStatus.PROVISIONING)
        await self.clone_and_build(request, ctx)

        self._track_event(request.task_id, TaskStatus.DEPLOYING)
        await self.provision_and_deploy(request, ctx)

        self._track_event(request.task_id, TaskStatus.CONFIGURING)
        await self.configure_dns_and_ssl(request, ctx)

        self._track_event(request.task_id, TaskStatus.FINALIZING)
        self.finalize(request, ctx)

        return {
            "status": "success",
            "container_image": ctx.container_image,
            "droplet_ids": ctx.droplet_ids,
            "domain": request.domain,
            "duration_seconds": ctx.end_time - ctx.start_time,
        }

    async def clone_and_build(self, request: DeploymentRequest, ctx: DeploymentContext):
        repo_dir = f"/tmp/{request.task_id}"
        self.logger.info(f"Cloning {request.repo_url}@{request.repo_branch} into {repo_dir}")

        git_clone_cmd = ["git", "clone", "--branch", request.repo_branch, request.repo_url, repo_dir]
        await asyncio.to_thread(subprocess.run, git_clone_cmd, check=True, capture_output=True)

        image_tag = f"{request.container_registry}:{request.task_id}"
        build_cmd = f"docker build -t {image_tag} ."
        self.logger.info(f"Building container image {image_tag}")
        await asyncio.to_thread(subprocess.run, build_cmd, shell=True, cwd=repo_dir, check=True, capture_output=True)

        self.logger.info(f"Pushing container image to registry")
        push_cmd = f"docker push {image_tag}"
        await asyncio.to_thread(subprocess.run, push_cmd, shell=True, check=True, capture_output=True)

        ctx.container_image = image_tag

    async def provision_and_deploy(self, request: DeploymentRequest, ctx: DeploymentContext):
        provider = request.cloud_provider.lower()
        if provider == "digitalocean":
            await self._provision_droplets(request, ctx)
            await self._deploy_to_droplets(request, ctx)
        elif provider == "aws":
            await self._deploy_to_aws_ecs(request, ctx)
        else:
            raise ValueError(f"Unsupported cloud provider: {provider}")

    async def _get_ssh_key_path(self) -> str:
        private_key = await self.cred_store.get_secret("deploy_ssh_private_key", self.agent_id)
        fd, path = tempfile.mkstemp()
        os.write(fd, private_key.encode('utf-8'))
        os.close(fd)
        os.chmod(path, 0o600)
        return path

    async def _provision_droplets(self, request: DeploymentRequest, ctx: DeploymentContext):
        token = await self.cred_store.get_secret("digitalocean_api_key", self.agent_id)
        from digitalocean import Manager, Droplet

        def blocking_provision():
            mgr = Manager(token=token)
            size = request.infra_spec.get("size", "s-1vcpu-1gb")
            region = request.infra_spec.get("region", "nyc3")
            count = request.infra_spec.get("replicas", 1)
            self.logger.info(f"Provisioning {count} Droplet(s) on DigitalOcean")
            for i in range(count):
                drop = Droplet(token=token, name=f"{request.task_id}-{i}", region=region, image="docker-20-04", size_slug=size)
                drop.create()
                ctx.droplet_ids[f"droplet_{i}"] = drop.id

        await asyncio.to_thread(blocking_provision)

    async def _deploy_to_droplets(self, request: DeploymentRequest, ctx: DeploymentContext):
        self.logger.info("Deploying container to droplets via SSH")
        ssh_key_path = await self._get_ssh_key_path()
        token = await self.cred_store.get_secret("digitalocean_api_key", self.agent_id)
        from digitalocean import Manager

        def get_ip(droplet_id):
            mgr = Manager(token=token)
            drop = mgr.get_droplet(droplet_id)
            while not drop.ip_address:
                time.sleep(5)
                drop.load()
            return drop.ip_address

        for name, droplet_id in ctx.droplet_ids.items():
            ip = await asyncio.to_thread(get_ip, droplet_id)
            run_cmd = (
                f"ssh -i {ssh_key_path} -o StrictHostKeyChecking=no root@{ip} "
                f"'docker pull {ctx.container_image} && "
                f"docker run -d --restart always -e ENV={request.target_environment} "
                f"-p 80:80 {ctx.container_image}'"
            )
            await asyncio.to_thread(subprocess.run, run_cmd, shell=True, check=True, capture_output=True)

    async def _deploy_to_aws_ecs(self, request: DeploymentRequest, ctx: DeploymentContext):
        aws_key = await self.cred_store.get_secret("aws_key", self.agent_id)
        aws_secret = await self.cred_store.get_secret("aws_secret", self.agent_id)

        def blocking_ecs_deploy():
            import boto3
            ecs = boto3.client("ecs", aws_access_key_id=aws_key,
                               aws_secret_access_key=aws_secret)
            cluster = request.infra_spec.get("cluster", "default")
            task_def = {
                "family": request.task_id,
                "networkMode": "awsvpc",
                "containerDefinitions": [
                    {"name": request.task_id, "image": ctx.container_image, "essential": True,
                     "portMappings": [{"containerPort": 80, "hostPort": 80}]}
                ],
            }
            self.logger.info(f"Registering ECS task definition for {request.task_id}")
            ecs.register_task_definition(**task_def)
            self.logger.info(f"Running ECS task on cluster {cluster}")
            ecs.run_task(cluster=cluster, launchType="FARGATE", taskDefinition=request.task_id)

        await asyncio.to_thread(blocking_ecs_deploy)

    async def configure_dns_and_ssl(self, request: DeploymentRequest, ctx: DeploymentContext):
        if not request.ssl:
            return

        api_key = await self.cred_store.get_secret("cloudflare_api_token", self.agent_id)

        if not ctx.droplet_ids:
            self.logger.warning("No droplets provisioned, cannot configure DNS.")
            return

        first_droplet_id = next(iter(ctx.droplet_ids.values()))
        token = await self.cred_store.get_secret("digitalocean_api_key", self.agent_id)
        from digitalocean import Manager

        def get_ip(droplet_id):
            mgr = Manager(token=token)
            drop = mgr.get_droplet(droplet_id)
            while not drop.ip_address:
                time.sleep(5)
                drop.load()
            return drop.ip_address

        droplet_ip = await asyncio.to_thread(get_ip, first_droplet_id)

        def blocking_dns_config():
            import CloudFlare
            self.logger.info(f"Configuring DNS and SSL for domain {request.domain}")
            cf = CloudFlare.CloudFlare(token=api_key)

            domain_parts = request.domain.split('.')
            zone_name = '.'.join(domain_parts[-2:])

            try:
                zones = cf.zones.get(params={"name": zone_name})
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                self.logger.error(f"Could not get zones from Cloudflare: {e}")
                raise

            if not zones:
                raise ValueError(f"Could not find Cloudflare zone for domain {zone_name}")

            zone_id = zones[0]["id"]

            record = {"type": "A", "name": request.domain, "content": droplet_ip, "ttl": 3600}
            self.logger.info(f"Creating DNS A record for {request.domain} pointing to {droplet_ip}")
            resp = cf.zones.dns_records.post(zone_id, data=record)
            ctx.dns_record = resp

            ssl_resp = cf.zones.settings.ssl.get(zone_id)
            ctx.ssl_certificate_id = ssl_resp['value']
            self.logger.info(f"SSL mode for zone is {ctx.ssl_certificate_id}")

        await asyncio.to_thread(blocking_dns_config)

    def finalize(self, request: DeploymentRequest, ctx: DeploymentContext):
        ctx.end_time = time.time()
        duration = ctx.end_time - ctx.start_time
        self.logger.info(f"Deployment {request.task_id} completed in {duration:.2f}s")
        self._track_final_event(request.task_id, duration)

    def _track_event(self, task_id: str, status: TaskStatus):
        posthog.capture(task_id, "deployment_phase", properties={
            "agent_type": self.agent_type.value,
            "phase": status.value,
            "timestamp": time.time()
        })

    def _track_final_event(self, task_id: str, duration: float):
        posthog.capture(task_id, "deployment_completed", properties={
            "agent_type": self.agent_type.value,
            "execution_time": duration,
            "timestamp": time.time()
        })
