# Tutorial 2: Building a Multi-Tool Server

Now that you've built your first MCP server, let's level up by creating a server with multiple tools. You'll build a simple calculator server with four operations: addition, subtraction, multiplication, and division.

## Learning Objectives

By completing this tutorial, you will:

1. Register multiple tools in a single server
2. Route tool calls to different handlers
3. Share common parameter schemas across tools
4. Implement proper error handling and validation
5. Understand when to group tools in one server vs. separate servers

## Time Estimate

45-60 minutes

## Prerequisites

- Completed Tutorial 1 (First MCP Server)
- Understanding of basic Python functions
- MCP SDK and Inspector installed and working

## What You'll Build

A calculator server with four tools:

- **add**: Add two numbers
- **subtract**: Subtract one number from another
- **multiply**: Multiply two numbers
- **divide**: Divide one number by another (with zero-division handling)

## Why Multiple Tools in One Server?

You might wonder: why put multiple tools in one server instead of creating separate servers?

**Use one server when tools are:**

- Closely related (like calculator operations)
- Share common state or configuration
- Logically grouped from a user perspective
- Part of the same domain or API

**Use separate servers when tools:**

- Are completely unrelated
- Have different security requirements
- Need different update schedules
- Come from different teams or systems

For our calculator, all operations are mathematically related, so one server makes sense.

## Step 1: Create the Project Structure

Create a new file for your calculator server:

```bash
cd mcp_exercises  # Or wherever you're working
touch calculator.py
```

## Step 2: Set Up the Basics

Start with imports and server initialization:

```python
#!/usr/bin/env python3
"""Simple Calculator MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create the server
app = Server("simple-calculator")
```

Nothing new here - same as Tutorial 1!

## Step 3: Register Multiple Tools

Now comes the interesting part. You'll register all four calculator tools at once:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Return all calculator tools.
    """
    # Define common schema for all tools (they all take two numbers)
    number_schema = {
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
    
    # Return all four tools
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema=number_schema
        ),
        Tool(
            name="subtract",
            description="Subtract the second number from the first",
            inputSchema=number_schema
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together",
            inputSchema=number_schema
        ),
        Tool(
            name="divide",
            description="Divide the first number by the second",
            inputSchema=number_schema
        )
    ]
```

**Key observations:**

- We define `number_schema` once and reuse it for all tools
- All four tools are returned in a single list
- Each tool has a unique name but the same parameters
- Clear descriptions help LLMs choose the right tool

## Step 4: Implement the Tool Handler with Routing

Now you need to handle calls to any of these four tools. You'll use if/elif to route to the correct operation:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle calculator tool calls.
    """
    # Extract parameters (same for all tools)
    a = arguments.get("a")
    b = arguments.get("b")
    
    # Basic validation
    if a is None or b is None:
        return [
            TextContent(
                type="text",
                text="Error: Both 'a' and 'b' parameters are required"
            )
        ]
    
    # Route to the correct operation
    if name == "add":
        result = a + b
        return [
            TextContent(
                type="text",
                text=f"{a} + {b} = {result}"
            )
        ]
    
    elif name == "subtract":
        result = a - b
        return [
            TextContent(
                type="text",
                text=f"{a} - {b} = {result}"
            )
        ]
    
    elif name == "multiply":
        result = a * b
        return [
            TextContent(
                type="text",
                text=f"{a} × {b} = {result}"
            )
        ]
    
    elif name == "divide":
        # Special handling for division by zero
        if b == 0:
            return [
                TextContent(
                    type="text",
                    text="Error: Cannot divide by zero"
                )
            ]
        result = a / b
        return [
            TextContent(
                type="text",
                text=f"{a} ÷ {b} = {result}"
            )
        ]
    
    else:
        # Unknown tool
        return [
            TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )
        ]
