import subprocess
import tempfile
import os

def execute_code(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        code_file = os.path.join(tmpdir, "main.py")
        with open(code_file, "w") as f:
            f.write(code)
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
