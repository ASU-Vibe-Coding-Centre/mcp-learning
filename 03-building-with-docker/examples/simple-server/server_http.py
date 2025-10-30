"""
Simple MCP Server: "Lucky Dice & Timekeeper" (HTTP Version)

Tools:
- roll_dice(sides: int = 6, rolls: int = 1) -> list[int]
- get_timestamp() -> str (ISO 8601)

This server uses the MCP Python SDK with Streamable HTTP transport via FastAPI.
Compare with server.py to see the difference between stdio and HTTP transports.

FastAPI provides a cleaner, simpler implementation compared to manual ASGI code.
"""

import asyncio
import datetime as dt
import os
import random
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool, TextContent
import uvicorn


# Create the MCP server instance. This name is shown to clients.
app = Server("lucky-dice-timekeeper")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Describe available tools with JSON Schemas.

    Returns:
        A list of Tool definitions discoverable by MCP clients.
    """
    # Advertise two tools: dice rolling and current timestamp.
    return [
        Tool(
            name="roll_dice",
            description=(
                "Roll one or more dice and return the results. "
                "Parameters: sides (int, default 6), rolls (int, default 1)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sides": {
                        "type": "integer",
                        "minimum": 2,
                        "default": 6,
                        "description": "Number of sides on the die",
                    },
                    "rolls": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 1,
                        "description": "How many dice to roll",
                    },
                },
            },
        ),
        Tool(
            name="get_timestamp",
            description="Return the current timestamp in ISO 8601 format (UTC).",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


def _validate_int(value: Any, default: int, minimum: int | None = None, maximum: int | None = None) -> int:
    """Validate and coerce an integer value with optional bounds.

    Args:
        value: Provided value (may be None).
        default: Value to use when input is None.
        minimum: Optional lower bound (inclusive).
        maximum: Optional upper bound (inclusive).

    Returns:
        A validated integer within the specified bounds.

    Raises:
        ValueError: If the value is not an int or violates bounds.
    """
    if value is None:
        return default
    if not isinstance(value, int):
        raise ValueError("Value must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"Value must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"Value must be <= {maximum}")
    return value


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations for roll_dice and get_timestamp.

    Args:
        name: Tool name provided by the client.
        arguments: JSON-serializable dict of tool arguments.

    Returns:
        A list with one TextContent message containing the result.

    Raises:
        ValueError: If an unknown tool name is requested.
    """
    # Dispatch to the correct tool by name.
    if name == "roll_dice":
        # Read and validate parameters with sensible defaults.
        sides = _validate_int(arguments.get("sides"), default=6, minimum=2)
        rolls = _validate_int(arguments.get("rolls"), default=1, minimum=1, maximum=100)

        # Generate the requested number of random rolls.
        results = [random.randint(1, sides) for _ in range(rolls)]
        return [
            TextContent(
                type="text",
                text=f"Rolled {rolls} d{sides}: {results}",
            )
        ]

    if name == "get_timestamp":
        # Produce an ISO 8601 UTC timestamp.
        now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        return [TextContent(type="text", text=now.isoformat())]

    raise ValueError(f"Unknown tool: {name}")


# Create the Streamable HTTP session manager
session_manager = StreamableHTTPSessionManager(app)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manage MCP session manager lifecycle with FastAPI.
    
    This lifespan context manager handles startup and shutdown of the MCP session manager.
    FastAPI calls this automatically when the application starts and stops.
    
    Startup: Starts the session manager background tasks
    Shutdown: Automatically cleans up when the app stops
    """
    # Startup: start the session manager
    async with session_manager.run():
        yield  # App runs here
    # Shutdown: cleanup happens automatically


# Create FastAPI app with lifespan events
# FastAPI handles HTTP routing, error handling, and lifespan management automatically
fastapi_app = FastAPI(lifespan=lifespan)


# Create ASGI app wrapper for MCP session manager
# This wrapper allows us to mount the MCP session manager at /mcp
class MCPASGIApp:
    """ASGI application wrapper for the MCP session manager.
    
    This class wraps the session manager's handle_request method as an ASGI application
    so it can be mounted in FastAPI. It delegates all HTTP requests to the session manager.
    """
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    async def __call__(self, scope, receive, send):
        """Handle ASGI requests by delegating to the session manager."""
        if scope["type"] == "http":
            await self.session_manager.handle_request(scope, receive, send)


# Mount the MCP ASGI app at /mcp
# FastAPI can mount other ASGI applications as sub-applications
# This routes all requests to /mcp/* to the MCP session manager
fastapi_app.mount("/mcp", MCPASGIApp(session_manager))


async def main() -> None:
    """Run the MCP server using FastAPI and uvicorn.
    
    This server uses FastAPI with Streamable HTTP transport, which provides a simpler,
    more efficient bidirectional communication over HTTP compared to the legacy SSE transport.
    
    Advantages of FastAPI over manual ASGI:
    - Cleaner code (~30 lines vs ~60 lines)
    - Built-in lifespan management
    - Automatic routing and error handling
    - Easy to extend with additional routes or middleware
    """
    port = int(os.getenv("PORT", "3333"))
    host = os.getenv("HOST", "0.0.0.0")
    
    # FastAPI is already an ASGI app, so we can use it directly with uvicorn
    config = uvicorn.Config(
        app=fastapi_app,
        host=host,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

