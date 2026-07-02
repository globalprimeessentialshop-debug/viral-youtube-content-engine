"""
Decision Maker - Makes optimal decisions for Master Brain
Evaluates options and picks best path
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecisionMaker:
    """
    Decision Making System
    Evaluates options and makes optimal choices
    """

    def __init__(self):
        self.decisions_made = 0
        self.decision_history = []

    def evaluate_options(self, options: List[Dict], criteria: Dict) -> Dict:
        """
        Evaluate multiple options against criteria
        
        Args:
            options: List of options to evaluate
            criteria: Evaluation criteria with weights
        
        Returns:
            Best option with reasoning
        """
        logger.info(f"🤔 Evaluating {len(options)} options...")
        
        scores = []
        for option in options:
            score = self.calculate_score(option, criteria)
            scores.append({
                "option": option,
                "score": score
            })
        
        # Sort by score
        scores.sort(key=lambda x: x["score"], reverse=True)
        best = scores[0]
        
        self.decisions_made += 1
        self.decision_history.append({
            "timestamp": datetime.now().isoformat(),
            "best_option": best["option"],
            "score": best["score"],
            "all_scores": scores
        })
        
        logger.info(f"✅ Best option selected: {best['option']} (Score: {best['score']})")
        
        return {
            "best_option": best["option"],
            "score": best["score"],
            "all_options": scores,
            "confidence": self.calculate_confidence(scores)
        }

    def calculate_score(self, option: Dict, criteria: Dict) -> float:
        """
        Calculate option score based on criteria
        """
        score = 0
        total_weight = sum(criteria.values())
        
        for criterion, weight in criteria.items():
            if criterion in option:
                # Normalize value to 0-100 if needed
                value = option[criterion]
                if isinstance(value, (int, float)):
                    normalized = min(100, max(0, value))
                else:
                    normalized = 50  # Default for non-numeric
                
                score += (normalized * weight) / total_weight
        
        return score

    def calculate_confidence(self, scores: List[Dict]) -> float:
        """
        Calculate confidence level in decision
        """
        if len(scores) < 2:
            return 100.0
        
        best_score = scores[0]["score"]
        second_best_score = scores[1]["score"]
        
        # Confidence based on gap between best and second-best
        gap = (best_score - second_best_score) / max(best_score, 1)
        confidence = min(100, max(0, gap * 100))
        
        return confidence

    def should_proceed(self, confidence_threshold: float = 75.0) -> Tuple[bool, float]:
        """
        Decide if should proceed based on confidence
        """
        if not self.decision_history:
            return False, 0.0
        
        last_decision = self.decision_history[-1]
        confidence = self.calculate_confidence(last_decision["all_scores"])
        
        return confidence >= confidence_threshold, confidence

    def get_decision_stats(self) -> Dict:
        """Get decision-making statistics"""
        return {
            "total_decisions": self.decisions_made,
            "recent_decisions": self.decision_history[-10:] if self.decision_history else [],
            "status": "ready"
        }
