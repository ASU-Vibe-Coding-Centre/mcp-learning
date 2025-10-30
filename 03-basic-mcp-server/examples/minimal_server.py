#!/usr/bin/env python3
"""
Minimal MCP Server Example

This is the simplest possible MCP (Model Context Protocol) server implementation.
It demonstrates the core concepts with minimal code complexity.

What this server does:
- Provides a single "echo" tool that returns whatever message you send it
- Shows the basic structure every MCP server needs
- Demonstrates the request-response pattern

This is your "Hello World" for MCP servers - start here!
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ============================================================================
# STEP 1: Create the Server Instance
# ============================================================================
# The Server object is the core of your MCP server. You give it a name that
# identifies it to clients (like Claude Desktop or the MCP Inspector).
#
# This name should be:
# - Lowercase with hyphens (convention)
# - Descriptive of what the server does
# - Unique among the servers a client might connect to

app = Server("minimal-echo-server")


# ============================================================================
# STEP 2: Register Tool Listing Handler
# ============================================================================
# The @app.list_tools() decorator registers a function that tells clients
# what tools this server provides. This function is called when a client
# first connects or when it wants to refresh the tool list.
#
# This function must:
# - Be async (use 'async def')
# - Return a list of Tool objects
# - Each Tool must have: name, description, and inputSchema

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Return the list of tools this server provides.
    
    Called by the client to discover available functionality.
    """
    return [
        Tool(
            # Unique identifier for this tool
            # The client will use this name when calling the tool
            name="echo",
            
            # Human-readable description of what the tool does
            # LLMs use this to decide when to call the tool
            # Be clear and specific about the tool's purpose
            description="Echo back any message you send. This is a simple test tool that returns your input unchanged.",
            
            # JSON Schema defining the tool's parameters
            # This tells clients what data to send when calling the tool
            inputSchema={
                # All tool schemas start with type: "object"
                "type": "object",
                
                # Properties define the parameters the tool accepts
                "properties": {
                    "message": {
                        # This parameter accepts a string
                        "type": "string",
                        
                        # Description helps LLMs understand what to provide
                        "description": "The message to echo back"
                    }
                },
                
                # Required array lists which parameters must be provided
                # Parameters not in this list are optional
                "required": ["message"]
            }
        )
    ]


# ============================================================================
# STEP 3: Register Tool Call Handler
# ============================================================================
# The @app.call_tool() decorator registers a function that handles tool
# invocations. When a client calls a tool, this function is executed.
#
# This function must:
# - Be async (use 'async def')
# - Accept 'name' (str) and 'arguments' (dict) parameters
# - Return a list of content items (usually TextContent)

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool invocation requests.
    
    Args:
        name: The name of the tool being called (e.g., "echo")
        arguments: Dictionary of parameters provided by the client
        
    Returns:
        List of content items to send back to the client
        
    Raises:
        ValueError: If an unknown tool name is provided
    """
    
    # Check which tool is being called
    # In a server with multiple tools, you'd have multiple if/elif branches
    if name == "echo":
        # Extract the 'message' parameter from the arguments dictionary
        # We know this exists because it's required in the inputSchema
        message = arguments["message"]
        
        # Create a TextContent response
        # TextContent is the most common response type - it contains text
        return [
            TextContent(
                # Type must be "text" for TextContent
                type="text",
                
                # The actual text to return to the client
                # This is what the LLM will see as the tool's output
                text=f"Echo: {message}"
            )
        ]
    
    # If we get here, the client requested a tool that doesn't exist
    # Raise an error to let them know
    raise ValueError(f"Unknown tool: {name}")


# ============================================================================
# STEP 4: Main Entry Point - Server Lifecycle
# ============================================================================
# The main() function sets up the server's communication channel and runs it.
# This is where the server lifecycle happens:
# 1. Set up stdio transport (communication over stdin/stdout)
# 2. Initialize the server
# 3. Run the server (blocks until shutdown)

async def main():
    """
    Run the MCP server.
    
    This function:
    1. Creates stdio streams for communication
    2. Runs the server with those streams
    3. Handles the server lifecycle
    """
    
    # stdio_server() creates input/output streams for MCP communication
    # MCP servers typically use stdio (standard input/output) to communicate
    # This means:
    # - Clients send JSON-RPC messages to the server's stdin
    # - Server sends JSON-RPC responses to stdout
    # - stderr is used for logging (not shown in this minimal example)
    
    async with stdio_server() as (read_stream, write_stream):
        # Run the server with:
        # - read_stream: where we receive messages from the client
        # - write_stream: where we send messages to the client
        # - initialization_options: server capabilities and metadata
        
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# ============================================================================
# STEP 5: Python Entry Point
# ============================================================================
# This is standard Python boilerplate to run the async main() function
# when the script is executed directly (not imported as a module)

if __name__ == "__main__":
    # asyncio.run() is the standard way to run an async main function
    # It:
    # 1. Creates an event loop
    # 2. Runs main() until it completes
    # 3. Closes the event loop
    asyncio.run(main())


# ============================================================================
# HOW TO USE THIS SERVER
# ============================================================================
#
# Option 1: Run directly (server will wait for input)
#   python minimal_server.py
#
# Option 2: Test with MCP Inspector (recommended for development)
#   npx @modelcontextprotocol/inspector python minimal_server.py
#
# Option 3: Connect from Claude Desktop
#   Add this to Claude's config file:
#   {
#     "mcpServers": {
#       "echo": {
#         "command": "python",
#         "args": ["/absolute/path/to/minimal_server.py"]
#       }
#     }
#   }
#
# ============================================================================
# WHAT HAPPENS WHEN YOU RUN IT
# ============================================================================
#
# 1. Server starts and waits for a client connection
# 2. Client connects and sends an "initialize" request
# 3. Server responds with its capabilities
# 4. Client sends "tools/list" request
# 5. Server responds with the list of tools (just "echo")
# 6. Client can now call "echo" with a message
# 7. Server processes the call and returns the echo response
# 8. This continues until the client disconnects
#
# ============================================================================
# NEXT STEPS
# ============================================================================
#
# Once you understand this minimal example, try:
#
# 1. Modify the echo tool to transform the message (uppercase, reverse, etc.)
# 2. Add a second tool (e.g., "reverse" that reverses the message)
# 3. Add input validation (check message length, reject empty messages)
# 4. Look at calculator_server.py for a multi-tool example
#
# ============================================================================

