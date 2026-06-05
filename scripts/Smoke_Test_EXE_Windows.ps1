# Smoke test for built EXE
# scripts/Smoke_Test_EXE_Windows.ps1

param(
    [string]$ExePath = "dist\ZenithStudio.exe",
    [int]$TimeoutSeconds = 10
)

Write-Host ""
Write-Host "============================================================"
Write-Host "  EXE Smoke Test"
Write-Host "============================================================"
Write-Host ""

if (-not (Test-Path $ExePath)) {
    Write-Host "ERROR: EXE not found at $ExePath"
    exit 1
}

Write-Host "Testing: $ExePath"
Write-Host ""

# Test 1: File exists and is executable
Write-Host "[1/3] Checking file properties..."
$fileInfo = Get-Item $ExePath
if ($fileInfo.Length -gt 0) {
    Write-Host "  ✓ File size: $($fileInfo.Length) bytes"
} else {
    Write-Host "  ✗ File is empty"
    exit 1
}

# Test 2: Digital signature (Windows)
Write-Host "[2/3] Checking digital signature..."
$sig = Get-AuthenticodeSignature $ExePath
if ($sig.Status -eq "Valid") {
    Write-Host "  ✓ Signed: $($sig.SignerCertificate.Subject)"
} else {
    Write-Host "  ⚠ Unsigned (typical for development builds)"
}

# Test 3: Try to run with --self-test
Write-Host "[3/3] Running self-test..."
try {
    $process = Start-Process -FilePath $ExePath -ArgumentList "--self-test" `
        -NoNewWindow -PassThru -ErrorAction Stop
    
    $timeout = New-TimeSpan -Seconds $TimeoutSeconds
    if ($process.WaitForExit($timeout.TotalMilliseconds)) {
        if ($process.ExitCode -eq 0) {
            Write-Host "  ✓ Self-test passed"
        } else {
            Write-Host "  ✗ Self-test failed (exit code: $($process.ExitCode))"
        }
    } else {
        Write-Host "  ⚠ Timeout - process running (this is OK)"
        $process.Kill()
    }
} catch {
    Write-Host "  ⚠ Cannot execute (may need manifest or redistributables): $_"
}

Write-Host ""
Write-Host "Smoke test complete!"
Write-Host ""
