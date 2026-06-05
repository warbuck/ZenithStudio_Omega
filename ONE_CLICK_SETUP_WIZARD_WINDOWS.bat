@echo off
REM ONE_CLICK_SETUP_WIZARD_WINDOWS.bat
REM ZenithStudio Omega v4.8.0 - Setup Wizard

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  ZenithStudio Omega v4.8.0 - Setup Wizard
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

echo [1/5] Checking requirements...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo [2/5] Initializing directories...
if not exist "data\missions" mkdir data\missions
if not exist "logs" mkdir logs
if not exist "workspace" mkdir workspace

echo [3/5] Running self-test...
python ZenithStudio.py --self-test >nul 2>&1

echo [4/5] Starting backend...
echo. > nul
echo Backend will start on http://127.0.0.1:5000

echo [5/5] Opening browser...
echo. > nul

echo.
echo Setup complete! Starting ZenithStudio Omega...
echo.

python ZenithStudio.py

pause
