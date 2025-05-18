FROM python:3.13-slim

# Install git for GitPython usage
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
RUN chown appuser:appuser /app

COPY --from=builder /app/venv /app/venv
RUN chown -R appuser:appuser /app/venv

ENV PATH="/app/venv/bin:$PATH"

USER appuser

COPY --chown=appuser:appuser . /app/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
