# Module 03: Basic MCP Server Implementation

Welcome to the practical heart of this learning journey. In this module, you'll build your first Model Context Protocol (MCP) servers from scratch, transforming conceptual knowledge into working code.

## Module Overview

This module focuses on implementing basic MCP servers using the Python SDK. You'll learn the fundamental patterns for creating servers, registering tools, handling requests, and returning responses. By the end of this module, you'll have built multiple working servers and understand the core mechanics of the MCP server lifecycle.

## Learning Objectives

By completing this module, you will be able to:

1. **Understand MCP Server Architecture**
   - Explain the lifecycle of an MCP server (initialization, registration, request handling, shutdown)
   - Identify the key components: server instance, transport layer, tool handlers
   - Understand how servers communicate with clients through the stdio transport

2. **Implement Basic MCP Servers**
   - Create a minimal working MCP server with proper initialization
   - Register tools with appropriate schemas and metadata
   - Implement tool handlers with correct function signatures
   - Configure server capabilities and metadata

3. **Define and Register Tools**
   - Write tool functions with proper parameter definitions
   - Use type hints and schemas for parameter validation
   - Return properly formatted tool responses
   - Handle multiple tools within a single server

4. **Handle Errors Gracefully**
   - Implement basic input validation
   - Return appropriate error messages to clients
   - Handle common failure scenarios (invalid inputs, missing parameters)

5. **Test MCP Servers**
   - Run servers in development mode
   - Use the MCP Inspector to test tool invocations
   - Write basic unit tests for tool functions

## What You'll Build

Throughout this module, you'll create several progressively complex MCP servers:

1. **Minimal Echo Server** - A single-tool server that echoes messages back (your "Hello World")
2. **Calculator Server** - A multi-tool server performing mathematical operations
3. **Text Processing Server** - Tools for string manipulation and text analysis
4. **Data Processing Server** - Tools for working with JSON and CSV data
5. **File Operations Server** - Basic file system operations (read, write, list)

Each server builds on concepts from the previous ones, gradually introducing new patterns and best practices.

## Prerequisites

Before starting this module, ensure you have:

- Completed Module 01 (Introduction to MCP)
- Completed Module 02 (Environment Setup)
- Python 3.9+ installed and configured
- MCP Python SDK installed (`mcp` package)
- A code editor (VSCode, Cursor, or similar)
- Basic familiarity with Python functions, type hints, and async/await

## Module Structure

### Core Concepts

#### 1. MCP Server Anatomy

An MCP server consists of several key components:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 1. Server Instance - The core object
app = Server("server-name")

# 2. Tool Registration - Defining what the server can do
@app.list_tools()
async def list_tools():
    return [Tool(...)]

# 3. Tool Handler - Implementing the functionality
@app.call_tool()
async def call_tool(name, arguments):
    # Your tool logic here
    return [TextContent(...)]

# 4. Server Lifecycle - Running the server
async def main():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )
```

**Key Components Explained:**

- **Server Instance**: The main `Server` object that coordinates all functionality
- **Transport Layer**: How the server communicates (stdio, SSE, HTTP) - we'll use stdio
- **Tool Registration**: The `list_tools()` handler that tells clients what tools are available
- **Tool Handlers**: The `call_tool()` handler that executes tool requests
- **Initialization Options**: Server capabilities and metadata

#### 2. Tool Definition

Tools are the primary way clients interact with MCP servers. Each tool needs:

**Required Elements:**
- **Name**: Unique identifier for the tool (e.g., "add", "echo", "search")
- **Description**: Clear explanation of what the tool does
- **Input Schema**: JSON Schema defining expected parameters
- **Handler Function**: The code that executes when the tool is called

**Example Tool Definition:**

```python
Tool(
    name="calculator_add",
    description="Add two numbers together",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            }
        },
        "required": ["a", "b"]
    }
)
```

#### 3. Tool Implementation

Tool handlers receive requests and return responses:

**Input**: Tool handlers receive:
- `name`: String identifying which tool to execute
- `arguments`: Dictionary containing the tool's parameters

**Output**: Tool handlers must return a list of content items:
- `TextContent`: For text responses
- `ImageContent`: For images (advanced)
- `EmbeddedResource`: For structured data (advanced)

**Basic Pattern:**

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculator_add":
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [TextContent(
            type="text",
            text=f"The sum of {a} and {b} is {result}"
        )]
    
    raise ValueError(f"Unknown tool: {name}")
```

