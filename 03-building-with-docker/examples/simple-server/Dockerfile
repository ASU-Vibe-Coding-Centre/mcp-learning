## Base image: small Python runtime suitable for production
FROM python:3.11-slim

## Set working directory inside the container
WORKDIR /app

## Install Python dependencies
##
## Using --no-cache-dir keeps the image smaller by not caching wheels.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## Copy application code
COPY server.py ./

## Expose the MCP server port if you switch to HTTP transport later
## (Not required for stdio transport)
# EXPOSE 3333

## Default command: run the MCP server via Python
CMD ["python", "server.py"]


