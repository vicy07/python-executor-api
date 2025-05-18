import subprocess
import tempfile
import os
from git import Repo

def run_code_from_git(repo_url: str, branch: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        Repo.clone_from(repo_url, tmpdir, branch=branch)
        requirements_path = os.path.join(tmpdir, "requirements.txt")
        if os.path.exists(requirements_path):
            subprocess.run(
                ["pip", "install", "-r", requirements_path],
                capture_output=True,
                text=True
            )
        code_file = os.path.join(tmpdir, "main.py")
        if not os.path.exists(code_file):
            return {
                "stdout": "",
                "stderr": "main.py not found in the repository.",
                "return_code": -1
            }
        try:
            result = subprocess.run(
                ["python", code_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Execution timed out.",
                "return_code": -1
            }
