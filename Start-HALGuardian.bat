@echo off
REM HAL Guardian Streamlit launcher
REM Uses PowerShell for robust process management and dependency checks.

REM Use the directory this batch file lives in as the project root
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

set POWERSHELL=powershell.exe
set PS_SCRIPT=%PROJECT_ROOT%tools\Restart-HALGuardianUI.ps1

cls
echo.
echo ============================================
echo   HAL Guardian - Local AI Security Suite
echo ============================================
echo.
echo Flushing stale HAL Guardian / Streamlit processes...
"%POWERSHELL%" -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name 'python','streamlit' -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 2"
echo.
echo Launching through PowerShell helper...
echo   %PS_SCRIPT%
echo.

if not exist "%PS_SCRIPT%" (
    echo ERROR: Restart helper not found: %PS_SCRIPT%
    pause
    exit /b 1
)

"%POWERSHELL%" -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

if %errorlevel% neq 0 (
    echo.
    echo HAL Guardian exited with an error.
    pause
)
