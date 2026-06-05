"""Script Guardian - Detect stale paths and version drift"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger('ScriptGuardian')

class ScriptGuardian:
    """Monitor scripts for common issues"""
    
    def __init__(self, scripts_path: Path = None):
        self.scripts_path = scripts_path or Path('scripts')
    
    def audit_scripts(self) -> Dict[str, Any]:
        """Audit all scripts for issues"""
        
        logger.info(f"Auditing scripts in {self.scripts_path}")
        
        results = {
            "scripts": [],
            "issues": [],
            "warnings": []
        }
        
        if not self.scripts_path.exists():
            results["warnings"].append(f"Scripts directory not found: {self.scripts_path}")
            return results
        
        script_files = list(self.scripts_path.glob('*.ps1')) + list(self.scripts_path.glob('*.sh'))
        
        for script_file in script_files:
            content = script_file.read_text()
            script_result = {
                "file": script_file.name,
                "issues": []
            }
            
            # Check for hardcoded paths
            if 'C:\\' in content or 'C:/' in content:
                script_result["issues"].append("Hardcoded C: drive path found")
            
            # Check for stale version references
            if 'v4.7' in content or 'v4.6' in content:
                script_result["issues"].append("Stale version reference found")
            
            if script_result["issues"]:
                results["issues"].append(script_result)
            
            results["scripts"].append(script_file.name)
        
        results["audit_result"] = "PASS" if not results["issues"] else "WARN"
        
        return results