```

**Understanding the routing pattern:**

1. Extract parameters first (common to all tools)
2. Validate that required parameters exist
3. Use if/elif to check which tool was called
4. Perform the operation and return the result
5. Handle errors specific to each operation
6. Catch unknown tool names in the final else

## Step 5: Add the Server Lifecycle

Complete the server with the main function:

```python
async def main():
    """Run the calculator server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 6: Test Your Calculator

Launch the Inspector:

```bash
npx @modelcontextprotocol/inspector python calculator.py
```

### Test Each Tool

Try these operations in the Inspector:

**Test 1: Addition**

- Tool: `add`
- Arguments: `{"a": 5, "b": 3}`
- Expected: `5 + 3 = 8`

**Test 2: Subtraction**

- Tool: `subtract`
- Arguments: `{"a": 10, "b": 4}`
- Expected: `10 - 4 = 6`

**Test 3: Multiplication**

- Tool: `multiply`
- Arguments: `{"a": 6, "b": 7}`
- Expected: `6 × 7 = 42`

**Test 4: Division**

- Tool: `divide`
- Arguments: `{"a": 20, "b": 4}`
- Expected: `20 ÷ 4 = 5.0`

**Test 5: Division by Zero**

- Tool: `divide`
- Arguments: `{"a": 10, "b": 0}`
- Expected: `Error: Cannot divide by zero`

**Test 6: Missing Parameter**

- Tool: `add`
- Arguments: `{"a": 5}` (missing b)
- Expected: Error message about missing parameter

## Step 7: Improve with Helper Functions

Your code works, but there's duplication. Let's refactor with helper functions:

```python
def create_response(message: str) -> list[TextContent]:
    """Helper to create a text response."""
    return [TextContent(type="text", text=message)]


def create_error(message: str) -> list[TextContent]:
    """Helper to create an error response."""
    return [TextContent(type="text", text=f"Error: {message}")]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls."""
    # Extract and validate parameters
    a = arguments.get("a")
    b = arguments.get("b")
    
    if a is None or b is None:
        return create_error("Both 'a' and 'b' parameters are required")
    
    # Route to operations
    if name == "add":
        result = a + b
        return create_response(f"{a} + {b} = {result}")
    
    elif name == "subtract":
        result = a - b
        return create_response(f"{a} - {b} = {result}")
    
    elif name == "multiply":
        result = a * b
        return create_response(f"{a} × {b} = {result}")
    
    elif name == "divide":
        if b == 0:
            return create_error("Cannot divide by zero")
        result = a / b
        return create_response(f"{a} ÷ {b} = {result}")
    
    else:
        return create_error(f"Unknown tool '{name}'")
```

**Benefits of helper functions:**

- Less repetitive code
- Consistent response format
- Easier to maintain
- Can be reused in other servers

## Step 8: Add Type Validation

What if someone passes a string instead of a number? Add validation:

```python
def validate_number(value, param_name: str) -> float:
    """
    Validate that a value is a number.
    
    Args:
        value: The value to validate
        param_name: Parameter name (for error messages)
        
    Returns:
        The value as a float
        
    Raises:
        ValueError: If value is not a number
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"'{param_name}' must be a number, got: {value}")
    
    raise ValueError(f"'{param_name}' must be a number")


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls."""
    # Extract parameters
    a = arguments.get("a")
    b = arguments.get("b")
    
    if a is None or b is None:
        return create_error("Both 'a' and 'b' parameters are required")
    
    # Validate types
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
    except ValueError as e:
        return create_error(str(e))
    
    # Rest of the handler remains the same...
```

Test this by trying to pass invalid values through the Inspector.

## Complete Final Code

Here's the complete, production-ready version:

```python
#!/usr/bin/env python3
"""Simple Calculator MCP Server"""

import asyncio
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("simple-calculator")


