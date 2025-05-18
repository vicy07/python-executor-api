# 🐍 Python Execution API on Railway

This service allows safe execution of Python code received via REST API, either as inline source code or from a Git repository. It is designed for integration with AI models that generate Python code.

## 🚀 Features

- `POST /run`: Execute arbitrary Python code (inline).
- `POST /run-from-git`: Clone a specified Git repo and execute its code.
- Automatically installs dependencies (via `# pip:` comment or `requirements.txt`).
- Outbound internet access is supported.
- Returns:
  - `stdout`
  - `stderr`
  - `return_code`
- Secured via token in URL (`?token=...`).

## 🛠 Installation

1. Deploy this repository to [Railway](https://railway.app).
2. Set the required environment variable:

```
EXEC_API_TOKEN=your_token_here
```

3. In Railway UI or CLI, configure the service as:
   - **Service Type**: Serverless
   - **RAM**: 512 MB
   - **CPU**: 1 vCPU

## 🔮 Testing

### Run inline code

```bash
curl -X POST https://<your-app>.up.railway.app/run?token=your_token \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from AI\")"}'
```

### Run code from Git

```bash
curl -X POST https://<your-app>.up.railway.app/run-from-git?token=your_token \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo.git", "branch": "main"}'
```

## 🔒 Security

- Access is protected via URL token.
- Code execution is time-limited.
- Additional sandboxing can be implemented (e.g., Docker-in-Docker, gVisor).

## 📄 License

MIT
