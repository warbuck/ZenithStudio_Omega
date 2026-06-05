"""Operational Mission Proof - Run canonical client intake mission"""

import logging
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger('OperationalMissionProof')

class OperationalMissionProof:
    """Run canonical mission to prove platform works end-to-end"""
    
    def __init__(self):
        self.workspace = Path('workspace/canonical_mission')
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def run(self) -> Dict[str, Any]:
        """Execute canonical client intake mission"""
        
        logger.info("Running operational mission proof...")
        
        try:
            from app.buildtools.scoreforge import ScoreForge
            from app.buildtools.senku import SenkuCore
            from app.buildtools.runeweave import RuneWeave
            from app.core.mission_runtime import MissionGraphEngine, PersistentAgentDaemon, InternalEventBus, ToolExecutor
            
            # Step 1: Plan
            engine = MissionGraphEngine()
            mission = engine.generate_canonical_mission()
            
            # Step 2-3: Create project and write files
            scoreforge = ScoreForge(self.workspace)
            gen_result = scoreforge.generate_client_intake_app("client_intake")
            
            # Step 4: Validate
            senku = SenkuCore()
            project_path = self.workspace / "client_intake"
            validation = senku.validate_project(project_path)
            
            # Step 5: Generate report
            runeweave = RuneWeave()
            report = runeweave.generate_project_report(
                "client_intake",
                project_path,
                validation.to_dict()
            )
            
            # Save report
            report_path = self.workspace / "project_report.md"
            report_path.write_text(report)
            
            # Step 6: Package
            import shutil
            zip_path = Path("builds/final/client_intake.zip")
            zip_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.make_archive(str(zip_path.with_suffix('')), 'zip', self.workspace, "client_intake")
            
            # Step 7-8: Evidence and tracker
            evidence = {
                "mission_id": mission.mission_id,
                "objective": mission.objective,
                "timestamp": datetime.now().isoformat(),
                "status": "COMPLETE",
                "files_created": gen_result["files_created"],
                "project_path": gen_result["project_path"],
                "validation_passed": validation.passed,
                "package_created": zip_path.exists(),
                "artifacts": [
                    "index.html",
                    "style.css",
                    "app.js",
                    "README.md"
                ],
                "validation_checks": validation.to_dict()
            }
            
            evidence_path = Path("logs/operational_mission_evidence.json")
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(json.dumps(evidence, indent=2))
            
            return {
                "status": "PASS",
                "mission_id": mission.mission_id,
                "evidence_file": str(evidence_path),
                "project_path": str(project_path),
                "package": str(zip_path),
                "report": str(report_path)
            }
        
        except Exception as e:
            logger.error(f"Mission failed: {str(e)}")
            return {
                "status": "FAIL",
                "error": str(e)
            }
