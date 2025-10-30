# HTTP Transport Version

This directory contains both stdio and HTTP versions of the practical server:

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
- Includes data persistence with SQLite

## Building the HTTP Version

```bash
docker build -f Dockerfile.http -t practical-mcp-server:http .
```

## Running the HTTP Version

```bash
# Create data directory for SQLite
mkdir -p data

# Run with volume mount for data persistence
docker run -d -p 3333:3333 -v "$PWD/data":/app/data --name practical-mcp practical-mcp-server:http
```

Note: Use a different port if you already have another server running on 3333:
```bash
docker run -d -p 3334:3333 -v "$PWD/data":/app/data --name practical-mcp practical-mcp-server:http
```

## Connecting from Cursor IDE

```json
{
  "mcpServers": {
    "practical": {
      "type": "http",
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

Or if using a different port:
```json
{
  "mcpServers": {
    "practical": {
      "type": "http",
      "url": "http://localhost:3334/mcp"
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
6. SQLite database persists in mounted volume
7. Cleaner, more maintainable code (~30 lines vs ~60 lines for manual ASGI)

## Tools Available

- `create_note` - Create a new note
- `get_note` - Get a note by ID
- `list_notes` - List all notes (most recent first)
- `update_note` - Update a note's title and/or content
- `delete_note` - Delete a note by ID

## Resources

- For more details on Streamable HTTP vs stdio, see the Module 03 documentation
- For advanced HTTP transport patterns, see `advanced/` directory

