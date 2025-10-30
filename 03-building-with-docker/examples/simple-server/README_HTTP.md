# HTTP Transport Version

This directory contains both stdio and HTTP versions of the simple server:

- `server.py` - stdio transport version (original)
- `server_http.py` - Streamable HTTP transport version
- `Dockerfile` - for stdio version
- `Dockerfile.http` - for HTTP version

## Why Two Versions?

**stdio transport** (`server.py`):
- Simpler to set up and debug
- Good for local development and testing
- Used in MCP Inspector for interactive testing
- No network configuration needed

**Streamable HTTP transport** (`server_http.py`):
- Uses FastAPI for clean, simple implementation
- Can run in Docker and be accessed remotely
- Better for production deployments
- Multiple clients can connect to the same server
- Recommended approach for containerized servers

## Building the HTTP Version

```bash
docker build -f Dockerfile.http -t simple-mcp-server:http .
```

## Running the HTTP Version

```bash
docker run -d -p 3333:3333 --name simple-mcp simple-mcp-server:http
```

## Connecting from Cursor IDE

```json
{
  "mcpServers": {
    "simple": {
      "type": "http",
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

## Testing

The HTTP server exposes the `/mcp` endpoint. You can test it with:

```bash
curl -H "Accept: text/event-stream" http://localhost:3333/mcp
```

You should see a JSON-RPC error about missing session ID (expected - Cursor will establish the session).

## Differences from stdio Version

1. Uses FastAPI for streamlined HTTP handling
2. Uses `StreamableHTTPSessionManager` instead of `stdio_server`
3. FastAPI's built-in lifespan management
4. Exposes port 3333 for HTTP connections
5. Uses uvicorn as the ASGI server
6. Cleaner, more maintainable code (~30 lines vs ~60 lines for manual ASGI)

## Resources

- For more details on Streamable HTTP vs stdio, see the Module 03 documentation
- For advanced HTTP transport patterns, see `advanced/` directory

