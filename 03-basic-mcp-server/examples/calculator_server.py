#!/usr/bin/env python3
"""
Calculator MCP Server

A multi-tool MCP server demonstrating:
- Multiple tool registration
- Input validation
- Error handling
- Type checking
- Helper functions

This server provides basic mathematical operations:
- add: Add two numbers
- subtract: Subtract one number from another
- multiply: Multiply two numbers
- divide: Divide one number by another (with zero-division protection)

Use this as a template for building servers with multiple related tools.
"""

import asyncio
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the server with a descriptive name
app = Server("calculator-server")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
# Helper functions keep your tool handlers clean and promote code reuse.
# These handle validation and error checking before performing operations.

def validate_number(value: Any, param_name: str) -> float:
    """
    Validate that a value is a number and convert it to float.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter (for error messages)
        
    Returns:
        The value as a float
        
    Raises:
        ValueError: If the value is not a valid number
    """
    # Check if the value is already a number type
    if isinstance(value, (int, float)):
        # Convert to float for consistent handling
        return float(value)
    
    # If it's a string, try to parse it as a number
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"Parameter '{param_name}' must be a number, got: '{value}'"
            )
    
    # Any other type is invalid
    raise ValueError(
        f"Parameter '{param_name}' must be a number, got type: {type(value).__name__}"
    )


def create_error_response(error_message: str) -> list[TextContent]:
    """
    Create a standardized error response.
    
    Args:
        error_message: The error message to return
        
    Returns:
        A list containing a TextContent error message
    """
    return [
        TextContent(
            type="text",
            text=f"Error: {error_message}"
        )
    ]


def create_success_response(result: str) -> list[TextContent]:
    """
    Create a standardized success response.
    
    Args:
        result: The result message to return
        
    Returns:
        A list containing a TextContent success message
    """
    return [
        TextContent(
            type="text",
            text=result
        )
    ]


# ============================================================================
# MATHEMATICAL OPERATION FUNCTIONS
# ============================================================================
# These functions implement the actual calculations.
# They're separated from the tool handlers for easier testing and reuse.

def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """
    Subtract b from a.
    
    Args:
        a: Number to subtract from
        b: Number to subtract
        
    Returns:
        The difference (a - b)
    """
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of a and b
    """
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """
    Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        The quotient (a / b)
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Return all available calculator tools.
    
    Each tool has the same parameter structure (two numbers),
    but different descriptions and operations.
    """
    
    # Common schema for all calculator operations
    # This can be reused since all tools take two numbers
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
    
    return [
        Tool(
            name="add",
            description="Add two numbers together and return the sum. Example: add(5, 3) returns 8.",
            inputSchema=number_schema
        ),
        Tool(
            name="subtract",
            description="Subtract the second number from the first and return the difference. Example: subtract(10, 3) returns 7.",
            inputSchema=number_schema
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together and return the product. Example: multiply(4, 5) returns 20.",
            inputSchema=number_schema
        ),
        Tool(
            name="divide",
            description="Divide the first number by the second and return the quotient. Returns an error if dividing by zero. Example: divide(10, 2) returns 5.",
            inputSchema=number_schema
        )
    ]


# ============================================================================
# TOOL CALL HANDLER
# ============================================================================

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle calculator tool invocations.
    
    This function:
    1. Validates the tool name
    2. Extracts and validates parameters
    3. Performs the calculation
    4. Returns formatted results or error messages
    
    Args:
        name: The tool being called
        arguments: Dictionary containing 'a' and 'b' parameters
        
    Returns:
        List containing the calculation result or error message
    """
    
    # Validate that required parameters exist
    if "a" not in arguments:
        return create_error_response("Missing required parameter 'a'")
    
    if "b" not in arguments:
        return create_error_response("Missing required parameter 'b'")
    
    # Extract and validate the parameters
    try:
        a = validate_number(arguments["a"], "a")
        b = validate_number(arguments["b"], "b")
    except ValueError as e:
        # Return validation error to the client
        return create_error_response(str(e))
    
    # Route to the appropriate calculation based on tool name
    try:
        if name == "add":
            result = add_numbers(a, b)
            return create_success_response(
                f"{a} + {b} = {result}"
            )
        
        elif name == "subtract":
            result = subtract_numbers(a, b)
            return create_success_response(
                f"{a} - {b} = {result}"
            )
        
        elif name == "multiply":
            result = multiply_numbers(a, b)
            return create_success_response(
                f"{a} × {b} = {result}"
            )
        
        elif name == "divide":
            # Division can raise ValueError for division by zero
            result = divide_numbers(a, b)
            return create_success_response(
                f"{a} ÷ {b} = {result}"
            )
        
        else:
            # Unknown tool requested
            return create_error_response(
                f"Unknown tool '{name}'. Available tools: add, subtract, multiply, divide"
            )
    
    except ValueError as e:
        # Catch calculation errors (e.g., division by zero)
        return create_error_response(str(e))
    
    except Exception as e:
        # Catch any unexpected errors
        # In production, you'd want to log these
        return create_error_response(
            f"An unexpected error occurred: {str(e)}"
        )


