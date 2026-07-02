"""
MASTER AGENT (BRAIN) - OpenJarvis YouTube Content Engine
The central AI that orchestrates all agents and evolves 24/7
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from typing import Dict, List, Any
import logging

# AI Libraries
from anthropic import Anthropic
import openai

# Local imports
from agents.script_agent import ScriptAgent
from agents.video_content_agent import VideoContentAgent
from agents.social_media_agent import SocialMediaAgent
from agents.youtube_distributor_agent import YouTubeDistributorAgent
from utils.memory_system import MemorySystem
from utils.learning_engine import LearningEngine
from utils.decision_maker import DecisionMaker

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MasterBrainAgent:
    """
    Master Agent (Brain) - Orchestrates all agents and makes autonomous decisions
    Evolves 24/7 to optimize video creation and virality
    """

    def __init__(self):
        self.agent_name = "Master Brain Agent"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = Anthropic()
        
        # Initialize sub-agents
        self.script_agent = ScriptAgent()
        self.video_content_agent = VideoContentAgent()
        self.social_media_agent = SocialMediaAgent()
        self.youtube_distributor_agent = YouTubeDistributorAgent()
        
        # Initialize learning systems
        self.memory_system = MemorySystem()
        self.learning_engine = LearningEngine()
        self.decision_maker = DecisionMaker()
        
        # State tracking
        self.current_project = None
        self.agents_status = {}
        self.evolution_count = 0
        self.conversation_history = []
        
    def initialize_agents(self):
        """Initialize all sub-agents with current context"""
        logger.info("🧠 Master Brain: Initializing all agents...")
        
        agents_config = {
            "script_agent": {
                "role": "Script Creator",
                "description": "Writes engaging video scripts",
                "status": "ready"
            },
            "video_content_agent": {
                "role": "Video Content Creator",
                "description": "Creates video content from scripts",
                "status": "ready"
            },
            "social_media_agent": {
                "role": "Social Media Manager",
                "description": "Manages thumbnails, titles, descriptions",
                "status": "ready"
            },
            "youtube_distributor_agent": {
                "role": "YouTube Distributor",
                "description": "Distributes videos and attracts viewers",
                "status": "ready"
            }
        }
        
        self.agents_status = agents_config
        logger.info(f"✅ All agents initialized: {list(agents_config.keys())}")
        return agents_config

    async def analyze_top_5_videos(self) -> Dict[str, Any]:
        """
        Step 1: Analyze top 5 most popular videos
        Returns insights for recreation
        """
        logger.info("🔍 Master Brain: Analyzing top 5 YouTube videos...")
        
        prompt = f"""
        You are the Master Brain Agent of an autonomous AI system for viral YouTube video creation.
        
        TASK: Analyze the top 5 most popular YouTube videos and provide strategic insights.
        
        For each video, provide:
        1. Content themes and patterns
        2. Engagement triggers (emotional hooks, CTR elements)
        3. Video structure and pacing
        4. Audience demographics
        5. Viral potential factors
        
        Then provide a COMBINED strategy to recreate these videos in an improved, more engaging way.
        
        Return a JSON response with:
        {{
            "videos_analyzed": 5,
            "common_themes": [],
            "engagement_patterns": [],
            "recommended_content_type": "",
            "viral_score_prediction": 0-100,
            "suggested_improvements": [],
            "strategy": ""
        }}
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = response.content[0].text
        self.conversation_history.append({
            "role": "master",
            "action": "analyze_top_5",
            "response": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        return json.loads(analysis) if analysis.startswith("{") else {"analysis": analysis}

    async def create_project_plan(self, analysis: Dict) -> Dict[str, Any]:
        """
        Step 2: Create comprehensive project plan based on analysis
        Returns detailed plan for video creation
        """
        logger.info("📋 Master Brain: Creating project plan...")
        
        prompt = f"""
        Based on this analysis of top YouTube videos:
        {json.dumps(analysis)}
        
        Create a DETAILED PROJECT PLAN that includes:
        
        1. VIDEO CONCEPT
           - Title ideas (3 variations)
           - Content premise
           - Target audience
           - Expected viral potential
        
        2. SCRIPT REQUIREMENTS
           - Script length and pacing
           - Key talking points
           - Emotional hooks
           - Call-to-action strategy
        
        3. VIDEO PRODUCTION
           - Visual style
           - Footage requirements
           - Graphics and animations needed
           - Editing style
        
        4. THUMBNAIL & METADATA
           - Thumbnail concept
           - Title optimization
           - Description strategy
           - Tags strategy
        
        5. DISTRIBUTION STRATEGY
           - Post timing
           - Social media angles
           - Promotion plan
           - Engagement strategy
        
        Return as JSON with all details.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        plan = response.content[0].text
        self.current_project = plan
        
        self.conversation_history.append({
            "role": "master",
            "action": "create_plan",
            "response": plan,
            "timestamp": datetime.now().isoformat()
        })
        
        return {"plan": plan, "status": "pending_approval"}

    async def request_user_approval(self, plan: str) -> bool:
        """
        Step 3: Request user approval before proceeding
        Master waits for human approval
        """
        logger.info("⏸️  Master Brain: Requesting user approval...")
        
        print("\n" + "="*80)
        print("🧠 MASTER BRAIN AGENT - PROJECT PLAN REVIEW")
        print("="*80)
        print(f"\n{plan}\n")
        print("="*80)
        
        while True:
            user_input = input("\n✅ Do you APPROVE this plan? (yes/no): ").strip().lower()
            if user_input in ["yes", "y"]:
                logger.info("✅ User approved the project plan")
                return True
            elif user_input in ["no", "n"]:
                logger.info("❌ User rejected the project plan")
                feedback = input("Please provide feedback for improvement: ")
                self.memory_system.store_feedback(feedback)
                return False
            else:
                print("Please enter 'yes' or 'no'")

    async def orchestrate_agent_pipeline(self) -> Dict[str, Any]:
        """
        Step 4: Orchestrate all agents in sequence
        Each agent builds on previous agent's output
        """
        logger.info("🎬 Master Brain: Orchestrating agent pipeline...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "project": self.current_project,
            "agents_executed": []
        }
        
        # AGENT 1: Script Agent
        logger.info("→ Calling Script Agent...")
        script_output = await self.script_agent.create_script(self.current_project)
        results["script"] = script_output
        results["agents_executed"].append("script_agent")
        self.agents_status["script_agent"]["status"] = "completed"
        
        # AGENT 2: Video Content Agent
        logger.info("→ Calling Video Content Agent...")
        video_output = await self.video_content_agent.create_video(script_output)
        results["video"] = video_output
        results["agents_executed"].append("video_content_agent")
        self.agents_status["video_content_agent"]["status"] = "completed"
        
        # AGENT 3: Social Media Agent
        logger.info("→ Calling Social Media Agent...")
        social_output = await self.social_media_agent.create_social_assets(
            script_output, video_output
        )
        results["social"] = social_output
        results["agents_executed"].append("social_media_agent")
        self.agents_status["social_media_agent"]["status"] = "completed"
        
        # AGENT 4: YouTube Distributor Agent
        logger.info("→ Calling YouTube Distributor Agent...")
        distribution_output = await self.youtube_distributor_agent.distribute_video(
            video_output, social_output
        )
        results["distribution"] = distribution_output
        results["agents_executed"].append("youtube_distributor_agent")
        self.agents_status["youtube_distributor_agent"]["status"] = "completed"
        
        return results

    async def request_final_approval(self, results: Dict) -> bool:
        """
        Step 5: Request final approval before posting
        """
        logger.info("⏸️  Master Brain: Requesting final approval before posting...")
        
        print("\n" + "="*80)
        print("🧠 MASTER BRAIN AGENT - FINAL REVIEW BEFORE POSTING")
        print("="*80)
        print(f"\nProject Summary:")
        print(f"- Script: ✅ Complete")
        print(f"- Video Content: ✅ Complete")
        print(f"- Thumbnails & Metadata: ✅ Complete")
        print(f"- Distribution Strategy: ✅ Complete")
        
        print(f"\nKey Metrics:")
        print(f"- Predicted Viral Score: {results.get('viral_score', 'N/A')}")
        print(f"- Target Audience: {results.get('target_audience', 'N/A')}")
        print(f"- Expected Views (24h): {results.get('expected_views', 'N/A')}")
        
        print("\n" + "="*80)
        
        while True:
            user_input = input("\n✅ APPROVE posting this video? (yes/no): ").strip().lower()
            if user_input in ["yes", "y"]:
                logger.info("✅ User approved final posting")
                return True
            elif user_input in ["no", "n"]:
                logger.info("❌ User rejected final posting")
                feedback = input("Please provide feedback: ")
                self.memory_system.store_feedback(feedback)
                return False
            else:
                print("Please enter 'yes' or 'no'")

    async def evolve_knowledge(self):
        """
        24/7 Evolution - Master learns and improves decision-making
        """
        logger.info("🧬 Master Brain: Initiating evolution cycle...")
        
        self.evolution_count += 1
        
        evolution_prompt = f"""
        You are the Master Brain Agent evolution system.
        
        EVOLUTION CYCLE #{self.evolution_count}
        Current timestamp: {datetime.now().isoformat()}
        
        Based on all previous interactions and project outcomes, evolve the decision-making strategy:
        
        1. ANALYZE PERFORMANCE
           - Review success metrics of past projects
           - Identify patterns in viral vs. non-viral content
           - Assess agent performance
        
        2. IDENTIFY IMPROVEMENTS
           - What worked exceptionally well?
           - What can be optimized?
           - New strategies to test?
        
        3. UPDATE DECISION RULES
           - New heuristics for content evaluation
           - Improved script evaluation criteria
           - Better viral score prediction
        
        4. ENHANCED INSTRUCTIONS FOR SUB-AGENTS
           - More specific guidelines
           - Better quality standards
           - Improved collaboration methods
        
        Provide evolution insights as JSON.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": evolution_prompt}]
        )
        
        evolution_data = response.content[0].text
        self.learning_engine.store_evolution(evolution_data)
        
        logger.info(f"✅ Evolution cycle #{self.evolution_count} completed")
        return evolution_data

    async def run_autonomous_cycle(self):
        """
        Main autonomous cycle - Run complete pipeline
        """
        logger.info("\n" + "="*80)
        logger.info("🚀 MASTER BRAIN AGENT - STARTING AUTONOMOUS CYCLE")
        logger.info("="*80 + "\n")
        
        try:
            # Initialize agents
            self.initialize_agents()
            
            # Step 1: Analyze top videos
            analysis = await self.analyze_top_5_videos()
            logger.info(f"✅ Analysis complete: {analysis}")
            
            # Step 2: Create project plan
            plan_result = await self.create_project_plan(analysis)
            plan = plan_result["plan"]
            
            # Step 3: Request approval
            approved = await self.request_user_approval(plan)
            if not approved:
                logger.info("Project rejected. Retrying with improvements...")
                await self.evolve_knowledge()
                return
            
            # Step 4: Orchestrate agents
            results = await self.orchestrate_agent_pipeline()
            
            # Step 5: Request final approval
            final_approved = await self.request_final_approval(results)
            if not final_approved:
                logger.info("Final approval rejected. Storing feedback for evolution...")
                await self.evolve_knowledge()
                return
            
            logger.info("✅ Video successfully created and approved for posting!")
            
            # Step 6: Continuous evolution
            await self.evolve_knowledge()
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in autonomous cycle: {str(e)}")
            raise

    def get_agent_status(self) -> Dict:
        """Get current status of all agents"""
        return {
            "master_agent": "active",
            "evolution_cycles": self.evolution_count,
            "agents": self.agents_status,
            "conversation_history_length": len(self.conversation_history)
        }

    def save_session(self, filename: str = "master_brain_session.json"):
        """Save session data for continuity"""
        session_data = {
            "master_agent": self.agent_name,
            "evolution_count": self.evolution_count,
            "agents_status": self.agents_status,
            "conversation_history": self.conversation_history,
            "current_project": str(self.current_project),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"💾 Session saved to {filename}")


# Main execution
if __name__ == "__main__":
    master_brain = MasterBrainAgent()
    
    # Run autonomous cycle
    asyncio.run(master_brain.run_autonomous_cycle())
    
    # Save session
    master_brain.save_session()
    
    # Display final status
    print("\n" + "="*80)
    print("📊 MASTER BRAIN STATUS")
    print("="*80)
    print(json.dumps(master_brain.get_agent_status(), indent=2))
