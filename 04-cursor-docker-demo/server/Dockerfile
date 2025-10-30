## Quick Decision Maker MCP Server - Dockerfile
##
## This Dockerfile packages the MCP server for easy deployment.
## The server uses FastAPI with Streamable HTTP transport, so port 3333 is exposed.

## Base image: Python 3.11 slim for small image size
## Using slim variant reduces image size while maintaining compatibility
FROM python:3.11-slim

## Set working directory inside the container
## All commands will run from this directory
WORKDIR /app

## Install Python dependencies
##
## Using --no-cache-dir keeps the image smaller by not caching pip's download cache.
## This reduces final image size significantly.
## We copy requirements.txt first so Docker can cache this layer separately.
## If we change server.py but not requirements.txt, Docker won't reinstall dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## Copy application code
## This is done after installing dependencies so code changes don't invalidate
## the dependency cache layer.
COPY server.py ./

## Expose port 3333 for HTTP transport
## MCP servers using Streamable HTTP transport communicate over HTTP.
## The server listens on port 3333 inside the container.
EXPOSE 3333

## Default command: run the MCP server via Python
## When the container starts, this command runs the HTTP server.
## Cursor IDE will connect to http://localhost:3333/mcp
CMD ["python", "server.py"]

