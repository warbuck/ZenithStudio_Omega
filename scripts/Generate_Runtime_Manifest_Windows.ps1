# Generate Runtime Manifest
# scripts/Generate_Runtime_Manifest_Windows.ps1

param(
    [string]$OutputPath = "runtime/runtime_manifest.json"
)

Write-Host "Generating runtime manifest..."

$manifest = @{
    version = "4.8.0"
    codename = "V5 Release Candidate"
    timestamp = (Get-Date -Format "o")
    platform = "Windows"
    python_version = (python --version 2>&1).Split(' ')[1]
    executable = "ZenithStudio.exe"
    data_directory = "ZenithStudio_Data"
    modules = @(
        "AI Operator",
        "AI Orchestrator",
        "Aegis HexaQVM",
        "Mission Runtime",
        "ScoreForge",
        "Senku",
        "RuneWeave",
        "RedMars Scheduler",
        "Proof Gates"
    )
    requirements = @(
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0"
    )
} | ConvertTo-Json -Depth 10

# Create directory if not exists
$dir = Split-Path -Path $OutputPath
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$manifest | Out-File -FilePath $OutputPath -Encoding UTF8

Write-Host "Manifest created: $OutputPath"
