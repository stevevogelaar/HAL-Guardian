"""
HAL Guardian Streamlit Application
Edge/on-device security suite powered by Gemma 4.
"""
import json
import sys
from pathlib import Path

import streamlit as st

# Ensure module imports work whether run as `streamlit run app.py` or via package
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hal_guardian.config import APP_TITLE, APP_ICON, DATA_DIR
from hal_guardian.code_guardian import review_file, review_code
from hal_guardian.trust_shield import scan_input
from hal_guardian.audit_engine import health_snapshot, read_audit_tail

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("Runs locally on Gemma 4 via Ollama. Nothing leaves your machine unless you choose to export it.")

# Sidebar navigation
page = st.sidebar.radio(
    "Choose a module",
    ["Home", "Code Guardian", "Trust Shield", "Audit Engine", "Health"],
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
                st.markdown("### Findings")
                if result.findings:
                    for f in result.findings:
                        st.markdown(f"- **{f.severity}** [{f.category}] {f.description}")
                st.markdown("### Full review")
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
            st.markdown("### Full review")
            st.text(result.raw_response)

elif page == "Trust Shield":
    st.subheader("Trust Shield — Untrusted Input Scanner")
    text = st.text_area("Paste untrusted text, prompt, or email content", height=200)
    source = st.selectbox("Source classification", ["untrusted", "unknown", "trusted"])
    decode = st.checkbox("Decode embedded payloads (base64, hex, URL-encoded)", value=True)
    if st.button("Scan input") and text:
        report = scan_input(text, source=source, decode_payloads=decode)
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
