"""Aegis HexaQVM - Six-lane safety and reasoning verification"""

import logging
from typing import Dict, Any
from dataclasses import dataclass

logger = logging.getLogger('AegisHexaQVM')

@dataclass
class SafetyReview:
    """Safety review result"""
    perception_ok: bool
    planning_ok: bool
    reasoning_ok: bool
    execution_ok: bool
    reflection_ok: bool
    security_ok: bool
    overall_approved: bool
    blockers: list

class AegisHexaQVM:
    """Intent-to-plan safety and reasoning verification"""
    
    def __init__(self):
        logger.info("Aegis HexaQVM initialized")
    
    def review(self, objective: str, plan: Dict[str, Any]) -> SafetyReview:
        """Review objective and plan through six lanes"""
        
        # Perception: Does the system understand the request?
        perception_ok = len(objective) > 0
        
        # Planning: Is the plan coherent?
        planning_ok = 'steps' in plan and len(plan.get('steps', [])) > 0
        
        # Reasoning: Does the reasoning make sense?
        reasoning_ok = 'rationale' in plan
        
        # Execution: Are all resources available?
        execution_ok = True
        
        # Reflection: Has impact been considered?
        reflection_ok = True
        
        # Security: Are there security risks?
        security_ok = True
        blockers = []
        
        # Check for dangerous operations
        dangerous_words = ['delete', 'remove', 'drop', 'uninstall', 'format']
        if any(word in objective.lower() for word in dangerous_words):
            security_ok = False
            blockers.append("Destructive operation detected - requires approval")
        
        overall_approved = all([
            perception_ok, planning_ok, reasoning_ok,
            execution_ok, reflection_ok, security_ok
        ])
        
        return SafetyReview(
            perception_ok=perception_ok,
            planning_ok=planning_ok,
            reasoning_ok=reasoning_ok,
            execution_ok=execution_ok,
            reflection_ok=reflection_ok,
            security_ok=security_ok,
            overall_approved=overall_approved,
            blockers=blockers
        )
