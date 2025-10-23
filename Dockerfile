# Dockerfile for Weather MCP Server
FROM python:3.11-slim

# Set environment variables for non-interactive mode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OPENWEATHER_API_KEY=

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY *.py .

# Set the entrypoint to run the server
ENTRYPOINT ["python", "-u", "server.py"]
