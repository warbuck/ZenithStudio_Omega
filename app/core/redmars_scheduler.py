"""RedMars Scheduler - Background job and workload orchestration"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger('RedMarsScheduler')

class JobStatus(Enum):
    """Job execution status"""
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class ComputeLane(Enum):
    """Virtual compute lanes"""
    CPU = "cpu"
    GPU = "gpu"
    NPU = "npu"
    TPU = "tpu"
    DPU = "dpu"

@dataclass
class Job:
    """Background job specification"""
    job_id: str
    name: str
    lane: str
    status: str = JobStatus.QUEUED.value
    priority: int = 5
    created_at: str = None
    started_at: str = None
    completed_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class RedMarsScheduler:
    """Virtual acceleration and job scheduling layer"""
    
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.queue: List[str] = []
        logger.info("RedMars Scheduler initialized")
    
    def schedule_job(self, job_name: str, lane: str = ComputeLane.CPU.value, 
                    priority: int = 5) -> Job:
        """Schedule a new background job"""
        
        job_id = f"job_{datetime.now().timestamp()}"
        job = Job(
            job_id=job_id,
            name=job_name,
            lane=lane,
            priority=priority
        )
        
        self.jobs[job_id] = job
        self.queue.append(job_id)
        
        logger.info(f"Job scheduled: {job_id} ({job_name}) on {lane}")
        return job
    
    def execute_job(self, job_id: str) -> Job:
        """Simulate job execution"""
        
        if job_id not in self.jobs:
            logger.error(f"Job not found: {job_id}")
            return None
        
        job = self.jobs[job_id]
        job.status = JobStatus.RUNNING.value
        job.started_at = datetime.now().isoformat()
        
        # Simulate execution
        logger.info(f"Executing job: {job_id}")
        
        job.status = JobStatus.COMPLETE.value
        job.completed_at = datetime.now().isoformat()
        
        return job
    
    def get_queue(self) -> List[Job]:
        """Get current job queue"""
        return [self.jobs[job_id] for job_id in self.queue if job_id in self.jobs]
    
    def get_lane_status(self, lane: str) -> Dict[str, Any]:
        """Get status of a compute lane"""
        lane_jobs = [j for j in self.jobs.values() if j.lane == lane]
        
        return {
            "lane": lane,
            "total_jobs": len(lane_jobs),
            "running": len([j for j in lane_jobs if j.status == JobStatus.RUNNING.value]),
            "completed": len([j for j in lane_jobs if j.status == JobStatus.COMPLETE.value]),
            "failed": len([j for j in lane_jobs if j.status == JobStatus.FAILED.value])
        }

class EvidenceAutocapture:
    """Automatically capture evidence of mission execution"""
    
    def __init__(self, evidence_path: str = "logs/evidence"):
        self.evidence_path = evidence_path
        logger.info(f"Evidence Autocapture initialized at {evidence_path}")
    
    def capture(self, mission_id: str, mission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Capture mission evidence"""
        
        evidence = {
            "mission_id": mission_id,
            "objective": mission_data.get('objective'),
            "timestamp": datetime.now().isoformat(),
            "status": mission_data.get('status'),
            "steps_completed": len([s for s in mission_data.get('steps', []) 
                                    if s.get('status') == 'COMPLETE']),
            "artifacts_generated": mission_data.get('artifacts', []),
            "validation_passed": mission_data.get('validation_passed', False),
            "package_created": mission_data.get('package_created', False),
        }
        
        return evidence
