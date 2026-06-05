# Windows Artifact Proof Check
# scripts/Windows_Artifact_Proof_Windows.ps1

Write-Host ""
Write-Host "============================================================"
Write-Host "  Windows Artifact Proof Check"
Write-Host "============================================================"
Write-Host ""

$artifacts = @{
    "EXE" = "dist\ZenithStudio.exe"
    "Runtime Manifest" = "runtime\runtime_manifest.json"
    "Installer" = "builds\installer\ZenithStudio_Setup.exe"
    "Smoke Test Report" = "logs\exe_smoke_test_report.json"
}

$results = @{}
$allPresent = $true

foreach ($name in $artifacts.Keys) {
    $path = $artifacts[$name]
    $exists = Test-Path $path
    
    if ($exists) {
        $item = Get-Item $path
        Write-Host "✓ $name : Found ($($item.Length) bytes)"
        $results[$name] = @{exists = $true; path = $path; size = $item.Length}
    } else {
        Write-Host "✗ $name : MISSING"
        $results[$name] = @{exists = $false; path = $path}
        $allPresent = $false
    }
}

Write-Host ""
if ($allPresent) {
    Write-Host "Status: PASS - All artifacts present"
    $proofStatus = "PASS"
} else {
    Write-Host "Status: BLOCKED - Missing artifacts"
    Write-Host ""
    Write-Host "Blockers:"
    Write-Host "  - Run ONE_CLICK_BUILD_SINGLE_APP_WINDOWS.bat to build EXE"
    Write-Host "  - Ensure NSIS installer builder is installed for installer"
    Write-Host "  - Run smoke test to generate test report"
    $proofStatus = "BLOCKED"
}

Write-Host ""
$resultsJson = $results | ConvertTo-Json -Depth 10
$resultsPath = "logs\windows_artifact_proof.json"

$dir = Split-Path -Path $resultsPath
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

@{
    timestamp = (Get-Date -Format "o")
    status = $proofStatus
    artifacts = $results
} | ConvertTo-Json -Depth 10 | Out-File -FilePath $resultsPath -Encoding UTF8

Write-Host "Results saved to: $resultsPath"
Write-Host ""
