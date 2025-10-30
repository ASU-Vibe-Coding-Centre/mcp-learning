"""
Quick Decision Maker - MCP Server

This MCP server provides simple decision-making tools for demonstration purposes.
It showcases how MCP servers can extend AI assistants with custom functionality.

Tools:
- flip_coin: Returns "heads" or "tails" randomly
- roll_dice: Accepts dice notation (e.g., "1d6", "2d20") and returns results

This server uses the MCP Python SDK with stdio transport, making it suitable
for running inside a Docker container and connecting to Cursor IDE.
"""

import asyncio
import random
import re
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


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
            name="flip_coin",
            description=(
                "Flip a coin and return either 'heads' or 'tails' randomly. "
                "No parameters required - just a simple random choice."
            ),
            # Empty schema means no parameters are needed
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="roll_dice",
            description=(
                "Roll one or more dice using standard dice notation. "
                "Format: 'NdS' where N is the number of dice and S is the number of sides. "
                "Examples: '1d6' (one six-sided die), '2d20' (two twenty-sided dice), "
                "'3d10' (three ten-sided dice). Returns individual rolls and total."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notation": {
                        "type": "string",
                        "description": "Dice notation in NdS format (e.g., '1d6', '2d20')",
                    },
                },
                "required": ["notation"],
            },
        ),
    ]


def parse_dice_notation(notation: str) -> tuple[int, int]:
    """Parse dice notation string into number of dice and sides.
    
    Dice notation follows the format: NdS
    - N: Number of dice (must be positive integer)
    - S: Number of sides per die (must be positive integer)
    
    Examples:
        "1d6" -> (1, 6)  # One six-sided die
        "2d20" -> (2, 20)  # Two twenty-sided dice
        "3d10" -> (3, 10)  # Three ten-sided dice
    
    Args:
        notation: Dice notation string in NdS format
        
    Returns:
        Tuple of (number_of_dice, number_of_sides)
        
    Raises:
        ValueError: If notation is invalid or contains invalid numbers
    """
    # Use regex to match NdS format where N and S are digits
    # Pattern explanation:
    #   ^ - start of string
    #   (\d+) - one or more digits (captured as number of dice)
    #   d - literal 'd' character
    #   (\d+) - one or more digits (captured as number of sides)
    #   $ - end of string
    pattern = r"^(\d+)d(\d+)$"
    match = re.match(pattern, notation.lower().strip())
    
    if not match:
        raise ValueError(
            f"Invalid dice notation '{notation}'. "
            "Expected format: NdS (e.g., '1d6', '2d20')"
        )
    
    num_dice = int(match.group(1))
    num_sides = int(match.group(2))
    
    # Validate that numbers are reasonable
    if num_dice < 1:
        raise ValueError(f"Number of dice must be at least 1, got {num_dice}")
    if num_dice > 100:
        raise ValueError(f"Number of dice cannot exceed 100, got {num_dice}")
    if num_sides < 2:
        raise ValueError(f"Number of sides must be at least 2, got {num_sides}")
    if num_sides > 1000:
        raise ValueError(f"Number of sides cannot exceed 1000, got {num_sides}")
    
    return (num_dice, num_sides)


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations from MCP clients.
    
    This function is called when an AI assistant (like Cursor's AI) wants to use
    one of our tools. The assistant uses the tool schemas from list_tools() to
    understand how to call each tool correctly.
    
    The flow:
    1. User types a prompt in Cursor (e.g., "Flip a coin")
    2. Cursor's AI sees the flip_coin tool is available
    3. Cursor calls this function with name="flip_coin" and arguments={}
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
    if name == "flip_coin":
        # Simple random choice between two outcomes
        # random.choice selects one item randomly from a sequence
        result = random.choice(["heads", "tails"])
        return [
            TextContent(
                type="text",
                text=f"The coin landed on: {result}",
            )
        ]
    
    if name == "roll_dice":
        # Extract dice notation from arguments
        notation = arguments.get("notation")
        
        if not notation:
            raise ValueError("Missing required parameter: notation")
        
        if not isinstance(notation, str):
            raise ValueError(f"Notation must be a string, got {type(notation).__name__}")
        
        try:
            # Parse the dice notation (e.g., "2d20" -> (2, 20))
            num_dice, num_sides = parse_dice_notation(notation)
            
            # Roll each die and collect results
            rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
            total = sum(rolls)
            
            # Format the output for readability
            if num_dice == 1:
                # Single die: just show the result
                result_text = f"Rolled {notation}: {rolls[0]}"
            else:
                # Multiple dice: show individual rolls and total
                rolls_str = ", ".join(map(str, rolls))
                result_text = f"Rolled {notation}: [{rolls_str}] = {total}"
            
            return [
                TextContent(
                    type="text",
                    text=result_text,
                )
            ]
            
        except ValueError as e:
            # Re-raise with clearer error message for the user
            raise ValueError(f"Error rolling dice: {str(e)}")
    
    # If we reach here, an unknown tool was requested
    raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """Run the MCP server over stdio transport.
    
    This is the entry point that starts the MCP server. It uses stdio transport,
    which means the server communicates via standard input/output streams.
    
    How it works:
    1. stdio_server() sets up JSON-RPC streams over stdin/stdout
    2. The Server instance (app) handles routing incoming requests to our handlers
    3. The server runs until it receives a shutdown signal
    
    When running in Docker:
    - Docker connects its stdin/stdout to the container's stdin/stdout
    - Cursor IDE connects to Docker's stdin/stdout
    - This creates a communication bridge: Cursor <-> Docker <-> MCP Server
    
    The server will continue running until:
    - The client sends a shutdown request
    - The container is stopped
    - An error occurs that causes the connection to close
    """
    # stdio_server provides JSON-RPC streams over stdin/stdout
    # This is the communication channel that MCP clients use to send requests
    async with stdio_server() as (read_stream, write_stream):
        # app.run handles initialization and routes incoming requests to our handlers
        # It automatically:
        # - Parses JSON-RPC messages from the read stream
        # - Routes tool calls to call_tool()
        # - Routes tool discovery to list_tools()
        # - Sends responses back through the write stream
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    # Run the async main function using asyncio
    # This starts the server and keeps it running
    asyncio.run(main())

