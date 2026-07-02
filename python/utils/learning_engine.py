"""
Learning Engine - Master Brain's evolution system
Improves decision-making 24/7
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LearningEngine:
    """
    Evolution and Learning Engine
    Continuously improves Master Brain's decision-making
    """

    def __init__(self, evolution_file: str = "memory/evolution_history.json"):
        self.evolution_file = evolution_file
        self.evolution_history = self.load_evolution_history()
        self.evolution_cycles = 0
        os.makedirs(os.path.dirname(evolution_file), exist_ok=True)

    def load_evolution_history(self) -> List[Dict]:
        """Load evolution history"""
        if os.path.exists(self.evolution_file):
            try:
                with open(self.evolution_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def store_evolution(self, evolution_data: Dict) -> None:
        """Store evolution cycle data"""
        self.evolution_cycles += 1
        
        evolution_entry = {
            "cycle": self.evolution_cycles,
            "timestamp": datetime.now().isoformat(),
            "data": evolution_data
        }
        
        self.evolution_history.append(evolution_entry)
        self.save_evolution_history()
        logger.info(f"🧬 Evolution cycle #{self.evolution_cycles} stored")

    def save_evolution_history(self) -> None:
        """Save evolution history to file"""
        os.makedirs(os.path.dirname(self.evolution_file), exist_ok=True)
        with open(self.evolution_file, 'w') as f:
            json.dump(self.evolution_history, f, indent=2)

    def get_latest_evolution(self) -> Dict:
        """Get most recent evolution data"""
        if self.evolution_history:
            return self.evolution_history[-1]
        return {}

    def get_evolution_trend(self) -> Dict:
        """Get trend across evolution cycles"""
        return {
            "total_cycles": self.evolution_cycles,
            "recent_cycles": self.evolution_history[-10:] if self.evolution_history else [],
            "trend": "improving" if self.evolution_cycles > 0 else "initializing"
        }

    def extract_improvements(self) -> Dict:
        """Extract what should be improved based on evolution history"""
        if not self.evolution_history:
            return {"status": "no_data_yet"}
        
        latest = self.evolution_history[-1]["data"]
        return {
            "improvements_identified": True,
            "latest_evolution_cycle": self.evolution_cycles,
            "recommendations": latest if isinstance(latest, dict) else {"data": str(latest)}
        }
