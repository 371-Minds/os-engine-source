import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketing_asst_agent import (
    MarketingAutomationAgent,
    ContentRequest,
    ContentType,
    PlatformType,
    SocialPost,
    SocialPlatform,
    PostType,
    EmailCampaign,
    EmailContact,
    EmailTemplate,
    EmailType,
    SegmentType,
    Task,
    GeneratedContent
)

# Mock Classes to simulate external dependencies
class MockAIContentCreator:
    async def generate_content(self, request: ContentRequest):
        print(f"--- Mock AI: Generating {request.content_type.value} for {request.topic} ---")
        return GeneratedContent(
            content_id=f"content_{datetime.now().timestamp()}",
            content_type=request.content_type,
            platform=request.platform,
            title=f"Mock Title for {request.topic}",
            body=f"This is mock content about {request.topic}. Brand voice: {request.brand_voice}",
            meta_data={"keywords": request.keywords},
            created_at=datetime.now(),
            approval_status="pending"
        )

class MockMultiPlatformPublisher:
    async def publish_post(self, post: SocialPost):
        print(f"--- Mock Publisher: Publishing post '{post.content[:30]}...' to {', '.join([p.value for p in post.platforms])} ---")
        return {platform: True for platform in post.platforms}

class MockDeliveryEngine:
    async def send_email(self, recipient: EmailContact, subject: str, html_content: str, campaign_id: str):
        print(f"--- Mock Email: Sending email '{subject}' to {recipient.email} ---")
        return True

async def run_benchmark():
    """
    Runs a benchmark of the MarketingAutomationAgent.
    """
    print("=========================================================")
    print("         Marketing Automation Agent Benchmark")
    print("=========================================================")
    print(f"Start Time: {datetime.now()}")
    print("---------------------------------------------------------")

    # 1. Initialize the Agent with Mock Dependencies
    print("\n[PHASE 1: INITIALIZATION]")
    agent = MarketingAutomationAgent(
        agent_id="benchmark_agent",
        ai_endpoint="mock_endpoint",
        brand_guidelines={"tone": "friendly", "values": ["innovation", "clarity"]},
        platform_settings={
            SocialPlatform.TWITTER: {"is_active": True, "access_token": "mock_token"},
            SocialPlatform.LINKEDIN: {"is_active": True, "access_token": "mock_token"}
        },
        email_provider_config={"api_key": "mock_key"}
    )
    # Replace systems with mock versions
    agent.content_generation_system.ai_creator = MockAIContentCreator()
    agent.social_media_system.publisher = MockMultiPlatformPublisher()
    agent.email_marketing_system.delivery_engine = MockDeliveryEngine()
    print("Agent initialized with mock dependencies.")
    print("---------------------------------------------------------")


    # 2. Test Content Generation
    print("\n[PHASE 2: CONTENT GENERATION]")
    content_task = Task(
        id="task_gen_001",
        agent_type=agent.agent_type,
        description="Generate blog post about AI in marketing",
        payload={
            "action": "generate_content",
            "request": {
                "content_type": ContentType.BLOG_ARTICLE,
                "topic": "The Future of AI in Marketing",
                "target_audience": "Tech enthusiasts",
                "brand_voice": "Informative and engaging",
                "keywords": ["AI", "Marketing", "Automation"],
                "context": {},
                "platform": PlatformType.MEDIUM,
                "length": 500,
                "call_to_action": "Subscribe to our newsletter"
            }
        }
    )
    print(f"Submitting content generation task: {content_task.payload['request']['topic']}")
    result = await agent.process_task(content_task)
    print(f"Content generation task successful. Content ID: {result.get('content_id')}")
    print("---------------------------------------------------------")


    # 3. Test Social Media Management
    print("\n[PHASE 3: SOCIAL MEDIA MANAGEMENT]")
    social_post_task = Task(
        id="task_soc_001",
        agent_type=agent.agent_type,
        description="Schedule a social media post",
        payload={
            "action": "schedule_social_post",
            "post": {
                "content": "Check out our new blog post on the future of AI in marketing!",
                "platforms": [SocialPlatform.TWITTER, SocialPlatform.LINKEDIN],
                "hashtags": ["AI", "MarTech"]
            }
        }
    )
    print(f"Submitting social media post task: {social_post_task.payload['post']['content']}")
    result = await agent.process_task(social_post_task)
    print(f"Social media post scheduled. Post ID: {result.get('post_id')}")

    # Verify scheduled post
    scheduled_posts = agent.social_media_system.get_scheduled_posts()
    print(f"Number of scheduled posts: {len(scheduled_posts)}")
    if scheduled_posts:
        print(f"Scheduled time for post: {scheduled_posts[0].scheduled_time}")
    print("---------------------------------------------------------")


    # 4. Test Email Marketing
    print("\n[PHASE 4: EMAIL MARKETING]")
    # Add a contact and a template first
    contact = EmailContact(
        email="test.subscriber@example.com",
        first_name="Test",
        last_name="Subscriber",
        segments=[SegmentType.NEW_SUBSCRIBERS]
    )
    agent.email_marketing_system.add_contact(contact)
    print(f"Added contact: {contact.email}")

    template = EmailTemplate(
        template_id="template_001",
        name="New Blog Post",
        email_type=EmailType.NEWSLETTER,
        subject_line="New Post: {{title}}",
        html_content="<h1>{{title}}</h1><p>Hi {{first_name}}, check out our new blog post!</p>",
        text_content="New Post: {{title}}. Hi {{first_name}}, check it out!",
        variables=["title", "first_name"]
    )
    agent.email_marketing_system.create_template(template)
    print(f"Created email template: {template.name}")

    email_campaign_task = Task(
        id="task_email_001",
        agent_type=agent.agent_type,
        description="Send an email campaign",
        payload={
            "action": "send_email_campaign",
            "campaign": {
                "campaign_id": "campaign_001",
                "name": "New Blog Promotion",
                "email_type": EmailType.NEWSLETTER,
                "template_id": "template_001",
                "target_segments": [SegmentType.NEW_SUBSCRIBERS],
                "send_time": datetime.now(),
                "personalization_rules": {"title": "The Future of AI in Marketing"}
            }
        }
    )
    print(f"Submitting email campaign task: {email_campaign_task.payload['campaign']['name']}")
    result = await agent.process_task(email_campaign_task)
    print("Email campaign task processed.")
    print(f"Metrics: {result.get('metrics')}")
    print("---------------------------------------------------------")

    print(f"\nEnd Time: {datetime.now()}")
    print("=========================================================")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
