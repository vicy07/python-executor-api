# 🐍 Python Execution API on Railway

This service allows safe execution of Python code received via REST API, either as inline source code or from a Git repository. Designed for integration with AI agents that generate Python code.

## 🚀 Features

- `POST /run`: Execute arbitrary Python code (inline).
- `POST /run-from-git`: Clone a specified Git repo and execute its code.
- Accepts optional Python package list in `imports`.
- Outbound internet access is supported.
- Returns:
  - `stdout`
  - `stderr`
  - `return_code`
- Secured via Bearer token (Swagger Authorize supported).

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

## 🧪 Example JSON for `/run`

```json
{
  "imports": ["requests"],
  "code": "import requests\nurl = 'https://api.chucknorris.io/jokes/random'\nresponse = requests.get(url)\nprint(response.json())"
}
```

## 🔄 Git Integration (`/run-from-git`)

```json
{
  "repo_url": "https://github.com/your-user/your-repo.git",
  "branch": "main"
}
```

## 🌐 Endpoints

- Swagger UI: `/docs`
- Root Info: `/`
- GitHub Repo: [vicy07/python-executor-api](https://github.com/vicy07/python-executor-api)

## 📄 License

MIT
