"""
Quick Decision Maker - MCP Server

This MCP server provides simple decision-making tools for demonstration purposes.
It showcases how MCP servers can extend AI assistants with custom functionality.

Tools:
- make_decision: Accepts a list of options and randomly selects one (core Quick Decision Maker functionality)
- random_number: Generates a random number within a specified range (useful for numeric decisions)

This server uses the MCP Python SDK with Streamable HTTP transport via FastAPI,
making it suitable for running inside a Docker container and connecting to Cursor IDE.
FastAPI provides a cleaner, simpler implementation compared to manual ASGI code.
Streamable HTTP provides a simpler, more efficient bidirectional communication over HTTP.
"""

import asyncio
import os
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool, TextContent
import uvicorn


# Create the MCP server instance
# This name identifies the server to MCP clients (like Cursor IDE)
# When Cursor connects, it will see "quick-decision-maker" in its MCP status
app = Server("quick-decision-maker")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Describe available tools with JSON Schemas.
    
    This function is called by MCP clients to discover what tools are available.
    Each Tool definition includes:
    - name: The identifier used to invoke the tool
    - description: Human-readable explanation of what the tool does
    - inputSchema: JSON Schema defining the tool's parameters
    
    The JSON Schema is important because AI assistants use it to understand:
    - What parameters are required vs optional
    - What data types are expected
    - How to format requests correctly
    
    Returns:
        A list of Tool definitions that MCP clients can discover and use.
    """
    return [
        Tool(
            name="make_decision",
            description=(
                "Make a random decision from a list of options. "
                "Provide a list of options (at least 2) and this tool will randomly select one. "
                "This is the core functionality of the Quick Decision Maker - perfect for choosing "
                "between multiple alternatives when you can't decide!"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "description": "List of options to choose from (minimum 2 required)",
                        "minItems": 2,
                    },
                },
                "required": ["options"],
            },
        ),
        Tool(
            name="random_number",
            description=(
                "Generate a random number within a specified range. "
                "Useful for numeric decisions like 'pick a number between 1 and 100', "
                "selecting random quantities, or choosing from numbered options."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "min": {
                        "type": "integer",
                        "description": "Minimum value (inclusive)",
                        "default": 1,
                    },
                    "max": {
                        "type": "integer",
                        "description": "Maximum value (inclusive)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations from MCP clients.
    
    This function is called when an AI assistant (like Cursor's AI) wants to use
    one of our tools. The assistant uses the tool schemas from list_tools() to
    understand how to call each tool correctly.
    
    The flow:
    1. User types a prompt in Cursor (e.g., "Flip a coin")
    2. Cursor's AI sees the make_decision tool is available
    3. Cursor calls this function with name="make_decision" and arguments={...}
    4. We execute the tool logic and return results
    5. Cursor's AI receives the results and can respond to the user
    
    Args:
        name: The tool name to invoke (must match a tool from list_tools())
        arguments: JSON-serializable dict containing tool parameters
        
    Returns:
        A list containing one TextContent message with the tool's result
        
    Raises:
        ValueError: If an unknown tool name is requested or if tool execution fails
    """
    if name == "make_decision":
        # Extract options list from arguments
        options = arguments.get("options")
        
        if not options:
            raise ValueError("Missing required parameter: options")
        
        if not isinstance(options, list):
            raise ValueError(f"Options must be a list, got {type(options).__name__}")
        
        if len(options) < 2:
            raise ValueError(f"At least 2 options are required, got {len(options)}")
        
        # Filter out empty strings and validate all items are strings
        valid_options = []
        for i, option in enumerate(options):
            if not isinstance(option, str):
                raise ValueError(f"All options must be strings, but option at index {i} is {type(option).__name__}")
            if option.strip():  # Skip empty strings
                valid_options.append(option.strip())
        
        if len(valid_options) < 2:
            raise ValueError("At least 2 non-empty options are required")
        
        # Randomly select one option
        selected = random.choice(valid_options)
        
        # Format the output nicely
        if len(valid_options) == 2:
            result_text = f"Decision: {selected}"
        else:
            # Show all options and the selected one
            options_list = ", ".join(f'"{opt}"' for opt in valid_options)
            result_text = f"Options: [{options_list}]\nDecision: {selected}"
        
        return [
            TextContent(
                type="text",
                text=result_text,
            )
        ]
    
    if name == "random_number":
        # Extract min and max from arguments (with defaults)
        min_val = arguments.get("min", 1)
        max_val = arguments.get("max", 100)
        
        # Validate types
        if not isinstance(min_val, int):
            raise ValueError(f"min must be an integer, got {type(min_val).__name__}")
        if not isinstance(max_val, int):
            raise ValueError(f"max must be an integer, got {type(max_val).__name__}")
        
        # Validate range
        if min_val > max_val:
            raise ValueError(f"min ({min_val}) cannot be greater than max ({max_val})")
        
        # Generate random number in range [min, max] (inclusive)
        result = random.randint(min_val, max_val)
        
        # Format the output
        if min_val == 1 and max_val == 100:
            # Default case - simple output
            result_text = f"Random number: {result}"
        else:
            # Custom range - show the range
            result_text = f"Random number between {min_val} and {max_val}: {result}"
        
        return [
            TextContent(
                type="text",
                text=result_text,
            )
        ]
    
    # If we reach here, an unknown tool was requested
    raise ValueError(f"Unknown tool: {name}")


# Create the Streamable HTTP session manager
# This is created at module level so it can be used in lifespan and request handling
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
    
    This is the entry point that starts the MCP server. It uses FastAPI with Streamable HTTP transport,
    which provides a simpler, more efficient bidirectional communication over HTTP.
    
    How it works:
    1. The server starts an HTTP server (uvicorn) on a specified port (default: 3333)
    2. Cursor IDE connects via HTTP URL (e.g., http://localhost:3333/mcp)
    3. Streamable HTTP uses a single bidirectional endpoint for both requests and responses
    4. The Server instance (app) handles routing incoming requests to our handlers
    5. The server runs until it receives a shutdown signal
    
    When running in Docker:
    - Docker exposes a port (e.g., 3333) and maps it to the host
    - Cursor IDE connects to http://localhost:3333/mcp
    - This creates a communication bridge: Cursor <-> Streamable HTTP <-> Docker Container <-> MCP Server
    
    Advantages of FastAPI over manual ASGI:
    - Cleaner code (~30 lines vs ~60 lines)
    - Built-in lifespan management
    - Automatic routing and error handling
    - Easy to extend with additional routes or middleware
    
    The server will continue running until:
    - The process receives SIGTERM/SIGINT
    - The container is stopped
    - An error occurs that causes the server to crash
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
    # Run the async main function using asyncio
    # This starts the HTTP server and keeps it running
    asyncio.run(main())
