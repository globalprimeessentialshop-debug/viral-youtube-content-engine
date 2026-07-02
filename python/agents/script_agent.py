"""
AGENT 2 - SCRIPT AGENT
Responsible for creating engaging video scripts based on viral patterns
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptAgent:
    """
    Script Creator Agent - Writes viral-optimized video scripts
    Takes project plan and creates engaging scripts with:
    - Hook (first 3 seconds)
    - Story/Content (middle)
    - Call-to-action (end)
    """

    def __init__(self):
        self.agent_name = "Script Agent"
        self.agent_role = "Script Creator"
        self.client = Anthropic()
        self.conversation_history = []
        self.scripts_created = 0

    async def create_script(self, project_plan: str) -> Dict[str, Any]:
        """
        Create engaging video script from project plan
        """
        logger.info(f"📝 {self.agent_name}: Creating video script...")

        prompt = f"""
        You are the Script Creator Agent for viral YouTube videos.
        
        PROJECT PLAN:
        {project_plan}
        
        Your task: Create a PROFESSIONAL, ENGAGING video script that:
        
        1. HOOK (0-3 seconds)
           - Immediate attention grabber
           - Reason to keep watching
           - Emotional trigger
        
        2. INTRODUCTION (3-10 seconds)
           - What the video is about
           - Promise of value
           - Why they should care
        
        3. MAIN CONTENT (10-80% of video)
           - Story-driven narrative
           - Clear progression
           - Emotional peaks
           - Visual cues for video team
           - [VISUAL: description] for animations/clips
        
        4. CALL-TO-ACTION (Last 5-10 seconds)
           - Clear action (subscribe, like, comment)
           - What to expect next
           - Urgency element
        
        5. RETENTION PATTERNS
           - Pattern interrupts every 5 seconds
           - Curiosity gaps
           - Reasons to not skip
        
        Return as JSON:
        {{
            "script_title": "",
            "estimated_duration": "minutes",
            "hook": "",
            "introduction": "",
            "main_content": "",
            "cta": "",
            "tone": "",
            "key_phrases": [],
            "visual_cues": [],
            "retention_techniques": [],
            "estimated_viral_score": 0-100,
            "full_script": "complete script text"
        }}
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        script_content = response.content[0].text
        self.scripts_created += 1

        self.conversation_history.append({
            "role": "script_agent",
            "action": "create_script",
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"✅ {self.agent_name}: Script created (#{self.scripts_created})")

        try:
            return json.loads(script_content)
        except:
            return {"script": script_content, "format": "text"}

    async def refine_script(self, script: Dict, feedback: str) -> Dict[str, Any]:
        """
        Refine script based on feedback
        """
        logger.info(f"🔄 {self.agent_name}: Refining script...")

        prompt = f"""
        Refine this script based on feedback:
        
        ORIGINAL SCRIPT:
        {json.dumps(script)}
        
        FEEDBACK:
        {feedback}
        
        Improve the script while maintaining viral appeal.
        Return updated JSON with same structure.
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        refined_script = response.content[0].text
        logger.info(f"✅ {self.agent_name}: Script refined")

        try:
            return json.loads(refined_script)
        except:
            return {"script": refined_script, "format": "text"}

    def get_agent_status(self) -> Dict:
        """Get current status"""
        return {
            "agent": self.agent_name,
            "role": self.agent_role,
            "scripts_created": self.scripts_created,
            "conversation_length": len(self.conversation_history)
        }
