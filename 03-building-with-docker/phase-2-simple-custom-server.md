## Phase 2: Build a Simple Custom MCP Server

In this phase you will build a minimal MCP server (e.g., dice roller, coin flip, or random quote generator), containerize it with Docker, and test it from Cursor IDE.

### Time Estimate
45–60 minutes

### Prerequisites
- Completed Phase 1
- Docker installed and running
- Python basics (functions, modules) if you want to extend the server

### What You’ll Build
You’ll build a tiny MCP server called "Lucky Dice & Timekeeper" that exposes two tools:
- roll_dice(sides: integer = 6, rolls: integer = 1) → list of integers
  - Returns one or more random integers between 1 and `sides`
- get_timestamp() → string
  - Returns the current timestamp in ISO 8601 format

Both tools will have clear JSON schemas, validation, and type hints. This is inspired by dice‑roller demos (e.g., NetworkChuck) but extends with multiple rolls and ISO timestamps to be a bit more practical and testable.

### Server Type Decision
Chosen type: Dice roller + timestamp utility ("Lucky Dice & Timekeeper").

### Project Layout
This repository includes a scaffold under `03-building-with-docker/examples/simple-server/`:
- `server.py` – server entrypoint (to be implemented in this phase)
- `Dockerfile` – minimal Python base image
- `requirements.txt` – dependencies (MCP SDK)

### Implementing the Tools (High-Level)
1) Define input/output schemas for each tool (e.g., sides: integer for roll_dice)
2) Implement tool logic and validation with clear type hints and docstrings
3) Register tools with the MCP server and start the HTTP server

You’ll add the concrete implementation directly in `server.py`.

### Building the Docker Image
Run these from `03-building-with-docker/examples/simple-server/` after the implementation is complete:

```bash
docker build -t simple-mcp-server:latest .
```

Tips:
- Ensure `requirements.txt` and `server.py` are in the same directory as the `Dockerfile`.
- Use `--no-cache` to force a clean build if dependencies changed:

```bash
docker build --no-cache -t simple-mcp-server:latest .
```

Verify the image exists:

```bash
docker images | grep simple-mcp-server
```

### Running the Container
This example server uses stdio transport, so no ports are required. Run:

```bash
docker run --rm --name simple-mcp simple-mcp-server:latest
```

Notes:
- For interactive testing with MCP Inspector, run the Python script directly on your host instead of inside Docker: `npx @modelcontextprotocol/inspector python server.py`
- To expose HTTP instead of stdio, you would switch to a Streamable HTTP transport server implementation (see Module 04 for an example).

### Connecting from Cursor IDE
Add or update your MCP configuration to include the server:

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

### Testing
Try prompts that invoke your tools, for example:
- "Roll a 6-sided die"
- "Give me the current timestamp"

You should see JSON responses produced by your containerized server.

#### Testing from Cursor IDE
1) Add the server to your MCP config as described above.
2) Open a new chat and type natural prompts that map to tools:
   - "Roll 3 six-sided dice"
   - "What time is it right now?"
3) Expected behavior:
   - For dice: a message like `Rolled 3 d6: [2, 5, 1]`
   - For timestamp: an ISO 8601 UTC string like `2025-01-15T12:34:56.789012+00:00`

If you get an error, check the server logs and verify your MCP configuration URL.

### Understanding the Code (Line-by-Line Highlights)
Open `examples/simple-server/server.py`:

1) Imports and server setup
- `from mcp.server import Server` – core MCP server class
- `from mcp.server.stdio import stdio_server` – stdio transport for JSON‑RPC
- `app = Server("lucky-dice-timekeeper")` – server identity shown to clients

2) Tool advertisement
- `@app.list_tools()` – declares available tools to the client
- Returns two `Tool` objects with `name`, `description`, and `inputSchema`
- `roll_dice` schema: `sides` (int, min 2, default 6), `rolls` (int, 1–100, default 1)
- `get_timestamp` schema: empty object (no args)

3) Validation helper
- `_validate_int(value, default, minimum, maximum)` – enforces type and bounds
- Raises `ValueError` on invalid input so clients get a clear error

4) Tool dispatcher
- `@app.call_tool()` – handles tool invocations
- `if name == "roll_dice"` – validates args, generates `rolls` random ints 1..sides
- `if name == "get_timestamp"` – returns ISO 8601 UTC timestamp
- Returns a list with one `TextContent` payload containing human‑readable output

5) Server runtime
- `async def main()` – opens stdio streams and calls `app.run(...)`
- `if __name__ == "__main__": asyncio.run(main())` – standard async entrypoint

Key idea: one place describes tools (`list_tools`), one place handles calls (`call_tool`).

### Troubleshooting
- If the server doesn’t start, check container logs: `docker logs simple-mcp`
- If Cursor can’t connect, verify port mapping and the URL in the MCP config
- Rebuild after code changes: `docker build -t simple-mcp-server:latest .`

### Next: Phase 3
Proceed to `phase-3-practical-custom-server.md` to build a practical server with data persistence.

### What You Just Built
- A working MCP stdio server with two tools: `roll_dice` and `get_timestamp`
- Clear JSON Schemas, input validation, and typed Python functions
- A minimal Docker image that packages and runs your server

Key concepts learned:
- Separating tool discovery (`list_tools`) from invocation handling (`call_tool`)
- Designing simple, robust tool schemas and validating inputs
- Containerizing a Python MCP server for repeatable runs


