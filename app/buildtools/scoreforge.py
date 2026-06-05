"""ScoreForge - Project Generation Engine"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger('ScoreForge')

@dataclass
class ProjectTemplate:
    """Project template specification"""
    name: str
    description: str
    language: str
    files: Dict[str, str]
    metadata: Dict[str, Any]

class ScoreForge:
    """Real project generation engine"""
    
    def __init__(self, workspace_path: Path = None):
        self.workspace_path = workspace_path or Path('workspace')
        self.workspace_path.mkdir(exist_ok=True)
        logger.info(f"ScoreForge initialized at {self.workspace_path}")
    
    def generate_client_intake_app(self, project_name: str = "client_intake") -> Dict[str, Any]:
        """Generate the canonical client intake web app"""
        
        project_path = self.workspace_path / project_name
        project_path.mkdir(exist_ok=True)
        
        logger.info(f"Generating client intake app: {project_name}")
        
        # HTML with form
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Intake Form</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Client Intake Form</h1>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search clients...">
        </div>
        
        <form id="intakeForm" class="intake-form">
            <div class="form-group">
                <label for="clientName">Client Name *</label>
                <input type="text" id="clientName" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email *</label>
                <input type="email" id="email" required>
            </div>
            
            <div class="form-group">
                <label for="phone">Phone</label>
                <input type="tel" id="phone">
            </div>
            
            <div class="form-group">
                <label for="service">Service Type *</label>
                <select id="service" required>
                    <option value="">Select a service</option>
                    <option value="consulting">Consulting</option>
                    <option value="development">Development</option>
                    <option value="design">Design</option>
                    <option value="support">Support</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="notes">Notes</label>
                <textarea id="notes" rows="4"></textarea>
            </div>
            
            <button type="submit" class="btn-primary">Submit</button>
        </form>
        
        <div id="preview" class="preview-section">
            <h2>Client Records</h2>
            <div id="recordsList" class="records-list"></div>
        </div>
        
        <button id="exportBtn" class="btn-secondary">Export as JSON</button>
        <button id="exportCSVBtn" class="btn-secondary">Export as CSV</button>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
'''
        
        # CSS styling
        css_content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    padding: 40px;
}

h1 {
    color: #333;
    margin-bottom: 30px;
    text-align: center;
}

h2 {
    color: #555;
    margin-top: 30px;
    margin-bottom: 15px;
    font-size: 1.3em;
}

.search-box {
    margin-bottom: 20px;
}

.search-box input {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
}

.intake-form {
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-weight: 500;
}

input, select, textarea {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    font-family: inherit;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-primary, .btn-secondary {
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin-right: 10px;
}

.btn-primary {
    background: #667eea;
    color: white;
    width: 100%;
}

.btn-primary:hover {
    background: #5568d3;
}

.btn-secondary {
    background: #f0f0f0;
    color: #333;
}

.btn-secondary:hover {
    background: #e0e0e0;
}

.preview-section {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 5px;
    border: 1px solid #eee;
}

.records-list {
    display: grid;
    gap: 15px;
}

.record-item {
    background: white;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.record-item h3 {
    color: #333;
    margin-bottom: 8px;
}

.record-item p {
    color: #666;
    font-size: 13px;
    margin-bottom: 4px;
}

.record-item .email {
    color: #667eea;
    text-decoration: none;
}

.empty-message {
    text-align: center;
    color: #999;
    padding: 40px 20px;
}
'''
        
        # JavaScript functionality
        js_content = '''class ClientIntakeApp {
    constructor() {
        this.clients = this.loadClients();
        this.setupEventListeners();
        this.renderClients();
    }
    
    setupEventListeners() {
        document.getElementById('intakeForm').addEventListener('submit', (e) => this.handleSubmit(e));
        document.getElementById('searchInput').addEventListener('input', (e) => this.handleSearch(e));
        document.getElementById('exportBtn').addEventListener('click', () => this.exportJSON());
        document.getElementById('exportCSVBtn').addEventListener('click', () => this.exportCSV());
    }
    
    handleSubmit(e) {
        e.preventDefault();
        
        const client = {
            id: Date.now(),
            name: document.getElementById('clientName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            service: document.getElementById('service').value,
            notes: document.getElementById('notes').value,
            date: new Date().toISOString()
        };
        
        // Validate
        if (!this.validateClient(client)) {
            alert('Please fill in all required fields');
            return;
        }
        
        this.clients.push(client);
        this.saveClients();
        this.renderClients();
        document.getElementById('intakeForm').reset();
        this.speak(`Client ${client.name} added successfully`);
    }
    
    validateClient(client) {
        return client.name && client.email && client.service;
    }
    
    handleSearch(e) {
        const query = e.target.value.toLowerCase();
        const filtered = this.clients.filter(c => 
            c.name.toLowerCase().includes(query) ||
            c.email.toLowerCase().includes(query)
        );
        this.renderClients(filtered);
    }
    
    renderClients(clients = this.clients) {
        const list = document.getElementById('recordsList');
        
        if (clients.length === 0) {
            list.innerHTML = '<div class="empty-message">No clients yet. Add one to get started!</div>';
            return;
        }
        
        list.innerHTML = clients.map(c => `
            <div class="record-item">
                <h3>${c.name}</h3>
                <p><strong>Email:</strong> <a href="mailto:${c.email}" class="email">${c.email}</a></p>
                <p><strong>Phone:</strong> ${c.phone || 'N/A'}</p>
                <p><strong>Service:</strong> ${c.service}</p>
                <p><strong>Notes:</strong> ${c.notes || 'N/A'}</p>
                <p><strong>Added:</strong> ${new Date(c.date).toLocaleDateString()}</p>
            </div>
        `).join('');
    }
    
    exportJSON() {
        const json = JSON.stringify(this.clients, null, 2);
        const blob = new Blob([json], {type: 'application/json'});
        this.downloadFile(blob, 'clients.json');
    }
    
    exportCSV() {
        let csv = 'Name,Email,Phone,Service,Notes,Date\n';
        csv += this.clients.map(c => 
            `"${c.name}","${c.email}","${c.phone}","${c.service}","${c.notes}","${c.date}"`
        ).join('\n');
        
        const blob = new Blob([csv], {type: 'text/csv'});
        this.downloadFile(blob, 'clients.csv');
    }
    
    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
    
    saveClients() {
        localStorage.setItem('clients', JSON.stringify(this.clients));
    }
    
    loadClients() {
        const stored = localStorage.getItem('clients');
        return stored ? JSON.parse(stored) : [];
    }
    
    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            speechSynthesis.speak(utterance);
        }
    }
}

const app = new ClientIntakeApp();
'''
        
        # README
        readme_content = '''# Client Intake Web App

A modern, responsive web application for collecting and managing client intake information.

## Features

- ✅ Client intake form with validation
- ✅ Local storage persistence (no backend required)
- ✅ Real-time search and filtering
- ✅ Export to JSON or CSV
- ✅ Responsive design
- ✅ Text-to-speech confirmation
- ✅ Production-ready HTML/CSS/JavaScript

## Quick Start

1. Open `index.html` in a modern web browser
2. Fill out the client intake form
3. Submit to add clients
4. Search for existing clients
5. Export data as JSON or CSV

## Structure

- `index.html` - Main form and UI
- `style.css` - Responsive styling
- `app.js` - Client-side logic and storage

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Data Storage

Clients are stored in browser's localStorage. Data persists across browser sessions.

## Export

- JSON: Full structured data export
- CSV: Spreadsheet-compatible format

## Notes

This is a fully functional, production-ready application. No external dependencies or backend server required.
'''
        
        # Write files
        (project_path / 'index.html').write_text(html_content)
        (project_path / 'style.css').write_text(css_content)
        (project_path / 'app.js').write_text(js_content)
        (project_path / 'README.md').write_text(readme_content)
        
        logger.info(f"Generated project files in {project_path}")
        
        return {
            "project_name": project_name,
            "project_path": str(project_path),
            "files_created": [
                "index.html",
                "style.css",
                "app.js",
                "README.md"
            ],
            "status": "COMPLETE",
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_python_project(self, project_name: str = "python_app") -> Dict[str, Any]:
        """Generate a Python project template"""
        
        project_path = self.workspace_path / project_name
        project_path.mkdir(exist_ok=True)
        
        # Create Python package structure
        (project_path / project_name).mkdir(exist_ok=True)
        (project_path / project_name / '__init__.py').write_text('')
        (project_path / project_name / 'main.py').write_text(
            f'"""Main entry point for {project_name}"""\n\nif __name__ == "__main__":\n    print("Hello from {project_name}")')
        
        (project_path / 'README.md').write_text(f'# {project_name}\n\nPython application.\n')
        (project_path / 'requirements.txt').write_text('# Add dependencies here\n')
        (project_path / '.gitignore').write_text('__pycache__/\n*.pyc\n.env\n')
        
        logger.info(f"Generated Python project: {project_name}")
        
        return {
            "project_name": project_name,
            "project_path": str(project_path),
            "language": "python",
            "status": "COMPLETE"
        }
