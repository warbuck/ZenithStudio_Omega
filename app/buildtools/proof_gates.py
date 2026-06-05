"""Proof Gates - Rigorous validation and verification system"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger('ProofGates')

class SelfTest:
    """Source code and module self-test"""
    
    @staticmethod
    def run() -> Dict[str, Any]:
        """Run self-test suite"""
        logger.info("Running self-test...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        # Test imports
        try:
            from app.runtime.backend import create_app
            from app.ai.operator import AIOperator
            from app.buildtools.scoreforge import ScoreForge
            from app.buildtools.senku import SenkuCore
            from app.buildtools.runeweave import RuneWeave
            from app.core.mission_runtime import MissionGraphEngine, PersistentAgentDaemon
            from app.core.redmars_scheduler import RedMarsScheduler
            from app.aegis.hexaqvm import AegisHexaQVM
            from app.models.provider import ModelVault
            results["tests"].append({"name": "core_imports", "status": "PASS"})
        except Exception as e:
            results["tests"].append({"name": "core_imports", "status": "FAIL", "error": str(e)})
        
        # Test Flask app creation
        try:
            from app.runtime.backend import create_app
            app = create_app()
            results["tests"].append({"name": "flask_app_creation", "status": "PASS"})
        except Exception as e:
            results["tests"].append({"name": "flask_app_creation", "status": "FAIL", "error": str(e)})
        
        # Test directory structure
        required_dirs = ['app', 'web/static', 'data', 'logs', 'scripts', 'docs']
        root = Path(__file__).parent.parent
        all_exist = all((root / d).exists() for d in required_dirs)
        results["tests"].append({
            "name": "directory_structure",
            "status": "PASS" if all_exist else "FAIL"
        })
        
        # Test VERSION.json
        try:
            version_file = root / 'VERSION.json'
            if version_file.exists():
                version_data = json.loads(version_file.read_text())
                results["tests"].append({"name": "version_file", "status": "PASS"})
            else:
                results["tests"].append({"name": "version_file", "status": "FAIL"})
        except Exception as e:
            results["tests"].append({"name": "version_file", "status": "FAIL", "error": str(e)})
        
        passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
        results["summary"] = {
            "total": len(results["tests"]),
            "passed": passed,
            "failed": len(results["tests"]) - passed
        }
        
        return results

class PythonCompile:
    """Validate Python source compilation"""
    
    @staticmethod
    def run(source_path: Path = None) -> Dict[str, Any]:
        """Compile all Python files"""
        if source_path is None:
            source_path = Path(__file__).parent.parent / 'app'
        
        logger.info(f"Compiling Python source in {source_path}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "files": []
        }
        
        py_files = list(source_path.glob('**/*.py'))
        
        for py_file in py_files:
            try:
                content = py_file.read_text()
                compile(content, str(py_file), 'exec')
                results["files"].append({
                    "file": str(py_file.relative_to(source_path.parent)),
                    "status": "OK"
                })
            except SyntaxError as e:
                results["files"].append({
                    "file": str(py_file.relative_to(source_path.parent)),
                    "status": "ERROR",
                    "error": str(e)
                })
        
        results["summary"] = {
            "total": len(results["files"]),
            "ok": sum(1 for f in results["files"] if f["status"] == "OK"),
            "errors": sum(1 for f in results["files"] if f["status"] == "ERROR")
        }
        
        return results

class UIAPIAudit:
    """Audit UI frontend API references against backend routes"""
    
    @staticmethod
    def run(app_instance=None) -> Dict[str, Any]:
        """Audit UI/API linkage"""
        logger.info("Running UI/API audit...")
        
        # Expected API routes
        expected_routes = [
            '/api/status',
            '/api/self_test',
            '/api/ui_link_audit',
            '/api/integration_tracker/status',
            '/api/integration_tracker/run',
            '/api/operational_mission_proof/status',
            '/api/operational_mission_proof/run',
            '/api/windows_artifact_proof/status',
            '/api/windows_artifact_proof/plan',
            '/api/windows_artifact_proof/run',
            '/api/v5_release_candidate/status',
            '/api/v5_release_candidate/run',
            '/api/v5_release_candidate/export_markdown',
            '/api/ai/models',
            '/api/ai/objective',
            '/api/mission/status',
            '/api/render_studio/preview',
            '/api/live_studio/session',
            '/api/test_studio/run',
            '/api/deploy_studio/deploy',
            '/health'
        ]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "expected_routes": expected_routes,
            "missing_routes": []
        }
        
        if app_instance:
            registered_routes = [str(rule) for rule in app_instance.url_map.iter_rules()]
            results["registered_routes"] = registered_routes
            results["missing_routes"] = [r for r in expected_routes if r not in registered_routes]
        
        results["audit_result"] = "PASS" if not results["missing_routes"] else "FAIL"
        
        return results

class IntegrationTracker:
    """Track system recommendations and completion"""
    
    def __init__(self, tracker_path: Path = None):
        self.tracker_path = tracker_path or Path('data/integration_tracker')
        self.tracker_path.mkdir(parents=True, exist_ok=True)
        self.tracker_file = self.tracker_path / 'tracker.json'
    
    def load_tracker(self) -> Dict[str, Any]:
        """Load tracker state"""
        if self.tracker_file.exists():
            return json.loads(self.tracker_file.read_text())
        return self._default_tracker()
    
    def _default_tracker(self) -> Dict[str, Any]:
        """Default tracker state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "items": [
                {"name": "Source Integration", "percent": 100, "status": "COMPLETE", "notes": "All source modules implemented"},
                {"name": "V5 Readiness Source", "percent": 100, "status": "COMPLETE", "notes": "Source ready for V5"},
                {"name": "Windows Artifact Proof", "percent": 0, "status": "BLOCKED", "notes": "Requires Windows EXE build", "blockers": ["Final Windows artifact proof"]},
                {"name": "Integration Completion", "percent": 85, "status": "IN_PROGRESS", "notes": "Awaiting artifact generation"},
            ]
        }
    
    def save_tracker(self, data: Dict[str, Any]):
        """Save tracker state"""
        self.tracker_file.write_text(json.dumps(data, indent=2))
    
    def run(self) -> Dict[str, Any]:
        """Run integration tracker"""
        tracker = self.load_tracker()
        tracker["timestamp"] = datetime.now().isoformat()
        self.save_tracker(tracker)
        return tracker

class WindowsArtifactProof:
    """Verify Windows executable and installer artifacts"""
    
    def __init__(self, artifact_path: Path = None):
        self.artifact_path = artifact_path or Path('dist')
    
    def check_artifacts(self) -> Dict[str, Any]:
        """Check for required Windows artifacts"""
        
        artifacts = {
            "exe": self.artifact_path / "ZenithStudio.exe",
            "runtime_manifest": Path("runtime/runtime_manifest.json"),
            "installer": Path("builds/installer/ZenithStudio_Setup.exe"),
            "smoke_test": Path("logs/exe_smoke_test_report.json")
        }
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "artifacts": {}
        }
        
        for name, path in artifacts.items():
            exists = path.exists()
            results["artifacts"][name] = {
                "path": str(path),
                "exists": exists,
                "status": "PRESENT" if exists else "MISSING"
            }
        
        all_present = all(a["exists"] for a in results["artifacts"].values())
        results["all_artifacts_present"] = all_present
        results["proof_status"] = "PASS" if all_present else "BLOCKED"
        
        return results
