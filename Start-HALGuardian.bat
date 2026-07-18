@echo off
REM HAL Guardian Streamlit launcher
REM Kills any existing HAL Guardian Streamlit processes, then starts fresh.

REM Use the directory this batch file lives in as the project root
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

set PYTHON=C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe
set URL=http://localhost:8501
set "APP_PATH=%PROJECT_ROOT%app.py"

echo.
echo ============================================
echo   HAL Guardian - Local AI Security Suite
echo ============================================
echo.
echo Stopping any existing HAL Guardian Streamlit processes...
echo.

REM Kill python processes that are running this specific app.py
for /f "tokens=2 delims=," %%a in ('wmic process where "name='python.exe' and CommandLine like '%%%APP_PATH%%%'" get ProcessId /format:csv ^| findstr "[0-9]"') do (
    echo   Stopping python.exe PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Also stop any streamlit.exe processes, just in case
for /f "tokens=2 delims=," %%a in ('wmic process where "name='streamlit.exe'" get ProcessId /format:csv ^| findstr "[0-9]"') do (
    echo   Stopping streamlit.exe PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo Starting Streamlit on %URL%
echo.
echo IMPORTANT:
echo   - Leave this window open while using HAL Guardian.
echo   - Press Ctrl+C then Y to stop the server.
echo.

REM Disable bytecode caching to avoid stale .pyc import issues during development
set PYTHONDONTWRITEBYTECODE=1

"%PYTHON%" -m streamlit run app.py

if %errorlevel% neq 0 (
    echo.
    echo Streamlit exited with an error.
    pause
)
