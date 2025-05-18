from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
import subprocess
import tempfile
import logging
import os
from git import Repo

app = FastAPI(
    title="Python Execution API",
    description="Execute Python code inline or from a Git repository with internet access and dependency management.",
    version="1.0.0"
)

EXPECTED_TOKEN = os.getenv("EXEC_API_TOKEN", "changeme")


def validate_token(request: Request, authorization: Optional[str]):
    logger = logging.getLogger("token-check")
    logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    logger.info(f"Authorization header: {authorization}")
    logger.info(f"Query token: {request.query_params.get('token')}")

    token = request.query_params.get("token")
    header_token = None
    if authorization and authorization.lower().startswith("bearer "):
        header_token = authorization[7:]

    final_token = token or header_token
    if final_token != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


class CodeRequest(BaseModel):
    code: str = Field(..., example="print('Hello, AI!')")


class GitRequest(BaseModel):
    repo_url: str = Field(..., example="https://github.com/user/repo.git")
    branch: Optional[str] = Field(default="main", example="main")


@app.post("/run", summary="Run inline Python code")
async def run_code(request: Request, payload: CodeRequest, authorization: Optional[str] = Header(None)):
    validate_token(request, authorization)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(payload.code)
        file_path = f.name

    try:
        result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=15)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    finally:
        os.remove(file_path)


@app.post("/run-from-git", summary="Run Python code from Git repo")
async def run_from_git(request: Request, payload: GitRequest, authorization: Optional[str] = Header(None)):
    validate_token(request, authorization)

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
