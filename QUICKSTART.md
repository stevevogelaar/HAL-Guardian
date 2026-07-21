# Quick Start — HAL Guardian

## Install (first time only)

1. **Install Python 3.12+** from https://www.python.org/downloads/

2. **Install Ollama** (local model server):
   - Download: https://ollama.com/download
   - Run the installer and follow the prompts
   - Verify: `ollama --version`

3. **Pull a model** (downloads to your local machine):

```powershell
# Gemma 4 2B — fast, good for demos (recommended for hackathon)
ollama pull gemma4:e2b

# Gemma 4 4B — deeper reasoning, slower
ollama pull gemma4:4b

# Gemma 3 270M — tiny, good for comparison testing
ollama pull gemma3:270m
```

4. **Install Python dependencies** from the project root:

```powershell
& "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

## Run

### Option A — Double-click the batch file

Run `Start-HALGuardian.bat` from the project root folder.

A terminal window opens, starts Streamlit, and prints:

```
Local URL: http://localhost:8501
```

Leave the terminal window open. Open `http://localhost:8501` in your browser.

### Option B — PowerShell one-liner

```powershell
& "C:\Users\Steve Vogelaar\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run "C:\Users\Steve Vogelaar\Documents\_IT Oversight\Hackathon\HAL-Guardian\app.py"
```

### Option C — Restart helper (kills old process first)

```powershell
& "C:\Users\Steve Vogelaar\Documents\_IT Oversight\Hackathon\HAL-Guardian\frontend\start.ps1"
```

## Stop

- Close the terminal window, or
- Press `Ctrl + C` in the terminal and confirm with `Y`.

## First Walkthrough

1. Open the UI at `http://localhost:8501`.
2. Select an **Active model** in the sidebar.
3. Try **Code Guardian**:
   - Upload `data/sample_code/bad_login.php`, or
   - Paste some code, choose the language, and click **Review pasted code**.
4. Try **Trust Shield**:
   - Paste a suspicious email, or upload `data/sample_inputs/suspicious_email.txt`.
   - Check **Deep scan** and click **Scan input**.
5. Open **Audit Engine** to see every action logged locally.
6. Visit **Manual** in the sidebar for full module documentation.

## Optional Webfetch Demo

Webfetch is disabled by default. To test it safely:

1. Go to **Settings** and enable **webfetch**.
2. Add `itoversight.ca` to the whitelist.
3. In **Code Guardian** or **Trust Shield**, choose **Fetch URL**.
4. Use one of the live demo pages:
   - `https://itoversight.ca/Hal_Guardian/broken-code-page.html`
   - `https://itoversight.ca/Hal_Guardian/injection-test-page.html`

Read the warning on the Settings page before enabling webfetch on private networks.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Ollama is not reachable" | Run `ollama serve` in another terminal |
| Browser shows old UI | Close terminal and rerun `Start-HALGuardian.bat` |
| `pip` not found | Use `python -m pip install -r requirements.txt` |
| Switching tabs cancels an in-flight review | Wait for the current model call to finish before changing sidebar modules |
