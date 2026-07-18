import json
import subprocess

def run_command(cmd):
    return subprocess.check_output(cmd, shell=True)

# SQL query with parameterization
import sqlite3
conn = sqlite3.connect("users.db")
c = conn.cursor()
name = input("Name: ")
c.execute("SELECT * FROM users WHERE name=?", (name,))
print(c.fetchall())
conn.close()

# No hardcoded secrets; config loaded from env
import os
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API_KEY not set")
