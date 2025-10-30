# Tutorial 1 Solution: First MCP Server

This is the complete solution for Tutorial 1. If you followed the tutorial step-by-step, your code should look very similar to this.

## Complete Code

```python
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
```

## Key Points

1. **Imports**: All necessary MCP components are imported
2. **Server Instance**: Created with a descriptive name
3. **Tool Registration**: `list_tools()` returns a list with one Tool
4. **Tool Handler**: `call_tool()` processes the "greet" tool
5. **Server Lifecycle**: `main()` runs the server with stdio transport

## Variations

### With Input Validation

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations with validation."""
    if name == "greet":
        person_name = arguments["name"]
        
        # Validate the input
        if not person_name or not person_name.strip():
            return [
                TextContent(
                    type="text",
                    text="Error: Name cannot be empty"
                )
            ]
        
        greeting = f"Hello, {person_name}! Welcome to MCP!"
        return [TextContent(type="text", text=greeting)]
    
    raise ValueError(f"Unknown tool: {name}")
```

### With Time-Based Greeting

```python
from datetime import datetime

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations with time-based greeting."""
    if name == "greet":
        person_name = arguments["name"]
        hour = datetime.now().hour
        
        # Choose greeting based on time
        if hour < 12:
            time_greeting = "Good morning"
        elif hour < 18:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        greeting = f"{time_greeting}, {person_name}! Welcome to MCP!"
        return [TextContent(type="text", text=greeting)]
    
    raise ValueError(f"Unknown tool: {name}")
```

## Common Mistakes and Fixes

### Mistake 1: Forgetting the decorator

```python
# WRONG - Missing decorator
async def list_tools() -> list[Tool]:
    return [Tool(...)]

# RIGHT
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(...)]
```

### Mistake 2: Not returning a list

```python
# WRONG - Returns single TextContent
return TextContent(type="text", text=greeting)

# RIGHT - Returns list of TextContent
return [TextContent(type="text", text=greeting)]
```

### Mistake 3: Wrong async/await usage

```python
# WRONG - Missing async
def call_tool(name: str, arguments: dict):
    ...

# RIGHT - Must be async
async def call_tool(name: str, arguments: dict):
    ...
```

## Testing Checklist

- [ ] Server starts without errors
- [ ] Tool appears in MCP Inspector
- [ ] Greeting works with normal name
- [ ] Handles empty string (if validation added)
- [ ] Handles special characters in names
- [ ] Error message appears for unknown tool

## Next Steps

After completing Tutorial 1:

1. Experiment with the greeting message
2. Add more parameters (like title, language)
3. Move on to Tutorial 2 (multiple tools)
4. Try Challenge 1 (custom tool design)

Congratulations on building your first MCP server!

