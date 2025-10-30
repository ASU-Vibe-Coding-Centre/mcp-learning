#!/usr/bin/env python3
"""My First MCP Server - A greeting server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create the server
app = Server("my-greeting-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Tell clients what tools this server provides."""
    return [
        Tool(
            name="greet",
            description="Generate a personalized greeting for a given name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person to greet"
                    }
                },
                "required": ["name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations."""
    if name == "greet":
        person_name = arguments["name"]
        greeting = f"Hello, {person_name}! Welcome to MCP!"
        return [
            TextContent(
                type="text",
                text=greeting
            )
        ]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())

