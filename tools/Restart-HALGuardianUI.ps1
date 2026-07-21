# HAL Guardian Streamlit restart helper
# Run this from PowerShell when the UI asks for a restart.
# It kills any python process running the HAL Guardian app, then relaunches it.

param(
    [string]$Port = "8501",
    [switch]$StopOnly
)

# Resolve project root relative to this script's location
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $scriptRoot

$python = "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe"
$app = Join-Path $ProjectRoot "app.py"

Write-Host "Stopping existing HAL Guardian Streamlit processes..."
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*$app*"
} | Stop-Process -Force
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

Start-Sleep -Seconds 2

if ($StopOnly) {
    Write-Host "HAL Guardian stopped."
    exit 0
}

# Ensure Ollama is reachable before launching the UI
$ollamaExe = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
$ollamaUrl = "http://127.0.0.1:11434"

try {
    $null = Invoke-WebRequest -Uri $ollamaUrl -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Ollama is reachable."
}
catch {
    if (Test-Path $ollamaExe) {
        Write-Host "Ollama not reachable. Starting $ollamaExe..."
        Start-Process -FilePath $ollamaExe -ArgumentList "serve" -WindowStyle Hidden
        $tries = 0
        while ($tries -lt 15) {
            Start-Sleep -Seconds 2
            try {
                $null = Invoke-WebRequest -Uri $ollamaUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
                Write-Host "Ollama is now running."
                break
            }
            catch {
                $tries++
            }
        }
        if ($tries -ge 15) {
            Write-Host "ERROR: Ollama still not reachable after auto-start. Please start it manually."
            exit 1
        }
    }
    else {
        Write-Host "ERROR: Ollama executable not found at $ollamaExe. Please install Ollama."
        exit 1
    }
}

Write-Host "Starting HAL Guardian Streamlit on port $Port..."
Write-Host "********************************************"
Write-Host "DO NOT CLOSE THIS WINDOW"
Write-Host "It is running the HAL Guardian server."
Write-Host "Close the browser tab first, then press"
Write-Host "Ctrl+C here and confirm Y to stop."
Write-Host "********************************************"
# Note: do not use --server.headless here so Streamlit opens the browser automatically.
& $python -m streamlit run $app --server.port $Port
