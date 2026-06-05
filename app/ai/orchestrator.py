"""AI Orchestrator - Route commands to appropriate systems"""

import logging
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger('AIOrchestrator')

class CommandType(Enum):
    """Types of commands"""
    MISSION = "mission"
    ANALYSIS = "analysis"
    GENERATION = "generation"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    TESTING = "testing"

class AIOrchestrator:
    """Route commands through appropriate subsystems"""
    
    def __init__(self):
        logger.info("AI Orchestrator initialized")
    
    def route_command(self, objective: str) -> Dict[str, Any]:
        """Route command to appropriate system"""
        
        # Simple keyword-based routing
        if any(word in objective.lower() for word in ['create', 'build', 'generate', 'make']):
            return {
                "route": "scoreforge",
                "command_type": CommandType.GENERATION.value,
                "urgency": "high"
            }
        elif any(word in objective.lower() for word in ['test', 'validate', 'check', 'verify']):
            return {
                "route": "senku",
                "command_type": CommandType.VALIDATION.value,
                "urgency": "medium"
            }
        elif any(word in objective.lower() for word in ['deploy', 'release', 'publish']):
            return {
                "route": "deploy_studio",
                "command_type": CommandType.DEPLOYMENT.value,
                "urgency": "high"
            }
        else:
            return {
                "route": "mission_runtime",
                "command_type": CommandType.MISSION.value,
                "urgency": "medium"
            }
