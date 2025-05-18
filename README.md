# 🐍 Python Execution API on Railway

This service allows safe execution of Python code received via REST API, either as inline source code or from a Git repository. It is designed for integration with AI models that generate Python code.

## 🚀 Features

- `POST /run`: Execute arbitrary Python code (inline).
- `POST /run-from-git`: Clone a specified Git repo and execute its code.
- Automatically installs dependencies via `# pip: package1 package2`.
- Outbound internet access is supported.
- Returns:
  - `stdout`
  - `stderr`
  - `return_code`
- Secured via Bearer token (global Swagger Authorize supported).

## 🛠 Installation

1. Deploy this repository to [Railway](https://railway.app).
2. Set the required environment variable:

```
EXEC_API_TOKEN=your_token_here
```

3. Configure the service:
   - **Service Type**: Serverless
   - **RAM**: 512 MB
   - **CPU**: 1 vCPU
   - **PORT**: 8000

## 🔐 Security

- Use Swagger UI's `Authorize` button to input:
  ```
  Bearer your_token_here
  ```
- Token is validated for all protected endpoints.

## 🔍 Example Input for `/run`

### Input (JSON body):

```json
{
  "code": "# pip: requests\nimport requests\nr = requests.get(\"https://api.ipify.org?format=json\")\nprint(\"IP:\", r.json()[\"ip\"])"
}
```

### Header:

```
Authorization: Bearer your_token_here
```

## 🔄 Git Integration (`/run-from-git`)

```json
{
  "repo_url": "https://github.com/your-user/your-repo.git",
  "branch": "main"
}
```

## 🌐 Useful Endpoints

- Swagger UI: [`/docs`](https://python-executor-api-production.up.railway.app/docs)
- Root Info: [`/`](https://python-executor-api-production.up.railway.app/)
- GitHub Repo: [vicy07/python-executor-api](https://github.com/vicy07/python-executor-api)

## 📄 License

MIT
