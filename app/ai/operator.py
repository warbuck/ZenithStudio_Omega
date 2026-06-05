"""AI Operator - User-facing command and control layer"""

import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger('AIOperator')

@dataclass
class Objective:
    """User objective"""
    text: str
    voice: bool = False
    timestamp: str = None
    approval_required: bool = False
    approved: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class AIOperator:
    """Browser-facing command layer"""
    
    def __init__(self):
        self.objectives = []
        self.current_objective = None
        logger.info("AI Operator initialized")
    
    def accept_objective(self, text: str, voice: bool = False) -> Objective:
        """Accept text or voice objective"""
        obj = Objective(text=text, voice=voice)
        self.objectives.append(obj)
        self.current_objective = obj
        logger.info(f"Objective accepted: {text[:50]}...")
        return obj
    
    def approve_objective(self, objective_id: int) -> bool:
        """Approve objective for execution"""
        if 0 <= objective_id < len(self.objectives):
            self.objectives[objective_id].approved = True
            return True
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get operator status"""
        return {
            "objectives_pending": len([o for o in self.objectives if not o.approved]),
            "current_objective": asdict(self.current_objective) if self.current_objective else None,
            "total_objectives": len(self.objectives)
        }
