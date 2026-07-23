@echo off
REM HAL Guardian Streamlit launcher
REM Uses PowerShell for robust process management and dependency checks.

REM Use the directory this batch file lives in as the project root
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

set POWERSHELL=powershell.exe
set PS_SCRIPT=%PROJECT_ROOT%tools\Restart-HALGuardianUI.ps1
set LOG_FILE=%PROJECT_ROOT%logs\start-error.log

REM Ensure logs directory exists
if not exist "%PROJECT_ROOT%logs" mkdir "%PROJECT_ROOT%logs"

cls
echo.
echo ============================================
echo   HAL Guardian - Local AI Security Suite
echo ============================================
echo.
echo Flushing stale HAL Guardian processes...
"%POWERSHELL%" -NoProfile -ExecutionPolicy Bypass -Command "Get-Process -Name 'python','streamlit' -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*HAL-Guardian*' } | Stop-Process -Force; Start-Sleep -Seconds 2"
echo.
echo.
echo ********************************************
echo   DO NOT CLOSE THIS WINDOW
echo   It is running the HAL Guardian server.
echo   Close the browser tab first, then press
echo   Ctrl+C here and confirm Y to stop.
echo ********************************************
echo.
echo Launching through PowerShell helper...
echo   %PS_SCRIPT%
echo.

if not exist "%PS_SCRIPT%" (
    echo ERROR: Restart helper not found: %PS_SCRIPT%
    pause
    exit /b 1
)

REM Run the PowerShell script and capture ALL output (stdout + stderr) to log file
"%POWERSHELL%" -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" >> "%LOG_FILE%" 2>&1

if %errorlevel% neq 0 (
    echo.
    echo HAL Guardian exited with an error. Code: %errorlevel%
    echo See log: %LOG_FILE%
    type "%LOG_FILE%"
    echo.
    pause
)
