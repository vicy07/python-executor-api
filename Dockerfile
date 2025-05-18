# Use a minimal official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Install Git to enable cloning repositories
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use an entrypoint that ensures PORT is interpreted by shell
ENTRYPOINT sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