#### 4. Server Configuration

Servers can declare their capabilities:

```python
Server(
    name="my-server",
    version="1.0.0"
)
```

The initialization options tell clients what features the server supports:
- **Tools**: Whether the server provides callable functions
- **Resources**: Whether the server exposes data (covered in Module 04)
- **Prompts**: Whether the server provides prompt templates (covered in Module 04)

#### 5. Running and Testing

**Development Mode:**
```bash
# Run your server directly
python my_server.py
```

The server will start and listen for JSON-RPC messages on stdin, sending responses to stdout.

**Testing with MCP Inspector:**
```bash
# Install MCP Inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
mcp-inspector python my_server.py
```

The Inspector provides a web interface to:
- List available tools
- Invoke tools with test parameters
- View request/response messages
- Debug communication issues

## Development Workflow

Follow this pattern when building MCP servers:

1. **Define**: Start by defining what tools your server will provide
2. **Implement**: Write the tool functions with proper error handling
3. **Register**: Connect your functions to the MCP server
4. **Test**: Use the Inspector to verify each tool works correctly
5. **Refine**: Add input validation, improve error messages, add documentation

## Common Patterns

### Pattern 1: Single-Tool Server

Perfect for simple, focused functionality:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("single-tool-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="Does one thing well",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {"type": "string"}
                },
                "required": ["input"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        result = process(arguments["input"])
        return [TextContent(type="text", text=result)]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Pattern 2: Multi-Tool Server

Group related functionality:

```python
@app.list_tools()
async def list_tools():
    return [
        Tool(name="add", ...),
        Tool(name="subtract", ...),
        Tool(name="multiply", ...),
        Tool(name="divide", ...)
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        return handle_add(arguments)
    elif name == "subtract":
        return handle_subtract(arguments)
    elif name == "multiply":
        return handle_multiply(arguments)
    elif name == "divide":
        return handle_divide(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")
```

### Pattern 3: Helper Functions

Keep tool handlers clean by extracting logic:

```python
def validate_number(value: float, name: str) -> float:
    """Validate a numeric input."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    return float(value)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "divide":
        a = validate_number(arguments["a"], "a")
        b = validate_number(arguments["b"], "b")
        
        if b == 0:
            return [TextContent(
                type="text",
                text="Error: Division by zero is not allowed"
            )]
        
        result = a / b
        return [TextContent(
            type="text",
            text=f"{a} / {b} = {result}"
        )]
```

## Best Practices

1. **Clear Tool Names**: Use descriptive, action-oriented names (e.g., `calculate_sum`, not `calc`)

2. **Comprehensive Descriptions**: Help LLMs understand when to use your tools
   - Good: "Calculate the sum of two numbers and return the result"
   - Bad: "Addition"

3. **Detailed Input Schemas**: Specify types, descriptions, and constraints
   ```python
   "amount": {
       "type": "number",
       "description": "The amount in dollars (must be positive)",
       "minimum": 0
   }
   ```

4. **Input Validation**: Always validate parameters before processing
   - Check types match expectations
   - Verify required fields are present
   - Validate value ranges and constraints

5. **Error Handling**: Return helpful error messages
   - Good: "Error: 'amount' must be a positive number, got -5"
   - Bad: "Invalid input"

6. **Type Hints**: Use Python type hints for better IDE support and documentation
   ```python
   async def call_tool(name: str, arguments: dict) -> list[TextContent]:
       ...
   ```

7. **Documentation**: Add docstrings to your functions
   ```python
   def calculate_sum(a: float, b: float) -> float:
       """
       Calculate the sum of two numbers.
       
       Args:
           a: First number
           b: Second number
           
       Returns:
           The sum of a and b
       """
       return a + b
   ```

## Troubleshooting Common Issues

### Issue: Server starts but tools don't appear

**Symptoms**: MCP Inspector connects but shows no tools

**Causes**:
- `list_tools()` handler not registered
- Handler returning wrong format
- Exception in list_tools() function

**Solution**: Check that:
```python
@app.list_tools()  # Decorator is present
async def list_tools():
    return [Tool(...)]  # Returns list of Tool objects
```

### Issue: Tool calls fail with "Unknown tool"

**Symptoms**: Error message saying tool doesn't exist

**Causes**:
- Mismatch between tool name in list_tools() and call_tool()
- Typo in tool name
- Case sensitivity issues

**Solution**: Ensure exact name match:
```python
# In list_tools()
Tool(name="my_tool", ...)

# In call_tool()
if name == "my_tool":  # Exact match, including case
    ...
```

### Issue: "Missing required property" errors

**Symptoms**: Tool calls fail saying parameter is missing

**Causes**:
- Required parameter not provided
- Parameter name mismatch
- Schema not correctly defined

**Solution**: Check schema matches handler:
```python
# Schema
"required": ["user_id"]

# Handler
def call_tool(name: str, arguments: dict):
    user_id = arguments["user_id"]  # Same name
```

### Issue: Type errors or unexpected values

**Symptoms**: Runtime errors with types (e.g., "can't multiply string by int")

**Causes**:
- No input validation
- Assuming parameter types
- JSON parsing issues (numbers as strings)

**Solution**: Always validate:
```python
if not isinstance(arguments.get("count"), int):
    return [TextContent(type="text", text="Error: 'count' must be an integer")]
```

## Examples in This Module

All example code is in the `examples/` directory:

- `minimal_server.py` - Simplest possible MCP server (start here)
- `calculator_server.py` - Multi-tool mathematical operations
- `file_server.py` - Basic file system operations
- `test_calculator_server.py` - Example tests using pytest

## Exercises

The `exercises/` directory contains hands-on practice:

### Tutorials (Step-by-Step Guidance)

1. **tutorial-1-hello-world.md** - Build your first MCP server
   - Estimated time: 30 minutes
   - Difficulty: Beginner
   - You'll create a minimal echo server from scratch

2. **tutorial-2-simple-tools.md** - Add multiple tools to a server
   - Estimated time: 45 minutes
   - Difficulty: Beginner
   - Build a calculator with add, subtract, multiply, divide

### Challenges (Test Your Skills)

3. **challenge-1-custom-tool.md** - Design your own tool
   - Estimated time: 45 minutes
   - Difficulty: Intermediate
   - Create a tool for a specific use case

4. **challenge-2-text-tools.md** - Build text manipulation tools
   - Estimated time: 60 minutes
   - Difficulty: Intermediate
   - Tools for uppercase, lowercase, word count, etc.

5. **challenge-3-data-tools.md** - Build data processing tools
   - Estimated time: 90 minutes
   - Difficulty: Intermediate-Advanced
   - Work with JSON and CSV data

All exercises include:
- Clear objectives and requirements
- Starter code templates (where helpful)
- Detailed solutions in `exercises/solutions/`
- AI assistance prompts to help when stuck

## Checkpoint

After completing this module, work through `checkpoint.md` to validate your understanding. The checkpoint includes:

- Concept review questions
- Hands-on coding task
- Self-assessment checklist

You should be able to build a working MCP server with multiple tools independently before moving to Module 04.

## Next Steps

After mastering basic servers, you'll move to:

**Module 04: Advanced Features**
- Streaming responses for long-running operations
- Resources for exposing data
- Prompt templates for common tasks
- Combining all features in sophisticated servers

## Getting Help

### Ask the AI Assistant

Throughout your exercises, you can ask the AI assistant questions like:

- "How do I add a required parameter to my tool schema?"
- "Why am I getting an 'Unknown tool' error?"
- "Can you explain how the call_tool handler works?"
- "How do I validate that a parameter is a positive number?"

The AI is configured to provide hints and guidance without giving away complete solutions.

### Review Examples

When stuck, refer to the example servers in `examples/`. They demonstrate:
- Complete, working implementations
- Best practices and patterns
- Common error handling approaches
- Comprehensive comments explaining each section

### Check the Cheat Sheet

See `resources/cheatsheets/mcp-cheatsheet.md` for quick reference on:
- Tool schema syntax
- Common type definitions
- Handler patterns
- Error handling templates

## Key Takeaways

By the end of this module, remember these core principles:

1. **MCP servers are simple**: Initialize → Register tools → Handle calls
2. **Tools need clear contracts**: Name, description, and schema are crucial
3. **Validation is essential**: Always check inputs before processing
4. **Errors should be helpful**: Guide users to fix issues
5. **Testing matters**: Use the Inspector to verify everything works

Start with `examples/minimal_server.py` to see these principles in action, then dive into the tutorials to build your own servers.

Happy coding!
