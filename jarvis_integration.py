"""
OpenJarvis Integration Module
Enables direct communication between OpenJarvis and Master Brain Agent
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Master Brain
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from python.agents.master_brain_agent import MasterBrainAgent
from jarvis_config import JARVIS_CONFIG


class JarvisIntegration:
    """
    Integration layer between OpenJarvis and Master Brain Agent
    Handles conversation routing, approval workflow, and monitoring
    """

    def __init__(self):
        self.config = JARVIS_CONFIG
        self.master_brain = None
        self.conversation_history = []
        self.current_project = None
        self.approval_pending = False
        self.monitoring_active = False
        self.agent_status = {}

    async def initialize(self) -> bool:
        """
        Initialize Jarvis integration and Master Brain
        """
        logger.info("🤖 Initializing OpenJarvis Integration...")
        
        try:
            self.master_brain = MasterBrainAgent()
            self.master_brain.initialize_agents()
            logger.info("✅ Master Brain initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {str(e)}")
            return False

    def process_voice_command(self, command: str) -> str:
        """
        Process voice commands from OpenJarvis
        Routes to appropriate action
        """
        logger.info(f"🎤 Processing command: {command}")
        
        command_lower = command.lower()
        
        # Check conversation triggers
        for trigger_type, keywords in self.config["conversation_triggers"].items():
            if any(keyword in command_lower for keyword in keywords):
                logger.info(f"🎯 Triggered: {trigger_type}")
                return trigger_type
        
        return "unknown"

    async def handle_master_brain_request(self) -> Dict[str, Any]:
        """
        Main entry point: User says 'Jarvis' or 'Open Jarvis'
        Starts the Master Brain workflow
        """
        logger.info("\n" + "="*80)
        logger.info("🧠 MASTER BRAIN AGENT ACTIVATED")
        logger.info("="*80 + "\n")
        
        print("""
        ╔════════════════════════════════════════════════════════════════════════╗
        ║                   🧠 MASTER BRAIN AGENT - JARVIS                       ║
        ║             Welcome! I'm ready to create viral YouTube videos          ║
        ╚════════════════════════════════════════════════════════════════════════╝
        
        What would you like me to do?
        
        1. 📊 Analyze top YouTube videos in a category
        2. 📋 Create a new video project plan
        3. 🎬 Execute the full agent pipeline
        4. 📈 Show real-time status of agents
        5. 💾 Show my evolution progress
        6. ❌ Cancel current project
        
        Type your choice or command:
        """)
        
        user_input = input("You: ").strip()
        return await self.route_command(user_input)

    async def route_command(self, command: str) -> Dict[str, Any]:
        """
        Route user command to appropriate action
        """
        command_lower = command.lower()
        
        if any(x in command_lower for x in ["1", "analyze", "research"]):
            return await self.start_analysis()
        elif any(x in command_lower for x in ["2", "create", "project"]):
            return await self.start_planning()
        elif any(x in command_lower for x in ["3", "execute", "pipeline"]):
            return await self.execute_pipeline()
        elif any(x in command_lower for x in ["4", "status", "show"]):
            return await self.show_status()
        elif any(x in command_lower for x in ["5", "evolution", "progress"]):
            return await self.show_evolution()
        elif any(x in command_lower for x in ["6", "cancel"]):
            return self.cancel_project()
        else:
            return {"status": "unknown_command", "message": "I didn't understand. Please try again."}

    async def start_analysis(self) -> Dict[str, Any]:
        """
        Start video analysis workflow
        """
        logger.info("📊 Starting video analysis...")
        
        print("\n📊 VIDEO ANALYSIS MODE")
        print("="*50)
        
        category = input("What category? (e.g., technology, gaming, education): ").strip()
        audience = input("Target audience description: ").strip()
        
        if not category:
            return {"status": "error", "message": "Category required"}
        
        self.start_monitoring()
        
        try:
            print(f"\n🔍 Analyzing top 5 videos in '{category}' for {audience}...\n")
            analysis = await self.master_brain.analyze_top_5_videos()
            
            self.conversation_history.append({
                "action": "analysis",
                "category": category,
                "audience": audience,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "status": "success",
                "action": "analysis",
                "data": analysis,
                "next_step": "Would you like me to create a project plan based on this analysis?"
            }
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            self.stop_monitoring()

    async def start_planning(self) -> Dict[str, Any]:
        """
        Start project planning workflow
        """
        logger.info("📋 Starting project planning...")
        
        print("\n📋 PROJECT PLANNING MODE")
        print("="*50)
        
        theme = input("Content theme/idea: ").strip()
        target_subs = input("Target subscriber count: ").strip()
        video_length = input("Video length (minutes): ").strip()
        
        if not theme:
            return {"status": "error", "message": "Theme required"}
        
        self.start_monitoring()
        
        try:
            print(f"\n📋 Creating project plan for '{theme}'...\n")
            
            # Run analysis first
            analysis = await self.master_brain.analyze_top_5_videos()
            
            # Create plan
            plan_result = await self.master_brain.create_project_plan(analysis)
            plan = plan_result["plan"]
            
            self.current_project = plan
            self.approval_pending = True
            
            self.conversation_history.append({
                "action": "planning",
                "theme": theme,
                "target_subs": target_subs,
                "timestamp": datetime.now().isoformat()
            })
            
            print("\n" + "="*80)
            print("📋 PROJECT PLAN CREATED - AWAITING YOUR APPROVAL")
            print("="*80)
            print(f"\n{plan}\n")
            print("="*80)
            
            return {
                "status": "pending_approval",
                "action": "planning",
                "plan": plan,
                "approval_required": True,
                "next_action": "Do you approve this plan? (yes/no)"
            }
        except Exception as e:
            logger.error(f"❌ Planning failed: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            self.stop_monitoring()

    async def execute_pipeline(self) -> Dict[str, Any]:
        """
        Execute full agent pipeline
        Requires prior approval
        """
        if not self.approval_pending or not self.current_project:
            return {
                "status": "error",
                "message": "No project plan approved. Please create a plan first."
            }
        
        logger.info("🎬 Executing agent pipeline...")
        
        self.start_monitoring()
        
        try:
            print("\n" + "="*80)
            print("🎬 EXECUTING AGENT PIPELINE")
            print("="*80 + "\n")
            
            results = await self.master_brain.orchestrate_agent_pipeline()
            
            # Request final approval
            final_approval = await self.master_brain.request_final_approval(results)
            
            if final_approval:
                self.approval_pending = False
                logger.info("✅ Pipeline executed successfully")
                return {
                    "status": "success",
                    "action": "pipeline_execution",
                    "results": results,
                    "message": "All agents completed successfully!"
                }
            else:
                logger.info("❌ Final approval rejected")
                return {
                    "status": "rejected",
                    "message": "Final approval rejected. Feedback stored for evolution."
                }
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            self.stop_monitoring()

    async def show_status(self) -> Dict[str, Any]:
        """
        Show real-time status of all agents
        """
        logger.info("📊 Showing agent status...")
        
        status = self.master_brain.get_agent_status()
        
        print("\n" + "="*80)
        print("📊 REAL-TIME AGENT STATUS")
        print("="*80)
        print(json.dumps(status, indent=2))
        print("="*80 + "\n")
        
        return {
            "status": "success",
            "data": status
        }

    async def show_evolution(self) -> Dict[str, Any]:
        """
        Show Master Brain evolution progress
        """
        logger.info("🧬 Showing evolution progress...")
        
        evolution_data = await self.master_brain.evolve_knowledge()
        
        print("\n" + "="*80)
        print("🧬 MASTER BRAIN EVOLUTION PROGRESS")
        print("="*80)
        print(f"Evolution Cycle: #{self.master_brain.evolution_count}")
        print(f"\n{evolution_data}\n")
        print("="*80 + "\n")
        
        return {
            "status": "success",
            "evolution_cycle": self.master_brain.evolution_count,
            "data": evolution_data
        }

    def cancel_project(self) -> Dict[str, Any]:
        """
        Cancel current project
        """
        logger.info("❌ Canceling project...")
        
        self.current_project = None
        self.approval_pending = False
        
        return {
            "status": "cancelled",
            "message": "Project cancelled. Ready for new project."
        }

    def start_monitoring(self) -> None:
        """
        Start real-time agent monitoring
        """
        self.monitoring_active = True
        logger.info("📡 Real-time monitoring started")

    def stop_monitoring(self) -> None:
        """
        Stop real-time monitoring
        """
        self.monitoring_active = False
        logger.info("📡 Real-time monitoring stopped")

    def get_conversation_history(self) -> List[Dict]:
        """
        Get conversation history
        """
        return self.conversation_history

    async def run_interactive_session(self) -> None:
        """
        Run interactive Jarvis session
        """
        print("""
        ╔═══════════════════════════════════════════════════════════════════════╗
        ║                                                                       ║
        ║              🤖 Welcome to OpenJarvis + Master Brain 🧠              ║
        ║                                                                       ║
        ║        Say "Jarvis" or "Open Jarvis" to start creating videos!        ║
        ║              Type "exit" to quit the system                         ║
        ║                                                                       ║
        ╚═══════════════════════════════════════════════════════════════════════╝
        """)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye! Your session has been saved.")
                self.master_brain.save_session()
                break
            
            command_type = self.process_voice_command(user_input)
            
            if command_type == "master_brain":
                await self.handle_master_brain_request()
            elif command_type == "approve":
                if self.approval_pending:
                    print("✅ Plan approved! Executing agents...")
                    await self.execute_pipeline()
                else:
                    print("No approval needed at this moment.")
            elif command_type == "reject":
                if self.approval_pending:
                    feedback = input("What needs to change? ")
                    print(f"❌ Plan rejected. Feedback stored: {feedback}")
                    self.cancel_project()
                else:
                    print("No approval pending.")
            elif command_type == "unknown":
                print("I didn't understand. Try 'Jarvis' to start, or 'exit' to quit.")
            
            # Save session periodically
            if len(self.conversation_history) % 5 == 0:
                self.master_brain.save_session()


# Main execution
if __name__ == "__main__":
    async def main():
        jarvis = JarvisIntegration()
        
        if await jarvis.initialize():
            await jarvis.run_interactive_session()
        else:
            print("❌ Failed to initialize Jarvis")
    
    asyncio.run(main())
