@echo off
REM HAL Guardian Streamlit launcher
REM Keeps the terminal open and shows the local URL.

cd /d "C:\Users\Steve Vogelaar\Documents\_IT Oversight\_The_HAL_Project\Hackathon"

set PYTHON="C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe"
set URL=http://localhost:8501

echo.
echo ============================================
echo   HAL Guardian - Local AI Security Suite
echo ============================================
echo.
echo Starting Streamlit on %URL%
echo.
echo IMPORTANT:
echo   - Leave this window open while using HAL Guardian.
echo   - Press Ctrl+C then Y to stop the server.
echo.

%PYTHON% -m streamlit run launch.py

if %errorlevel% neq 0 (
    echo.
    echo Streamlit exited with an error.
    pause
)
