from fastapi import FastAPI, Request, HTTPException
from app.executor import execute_code
from app.git_runner import run_code_from_git

app = FastAPI()

EXPECTED_TOKEN = "your_secure_token"

def validate_token(request: Request):
    token = request.query_params.get("token")
    if token != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/run")
async def run_code(request: Request):
    validate_token(request)
    data = await request.json()
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")
    result = execute_code(code)
    return result

@app.post("/run-from-git")
async def run_from_git(request: Request):
    validate_token(request)
    data = await request.json()
    repo_url = data.get("repo_url")
    branch = data.get("branch", "main")
    if not repo_url:
        raise HTTPException(status_code=400, detail="Repository URL not provided")
    result = run_code_from_git(repo_url, branch)
    return result
