## Base image: slim Python for smaller footprint
FROM python:3.11-slim

## Working directory inside the container
WORKDIR /app

## Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## Copy application code
COPY server.py ./

## Data directory for SQLite persistence (bind-mount from host recommended)
RUN mkdir -p /app/data
VOLUME ["/app/data"]

## Default command: run the MCP stdio server
CMD ["python", "server.py"]


