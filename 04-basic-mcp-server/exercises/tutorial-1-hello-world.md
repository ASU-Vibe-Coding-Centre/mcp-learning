# Tutorial 1: Building Your First MCP Server

Welcome to your first hands-on MCP development experience! In this tutorial, you'll build a working MCP server from scratch, step by step. By the end, you'll have a functioning echo server that you can test with the MCP Inspector.

## Learning Objectives

By completing this tutorial, you will:

1. Understand the basic structure of an MCP server
2. Learn how to register tools
3. Implement a tool handler
4. Run and test your server with the MCP Inspector
5. Gain confidence to build more complex servers

## Time Estimate

30-45 minutes

## Prerequisites

Before starting, ensure you have:

- Python 3.9+ installed
- MCP Python SDK installed (`pip install mcp`)
- A code editor (VSCode, Cursor, PyCharm, etc.)
- MCP Inspector installed (`npm install -g @modelcontextprotocol/inspector`)

Verify your setup:

```bash
python --version  # Should be 3.9 or higher
python -c "import mcp; print('MCP SDK installed')"
npx @modelcontextprotocol/inspector --version
```

## What You'll Build

You'll create an MCP server with a single "greet" tool that:

- Accepts a name as input
- Returns a personalized greeting message
- Demonstrates the complete request-response cycle

This is your "Hello World" for MCP servers!

## Step 1: Create the Project File

Create a new file called `my_first_server.py` in your working directory.

```bash
# Create a directory for your work
mkdir -p mcp_exercises
cd mcp_exercises

# Create the server file
touch my_first_server.py
```

Open `my_first_server.py` in your editor. You'll add code to this file throughout the tutorial.

## Step 2: Import Required Modules

Add the necessary imports at the top of your file:

```python
#!/usr/bin/env python3
"""My First MCP Server - A greeting server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
```

**What each import does:**

- `asyncio`: Python's async/await support (MCP uses async operations)
- `Server`: The core MCP server class
- `stdio_server`: Communication layer using standard input/output
- `Tool`: Type for defining tool metadata
- `TextContent`: Type for text responses

## Step 3: Create the Server Instance

Add this line to create your server:

```python
# Create the server with a unique name
app = Server("my-greeting-server")
```

**Key points:**

- The server name should be lowercase with hyphens
- This name identifies your server to clients
- Choose a descriptive name that reflects what the server does

## Step 4: Register Your Tool

Add the tool registration handler:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Tell clients what tools this server provides.
    """
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
```

**Understanding the tool definition:**

- **name**: Unique identifier (`"greet"`)
- **description**: Helps LLMs understand when to use this tool
- **inputSchema**: JSON Schema defining the tool's parameters
  - `type: "object"`: All tool inputs are objects
  - `properties`: Defines each parameter
  - `required`: Lists mandatory parameters

## Step 5: Implement the Tool Handler

Add the handler that processes tool calls:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool invocations.
    """
    # Check which tool is being called
    if name == "greet":
        # Extract the 'name' parameter
        person_name = arguments["name"]
        
        # Create the greeting
        greeting = f"Hello, {person_name}! Welcome to MCP!"
        
        # Return the response
        return [
            TextContent(
                type="text",
                text=greeting
            )
        ]
    
    # Handle unknown tools
    raise ValueError(f"Unknown tool: {name}")
```

**Understanding the handler:**

- Receives `name` (which tool) and `arguments` (parameters)
- Extracts parameters from the `arguments` dictionary
- Creates and returns a list of `TextContent` objects
- Raises an error for unknown tools

## Step 6: Set Up the Server Lifecycle

Add the main function to run your server:

```python
async def main():
    """
    Run the MCP server using stdio transport.
    """
    # Set up stdio communication
    async with stdio_server() as (read_stream, write_stream):
        # Run the server
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# Python entry point
if __name__ == "__main__":
    asyncio.run(main())
```

**What this does:**

- `stdio_server()`: Creates communication streams
- `app.run()`: Starts the server and handles requests
- `asyncio.run()`: Executes the async main function

## Step 7: Complete Code Review

Your complete `my_first_server.py` should look like this:

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

Take a moment to review the code and understand how the pieces fit together.

## Step 8: Test Your Server

Now let's test your server with the MCP Inspector!

### Launch the Inspector

Run this command in your terminal:

```bash
npx @modelcontextprotocol/inspector python my_first_server.py
```

You should see output like:

```
MCP Inspector running at http://localhost:5173
```

### Open the Inspector Interface

1. Open your web browser
2. Navigate to `http://localhost:5173`
3. You should see the MCP Inspector interface

### Explore Available Tools

In the Inspector:

1. Look for the "Tools" section
2. You should see your "greet" tool listed
3. Click on it to see its description and parameters

### Test the Tool

