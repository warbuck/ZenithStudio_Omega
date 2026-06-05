"""RuneWeave - Integration Report Engine"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger('RuneWeave')

class RuneWeave:
    """Generate readable integration and project reports"""
    
    def __init__(self):
        logger.info("RuneWeave initialized")
    
    def generate_project_report(self, project_name: str, 
                                project_path: Path,
                                validation_result: Dict[str, Any]) -> str:
        """Generate human-readable project report"""
        
        report = f"""# {project_name} - Project Report

Generated: {datetime.now().isoformat()}

## Project Overview

**Project Name:** {project_name}
**Location:** {project_path}
**Status:** {'✅ COMPLETE' if validation_result.get('passed') else '❌ FAILED'}

## Files Generated

"""
        
        if project_path.exists():
            files = list(project_path.glob('**/*'))
            file_list = [f for f in files if f.is_file()]
            
            report += f"Total files: {len(file_list)}\n\n"
            report += "```\n"
            for f in file_list:
                relative = f.relative_to(project_path)
                size = f.stat().st_size
                report += f"  {relative} ({size} bytes)\n"
            report += "```\n\n"
        
        # Validation results
        report += "## Validation Results\n\n"
        if validation_result.get('checks'):
            report += "| Check | Status | Message |\n"
            report += "|-------|--------|---------|\n"
            for check in validation_result['checks']:
                status_icon = '✅' if check['status'] == 'PASS' else '❌'
                report += f"| {check['name']} | {status_icon} {check['status']} | {check.get('message', '')} |\n"
        
        # Summary
        report += f"\n## Summary\n\n"
        report += f"- Total checks: {validation_result.get('total_checks', 0)}\n"
        report += f"- Passed: {validation_result.get('total_checks', 0) - validation_result.get('failed_checks', 0)}\n"
        report += f"- Failed: {validation_result.get('failed_checks', 0)}\n"
        
        if validation_result.get('errors'):
            report += f"\n### Errors\n"
            for error in validation_result['errors']:
                report += f"- {error}\n"
        
        if validation_result.get('warnings'):
            report += f"\n### Warnings\n"
            for warning in validation_result['warnings']:
                report += f"- {warning}\n"
        
        report += f"\n## Module Connections\n\n"
        report += "```\nUser Objective\n  ↓\nAI Orchestrator\n  ↓\nScoreForge (Generation)\n  ↓\nSenku (Validation)\n  ↓\nRuneWeave (Report)\n  ↓\nPackage & Evidence\n```\n"
        
        report += f"\n## Next Steps\n\n"
        report += "1. Review generated files\n"
        report += "2. Customize for your use case\n"
        report += "3. Test functionality\n"
        report += "4. Deploy or package\n"
        
        return report
    
    def generate_mission_report(self, mission_data: Dict[str, Any]) -> str:
        """Generate mission execution report"""
        
        report = f"""# Mission Report

**Mission ID:** {mission_data.get('mission_id', 'unknown')}
**Objective:** {mission_data.get('objective', 'unknown')}
**Status:** {mission_data.get('status', 'unknown')}
**Start Time:** {mission_data.get('start_time', 'unknown')}
**End Time:** {mission_data.get('end_time', 'unknown')}

## Mission Steps

"""
        
        for i, step in enumerate(mission_data.get('steps', []), 1):
            status_icon = '✅' if step.get('status') == 'COMPLETE' else '⏳'
            report += f"{i}. [{status_icon}] {step.get('name', 'Unknown')}\n"
            if step.get('result'):
                report += f"   Result: {step['result']}\n"
        
        report += f"\n## Artifacts Generated\n\n"
        for artifact in mission_data.get('artifacts', []):
            report += f"- {artifact}\n"
        
        report += f"\n## Evidence Summary\n\n"
        report += f"- Files created: {mission_data.get('files_created', 0)}\n"
        report += f"- Validation passed: {mission_data.get('validation_passed', False)}\n"
        report += f"- Package created: {mission_data.get('package_created', False)}\n"
        
        return report
