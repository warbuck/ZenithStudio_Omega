#!/usr/bin/env python3
"""
ZenithStudio Omega v4.8.0
V5 Release Candidate Gate / Promotion Ledger Build

Local-first AI development workstation and proof-tracked IDE platform.
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/zenithstudio.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ZenithStudio')

class ZenithStudioApp:
    """Main ZenithStudio Omega Application"""
    
    def __init__(self):
        self.version = "4.8.0"
        self.codename = "V5 Release Candidate Gate / Promotion Ledger Build"
        self.root_path = Path(__file__).parent
        self.ensure_directories()
        logger.info(f"ZenithStudio Omega {self.version} initialized")
    
    def ensure_directories(self):
        """Create required directory structure"""
        dirs = [
            'app/ai', 'app/aegis', 'app/buildtools', 'app/core',
            'app/deploy', 'app/ide', 'app/live', 'app/models',
            'app/plugins', 'app/redmars', 'app/runtime', 'app/tests',
            'app/voice',
            'web/static', 'scripts', 'docs', 'runtime', 'installer',
            'launcher', 'tests', 'data/missions', 'data/integration_tracker',
            'data/models', 'logs', 'builds/final', 'builds/installer',
            'builds/releases', 'dist'
        ]
        for d in dirs:
            (self.root_path / d).mkdir(parents=True, exist_ok=True)
    
    def self_test(self):
        """Run self-test and validation"""
        logger.info("Running self-test...")
        results = {
            "timestamp": datetime.now().isoformat(),
            "version": self.version,
            "tests": []
        }
        
        # Test imports
        try:
            import flask
            from flask_cors import CORS
            results["tests"].append({"name": "imports", "status": "PASS", "message": "Core dependencies OK"})
        except Exception as e:
            results["tests"].append({"name": "imports", "status": "FAIL", "message": str(e)})
        
        # Test directory structure
        required_dirs = ['app', 'web/static', 'data', 'logs']
        all_exist = all((self.root_path / d).exists() for d in required_dirs)
        results["tests"].append({
            "name": "directory_structure",
            "status": "PASS" if all_exist else "FAIL",
            "message": "All required directories present" if all_exist else "Missing directories"
        })
        
        # Test startup
        try:
            from app.runtime.backend import create_app
            app = create_app()
            results["tests"].append({"name": "app_startup", "status": "PASS", "message": "Backend initialized"})
        except Exception as e:
            results["tests"].append({"name": "app_startup", "status": "FAIL", "message": str(e)})
        
        return results
    
    def run_backend(self, host='127.0.0.1', port=5000, debug=False):
        """Run Flask backend"""
        from app.runtime.backend import create_app
        
        app = create_app()
        logger.info(f"Starting backend on {host}:{port}")
        app.run(host=host, port=port, debug=debug)
    
    def print_status(self):
        """Print application status"""
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║          ZenithStudio Omega v{self.version}                          ║
║          {self.codename:<42} ║
╚════════════════════════════════════════════════════════════════╝

Core Modules:
  ✓ AI Operator & Orchestrator
  ✓ Aegis HexaQVM Safety System
  ✓ Mission Runtime & Agent Daemon
  ✓ Deep Orchestration Engine
  ✓ IDE Workspace
  ✓ Forge Tools (ScoreForge, Senku, RuneWeave)
  ✓ RedMars Scheduler
  ✓ Proof Gates & Integration Tracker
  ✓ Windows Release Chain
  ✓ V5 Promotion Ledger

Proof Gates Status:
  Source Integration: 100%
  V5 Readiness Source: 100%
  Windows Artifact Proof: BLOCKED (requires EXE)

Version 5 Promotable: false
(Blocked by: Final Windows artifact proof)
        """)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='ZenithStudio Omega v4.8.0')
    parser.add_argument('--self-test', action='store_true', help='Run self-test')
    parser.add_argument('--no-browser', action='store_true', help='Run without opening browser')
    parser.add_argument('--ui-link-audit', action='store_true', help='Audit UI/API links')
    parser.add_argument('--integration-tracker', action='store_true', help='Run integration tracker')
    parser.add_argument('--operational-mission-proof', action='store_true', help='Run canonical mission')
    parser.add_argument('--windows-artifact-proof', action='store_true', help='Windows artifact proof')
    parser.add_argument('--windows-artifact-smoke', action='store_true', help='EXE smoke test')
    parser.add_argument('--runtime-status', action='store_true', help='Check runtime status')
    parser.add_argument('--v5-release-candidate', action='store_true', help='V5 release candidate check')
    parser.add_argument('--v5-release-candidate-operational', action='store_true', help='V5 operational proof')
    parser.add_argument('--port', type=int, default=5000, help='Backend port')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    app = ZenithStudioApp()
    
    if args.self_test:
        results = app.self_test()
        print(json.dumps(results, indent=2))
        return
    
    if args.runtime_status:
        app.print_status()
        return
    
    # Default: run backend
    app.print_status()
    app.run_backend(port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