def validate_number(value: Any, param_name: str) -> float:
    """Validate and convert a value to a number."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"'{param_name}' must be a number, got: {value}")
    raise ValueError(f"'{param_name}' must be a number")


def create_response(message: str) -> list[TextContent]:
    """Create a text response."""
    return [TextContent(type="text", text=message)]


def create_error(message: str) -> list[TextContent]:
    """Create an error response."""
    return [TextContent(type="text", text=f"Error: {message}")]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return all calculator tools."""
    number_schema = {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }
    
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema=number_schema
        ),
        Tool(
            name="subtract",
            description="Subtract the second number from the first",
            inputSchema=number_schema
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together",
            inputSchema=number_schema
        ),
        Tool(
            name="divide",
            description="Divide the first number by the second",
            inputSchema=number_schema
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls."""
    # Extract and validate parameters
    a = arguments.get("a")
    b = arguments.get("b")
    
    if a is None or b is None:
        return create_error("Both 'a' and 'b' parameters are required")
    
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
    except ValueError as e:
        return create_error(str(e))
    
    # Route to operations
    if name == "add":
        result = a + b
        return create_response(f"{a} + {b} = {result}")
    
    elif name == "subtract":
        result = a - b
        return create_response(f"{a} - {b} = {result}")
    
    elif name == "multiply":
        result = a * b
        return create_response(f"{a} × {b} = {result}")
    
    elif name == "divide":
        if b == 0:
            return create_error("Cannot divide by zero")
        result = a / b
        return create_response(f"{a} ÷ {b} = {result}")
    
    else:
        return create_error(f"Unknown tool '{name}'")


async def main():
    """Run the calculator server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Extension Challenges

Want to practice more? Try adding these features:

### Challenge 1: Add More Operations

Add these tools:

- `power`: Raise a to the power of b
- `modulo`: Get remainder of a divided by b
- `square_root`: Calculate square root of a (only needs one parameter!)

### Challenge 2: Add Operation History

Keep track of the last 5 operations performed and add a tool to retrieve them.

Hint: Use a module-level list:

```python
history = []

# In your handler:
history.append(f"{a} + {b} = {result}")
if len(history) > 5:
    history.pop(0)  # Remove oldest
```

### Challenge 3: Support Multiple Operations

Add a tool `calculate` that accepts an expression string like "5 + 3 * 2" and evaluates it.

Warning: Be careful with `eval()`! You'll need to sanitize input.

### Challenge 4: Add Decimal Precision

Add an optional `decimals` parameter to control result precision:

```python
"decimals": {
    "type": "integer",
    "description": "Number of decimal places (default: 2)",
    "minimum": 0,
    "maximum": 10
}
```

Update the schema to have `"required": ["a", "b"]` only (decimals is optional).

## Common Issues

### Issue: Tools don't appear in Inspector

Check that:

- All tools are in the list returned by `list_tools()`
- No syntax errors in the tool definitions
- Schema is valid JSON Schema format

### Issue: Wrong tool gets called

Check that:

- Tool names are unique
- Tool name in handler matches tool name in definition
- if/elif conditions are correct

### Issue: Type errors with numbers

Check that:

- You're using `"type": "number"` not `"type": "integer"`
- You're validating types before using them
- You're handling both int and float types

## Checkpoint Questions

1. **Why did we define `number_schema` as a variable instead of repeating it for each tool?**
   <details>
   <summary>Answer</summary>
   
   To avoid duplication and make the schema easier to maintain. If we need to change the schema (e.g., add a parameter), we only change it in one place.
   </details>

2. **What's the purpose of the final `else` clause in the handler?**
   <details>
   <summary>Answer</summary>
   
   It catches any tool names that weren't matched by the if/elif conditions. This should never happen in normal operation, but provides a safety net if there's a bug or unexpected input.
   </details>

3. **Why do we validate types even though the schema says they're numbers?**
   <details>
   <summary>Answer</summary>
   
   The schema is a contract, but JSON-RPC might send numbers as strings. Validation ensures robustness and provides clear error messages if something goes wrong.
   </details>

4. **When would you split this into multiple servers instead of one?**
   <details>
   <summary>Answer</summary>
   
   If operations had different security requirements, needed different update schedules, or were maintained by different teams. For basic math operations, one server makes sense.
   </details>

## What You've Learned

- How to register multiple related tools in one server
- Routing patterns using if/elif statements
- Sharing common schemas across tools
- Helper functions for cleaner code
- Input validation for robustness
- Error handling for edge cases (division by zero)

## Next Steps

- **Challenge 1**: Design and implement your own custom tool
- **Challenge 2**: Build text manipulation tools
- **Challenge 3**: Build data processing tools
- Explore `../examples/calculator_server.py` for an even more robust implementation

## Ask the AI

Questions you might have:

- "How do I handle optional parameters?"
- "Can tools have different numbers of parameters?"
- "Should I use a class instead of if/elif for routing?"
- "How do I test my handlers without running the full server?"
- "What's the best way to organize code for many tools?"

Keep building and experimenting!

