@echo off
REM HAL Guardian Streamlit launcher
REM Kills stale HAL Guardian processes, verifies dependencies, then starts fresh.

REM Use the directory this batch file lives in as the project root
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

set PYTHON=C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe
set URL=http://localhost:8501
set "APP_PATH=%PROJECT_ROOT%app.py"
set OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe
set OLLAMA_URL=http://127.0.0.1:11434

cls
echo.
echo ============================================
echo   HAL Guardian - Local AI Security Suite
echo ============================================
echo.

REM --- Kill stale HAL Guardian processes ---
echo Stopping any existing HAL Guardian Streamlit processes...
for /f "tokens=2 delims=," %%a in ('wmic process where "name='python.exe' and CommandLine like '%%%APP_PATH%%%'" get ProcessId /format:csv ^| findstr "[0-9]"') do (
    echo   Stopping python.exe PID %%a
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=2 delims=," %%a in ('wmic process where "name='streamlit.exe'" get ProcessId /format:csv ^| findstr "[0-9]"') do (
    echo   Stopping streamlit.exe PID %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM --- Dependency: Ollama ---
echo.
echo Checking Ollama at %OLLAMA_URL%...
%PYTHON% -c "import urllib.request; urllib.request.urlopen('%OLLAMA_URL%', timeout=3)" >nul 2>&1
if %errorlevel% neq 0 (
    echo   Ollama is not reachable.
    if exist "%OLLAMA_EXE%" (
        echo   Starting Ollama from %OLLAMA_EXE%...
        start "" /B "%OLLAMA_EXE%" serve
        timeout /T 8 /NOBREAK >nul
        %PYTHON% -c "import urllib.request; urllib.request.urlopen('%OLLAMA_URL%', timeout=3)" >nul 2>&1
        if %errorlevel% neq 0 (
            echo   ERROR: Ollama still not reachable after auto-start.
            echo   Please run Ollama manually and press any key to retry.
            pause >nul
            goto :ollama_check
        ) else (
            echo   Ollama is now running.
        )
    ) else (
        echo   ERROR: Ollama executable not found at %OLLAMA_EXE%.
        echo   Please install Ollama from https://ollama.com/download
        pause
        exit /b 1
    )
) else (
    echo   Ollama is reachable.
)

REM --- Dependency: Gemma 4 model ---
echo.
echo Checking for a local Gemma 4 model...
%PYTHON% -c "import ollama; m=[x['name'] for x in ollama.Client(host='%OLLAMA_URL%').list()['models']]; assert any('gemma' in x for x in m), 'No gemma model found'" >nul 2>&1
if %errorlevel% neq 0 (
    echo   No Gemma model found locally. Pulling gemma4:e2b...
    "%OLLAMA_EXE%" pull gemma4:e2b
    if %errorlevel% neq 0 (
        echo   ERROR: Failed to pull gemma4:e2b. Check your internet connection and Ollama setup.
        pause
        exit /b 1
    )
) else (
    echo   Gemma model is available.
)

REM --- Dependency: SQLite / memory ---
echo.
echo Initializing SQLite memory...
%PYTHON% -c "from hal_guardian.memory import init_db; init_db(); print('OK')" >nul 2>&1
if %errorlevel% neq 0 (
    echo   WARNING: SQLite memory initialization failed. Some features may not persist across restarts.
) else (
    echo   SQLite memory is ready.
)

REM --- Python dependencies ---
echo.
echo Checking Python dependencies...
%PYTHON% -c "import streamlit, ollama, requests, pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo   Missing dependencies. Installing from requirements.txt...
    "%PYTHON%" -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo   ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo   Core dependencies are present.
)

REM --- Launch Streamlit ---
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

:ollama_check
REM Re-check Ollama if we paused for manual start above
%PYTHON% -c "import urllib.request; urllib.request.urlopen('%OLLAMA_URL%', timeout=3)" >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is still not reachable. Exiting.
    pause
    exit /b 1
)
