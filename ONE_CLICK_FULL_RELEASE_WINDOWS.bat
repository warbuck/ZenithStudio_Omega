@echo off
REM ONE_CLICK_FULL_RELEASE_WINDOWS.bat
REM ZenithStudio Omega v4.8.0 - Full Release Build

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  ZenithStudio Omega v4.8.0 - Full Release Build
echo  V5 Release Candidate Gate / Promotion Ledger Build
echo ============================================================
echo.

echo [Phase 1-5] Running proof gates...
python ZenithStudio.py --self-test
python ZenithStudio.py --ui-link-audit
python ZenithStudio.py --integration-tracker

echo.
echo [Phase 6] Building Windows artifacts...
echo.

REM Build EXE
echo Building EXE...
pip install pyinstaller >nul 2>&1
if exist "dist" rmdir /s /q dist
pyinstaller --onefile --name=ZenithStudio ZenithStudio.py

if errorlevel 1 (
    echo ERROR: EXE build failed
    pause
    exit /b 1
)

echo Creating application data directory...
if not exist "dist\ZenithStudio_Data" mkdir dist\ZenithStudio_Data
copy /Y data\*.* dist\ZenithStudio_Data >nul 2>&1

echo.
echo [Phase 7] Running operational mission proof...
python -c "from app.buildtools.operational_mission_proof import OperationalMissionProof; p = OperationalMissionProof(); print(p.run())"

echo.
echo [Phase 8] Checking V5 promotion readiness...
python ZenithStudio.py --v5-release-candidate

echo.
echo ============================================================
echo  Release build complete!
echo ============================================================
echo.
echo Artifacts:
echo   - dist\ZenithStudio.exe
echo   - runtime\runtime_manifest.json
echo   - builds\final\client_intake.zip
echo   - logs\exe_smoke_test_report.json
echo   - logs\operational_mission_evidence.json
echo.
echo Check data/integration_tracker/v5_promotion_ledger.json
echo to see if version_5_promotable is true.
echo.

pause
