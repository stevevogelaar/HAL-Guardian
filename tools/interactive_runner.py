#!/usr/bin/env python3
"""
Interactive HAL Guardian tool runner.

Reads tools_manifest.json, lets a user pick a tool, prompts for required
parameters, runs `python orchestrate.py <tool> ...`, and echoes the JSON.

Can also be driven by an AI agent: the agent reads tools_manifest.json,
displays the available tools, asks the user for inputs, then calls this
script or the underlying `orchestrate.py` command.
"""

import json
import shlex
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "tools_manifest.json"
PYTHON = Path("C:/Users/Steve Vogelaar/AppData/Local/Programs/Python/Python312/python.exe")


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"ERROR: tools_manifest.json not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def list_tools(manifest: dict) -> None:
    print(f"\n{manifest['project']} — available tools:\n")
    for idx, tool in enumerate(manifest["tools"], start=1):
        req = [p["name"] for p in tool.get("parameters", []) if p.get("required")]
        req_str = f"Requires: {', '.join(req)}" if req else "No parameters required"
        print(f"  {idx}. {tool['name']}")
        print(f"     {tool['description']}")
        print(f"     Agent: {tool['agent']} | {req_str}\n")


def ask_for_input(prompt_text: str, default=None) -> str:
    full = prompt_text
    if default is not None:
        full = f"{full} [default: {default}]: "
    else:
        full = f"{full}: "
    value = input(full).strip()
    if not value and default is not None:
        return str(default)
    return value


def collect_parameters(tool: dict) -> dict:
    values = {}
    for param in tool.get("parameters", []):
        name = param["name"]
        required = param.get("required", False)
        default = param.get("default")
        description = param.get("description", "")
        prompt = f"{name} — {description}"

        value = ask_for_input(prompt, default)
        while required and not value:
            print("This parameter is required.")
            value = ask_for_input(prompt, default)

        if param.get("type") == "boolean" and isinstance(value, str):
            value = value.lower() in ("true", "yes", "1", "y")

        values[name] = value
    return values


def build_command(manifest: dict, tool_name: str, params: dict) -> list:
    cmd = [str(PYTHON), "orchestrate.py", tool_name]
    for param in manifest["tools"]:
        if param["name"] == tool_name:
            # orchestrate.py expects the primary input as a positional target argument
            target_name = param.get("target_parameter", "target")
            if target_name in params:
                cmd.append(str(params[target_name]))
            for p in param.get("parameters", []):
                name = p["name"]
                if name == target_name:
                    continue
                if name in params:
                    value = params[name]
                    if isinstance(value, bool):
                        flag = f"--{name}={str(value).lower()}"
                    else:
                        flag = f"--{name}={value}"
                    cmd.append(flag)
            break
    return cmd


def run_tool(cmd: list) -> dict:
    print(f"\nRunning: {' '.join(shlex.quote(str(c)) for c in cmd)}\n")
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR: tool failed", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Raw output (not valid JSON):")
        print(result.stdout)
        sys.exit(1)


def parse_cli_args(tool: dict, argv: list) -> dict:
    """Parse --name=value style arguments from the command line."""
    params = {}
    for arg in argv:
        if arg.startswith("--"):
            parts = arg[2:].split("=", 1)
            if len(parts) == 2:
                params[parts[0]] = parts[1]
    return params


def main() -> None:
    manifest = load_manifest()

    if len(sys.argv) >= 2:
        tool_name = sys.argv[1]
    else:
        list_tools(manifest)
        choice = input("Enter tool name or number: ").strip()
        try:
            idx = int(choice) - 1
            tool_name = manifest["tools"][idx]["name"]
        except (ValueError, IndexError):
            tool_name = choice

    tool = next((t for t in manifest["tools"] if t["name"] == tool_name), None)
    if tool is None:
        print(f"ERROR: unknown tool '{tool_name}'", file=sys.stderr)
        sys.exit(1)

    print(f"\nSelected tool: {tool['name']} ({tool['agent']})")
    print(f"{tool['description']}\n")

    cli_params = parse_cli_args(tool, sys.argv[2:])
    missing_required = [
        p["name"] for p in tool.get("parameters", [])
        if p.get("required") and p["name"] not in cli_params
    ]

    if missing_required:
        print("Some required parameters were not provided on the command line.")
        interactive_params = collect_parameters(tool)
        interactive_params.update(cli_params)
        params = interactive_params
    else:
        params = cli_params
        # Fill in defaults for optional parameters not provided
        for p in tool.get("parameters", []):
            if p["name"] not in params and "default" in p:
                params[p["name"]] = p["default"]

    cmd = build_command(manifest, tool_name, params)
    output = run_tool(cmd)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
