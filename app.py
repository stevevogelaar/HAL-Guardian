"""
HAL Guardian Streamlit Application
Edge/on-device security suite powered by Gemma 4.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

# Ensure module imports work whether run as `streamlit run app.py` or via package
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hal_guardian.config import APP_TITLE, APP_ICON, DATA_DIR
from hal_guardian.code_guardian import review_file, review_code
from hal_guardian.trust_shield import scan_input
from hal_guardian.audit_engine import health_snapshot, read_audit_tail
from hal_guardian.orchestrator import run as run_orchestrator, help_text, list_commands

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("Runs locally on Gemma 4 via Ollama. Nothing leaves your machine unless you choose to export it.")

# Restart button in sidebar (requires external helper due to OS process limits)
with st.sidebar:
    st.divider()
    if st.button("Restart Server", help="Writes a restart flag. Run tools\\Restart-HALGuardianUI.ps1 externally to relaunch."):
        restart_flag = Path(__file__).resolve().parent / "tools" / "restart-requested.flag"
        restart_flag.write_text(f"restart requested at {datetime.now(timezone.utc).isoformat()}\n")
        st.warning("Restart flag set. Please run tools\\Restart-HALGuardianUI.ps1 from PowerShell to relaunch the UI.")
    st.divider()

# Sidebar navigation
page = st.sidebar.radio(
    "Choose a module",
    ["Home", "Code Guardian", "Trust Shield", "Audit Engine", "Health", "Subagent Console"],
)

if page == "Home":
    st.markdown("""
    **HAL Guardian** is an edge-deployed AI security assistant built for the Gemma 4 hackathon.

    Use the sidebar to:
    - **Code Guardian** — review source files or pasted code for security, testing, complexity, and style issues.
    - **Trust Shield** — classify untrusted text, prompts, or email content and detect prompt injection or embedded commands.
    - **Audit Engine** — review the last logged actions.
    - **Health** — check Ollama reachability, available models, and recent failure patterns.

    All reasoning is performed locally through Ollama (`gemma4:e2b` by default).
    """)
    snap = health_snapshot()
    st.subheader("Current Environment")
    st.json(snap)

elif page == "Code Guardian":
    st.subheader("Code Guardian — Local Code Review")
    mode = st.radio("Input mode", ["Upload a file", "Paste code"])

    if mode == "Upload a file":
        uploaded = st.file_uploader("Upload source file", type=None)
        if uploaded is not None:
            tmp_path = Path(DATA_DIR) / "uploads" / uploaded.name
            tmp_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path.write_bytes(uploaded.read())
            st.info(f"Saved to {tmp_path}")
            if st.button("Review uploaded file"):
                with st.spinner("Asking Gemma 4 to review locally..."):
                    result = review_file(str(tmp_path))
                st.success(f"Status: {result.execution_status}")
                st.write(f"**Verdict:** `{result.verdict}`")
                st.write(f"**Model:** {result.model}")
                st.json(result.summary_table)
                st.markdown("### Structured findings")
                if result.findings:
                    for f in result.findings:
                        with st.expander(f"{f.severity.upper()} — {f.category} (line {f.line})"):
                            st.write(f.description)
                            st.markdown(f"**Recommendation:** {f.recommendation}")
                with st.expander("Raw review (Markdown)"):
                    st.text(result.raw_response)
    else:
        code = st.text_area("Paste code to review", height=300)
        language = st.text_input("Language", value="python")
        if st.button("Review pasted code") and code:
            with st.spinner("Asking Gemma 4 to review locally..."):
                result = review_code(code, language)
            st.success(f"Status: {result.execution_status}")
            st.write(f"**Verdict:** `{result.verdict}`")
            st.write(f"**Model:** {result.model}")
            st.json(result.summary_table)
            st.markdown("### Structured findings")
            if result.findings:
                for f in result.findings:
                    with st.expander(f"{f.severity.upper()} — {f.category} (line {f.line})"):
                        st.write(f.description)
                        st.markdown(f"**Recommendation:** {f.recommendation}")
            with st.expander("Raw review (Markdown)"):
                st.text(result.raw_response)

elif page == "Trust Shield":
    st.subheader("Trust Shield — Untrusted Input Scanner")
    text = st.text_area("Paste untrusted text, prompt, or email content", height=200)
    source = st.selectbox("Source classification", ["untrusted", "unknown", "trusted"])
    decode = st.checkbox("Decode embedded payloads (base64, hex, URL-encoded)", value=True)
    deep = st.checkbox("Deep scan with Gemma 4 (slower, catches subtle attacks)", value=False)
    if st.button("Scan input") and text:
        with st.spinner("Running Trust Shield..."):
            report = scan_input(text, source=source, decode_payloads=decode, deep=deep)
        st.write(f"**Trust level:** `{report.trust_level}`")
        st.write(f"Command language: {report.contains_command_language}")
        st.write(f"Meta-instruction framing: {report.contains_meta_instruction}")
        st.write(f"Encoded payload: {report.contains_encoded_payload}")
        if report.decoded_payloads:
            st.markdown("### Decoded payloads")
            for p in report.decoded_payloads:
                st.json(p.model_dump())
        if report.findings:
            st.markdown("### Findings")
            for finding in report.findings:
                st.markdown(f"- {finding}")
        if hasattr(report, "deep_analysis") and report.deep_analysis:
            st.markdown("### Deep analysis (Gemma 4)")
            da = report.deep_analysis
            st.write(f"**Verdict:** {da.get('verdict')}")
            st.write(f"**Severity:** {da.get('severity')}")
            st.write(f"**Confidence:** {da.get('confidence')}")
            st.write(f"**Intent:** {da.get('intent')}")
            st.info(da.get("explanation"))
            st.write(f"**Recommended action:** {da.get('recommended_action')}")
            with st.expander("Raw deep analysis"):
                st.text(da.get("raw_response"))
        st.markdown("### Recommendation")
        st.info(report.recommendation)
        st.markdown("### Sanitized text")
        st.text(report.sanitized_text)

elif page == "Audit Engine":
    st.subheader("Audit Engine — Recent Activity")
    limit = st.slider("Number of recent entries", 10, 200, 50)
    records = read_audit_tail(limit=limit)
    st.write(f"Showing last {len(records)} entries from `audits/hal-guardian-audit.jsonl`")
    for r in records:
        st.json(r)

elif page == "Health":
    st.subheader("Health — HAL Guardian Status")
    snap = health_snapshot()
    st.json(snap)
    if snap["ollama_status"] == "reachable":
        st.success("Ollama is reachable.")
    else:
        st.error("Ollama is not reachable. Make sure `ollama serve` is running.")

elif page == "Subagent Console":
    st.subheader("Subagent Console — Direct Agent Commands")
    st.markdown("""
    This tab lets you call any HAL Guardian subagent through the orchestrator.
    The same commands work from Python, PowerShell, or another AI agent.

    **Commands:** `review`, `review_code`, `scan`, `health`, `audit`
    """)

    with st.expander("Show command reference"):
        st.text(help_text())

    cmd = st.selectbox("Command", ["review", "review_dir", "review_code", "scan", "health", "audit"])
    target = st.text_area("Target (file path, directory, code, or text)", height=120)

    with st.expander("Modifiers"):
        model = st.text_input("--model", value="gemma4:e2b")
        language = st.text_input("--language", value="python")
        source = st.selectbox("--source", ["untrusted", "trusted", "unknown"], index=0)
        decode = st.selectbox("--decode", ["true", "false"], index=0)
        deep = st.selectbox("--deep", ["false", "true"], index=0)
        deep_model = st.text_input("--deep_model", value="gemma4:e2b")
        recursive = st.selectbox("--recursive", ["false", "true"], index=0)
        limit = st.number_input("--limit", min_value=1, max_value=200, value=10)

    kwargs = {}
    if model:
        kwargs["model"] = model
    if language:
        kwargs["language"] = language
    if source:
        kwargs["source"] = source
    if decode:
        kwargs["decode"] = decode
    if deep:
        kwargs["deep"] = deep
    if deep_model:
        kwargs["deep_model"] = deep_model
    if recursive:
        kwargs["recursive"] = recursive
    if limit:
        kwargs["limit"] = int(limit)

    if st.button("Run subagent"):
        with st.spinner("Routing to subagent..."):
            result = run_orchestrator(cmd, target=target, **kwargs)
        if result.get("ok"):
            st.success(f"Agent `{result['agent']}` completed in {result.get('duration_ms', 0)} ms")
        else:
            st.error(f"Subagent failed: {result.get('error')}")
        st.json(result, expanded=False)

    # Quick action presets
    st.markdown("### Quick presets")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Scan suspicious email"):
            email_path = Path(DATA_DIR) / "sample_inputs" / "suspicious_email.txt"
            text = email_path.read_text(encoding="utf-8")
            result = run_orchestrator("scan", target=text, source="untrusted")
            st.json(result, expanded=False)
    with c2:
        if st.button("Review bad_login.php"):
            result = run_orchestrator("review", target="data/sample_code/bad_login.php", model="gemma4:e2b")
            st.json(result, expanded=False)
    with c3:
        if st.button("Health snapshot"):
            result = run_orchestrator("health")
            st.json(result, expanded=False)
    with c4:
        if st.button("Review sample code dir"):
            result = run_orchestrator("review_dir", target="data/sample_code", model="gemma4:e2b")
            st.json(result, expanded=False)
