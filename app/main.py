from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
import subprocess
import tempfile
import os
import site
from git import Repo

app = FastAPI(
    title="Python Execution API",
    description="Execute Python code inline or from a Git repository with internet access and dependency management.",
    version="1.0.0"
)

security = HTTPBearer()
EXPECTED_TOKEN = os.getenv("EXEC_API_TOKEN", "changeme")


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    if token != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


class CodeRequest(BaseModel):
    code: str = Field(..., example="print('Hello, AI!')")


class GitRequest(BaseModel):
    repo_url: str = Field(..., example="https://github.com/user/repo.git")
    branch: Optional[str] = Field(default="main", example="main")


@app.post("/run", summary="Run inline Python code")
async def run_code(payload: CodeRequest, auth=Depends(validate_token)):
    code_lines = payload.code.strip().splitlines()
    if code_lines and code_lines[0].startswith("# pip:"):
        packages = code_lines[0].replace("# pip:", "").strip()
        subprocess.run(["pip", "install", "--user"] + packages.split(), check=False)

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(payload.code)
        file_path = f.name

    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = site.getusersitepackages()
        result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=15, env=env)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    finally:
        os.remove(file_path)


@app.post("/run-from-git", summary="Run Python code from Git repo")
async def run_from_git(payload: GitRequest, auth=Depends(validate_token)):
    tmp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(payload.repo_url, tmp_dir, branch=payload.branch)
        code_file = os.path.join(tmp_dir, "main.py")

        if os.path.exists(os.path.join(tmp_dir, "requirements.txt")):
            subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=tmp_dir, check=False)

        result = subprocess.run(["python", code_file], capture_output=True, text=True, timeout=15)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    finally:
        os.system(f"rm -rf {tmp_dir}")


@app.get("/", summary="Redirect info")
async def root():
    return {
        "message": "Welcome to Python Executor API",
        "docs": "/docs",
        "repository": "https://github.com/vicy07/python-executor-api"
    }
