FROM python:3.12-slim

WORKDIR /workspace

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir requests beautifulsoup4 numpy matplotlib

# Set a non-root user for security
RUN useradd -m appuser && chown -R appuser /workspace
USER appuser