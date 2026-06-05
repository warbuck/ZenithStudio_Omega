"""Senku Core - Validation Engine"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger('Senku')

class ValidationResult:
    """Validation result"""
    
    def __init__(self):
        self.checks = []
        self.errors = []
        self.warnings = []
        self.passed = True
    
    def add_check(self, name: str, status: str, message: str = ""):
        self.checks.append({
            "name": name,
            "status": status,
            "message": message
        })
        if status == "FAIL":
            self.passed = False
            self.errors.append(f"{name}: {message}")
        elif status == "WARN":
            self.warnings.append(f"{name}: {message}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "total_checks": len(self.checks),
            "failed_checks": len(self.errors)
        }

class SenkuCore:
    """Validation and code quality engine"""
    
    def __init__(self):
        logger.info("Senku Core initialized")
    
    def validate_project(self, project_path: Path) -> ValidationResult:
        """Validate generated project"""
        
        result = ValidationResult()
        
        # Check directory exists
        if not project_path.exists():
            result.add_check("project_exists", "FAIL", "Project directory not found")
            return result
        
        result.add_check("project_exists", "PASS", "Project directory found")
        
        # Check for README
        if (project_path / 'README.md').exists():
            result.add_check("readme", "PASS", "README.md present")
        else:
            result.add_check("readme", "WARN", "README.md not found")
        
        # Check for files
        file_count = len(list(project_path.glob('*')))
        if file_count > 0:
            result.add_check("files_created", "PASS", f"{file_count} files created")
        else:
            result.add_check("files_created", "FAIL", "No files found in project")
        
        # Check for Python syntax if applicable
        self._check_python_files(project_path, result)
        
        # Check file sizes (not empty)
        self._check_file_sizes(project_path, result)
        
        return result
    
    def _check_python_files(self, project_path: Path, result: ValidationResult):
        """Check Python file syntax"""
        py_files = list(project_path.glob('**/*.py'))
        
        if not py_files:
            return
        
        for py_file in py_files:
            try:
                compile(py_file.read_text(), str(py_file), 'exec')
                result.add_check(f"python_syntax_{py_file.name}", "PASS", "Valid Python syntax")
            except SyntaxError as e:
                result.add_check(f"python_syntax_{py_file.name}", "FAIL", str(e))
    
    def _check_file_sizes(self, project_path: Path, result: ValidationResult):
        """Check that files are not empty"""
        for file_path in project_path.glob('**/*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size == 0:
                    result.add_check(f"file_empty_{file_path.name}", "WARN", "File is empty")
                elif size > 0:
                    result.add_check(f"file_size_{file_path.name}", "PASS", f"{size} bytes")
    
    def validate_python_source(self, source_path: Path) -> ValidationResult:
        """Validate Python source code"""
        
        result = ValidationResult()
        
        py_files = list(source_path.glob('**/*.py'))
        
        if not py_files:
            result.add_check("python_files_found", "WARN", "No Python files found")
            return result
        
        result.add_check("python_files_found", "PASS", f"{len(py_files)} Python files found")
        
        for py_file in py_files:
            try:
                content = py_file.read_text()
                compile(content, str(py_file), 'exec')
                result.add_check(f"compile_{py_file.relative_to(source_path)}", "PASS", "Compiles OK")
            except SyntaxError as e:
                result.add_check(f"compile_{py_file.name}", "FAIL", str(e))
        
        return result
    
    def validate_api_routes(self, flask_app) -> ValidationResult:
        """Validate Flask API routes"""
        
        result = ValidationResult()
        
        rules = flask_app.url_map.iter_rules()
        route_count = 0
        
        for rule in rules:
            if rule.endpoint != 'static':
                route_count += 1
        
        if route_count > 0:
            result.add_check("api_routes_exist", "PASS", f"{route_count} routes registered")
        else:
            result.add_check("api_routes_exist", "FAIL", "No API routes found")
        
        return result
