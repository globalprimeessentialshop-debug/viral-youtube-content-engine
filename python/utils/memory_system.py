"""
Memory System - Stores and recalls learned information
Helps Master Brain remember past successes and failures
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemorySystem:
    """
    Persistent memory for Master Brain Agent
    Stores:
    - Past project results
    - User feedback
    - Successful patterns
    - Failed patterns
    - Evolution history
    """

    def __init__(self, memory_file: str = "memory/master_brain_memory.json"):
        self.memory_file = memory_file
        self.memory = self.load_memory()
        os.makedirs(os.path.dirname(memory_file), exist_ok=True)

    def load_memory(self) -> Dict:
        """Load existing memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return self.initialize_memory()
        return self.initialize_memory()

    def initialize_memory(self) -> Dict:
        """Initialize empty memory structure"""
        return {
            "projects": [],
            "successful_patterns": [],
            "failed_patterns": [],
            "user_feedback": [],
            "viral_insights": [],
            "agent_performance": {},
            "monetization_data": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

    def store_project(self, project_data: Dict) -> None:
        """Store completed project"""
        self.memory["projects"].append({
            **project_data,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()
        logger.info("💾 Project stored in memory")

    def store_feedback(self, feedback: str, category: str = "general") -> None:
        """Store user feedback"""
        self.memory["user_feedback"].append({
            "feedback": feedback,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()
        logger.info("💾 Feedback stored")

    def store_success_pattern(self, pattern: Dict) -> None:
        """Store successful patterns"""
        self.memory["successful_patterns"].append({
            **pattern,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()
        logger.info("💾 Success pattern stored")

    def store_failure_pattern(self, pattern: Dict) -> None:
        """Store failure patterns to avoid"""
        self.memory["failed_patterns"].append({
            **pattern,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()
        logger.info("💾 Failure pattern stored")

    def store_agent_performance(self, agent_name: str, metrics: Dict) -> None:
        """Track individual agent performance"""
        if agent_name not in self.memory["agent_performance"]:
            self.memory["agent_performance"][agent_name] = []
        
        self.memory["agent_performance"][agent_name].append({
            **metrics,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()
        logger.info(f"💾 {agent_name} performance recorded")

    def get_successful_patterns(self) -> List[Dict]:
        """Retrieve all successful patterns"""
        return self.memory["successful_patterns"]

    def get_failed_patterns(self) -> List[Dict]:
        """Retrieve all failed patterns to avoid"""
        return self.memory["failed_patterns"]

    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """Get recent user feedback"""
        return self.memory["user_feedback"][-limit:]

    def get_agent_stats(self, agent_name: str) -> Dict:
        """Get performance stats for specific agent"""
        if agent_name in self.memory["agent_performance"]:
            performances = self.memory["agent_performance"][agent_name]
            return {
                "total_tasks": len(performances),
                "recent_tasks": performances[-5:],
                "performance_trend": "analyzing..."
            }
        return {"agent": agent_name, "data": "No data yet"}

    def save_memory(self) -> None:
        """Save memory to file"""
        self.memory["last_updated"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def get_memory_summary(self) -> Dict:
        """Get summary of all stored memory"""
        return {
            "total_projects": len(self.memory["projects"]),
            "successful_patterns_count": len(self.memory["successful_patterns"]),
            "failed_patterns_count": len(self.memory["failed_patterns"]),
            "feedback_count": len(self.memory["user_feedback"]),
            "agents_tracked": list(self.memory["agent_performance"].keys()),
            "last_updated": self.memory["last_updated"]
        }
