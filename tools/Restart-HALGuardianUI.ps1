# HAL Guardian Streamlit restart helper
# Run this from PowerShell when the UI asks for a restart.
# It kills any python process running the HAL Guardian app, then relaunches it.

# Resolve project root relative to this script's location
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $scriptRoot

param(
    [string]$Port = "8501"
)

$python = "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe"
$app = Join-Path $ProjectRoot "app.py"

Write-Host "Stopping existing HAL Guardian Streamlit processes..."
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*$app*"
} | Stop-Process -Force

Start-Sleep -Seconds 2

Write-Host "Starting HAL Guardian Streamlit on port $Port..."
& $python -m streamlit run $app --server.headless true --server.port $Port
