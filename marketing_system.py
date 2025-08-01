from base_agent import BaseAgent, AgentType, Task, TaskStatus, AgentCapability
"""
371 Minds Operating System - Integrated Marketing Automation System

This module combines the functionality of content generation, social media management,
and email marketing into a single, cohesive system.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
import asyncio
from datetime import datetime, timedelta
import json

# ==============================================================================
# Content Generation System
# ==============================================================================

class ContentType(Enum):
    EMAIL = "email"
    SOCIAL_POST = "social_post"
    BLOG_ARTICLE = "blog_article"
    NEWSLETTER = "newsletter"
    MARKETING_COPY = "marketing_copy"
    VIDEO_SCRIPT = "video_script"

class PlatformType(Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    BLUESKY = "bluesky"
    SUBSTACK = "substack"
    MEDIUM = "medium"
    
@dataclass
class ContentRequest:
    content_type: ContentType
    platform: Optional[PlatformType]
    topic: str
    target_audience: str
    brand_voice: str
    length: Optional[int]
    call_to_action: Optional[str]
    keywords: List[str]
    context: Dict[str, Any]

@dataclass
class GeneratedContent:
    content_id: str
    content_type: ContentType
    platform: Optional[PlatformType]
    title: str
    body: str
    meta_data: Dict[str, Any]
    created_at: datetime
    approval_status: str = "pending"

class AIContentCreator:
    def __init__(self, ai_model_endpoint: str, brand_guidelines: Dict[str, Any]):
        self.ai_model_endpoint = ai_model_endpoint
        self.brand_guidelines = brand_guidelines

    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        # Construct AI prompt based on brand guidelines and request
        prompt = self._build_prompt(request)

        # Call AI model (placeholder for actual implementation)
        generated_text = await self._call_ai_model(prompt)

        # Apply brand voice and optimize
        optimized_content = self._apply_brand_voice(generated_text, request.brand_voice)

        return GeneratedContent(
            content_id=f"content_{datetime.now().timestamp()}",
            content_type=request.content_type,
            platform=request.platform,
            title=self._extract_title(optimized_content),
            body=optimized_content,
            meta_data={
                "keywords": request.keywords,
                "target_audience": request.target_audience,
                "estimated_engagement": self._predict_engagement(optimized_content)
            },
            created_at=datetime.now()
        )

    def _build_prompt(self, request: ContentRequest) -> str:
        base_prompt = f'''
        Create {request.content_type.value} content for {request.platform.value if request.platform else "general"} platform.

        Topic: {request.topic}
        Target Audience: {request.target_audience}
        Brand Voice: {request.brand_voice}
        Keywords to include: {", ".join(request.keywords)}

        Brand Guidelines:
        - Tone: {self.brand_guidelines.get("tone", "professional")}
        - Values: {self.brand_guidelines.get("values", [])}
        - Avoid: {self.brand_guidelines.get("avoid_words", [])}

        Requirements:
        - Length: {request.length or "optimal for platform"}
        - Call to Action: {request.call_to_action or "engage audience"}
        - Include relevant hashtags if applicable
        - Ensure content is engaging and conversion-focused
        '''

        return base_prompt

    async def _call_ai_model(self, prompt: str) -> str:
        # Placeholder for actual AI model call
        # In real implementation, this would call OpenAI, Claude, or local model
        return f"Generated content based on: {prompt[:100]}..."

    def _apply_brand_voice(self, content: str, brand_voice: str) -> str:
        # Apply brand voice transformations
        # This would include tone adjustments, terminology preferences, etc.
        return content

    def _extract_title(self, content: str) -> str:
        # Extract or generate title from content
        lines = content.split('\\n')
        return lines[0] if lines else "Generated Content"

    def _predict_engagement(self, content: str) -> float:
        # Placeholder for engagement prediction algorithm
        return 0.75  # 75% predicted engagement score

class TemplateEngine:
    def __init__(self):
        self.templates = {
            ContentType.EMAIL: {
                "welcome": "Welcome to {brand}! Here's what you can expect...",
                "newsletter": "This week in {industry}: {main_topics}",
                "promotional": "Special offer: {offer_details}"
            },
            ContentType.SOCIAL_POST: {
                "announcement": "🚀 Exciting news! {announcement_text}",
                "tip": "💡 Pro tip: {tip_content}",
                "behind_scenes": "Behind the scenes: {story_content}"
            }
        }

    def get_template(self, content_type: ContentType, template_name: str) -> str:
        return self.templates.get(content_type, {}).get(template_name, "")

    def apply_template(self, template: str, variables: Dict[str, str]) -> str:
        return template.format(**variables)

class ContentOptimizer:
    def __init__(self):
        self.platform_limits = {
            PlatformType.TWITTER: {"max_chars": 280, "hashtag_limit": 2},
            PlatformType.LINKEDIN: {"max_chars": 3000, "hashtag_limit": 5},
            PlatformType.INSTAGRAM: {"max_chars": 2200, "hashtag_limit": 30},
            PlatformType.FACEBOOK: {"max_chars": 63206, "hashtag_limit": 10}
        }

    def optimize_for_platform(self, content: GeneratedContent) -> GeneratedContent:
        if not content.platform:
            return content

        limits = self.platform_limits.get(content.platform, {})

        # Truncate if necessary
        if "max_chars" in limits and len(content.body) > limits["max_chars"]:
            content.body = content.body[:limits["max_chars"]-3] + "..."

        # Optimize hashtags
        if "hashtag_limit" in limits:
            content.body = self._optimize_hashtags(content.body, limits["hashtag_limit"])

        return content

    def _optimize_hashtags(self, content: str, limit: int) -> str:
        # Extract and limit hashtags
        import re
        hashtags = re.findall(r'#\\w+', content)
        if len(hashtags) > limit:
            # Keep most relevant hashtags
            content = re.sub(r'#\\w+', '', content)
            content += " " + " ".join(hashtags[:limit])
        return content

class ContentGenerationEngine:
    def __init__(self, ai_endpoint: str, brand_guidelines: Dict[str, Any]):
        self.ai_creator = AIContentCreator(ai_endpoint, brand_guidelines)
        self.template_engine = TemplateEngine()
        self.optimizer = ContentOptimizer()
        self.content_queue = []

    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        # Generate base content
        content = await self.ai_creator.generate_content(request)

        # Optimize for platform
        if request.platform:
            content = self.optimizer.optimize_for_platform(content)

        # Add to queue for approval
        self.content_queue.append(content)

        return content

    def get_pending_content(self) -> List[GeneratedContent]:
        return [c for c in self.content_queue if c.approval_status == "pending"]

    def approve_content(self, content_id: str) -> bool:
        for content in self.content_queue:
            if content.content_id == content_id:
                content.approval_status = "approved"
                return True
        return False

# ==============================================================================
# Social Media Management System
# ==============================================================================

class SocialPlatform(Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    THREADS = "threads"
    MASTODON = "mastodon"
    BLUESKY = "bluesky"
    SUBSTACK = "substack"
    MEDIUM = "medium"

class PostType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"
    POLL = "poll"

class PostStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

@dataclass
class MediaAsset:
    asset_id: str
    file_path: str
    asset_type: str  # image, video, gif
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    dimensions: Optional[Dict[str, int]] = None
    file_size: Optional[int] = None

@dataclass
class SocialPost:
    post_id: str
    content: str
    platforms: List[SocialPlatform]
    post_type: PostType
    media_assets: List[MediaAsset] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    scheduled_time: Optional[datetime] = None
    status: PostStatus = PostStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    engagement_data: Dict[SocialPlatform, Dict[str, int]] = field(default_factory=dict)

@dataclass
class PlatformSettings:
    platform: SocialPlatform
    is_active: bool
    access_token: str
    refresh_token: Optional[str] = None
    account_id: Optional[str] = None
    page_id: Optional[str] = None
    rate_limits: Dict[str, int] = field(default_factory=dict)
    last_post_time: Optional[datetime] = None

@dataclass
class EngagementMetrics:
    platform: SocialPlatform
    post_id: str
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0
    clicks: int = 0
    saves: int = 0
    reach: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class SocialPlatformOptimizer:
    def __init__(self):
        self.platform_specs = {
            SocialPlatform.TWITTER: {
                "max_chars": 280,
                "max_hashtags": 2,
                "image_specs": {"max_width": 1200, "max_height": 675, "formats": ["jpg", "png", "gif"]},
                "video_specs": {"max_duration": 140, "max_size_mb": 512}
            },
            SocialPlatform.LINKEDIN: {
                "max_chars": 3000,
                "max_hashtags": 5,
                "image_specs": {"max_width": 1200, "max_height": 627, "formats": ["jpg", "png"]},
                "video_specs": {"max_duration": 600, "max_size_mb": 200}
            },
            SocialPlatform.INSTAGRAM: {
                "max_chars": 2200,
                "max_hashtags": 30,
                "image_specs": {"aspect_ratios": ["1:1", "4:5", "16:9"], "formats": ["jpg", "png"]},
                "video_specs": {"max_duration": 60, "max_size_mb": 100}
            },
            SocialPlatform.FACEBOOK: {
                "max_chars": 63206,
                "max_hashtags": 10,
                "image_specs": {"max_width": 1200, "max_height": 630, "formats": ["jpg", "png"]},
                "video_specs": {"max_duration": 240, "max_size_mb": 1024}
            },
            SocialPlatform.TIKTOK: {
                "max_chars": 300,
                "max_hashtags": 100,
                "video_specs": {"aspect_ratio": "9:16", "max_duration": 180, "max_size_mb": 287}
            },
            SocialPlatform.YOUTUBE: {
                "title_max_chars": 100,
                "description_max_chars": 5000,
                "video_specs": {"max_duration": 43200, "max_size_gb": 256}  # 12 hours, 256GB
            }
        }

    def optimize_post_for_platform(self, post: SocialPost, platform: SocialPlatform) -> SocialPost:
        specs = self.platform_specs.get(platform, {})
        optimized_post = post

        # Optimize text length
        max_chars = specs.get("max_chars", float('inf'))
        if len(post.content) > max_chars:
            optimized_post.content = post.content[:max_chars-3] + "..."

        # Optimize hashtags
        max_hashtags = specs.get("max_hashtags", len(post.hashtags))
        if len(post.hashtags) > max_hashtags:
            optimized_post.hashtags = post.hashtags[:max_hashtags]

        # Platform-specific formatting
        if platform == SocialPlatform.LINKEDIN:
            optimized_post.content = self._format_for_linkedin(optimized_post.content)
        elif platform == SocialPlatform.TWITTER:
            optimized_post.content = self._format_for_twitter(optimized_post.content)
        elif platform == SocialPlatform.INSTAGRAM:
            optimized_post.content = self._format_for_instagram(optimized_post.content)

        return optimized_post

    def _format_for_linkedin(self, content: str) -> str:
        # Add professional tone markers
        if not content.endswith(('.', '!', '?')):
            content += '.'
        return content

    def _format_for_twitter(self, content: str) -> str:
        # Optimize for Twitter engagement
        return content

    def _format_for_instagram(self, content: str) -> str:
        # Add Instagram-style line breaks
        return content.replace('.', '.\\n\\n')

class ContentFormatter:
    def __init__(self):
        self.formatters = {
            SocialPlatform.LINKEDIN: self._format_linkedin,
            SocialPlatform.TWITTER: self._format_twitter,
            SocialPlatform.INSTAGRAM: self._format_instagram,
            SocialPlatform.FACEBOOK: self._format_facebook,
            SocialPlatform.TIKTOK: self._format_tiktok
        }

    def format_content(self, post: SocialPost, platform: SocialPlatform) -> str:
        formatter = self.formatters.get(platform, lambda x: x.content)
        return formatter(post)

    def _format_linkedin(self, post: SocialPost) -> str:
        content = post.content

        # Add hashtags at the end
        if post.hashtags:
            content += "\\n\\n" + " ".join(f"#{tag}" for tag in post.hashtags)

        return content

    def _format_twitter(self, post: SocialPost) -> str:
        content = post.content

        # Integrate hashtags naturally
        if post.hashtags:
            content += " " + " ".join(f"#{tag}" for tag in post.hashtags)

        return content

    def _format_instagram(self, post: SocialPost) -> str:
        content = post.content

        # Add hashtags in a separate paragraph
        if post.hashtags:
            content += "\\n\\n" + " ".join(f"#{tag}" for tag in post.hashtags)

        return content

    def _format_facebook(self, post: SocialPost) -> str:
        return post.content

    def _format_tiktok(self, post: SocialPost) -> str:
        content = post.content

        # TikTok loves hashtags
        if post.hashtags:
            content += " " + " ".join(f"#{tag}" for tag in post.hashtags)

        return content

class PostScheduler:
    def __init__(self):
        self.scheduled_posts = []
        self.optimal_times = {
            SocialPlatform.LINKEDIN: {
                "weekdays": [(9, 0), (12, 0), (17, 0)],  # 9 AM, 12 PM, 5 PM
                "weekends": [(10, 0), (14, 0)]  # 10 AM, 2 PM
            },
            SocialPlatform.TWITTER: {
                "weekdays": [(8, 0), (12, 0), (17, 0), (19, 0)],
                "weekends": [(9, 0), (13, 0), (15, 0)]
            },
            SocialPlatform.INSTAGRAM: {
                "weekdays": [(11, 0), (13, 0), (17, 0)],
                "weekends": [(10, 0), (13, 0), (16, 0)]
            },
            SocialPlatform.FACEBOOK: {
                "weekdays": [(9, 0), (15, 0)],
                "weekends": [(12, 0), (15, 0)]
            }
        }

    def schedule_post(self, post: SocialPost, optimal_timing: bool = True):
        if optimal_timing and not post.scheduled_time:
            post.scheduled_time = self._get_optimal_time(post.platforms[0])

        post.status = PostStatus.SCHEDULED
        self.scheduled_posts.append(post)

    def _get_optimal_time(self, platform: SocialPlatform) -> datetime:
        now = datetime.now()
        optimal_times = self.optimal_times.get(platform, {"weekdays": [(12, 0)]})

        # Get today's optimal times
        times = optimal_times["weekdays"] if now.weekday() < 5 else optimal_times["weekends"]

        # Find next optimal time
        for hour, minute in times:
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target_time > now:
                return target_time

        # If no time today, schedule for tomorrow's first optimal time
        tomorrow = now + timedelta(days=1)
        first_time = times[0]
        return tomorrow.replace(hour=first_time[0], minute=first_time[1], second=0, microsecond=0)

    async def process_scheduled_posts(self, publisher):
        now = datetime.now()

        for post in self.scheduled_posts[:]:  # Copy list to modify during iteration
            if post.scheduled_time and post.scheduled_time <= now:
                try:
                    await publisher.publish_post(post)
                    post.status = PostStatus.PUBLISHED
                    post.published_at = now
                    self.scheduled_posts.remove(post)
                except Exception as e:
                    post.status = PostStatus.FAILED
                    print(f"Failed to publish post {post.post_id}: {e}")

class MultiPlatformPublisher:
    def __init__(self, platform_settings: Dict[SocialPlatform, PlatformSettings]):
        self.platform_settings = platform_settings
        self.optimizer = SocialPlatformOptimizer()
        self.formatter = ContentFormatter()
        self.rate_limiters = {}

    async def publish_post(self, post: SocialPost) -> Dict[SocialPlatform, bool]:
        results = {}

        for platform in post.platforms:
            if platform not in self.platform_settings:
                results[platform] = False
                continue

            # Check rate limits
            if not self._check_rate_limit(platform):
                results[platform] = False
                continue

            # Optimize and format post
            optimized_post = self.optimizer.optimize_post_for_platform(post, platform)
            formatted_content = self.formatter.format_content(optimized_post, platform)

            # Publish to platform
            success = await self._publish_to_platform(platform, formatted_content, optimized_post.media_assets)
            results[platform] = success

            if success:
                self._update_rate_limit(platform)

        return results

    def _check_rate_limit(self, platform: SocialPlatform) -> bool:
        settings = self.platform_settings[platform]
        rate_limits = settings.rate_limits

        if not rate_limits or not settings.last_post_time:
            return True

        # Simple rate limiting check
        time_since_last = (datetime.now() - settings.last_post_time).total_seconds()
        min_interval = rate_limits.get("min_interval_seconds", 0)

        return time_since_last >= min_interval

    def _update_rate_limit(self, platform: SocialPlatform):
        self.platform_settings[platform].last_post_time = datetime.now()

    async def _publish_to_platform(self, platform: SocialPlatform, content: str, media_assets: List[MediaAsset]) -> bool:
        # Placeholder for actual platform API calls
        # In real implementation, this would integrate with each platform's API

        if platform == SocialPlatform.TWITTER:
            return await self._publish_to_twitter(content, media_assets)
        elif platform == SocialPlatform.LINKEDIN:
            return await self._publish_to_linkedin(content, media_assets)
        elif platform == SocialPlatform.INSTAGRAM:
            return await self._publish_to_instagram(content, media_assets)
        elif platform == SocialPlatform.FACEBOOK:
            return await self._publish_to_facebook(content, media_assets)
        elif platform == SocialPlatform.TIKTOK:
            return await self._publish_to_tiktok(content, media_assets)

        return False

    async def _publish_to_twitter(self, content: str, media_assets: List[MediaAsset]) -> bool:
        # Twitter API v2 integration
        print(f"Publishing to Twitter: {content[:50]}...")
        return True

    async def _publish_to_linkedin(self, content: str, media_assets: List[MediaAsset]) -> bool:
        # LinkedIn API integration
        print(f"Publishing to LinkedIn: {content[:50]}...")
        return True

    async def _publish_to_instagram(self, content: str, media_assets: List[MediaAsset]) -> bool:
        # Instagram Basic Display API integration
        print(f"Publishing to Instagram: {content[:50]}...")
        return True

    async def _publish_to_facebook(self, content: str, media_assets: List[MediaAsset]) -> bool:
        # Facebook Graph API integration
        print(f"Publishing to Facebook: {content[:50]}...")
        return True

    async def _publish_to_tiktok(self, content: str, media_assets: List[MediaAsset]) -> bool:
        # TikTok API integration
        print(f"Publishing to TikTok: {content[:50]}...")
        return True

class EngagementMonitor:
    def __init__(self):
        self.metrics = []
        self.monitoring_active = False

    async def start_monitoring(self, published_posts: List[SocialPost]):
        self.monitoring_active = True

        while self.monitoring_active:
            for post in published_posts:
                if post.status == PostStatus.PUBLISHED:
                    for platform in post.platforms:
                        metrics = await self._fetch_engagement_metrics(platform, post.post_id)
                        if metrics:
                            self.metrics.append(metrics)
                            post.engagement_data[platform] = {
                                "likes": metrics.likes,
                                "shares": metrics.shares,
                                "comments": metrics.comments,
                                "views": metrics.views,
                                "reach": metrics.reach
                            }

            # Wait before next monitoring cycle
            await asyncio.sleep(3600)  # Check every hour

    async def _fetch_engagement_metrics(self, platform: SocialPlatform, post_id: str) -> Optional[EngagementMetrics]:
        # Placeholder for actual API calls to fetch metrics
        # Would integrate with each platform's analytics API

        # Simulate metrics
        import random
        return EngagementMetrics(
            platform=platform,
            post_id=post_id,
            likes=random.randint(10, 1000),
            shares=random.randint(1, 100),
            comments=random.randint(0, 50),
            views=random.randint(100, 10000),
            reach=random.randint(500, 50000),
            engagement_rate=random.uniform(0.01, 0.15)
        )

    def get_metrics_summary(self, post_id: str) -> Dict[SocialPlatform, EngagementMetrics]:
        post_metrics = {}
        for metric in self.metrics:
            if metric.post_id == post_id:
                post_metrics[metric.platform] = metric
        return post_metrics

class SocialMediaSystem:
    def __init__(self, platform_settings: Dict[SocialPlatform, PlatformSettings]):
        self.platform_settings = platform_settings
        self.posts = []

        self.optimizer = SocialPlatformOptimizer()
        self.scheduler = PostScheduler()
        self.publisher = MultiPlatformPublisher(platform_settings)
        self.engagement_monitor = EngagementMonitor()

        # Start background tasks
        asyncio.create_task(self._background_processor())

    def create_post(self, content: str, platforms: List[SocialPlatform], post_type: PostType = PostType.TEXT,
                   media_assets: List[MediaAsset] = None, hashtags: List[str] = None) -> SocialPost:
        post = SocialPost(
            post_id=f"post_{datetime.now().timestamp()}",
            content=content,
            platforms=platforms,
            post_type=post_type,
            media_assets=media_assets or [],
            hashtags=hashtags or []
        )

        self.posts.append(post)
        return post

    def schedule_post(self, post: SocialPost, scheduled_time: Optional[datetime] = None):
        if scheduled_time:
            post.scheduled_time = scheduled_time

        self.scheduler.schedule_post(post, optimal_timing=scheduled_time is None)

    async def publish_immediately(self, post: SocialPost) -> Dict[SocialPlatform, bool]:
        results = await self.publisher.publish_post(post)

        if any(results.values()):
            post.status = PostStatus.PUBLISHED
            post.published_at = datetime.now()
        else:
            post.status = PostStatus.FAILED

        return results

    def get_post_analytics(self, post_id: str) -> Dict[SocialPlatform, EngagementMetrics]:
        return self.engagement_monitor.get_metrics_summary(post_id)

    def get_scheduled_posts(self) -> List[SocialPost]:
        return [post for post in self.posts if post.status == PostStatus.SCHEDULED]

    def get_published_posts(self) -> List[SocialPost]:
        return [post for post in self.posts if post.status == PostStatus.PUBLISHED]

    async def _background_processor(self):
        while True:
            # Process scheduled posts
            await self.scheduler.process_scheduled_posts(self.publisher)

            # Update engagement metrics
            published_posts = self.get_published_posts()
            if published_posts and not self.engagement_monitor.monitoring_active:
                asyncio.create_task(self.engagement_monitor.start_monitoring(published_posts))

            # Wait before next cycle
            await asyncio.sleep(60)  # Check every minute

# ==============================================================================
# Email Marketing System
# ==============================================================================

class EmailType(Enum):
    WELCOME = "welcome"
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"
    TRANSACTIONAL = "transactional"
    NURTURE_SEQUENCE = "nurture_sequence"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT = "re_engagement"

class SegmentType(Enum):
    NEW_SUBSCRIBERS = "new_subscribers"
    ACTIVE_USERS = "active_users"
    DORMANT_USERS = "dormant_users"
    HIGH_VALUE = "high_value"
    CUSTOM = "custom"

@dataclass
class EmailContact:
    email: str
    first_name: str
    last_name: str
    segments: List[SegmentType]
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    subscription_date: datetime = field(default_factory=datetime.now)
    last_interaction: Optional[datetime] = None
    engagement_score: float = 0.0
    is_active: bool = True

@dataclass
class EmailTemplate:
    template_id: str
    name: str
    email_type: EmailType
    subject_line: str
    html_content: str
    text_content: str
    variables: List[str]
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class EmailCampaign:
    campaign_id: str
    name: str
    email_type: EmailType
    template_id: str
    target_segments: List[SegmentType]
    send_time: datetime
    personalization_rules: Dict[str, Any]
    ab_test_config: Optional[Dict[str, Any]] = None
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class EmailMetrics:
    campaign_id: str
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    unsubscribed_count: int
    bounced_count: int
    spam_count: int
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def open_rate(self) -> float:
        return (self.opened_count / self.delivered_count) if self.delivered_count > 0 else 0.0

    @property
    def click_rate(self) -> float:
        return (self.clicked_count / self.delivered_count) if self.delivered_count > 0 else 0.0

    @property
    def unsubscribe_rate(self) -> float:
        return (self.unsubscribed_count / self.delivered_count) if self.delivered_count > 0 else 0.0

class SegmentationEngine:
    def __init__(self):
        self.segment_rules = {
            SegmentType.NEW_SUBSCRIBERS: lambda contact: (datetime.now() - contact.subscription_date).days <= 30,
            SegmentType.ACTIVE_USERS: lambda contact: contact.last_interaction and (datetime.now() - contact.last_interaction).days <= 30,
            SegmentType.DORMANT_USERS: lambda contact: not contact.last_interaction or (datetime.now() - contact.last_interaction).days > 90,
            SegmentType.HIGH_VALUE: lambda contact: contact.engagement_score > 0.8
        }

    def segment_contacts(self, contacts: List[EmailContact]) -> Dict[SegmentType, List[EmailContact]]:
        segments = {}

        for segment_type, rule in self.segment_rules.items():
            segments[segment_type] = [contact for contact in contacts if rule(contact)]

        return segments

    def create_custom_segment(self, name: str, rule: Callable[[EmailContact], bool]) -> SegmentType:
        custom_segment = SegmentType.CUSTOM
        self.segment_rules[custom_segment] = rule
        return custom_segment

class PersonalizationEngine:
    def __init__(self):
        self.personalization_rules = {}

    def personalize_content(self, template: EmailTemplate, contact: EmailContact) -> tuple[str, str]:
        # Personalize subject line
        subject = self._apply_personalization(template.subject_line, contact)

        # Personalize content
        html_content = self._apply_personalization(template.html_content, contact)

        return subject, html_content

    def _apply_personalization(self, content: str, contact: EmailContact) -> str:
        # Replace basic variables
        content = content.replace("{{first_name}}", contact.first_name)
        content = content.replace("{{last_name}}", contact.last_name)
        content = content.replace("{{email}}", contact.email)

        # Apply custom field replacements
        for field, value in contact.custom_fields.items():
            content = content.replace(f"{{{{{field}}}}}", str(value))

        # Apply dynamic content based on segments
        if SegmentType.HIGH_VALUE in contact.segments:
            content = content.replace("{{tier_content}}", "As a valued customer, here's an exclusive offer...")
        elif SegmentType.NEW_SUBSCRIBERS in contact.segments:
            content = content.replace("{{tier_content}}", "Welcome! Here's everything you need to know...")

        return content

class ABTestManager:
    def __init__(self):
        self.active_tests = {}

    def create_ab_test(self, campaign: EmailCampaign, variant_a: Dict[str, Any], variant_b: Dict[str, Any], split_ratio: float = 0.5) -> str:
        test_id = f"test_{campaign.campaign_id}_{datetime.now().timestamp()}"

        self.active_tests[test_id] = {
            "campaign_id": campaign.campaign_id,
            "variant_a": variant_a,
            "variant_b": variant_b,
            "split_ratio": split_ratio,
            "results": {"a": {"sent": 0, "opened": 0, "clicked": 0}, "b": {"sent": 0, "opened": 0, "clicked": 0}}
        }

        return test_id

    def determine_variant(self, test_id: str, contact: EmailContact) -> str:
        import hashlib

        # Use email hash to consistently assign variant
        hash_val = int(hashlib.md5(contact.email.encode()).hexdigest(), 16)
        test = self.active_tests[test_id]

        return "a" if (hash_val % 100) < (test["split_ratio"] * 100) else "b"

    def record_interaction(self, test_id: str, variant: str, interaction_type: str):
        if test_id in self.active_tests:
            self.active_tests[test_id]["results"][variant][interaction_type] += 1

class DeliveryEngine:
    def __init__(self, email_provider_config: Dict[str, Any]):
        self.provider_config = email_provider_config
        self.delivery_queue = []
        self.rate_limits = {
            "per_second": 10,
            "per_minute": 600,
            "per_hour": 36000
        }

    async def send_email(self, recipient: EmailContact, subject: str, html_content: str, campaign_id: str) -> bool:
        # Check rate limits
        if not self._check_rate_limits():
            # Queue for later delivery
            self.delivery_queue.append({
                "recipient": recipient,
                "subject": subject,
                "html_content": html_content,
                "campaign_id": campaign_id,
                "queued_at": datetime.now()
            })
            return False

        # Send email via provider
        success = await self._send_via_provider(recipient, subject, html_content)

        if success:
            # Update contact interaction
            recipient.last_interaction = datetime.now()

        return success

    def _check_rate_limits(self) -> bool:
        # Implement rate limiting logic
        # This is a placeholder - real implementation would track actual rates
        return True

    async def _send_via_provider(self, recipient: EmailContact, subject: str, html_content: str) -> bool:
        # Placeholder for actual email provider integration
        # Would integrate with SendGrid, Mailgun, AWS SES, Resend, etc.
        print(f"Sending email to {recipient.email}: {subject}")
        return True

    async def process_queue(self):
        while self.delivery_queue:
            if self._check_rate_limits():
                email_data = self.delivery_queue.pop(0)
                await self._send_via_provider(
                    email_data["recipient"],
                    email_data["subject"],
                    email_data["html_content"]
                )
            else:
                await asyncio.sleep(1)  # Wait before checking again

class WorkflowEngine:
    def __init__(self):
        self.workflows = {}
        self.triggers = {}

    def create_workflow(self, name: str, trigger: str, actions: List[Dict[str, Any]]) -> str:
        workflow_id = f"workflow_{datetime.now().timestamp()}"

        self.workflows[workflow_id] = {
            "name": name,
            "trigger": trigger,
            "actions": actions,
            "is_active": True
        }

        # Register trigger
        if trigger not in self.triggers:
            self.triggers[trigger] = []
        self.triggers[trigger].append(workflow_id)

        return workflow_id

    async def execute_workflow(self, workflow_id: str, context: Dict[str, Any]):
        workflow = self.workflows.get(workflow_id)
        if not workflow or not workflow["is_active"]:
            return

        for action in workflow["actions"]:
            await self._execute_action(action, context)

    async def _execute_action(self, action: Dict[str, Any], context: Dict[str, Any]):
        action_type = action.get("type")

        if action_type == "send_email":
            # Queue email for sending
            pass
        elif action_type == "add_to_segment":
            # Add contact to segment
            pass
        elif action_type == "wait":
            # Wait for specified time
            await asyncio.sleep(action.get("duration", 0))

class EmailMarketingSystem:
    def __init__(self, email_provider_config: Dict[str, Any]):
        self.contacts = []
        self.templates = []
        self.campaigns = []

        self.segmentation_engine = SegmentationEngine()
        self.personalization_engine = PersonalizationEngine()
        self.ab_test_manager = ABTestManager()
        self.delivery_engine = DeliveryEngine(email_provider_config)
        self.workflow_engine = WorkflowEngine()

        self.metrics_store = []

    def add_contact(self, contact: EmailContact):
        self.contacts.append(contact)

        # Auto-segment the contact
        segments = self.segmentation_engine.segment_contacts([contact])
        for segment_type, contacts in segments.items():
            if contact in contacts:
                contact.segments.append(segment_type)

    def create_template(self, template: EmailTemplate):
        self.templates.append(template)

    def create_campaign(self, campaign: EmailCampaign) -> str:
        self.campaigns.append(campaign)
        return campaign.campaign_id

    async def send_campaign(self, campaign_id: str) -> EmailMetrics:
        campaign = next((c for c in self.campaigns if c.campaign_id == campaign_id), None)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        template = next((t for t in self.templates if t.template_id == campaign.template_id), None)
        if not template:
            raise ValueError(f"Template {campaign.template_id} not found")

        # Get target contacts
        target_contacts = []
        for contact in self.contacts:
            if any(segment in contact.segments for segment in campaign.target_segments):
                target_contacts.append(contact)

        metrics = EmailMetrics(
            campaign_id=campaign_id,
            sent_count=0,
            delivered_count=0,
            opened_count=0,
            clicked_count=0,
            unsubscribed_count=0,
            bounced_count=0,
            spam_count=0
        )

        # Send to each contact
        for contact in target_contacts:
            if not contact.is_active:
                continue

            # Personalize content
            subject, html_content = self.personalization_engine.personalize_content(template, contact)

            # Handle A/B testing
            if campaign.ab_test_config:
                test_id = campaign.ab_test_config.get("test_id")
                variant = self.ab_test_manager.determine_variant(test_id, contact)

                if variant == "b":
                    subject = campaign.ab_test_config["variant_b"]["subject"]
                    html_content = campaign.ab_test_config["variant_b"]["content"]

            # Send email
            success = await self.delivery_engine.send_email(contact, subject, html_content, campaign_id)

            if success:
                metrics.sent_count += 1
                metrics.delivered_count += 1  # Simplified - would track actual delivery

        self.metrics_store.append(metrics)
        campaign.status = "sent"

        return metrics

    def get_campaign_metrics(self, campaign_id: str) -> Optional[EmailMetrics]:
        return next((m for m in self.metrics_store if m.campaign_id == campaign_id), None)

    def create_nurture_sequence(self, name: str, emails: List[Dict[str, Any]], segment: SegmentType):
        # Create automated email sequence
        workflow_actions = []

        for i, email_config in enumerate(emails):
            if i > 0:
                workflow_actions.append({"type": "wait", "duration": email_config.get("delay", 86400)})  # 1 day default

            workflow_actions.append({
                "type": "send_email",
                "template_id": email_config["template_id"],
                "personalization": email_config.get("personalization", {})
            })

        return self.workflow_engine.create_workflow(
            name=name,
            trigger=f"segment_added_{segment.value}",
            actions=workflow_actions
        )

# ==============================================================================
# Master Marketing Automation Agent
# ==============================================================================

class MarketingAutomationAgent(BaseAgent):
    """
    An integrated agent that orchestrates content generation, social media,
    and email marketing systems.
    """
    def __init__(self, agent_id: str = "marketing_agent_001",
                 ai_endpoint: str = "",
                 brand_guidelines: Dict[str, Any] = None,
                 platform_settings: Dict[SocialPlatform, PlatformSettings] = None,
                 email_provider_config: Dict[str, Any] = None):

        capabilities = [
            AgentCapability(name="generate_marketing_content", description="Generate content for various platforms."),
            AgentCapability(name="manage_social_media", description="Create, schedule, and publish social media posts."),
            AgentCapability(name="execute_email_campaigns", description="Design and send email marketing campaigns."),
            AgentCapability(name="run_full_marketing_campaign", description="Orchestrate a complete marketing campaign from content creation to distribution.")
        ]

        super().__init__(agent_id, AgentType.MARKETING_ASSET, capabilities)

        self.content_generation_system = ContentGenerationEngine(ai_endpoint, brand_guidelines or {})
        self.social_media_system = SocialMediaSystem(platform_settings or {})
        self.email_marketing_system = EmailMarketingSystem(email_provider_config or {})

    async def process_task(self, task: Task) -> Dict[str, Any]:
        """Process a marketing task by routing to the appropriate subsystem."""
        action = task.payload.get("action")

        if action == "generate_content":
            request = ContentRequest(**task.payload["request"])
            content = await self.content_generation_system.generate_content(request)
            return {"status": "success", "content_id": content.content_id}

        elif action == "schedule_social_post":
            post_details = task.payload["post"]
            post = self.social_media_system.create_post(**post_details)
            self.social_media_system.schedule_post(post)
            return {"status": "scheduled", "post_id": post.post_id}

        elif action == "send_email_campaign":
            campaign_details = task.payload["campaign"]
            campaign = EmailCampaign(**campaign_details)
            self.email_marketing_system.create_campaign(campaign)
            metrics = await self.email_marketing_system.send_campaign(campaign.campaign_id)
            return {"status": "sent", "metrics": metrics.__dict__}

        else:
            raise ValueError(f"Unknown marketing action: {action}")

    async def health_check(self) -> bool:
        # For now, we assume the subsystems are healthy if they exist.
        # A more robust check would test each subsystem's health.
        return all([
            self.content_generation_system is not None,
            self.social_media_system is not None,
            self.email_marketing_system is not None
        ])
