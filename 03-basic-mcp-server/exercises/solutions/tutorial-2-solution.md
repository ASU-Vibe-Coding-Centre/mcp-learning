# Tutorial 2 Solution: Multi-Tool Calculator Server

This is the complete, production-ready solution for Tutorial 2. It includes all the improvements discussed in the tutorial.

## Complete Code

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

## Alternative Implementation: Class-Based Routing

For servers with many tools, you might prefer a class-based approach:

```python
class Calculator:
    """Calculator operations."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls."""
    # Validate parameters
    a = arguments.get("a")
    b = arguments.get("b")
    
    if a is None or b is None:
        return create_error("Both 'a' and 'b' parameters are required")
    
    try:
        a = validate_number(a, "a")
        b = validate_number(b, "b")
    except ValueError as e:
        return create_error(str(e))
    
    # Map tool names to methods
    operations = {
        "add": Calculator.add,
        "subtract": Calculator.subtract,
        "multiply": Calculator.multiply,
        "divide": Calculator.divide
    }
    
    if name not in operations:
        return create_error(f"Unknown tool '{name}'")
    
    try:
        result = operations[name](a, b)
        return create_response(f"Result: {result}")
    except ValueError as e:
        return create_error(str(e))
```

## Extension: Adding More Operations

### Power Operation

```python
# In list_tools(), add:
Tool(
    name="power",
    description="Raise first number to the power of the second",
    inputSchema=number_schema
)

# In call_tool(), add:
elif name == "power":
    result = a ** b
    return create_response(f"{a} ^ {b} = {result}")
```

### Modulo Operation

```python
# In list_tools(), add:
Tool(
    name="modulo",
    description="Get remainder of first number divided by second",
    inputSchema=number_schema
)

# In call_tool(), add:
elif name == "modulo":
    if b == 0:
        return create_error("Cannot calculate modulo with zero")
    result = a % b
    return create_response(f"{a} % {b} = {result}")
```

### Square Root (Single Parameter)

```python
# Different schema for single-parameter tool:
square_root_schema = {
    "type": "object",
    "properties": {
        "number": {
            "type": "number",
            "description": "Number to calculate square root of (must be non-negative)"
        }
    },
    "required": ["number"]
}

# In list_tools(), add:
Tool(
    name="square_root",
    description="Calculate the square root of a number",
    inputSchema=square_root_schema
)

# In call_tool(), add:
elif name == "square_root":
    number = arguments.get("number")
    if number is None:
        return create_error("'number' parameter is required")
    
    try:
        number = validate_number(number, "number")
    except ValueError as e:
        return create_error(str(e))
    
    if number < 0:
        return create_error("Cannot calculate square root of negative number")
    
    result = number ** 0.5
    return create_response(f"√{number} = {result}")
```

## Extension Challenge Solutions

### Challenge 1: Operation History

```python
# Module-level list to track history
operation_history = []

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls with history tracking."""
    global operation_history
    
    # ... existing validation code ...
    
    # After calculating result, add to history
    if name in ["add", "subtract", "multiply", "divide"]:
        # ... perform operation ...
        
        # Track in history
        operation_history.append(f"{a} {symbol} {b} = {result}")
        if len(operation_history) > 5:
            operation_history.pop(0)
        
        return create_response(f"{a} {symbol} {b} = {result}")

# Add history tool
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return all calculator tools including history."""
    # ... existing tools ...
    tools.append(
        Tool(
            name="history",
            description="Get the last 5 calculations performed",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    )
    return tools

# Handle history tool
# In call_tool():
elif name == "history":
    if not operation_history:
        return create_response("No operations performed yet")
    
    history_text = "Last operations:\n" + "\n".join(operation_history)
    return create_response(history_text)
```

### Challenge 4: Decimal Precision

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return calculator tools with optional decimals parameter."""
    number_schema_with_decimals = {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"},
            "decimals": {
                "type": "integer",
                "description": "Number of decimal places (default: 2)",
                "minimum": 0,
                "maximum": 10
            }
        },
        "required": ["a", "b"]  # decimals is optional
    }
    # ... use this schema for tools ...


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator tool calls with decimal precision."""
    # ... existing validation ...
    
    # Get optional decimals parameter
    decimals = arguments.get("decimals", 2)  # Default to 2
    
    # Validate decimals
    if not isinstance(decimals, int) or decimals < 0 or decimals > 10:
        return create_error("'decimals' must be an integer between 0 and 10")
    
    # After calculating result:
    result = round(result, decimals)
    return create_response(f"{a} + {b} = {result}")
```

## Testing Checklist

- [ ] All four operations work correctly
- [ ] Division by zero returns error
- [ ] Invalid types return helpful error
- [ ] Missing parameters return error
- [ ] Results are correctly formatted
- [ ] Helper functions reduce code duplication

## Key Takeaways

1. **Shared Schemas**: Define once, reuse for all tools with same parameters
2. **Helper Functions**: Extract common patterns (validation, responses)
3. **Type Validation**: Don't assume parameters are correct types
4. **Error Handling**: Return helpful, specific error messages
5. **Code Organization**: Group related functionality logically

## Next Steps

1. Try adding the extension operations (power, modulo, square_root)
2. Implement the history feature
3. Move on to Challenge 1 (custom tool design)
4. Explore the advanced `calculator_server.py` example

Excellent work building a multi-tool server!

