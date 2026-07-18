"""
HAL Guardian Streamlit launcher — fresh entry point.
Use this if app.py gives stale import errors.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

import streamlit.web.cli as stcli

stcli.main()
