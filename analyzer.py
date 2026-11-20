import ast
import subprocess
import tempfile
from pathlib import Path


def analyze_code(code: str, filename: str = "reviewed_code.py") -> dict:
    """
    Run Ruff and Bandit on Python code and return their findings.
    """

    if not filename.endswith(".py"):
        return {
            "ruff_findings": [],
            "bandit_findings": [],
            "error": "Only Python files are supported."
        }

    # Check that the supplied code is valid Python.
    try:
        ast.parse(code)
    except SyntaxError as error:
        return {
            "ruff_findings": [],
            "bandit_findings": [],
            "error": f"Python syntax error: {error}"
        }

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / Path(filename).name
        file_path.write_text(code, encoding="utf-8")

        # Run Ruff for code quality checks.
        ruff_result = subprocess.run(
            ["ruff", "check", str(file_path), "--output-format", "json"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )

        # Run Bandit for security checks.
        bandit_result = subprocess.run(
            ["bandit", "-f", "json", str(file_path)],
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )

        import json

        try:
            ruff_findings = json.loads(ruff_result.stdout)
        except json.JSONDecodeError:
            ruff_findings = []

        try:
            bandit_data = json.loads(bandit_result.stdout)
            bandit_findings = bandit_data.get("results", [])
        except json.JSONDecodeError:
            bandit_findings = []

    return {
        "ruff_findings": ruff_findings,
        "bandit_findings": bandit_findings,
        "error": None
    }