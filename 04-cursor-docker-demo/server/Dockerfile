## Quick Decision Maker MCP Server - Dockerfile
##
## This Dockerfile packages the MCP server for easy deployment.
## The server uses stdio transport, so no ports need to be exposed.

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

## Note: No EXPOSE needed for stdio transport
## MCP servers using stdio communicate via stdin/stdout, not network ports.
## If you switch to HTTP/SSE transport later, you would add: EXPOSE 3333

## Default command: run the MCP server via Python
## When the container starts, this command runs the server.
## Cursor IDE will connect to the container's stdio streams.
CMD ["python", "server.py"]