1. Find the "greet" tool in the interface
2. Click "Test" or "Execute"
3. Enter a name (e.g., "Alice") in the parameter field
4. Click "Submit" or "Call"
5. You should see the response: `Hello, Alice! Welcome to MCP!`

### Try Different Inputs

Test your tool with various names:

- Your own name
- "World"
- "MCP Learner"
- An empty string (what happens?)

## Step 9: Understanding What Happened

When you tested your tool, here's what occurred:

1. **Inspector connected** to your server via stdio
2. **Server initialized** and declared its capabilities
3. **Inspector listed tools** by calling your `list_tools()` handler
4. **User invoked tool** through the Inspector interface
5. **Inspector sent request** to your server as JSON-RPC message
6. **Server processed** the request in your `call_tool()` handler
7. **Server returned response** as TextContent
8. **Inspector displayed** the result

This is the complete MCP request-response cycle!

## Step 10: Experiment and Extend

Now that you have a working server, try these experiments:

### Experiment 1: Change the Greeting

Modify the greeting message:

```python
greeting = f"Greetings, {person_name}! You're now an MCP developer!"
```

Restart the Inspector and test the change.

### Experiment 2: Add Personality

Make the greeting more elaborate:

```python
greeting = f"""
Hello, {person_name}!

Welcome to the world of Model Context Protocol!
You've successfully created and tested your first MCP server.

Keep up the great work!
"""
```

### Experiment 3: Add Input Validation

What if someone provides an empty name? Add validation:

```python
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
```

Test this by providing an empty string or just spaces.

### Experiment 4: Add Time-Based Greeting

Make the greeting time-aware:

```python
from datetime import datetime

# In your call_tool handler:
if name == "greet":
    person_name = arguments["name"]
    
    # Get current hour
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
```

Don't forget to add the import at the top of your file!

## Common Issues and Solutions

### Issue: "Module 'mcp' not found"

**Solution**: Install the MCP SDK:

```bash
pip install mcp
```

### Issue: "npx command not found"

**Solution**: Install Node.js and npm:

- Download from [nodejs.org](https://nodejs.org)
- Or use a package manager (brew, apt, etc.)

### Issue: Inspector shows no tools

**Solution**: Check that:

1. `list_tools()` has the `@app.list_tools()` decorator
2. It returns a list of Tool objects
3. Your server is running without errors

### Issue: Tool calls fail

**Solution**: Check that:

1. Tool name in `call_tool()` matches the name in `list_tools()`
2. You're returning a list of TextContent
3. Parameter names match the schema

### Issue: Server crashes on start

**Solution**: Look for:

1. Syntax errors
2. Missing imports
3. Incorrect indentation
4. Check the error message in the terminal

## Checkpoint Questions

Before moving on, make sure you can answer these:

1. **What are the three main components of an MCP server?**
   <details>
   <summary>Click to reveal answer</summary>
   
   - Server instance creation
   - Tool registration (`list_tools()`)
   - Tool handler (`call_tool()`)
   </details>

2. **What does the `@app.list_tools()` decorator do?**
   <details>
   <summary>Click to reveal answer</summary>
   
   It registers a function that returns the list of tools available on this server. Clients call this to discover what the server can do.
   </details>

3. **Why do we return a *list* of TextContent instead of a single object?**
   <details>
   <summary>Click to reveal answer</summary>
   
   MCP supports multiple content types in a single response (text, images, embedded resources). Even if you're returning just text, it's wrapped in a list for consistency.
   </details>

4. **What happens if `call_tool()` receives a tool name that doesn't exist?**
   <details>
   <summary>Click to reveal answer</summary>
   
   The handler should raise a ValueError to indicate an unknown tool. This tells the client that the requested tool doesn't exist.
   </details>

## What You've Learned

By completing this tutorial, you've:

- Created a complete MCP server from scratch
- Registered and implemented a tool
- Tested your server with the MCP Inspector
- Understood the request-response cycle
- Made modifications and experiments

## Next Steps

Ready for more? Try these:

1. **Tutorial 2**: Add multiple tools to a server (calculator)
2. **Challenge 1**: Design your own custom tool
3. Review the example servers in `../examples/`:
   - `minimal_server.py` - Similar to what you built
   - `calculator_server.py` - Multiple tools with validation
   - `file_server.py` - Working with the file system

## Ask the AI Assistant

If you're stuck or curious, ask questions like:

- "How do I add a second tool to my server?"
- "Why do I need to use async/await?"
- "Can I return something other than text?"
- "How do I test my server without the Inspector?"
- "What's the difference between Tool and TextContent?"

The AI assistant is configured to provide helpful guidance while encouraging you to solve problems yourself.

## Congratulations!

You've built and tested your first MCP server! This is a significant milestone in your MCP journey. The patterns you've learned here form the foundation for all MCP server development.

Keep experimenting, stay curious, and enjoy building with MCP!

