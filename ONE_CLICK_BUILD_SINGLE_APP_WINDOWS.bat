@echo off
REM ONE_CLICK_BUILD_SINGLE_APP_WINDOWS.bat
REM ZenithStudio Omega v4.8.0 - Build EXE Artifact

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  ZenithStudio Omega v4.8.0 - Windows Artifact Build
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo [1/4] Installing build dependencies...
pip install pyinstaller >nul 2>&1

echo [2/4] Building EXE with PyInstaller...
if exist "dist" rmdir /s /q dist

pyinstaller --onefile --windowed --icon=icon.ico --name=ZenithStudio ZenithStudio.py

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo [3/4] Generating runtime manifest...
python scripts/Generate_Runtime_Manifest_Windows.ps1

echo [4/4] Creating package structure...
if not exist "dist\ZenithStudio_Data" mkdir dist\ZenithStudio_Data

echo.
echo Build complete!
echo Executable: dist\ZenithStudio.exe
echo.

pause
