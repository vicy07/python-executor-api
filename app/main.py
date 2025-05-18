from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
import subprocess
import tempfile
import os
from git import Repo

app = FastAPI(
    title="Python Execution API",
    description="Execute Python code inline or from a Git repository with internet access and dependency management.",
    version="1.0.0"
)

security = HTTPBearer()
EXPECTED_TOKEN = os.getenv("EXEC_API_TOKEN", "changeme")


import logging

def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    logger = logging.getLogger("token-check")
    logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Bearer token received: {token}")

    if token != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


class CodeRequest(BaseModel):
    code: str = Field(..., example="print('Hello, AI!')")


class GitRequest(BaseModel):
    repo_url: str = Field(..., example="https://github.com/user/repo.git")
    branch: Optional[str] = Field(default="main", example="main")


@app.post("/run", summary="Run inline Python code")
async def run_code(payload: CodeRequest, auth=Depends(validate_token)):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(payload.code)
        file_path = f.name

    try:
        # extract and install dependencies if present
    first_line = payload.code.strip().splitlines()[0]
    if first_line.startswith("# pip:"):
        packages = first_line.replace("# pip:", "").strip()
        subprocess.run(["pip", "install"] + packages.split(), check=False)

    result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=15)
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
