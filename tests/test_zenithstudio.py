"""ZenithStudio Tests"""

import pytest
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.runtime.backend import create_app
from app.ai.operator import AIOperator
from app.buildtools.scoreforge import ScoreForge
from app.buildtools.senku import SenkuCore
from app.core.mission_runtime import MissionGraphEngine

class TestBackend:
    """Test Flask backend"""
    
    def test_app_creation(self):
        app = create_app()
        assert app is not None
    
    def test_status_route(self):
        app = create_app()
        client = app.test_client()
        response = client.get('/api/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
    
    def test_health_route(self):
        app = create_app()
        client = app.test_client()
        response = client.get('/health')
        assert response.status_code == 200

class TestAIOperator:
    """Test AI Operator"""
    
    def test_operator_creation(self):
        operator = AIOperator()
        assert operator is not None
    
    def test_accept_objective(self):
        operator = AIOperator()
        obj = operator.accept_objective("Create a web app")
        assert obj.text == "Create a web app"
        assert not obj.voice

class TestScoreForge:
    """Test ScoreForge"""
    
    def test_scoreforge_creation(self):
        forge = ScoreForge(Path('workspace_test'))
        assert forge is not None
    
    def test_client_intake_generation(self):
        forge = ScoreForge(Path('workspace_test'))
        result = forge.generate_client_intake_app("test_app")
        assert result['status'] == 'COMPLETE'
        assert len(result['files_created']) > 0

class TestSenku:
    """Test Senku"""
    
    def test_senku_creation(self):
        senku = SenkuCore()
        assert senku is not None
    
    def test_python_validation(self):
        senku = SenkuCore()
        result = senku.validate_python_source(Path('app'))
        assert result is not None

class TestMissionRuntime:
    """Test Mission Runtime"""
    
    def test_mission_graph_engine(self):
        engine = MissionGraphEngine()
        assert engine is not None
    
    def test_canonical_mission_generation(self):
        engine = MissionGraphEngine()
        mission = engine.generate_canonical_mission()
        assert mission.objective is not None
        assert len(mission.steps) > 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
