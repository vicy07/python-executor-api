FROM python:3.11-slim

# Install essential build tools and libraries for most pip packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    pkg-config \
    wget \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libjpeg-dev \
    libfreetype6-dev \
    locales \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set UTF-8 locale for Unicode support
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app

# Create unprivileged user for better security
RUN useradd -m appuser
RUN chown -R appuser /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

# Expose the default port for FastAPI/Uvicorn
EXPOSE 8000

# Start the app with Uvicorn, using a dynamic port if set by the environment
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
