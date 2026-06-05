# Build EXE with PyInstaller on Windows
# scripts/Build_EXE_Windows.ps1

param(
    [string]$IconPath = "icon.ico",
    [string]$OutputDir = "dist",
    [switch]$Windowed = $true
)

Write-Host ""
Write-Host "============================================================"
Write-Host "  Building ZenithStudio.exe with PyInstaller"
Write-Host "============================================================"
Write-Host ""

# Check PyInstaller
$pyinstaller = python -m pip list | Select-String 'pyinstaller'
if ($null -eq $pyinstaller) {
    Write-Host "[1/3] Installing PyInstaller..."
    python -m pip install pyinstaller -q
}

# Build
Write-Host "[2/3] Building EXE..."
if (Test-Path $OutputDir) {
    Remove-Item $OutputDir -Recurse -Force
}

$args = @(
    "--onefile",
    "--name=ZenithStudio",
    "--distpath=$OutputDir",
    "ZenithStudio.py"
)

if ($Windowed) {
    $args += "--windowed"
}

if (Test-Path $IconPath) {
    $args += "--icon=$IconPath"
}

pyinstaller @args

# Check result
if (Test-Path "$OutputDir\ZenithStudio.exe") {
    Write-Host "[3/3] Success!"
    Write-Host ""
    Write-Host "EXE created: $OutputDir\ZenithStudio.exe"
    Write-Host ""
    exit 0
} else {
    Write-Host "ERROR: EXE build failed"
    exit 1
}
