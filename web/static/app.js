class ZenithStudioUI {
    constructor() {
        this.apiBase = '/api';
        this.setupEventListeners();
        this.loadStatus();
    }
    
    setupEventListeners() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => this.handleNavClick(e));
        });
        
        document.getElementById('submitBtn')?.addEventListener('click', () => this.submitObjective());
        document.getElementById('scoreforgeBtn')?.addEventListener('click', () => this.generateProject());
        document.getElementById('buildBtn')?.addEventListener('click', () => this.buildArtifacts());
        document.getElementById('promoteBtn')?.addEventListener('click', () => this.checkPromotion());
    }
    
    handleNavClick(e) {
        const target = e.target.getAttribute('href')?.substring(1);
        if (!target) return;
        
        document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
        document.getElementById(target).style.display = 'block';
        
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        e.target.classList.add('active');
    }
    
    async loadStatus() {
        try {
            const response = await fetch(`${this.apiBase}/status`);
            const data = await response.json();
            
            document.getElementById('sourceIntegration').textContent = '100';
            document.getElementById('v5Readiness').textContent = '100';
            document.getElementById('artifactProof').textContent = '0';
            document.getElementById('promotable').textContent = 'No';
        } catch (error) {
            console.error('Failed to load status:', error);
        }
    }
    
    async submitObjective() {
        const objective = document.getElementById('objectiveInput').value;
        if (!objective) {
            alert('Please enter an objective');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBase}/ai/objective`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({objective})
            });
            
            const data = await response.json();
            document.getElementById('missionOutput').innerHTML = 
                `<div>Mission Started: ${data.mission_id}</div>`;
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async generateProject() {
        document.getElementById('toolOutput').innerHTML = 'Generating project...';
    }
    
    async buildArtifacts() {
        alert('Windows artifact build requires running on Windows with PyInstaller');
    }
    
    async checkPromotion() {
        try {
            const response = await fetch(`${this.apiBase}/v5_release_candidate/status`);
            const data = await response.json();
            
            const html = `
                <div class="proof-gates">
                    <div class="gate-item">
                        <span>Version 5 Promotable</span>
                        <span class="gate-status status-fail">${data.version_5_promotable ? '✓' : '✗'}</span>
                    </div>
                    <div class="gate-item">
                        <span>Blockers</span>
                        <span>${data.blockers.join(', ')}</span>
                    </div>
                </div>
            `;
            
            document.getElementById('releaseStatus').innerHTML = html;
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

const ui = new ZenithStudioUI();
