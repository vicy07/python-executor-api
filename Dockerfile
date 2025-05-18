# Stage 1: Builder stage
FROM python:3.13-slim AS builder

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Create a virtual environment and install dependencies with uv
RUN uv venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN uv pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.13-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory and ownership preemptively
WORKDIR /app
RUN chown appuser:appuser /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv
RUN chown -R appuser:appuser /app/venv

# Set environment path
ENV PATH="/app/venv/bin:$PATH"

# Switch to non-root user before copying application code
USER appuser

# Copy only the application code with correct ownership using --chown
COPY --chown=appuser:appuser . /app/

# Expose default port (for local dev); actual port is provided by Railway
EXPOSE 8000

# Start FastAPI with dynamic port from Railway or default to 8000 locally
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
