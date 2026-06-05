"""Windows Runner Doctor - Check PowerShell/Python runner hazards"""

import logging
import platform
from typing import Dict, Any, List

logger = logging.getLogger('WindowsRunnerDoctor')

class WindowsRunnerDoctor:
    """Check Windows-specific execution environment"""
    
    def diagnose(self) -> Dict[str, Any]:
        """Run diagnostics on Windows environment"""
        
        logger.info("Running Windows Runner Doctor...")
        
        results = {
            "checks": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check OS
        is_windows = platform.system() == 'Windows'
        results["checks"].append({
            "name": "Windows OS",
            "status": "OK" if is_windows else "WARN",
            "value": platform.system()
        })
        
        if not is_windows:
            results["warnings"].append("Not running on Windows - artifact build will not work")
            results["recommendations"].append("Build Windows artifacts on Windows machine")
        
        # Check Python
        import sys
        results["checks"].append({
            "name": "Python Version",
            "status": "OK" if sys.version_info >= (3, 10) else "WARN",
            "value": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        })
        
        # Check PowerShell (Windows only)
        if is_windows:
            try:
                import subprocess
                result = subprocess.run(['powershell', '-Command', '$PSVersionTable.PSVersion.Major'],
                                      capture_output=True, text=True, timeout=5)
                ps_version = result.stdout.strip()
                results["checks"].append({
                    "name": "PowerShell Version",
                    "status": "OK" if int(ps_version) >= 5 else "WARN",
                    "value": ps_version
                })
            except:
                results["checks"].append({
                    "name": "PowerShell",
                    "status": "FAIL",
                    "value": "Not available"
                })
        
        results["diagnosis_complete"] = True
        return results
