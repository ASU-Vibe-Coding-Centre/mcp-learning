# Use Python 3.11 slim image for smaller size while maintaining compatibility
FROM python:3.11-slim

# Set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1
# Ensure pip doesn't cache packages to keep image size smaller
ENV PIP_NO_CACHE_DIR=1
# Upgrade pip to latest version for better dependency resolution
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
# git: for version control and cloning repositories
# curl: for downloading files and health checks
# vim: for editing files inside container (development convenience)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker layer caching
# If requirements.txt doesn't change, this layer will be cached
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir: don't cache downloaded packages (smaller image)
# --upgrade: ensure we get the latest compatible versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
# This is done after installing dependencies to leverage caching
COPY . .

# Create a non-root user for security best practices
# Running as root inside container is a security risk
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Expose port 3000 for MCP server (common MCP server port)
# This is documentation - actual port mapping happens at runtime
EXPOSE 3000

# Default command: start an interactive shell
# Override this in docker-compose.yml or at runtime for specific servers
CMD ["/bin/bash"]

