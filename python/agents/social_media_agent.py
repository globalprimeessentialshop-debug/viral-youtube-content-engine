"""
AGENT 4 - SOCIAL MEDIA AGENT
Responsible for creating thumbnails, titles, descriptions, and social media assets
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaAgent:
    """
    Social Media Manager Agent - Creates engaging thumbnails and metadata
    Generates:
    - YouTube thumbnails (visual + text design)
    - Multiple title variations
    - Optimized descriptions
    - Tags and keywords
    - Social media posts (Twitter, Instagram, TikTok)
    """

    def __init__(self):
        self.agent_name = "Social Media Agent"
        self.agent_role = "Social Media Manager"
        self.client = Anthropic()
        self.conversation_history = []
        self.assets_created = 0

    async def create_social_assets(self, script: Dict, video_spec: Dict) -> Dict[str, Any]:
        """
        Create comprehensive social media assets
        """
        logger.info(f"📱 {self.agent_name}: Creating social media assets...")

        prompt = f"""
        You are the Social Media Manager Agent for viral YouTube content.
        
        SCRIPT:
        {json.dumps(script)}
        
        VIDEO SPEC:
        {json.dumps(video_spec)}
        
        Create COMPLETE SOCIAL MEDIA PACKAGE:
        
        1. YOUTUBE THUMBNAIL DESIGN
           - Color scheme (high contrast colors)
           - Main focal point (face/object/text)
           - Text overlay (max 3 words, readable on mobile)
           - Emotion/expression
           - Design principles (rule of thirds, bold colors)
        
        2. YOUTUBE TITLES (5 variations)
           - SEO optimized
           - Curiosity gap
           - Emotional trigger
           - Word count (50-60 characters ideal)
           - Include power words
        
        3. YOUTUBE DESCRIPTION
           - Hook (first 2-3 lines)
           - Full description (250-500 chars)
           - Timestamps
           - Links/CTAs
           - Hashtags (5-10)
        
        4. TAGS & KEYWORDS (20-30 tags)
           - Primary keywords
           - Long-tail keywords
           - Competitor keywords
           - Trending keywords
        
        5. SOCIAL MEDIA POSTS
           - Twitter (280 chars with hook and CTA)
           - Instagram caption (1000+ chars, story of video)
           - TikTok description (engaging, trending sounds)
           - LinkedIn version (professional angle)
        
        6. HASHTAG STRATEGY
           - Branded hashtag
           - Trending hashtags
           - Niche hashtags
           - Community hashtags
        
        Return as JSON:
        {{
            "thumbnail_design": {{}},
            "title_variations": [],
            "primary_title": "",
            "description": "",
            "timestamps": [],
            "tags": [],
            "keywords": [],
            "social_posts": {{}},
            "hashtags": {{}},
            "ctr_prediction": "0-100%",
            "viral_score_boost": "0-100%"
        }}
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        assets = response.content[0].text
        self.assets_created += 1

        self.conversation_history.append({
            "role": "social_media_agent",
            "action": "create_assets",
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"✅ {self.agent_name}: Social assets created (#{self.assets_created})")

        try:
            return json.loads(assets)
        except:
            return {"assets": assets, "format": "text"}

    async def optimize_for_ctr(self, assets: Dict, platform_metrics: Dict = None) -> Dict[str, Any]:
        """
        Optimize assets for Click-Through Rate
        """
        logger.info(f"🎯 {self.agent_name}: Optimizing for CTR...")

        prompt = f"""
        Optimize these social media assets for MAXIMUM click-through rate (CTR).
        
        CURRENT ASSETS:
        {json.dumps(assets)}
        
        Focus on:
        - Thumbnail visual appeal and clarity
        - Title curiosity gap and power words
        - Description compelling first 2 lines
        - Color psychology
        - Thumb-scroll optimization
        - Emotional triggers
        
        Return optimized assets as JSON.
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        optimized = response.content[0].text
        logger.info(f"✅ {self.agent_name}: CTR optimization complete")

        try:
            return json.loads(optimized)
        except:
            return {"optimized_assets": optimized, "format": "text"}

    def get_agent_status(self) -> Dict:
        """Get current status"""
        return {
            "agent": self.agent_name,
            "role": self.agent_role,
            "assets_created": self.assets_created,
            "conversation_length": len(self.conversation_history)
        }
