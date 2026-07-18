# Quick Start — HAL Guardian

## Install (first time only)

1. Install Python 3.12+ and Ollama.
2. Pull the default model:

```powershell
ollama pull gemma4:e2b
```

3. Install Python dependencies:

```powershell
& "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

## Run

### Option A — Double-click the batch file

Run `Start-HALGuardian.bat` from this folder.

A terminal window opens, starts Streamlit, and prints:

```
Local URL: http://localhost:8501
```

Leave the terminal window open. Open `http://localhost:8501` in your browser.

### Option B — PowerShell one-liner

```powershell
& "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run "C:\Users\Steve Vogelaar\Documents\_IT Oversight\_The_HAL_Project\Hackathon\app.py"
```

### Option C — Restart helper (kills old process first)

```powershell
& "C:\Users\Steve Vogelaar\Documents\_IT Oversight\_The_HAL_Project\Hackathon\tools\Restart-HALGuardianUI.ps1"
```

## Stop

- Close the terminal window, or
- Press `Ctrl + C` in the terminal and confirm with `Y`.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Ollama is not reachable" | Run `ollama serve` in another terminal |
| Browser shows old UI | Close terminal and rerun `Start-HALGuardian.bat` |
| `pip` not found | Use `python -m pip install -r requirements.txt` |