# ============================================================================
# SERVER LIFECYCLE
# ============================================================================

async def main():
    """
    Run the calculator MCP server.
    
    Sets up stdio transport and runs the server until shutdown.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    # Run the server
    asyncio.run(main())


# ============================================================================
# USAGE EXAMPLES
# ============================================================================
#
# Test with MCP Inspector:
#   npx @modelcontextprotocol/inspector python calculator_server.py
#
# Example interactions:
#
# Tool: add
# Arguments: {"a": 5, "b": 3}
# Response: "5.0 + 3.0 = 8.0"
#
# Tool: subtract
# Arguments: {"a": 10, "b": 3}
# Response: "10.0 - 3.0 = 7.0"
#
# Tool: multiply
# Arguments: {"a": 4, "b": 5}
# Response: "4.0 × 5.0 = 20.0"
#
# Tool: divide
# Arguments: {"a": 10, "b": 2}
# Response: "10.0 ÷ 2.0 = 5.0"
#
# Tool: divide
# Arguments: {"a": 10, "b": 0}
# Response: "Error: Division by zero is not allowed"
#
# Tool: add
# Arguments: {"a": "not a number", "b": 3}
# Response: "Error: Parameter 'a' must be a number, got: 'not a number'"
#
# ============================================================================
# KEY PATTERNS DEMONSTRATED
# ============================================================================
#
# 1. MULTI-TOOL SERVER
#    - Multiple tools in list_tools()
#    - if/elif routing in call_tool()
#
# 2. INPUT VALIDATION
#    - Check for required parameters
#    - Validate parameter types
#    - Convert string inputs to numbers when possible
#
# 3. ERROR HANDLING
#    - Try/except blocks for validation
#    - Try/except blocks for calculations
#    - Catch-all for unexpected errors
#    - Return user-friendly error messages
#
# 4. HELPER FUNCTIONS
#    - validate_number() for reusable validation
#    - create_error_response() for consistent error format
#    - create_success_response() for consistent success format
#    - Separate calculation functions for testability
#
# 5. DOCUMENTATION
#    - Docstrings on all functions
#    - Type hints for parameters and returns
#    - Comments explaining design decisions
#
# 6. CODE ORGANIZATION
#    - Helper functions at the top
#    - Tool registration in the middle
#    - Tool handlers after registration
#    - Server lifecycle at the bottom
#
# ============================================================================
# EXTENDING THIS SERVER
# ============================================================================
#
# To add more mathematical operations:
#
# 1. Create a calculation function:
#    def power_numbers(base: float, exponent: float) -> float:
#        return base ** exponent
#
# 2. Add the tool to list_tools():
#    Tool(
#        name="power",
#        description="Raise first number to the power of the second",
#        inputSchema=number_schema
#    )
#
# 3. Add handling in call_tool():
#    elif name == "power":
#        result = power_numbers(a, b)
#        return create_success_response(f"{a} ^ {b} = {result}")
#
# ============================================================================

