"""
Simple MCP Server: "Lucky Dice & Timekeeper"

Tools:
- roll_dice(sides: int = 6, rolls: int = 1) -> list[int]
- get_timestamp() -> str (ISO 8601)

This server uses the MCP Python SDK with stdio transport.
See advanced examples for more patterns.
"""

import asyncio
import datetime as dt
import random
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create the MCP server instance. This name is shown to clients.
app = Server("lucky-dice-timekeeper")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Describe available tools with JSON Schemas.

    Returns:
        A list of Tool definitions discoverable by MCP clients.
    """
    # Advertise two tools: dice rolling and current timestamp.
    return [
        Tool(
            name="roll_dice",
            description=(
                "Roll one or more dice and return the results. "
                "Parameters: sides (int, default 6), rolls (int, default 1)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sides": {
                        "type": "integer",
                        "minimum": 2,
                        "default": 6,
                        "description": "Number of sides on the die",
                    },
                    "rolls": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 1,
                        "description": "How many dice to roll",
                    },
                },
            },
        ),
        Tool(
            name="get_timestamp",
            description="Return the current timestamp in ISO 8601 format (UTC).",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


def _validate_int(value: Any, default: int, minimum: int | None = None, maximum: int | None = None) -> int:
    """Validate and coerce an integer value with optional bounds.

    Args:
        value: Provided value (may be None).
        default: Value to use when input is None.
        minimum: Optional lower bound (inclusive).
        maximum: Optional upper bound (inclusive).

    Returns:
        A validated integer within the specified bounds.

    Raises:
        ValueError: If the value is not an int or violates bounds.
    """
    if value is None:
        return default
    if not isinstance(value, int):
        raise ValueError("Value must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"Value must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"Value must be <= {maximum}")
    return value


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool invocations for roll_dice and get_timestamp.

    Args:
        name: Tool name provided by the client.
        arguments: JSON-serializable dict of tool arguments.

    Returns:
        A list with one TextContent message containing the result.

    Raises:
        ValueError: If an unknown tool name is requested.
    """
    # Dispatch to the correct tool by name.
    if name == "roll_dice":
        # Read and validate parameters with sensible defaults.
        sides = _validate_int(arguments.get("sides"), default=6, minimum=2)
        rolls = _validate_int(arguments.get("rolls"), default=1, minimum=1, maximum=100)

        # Generate the requested number of random rolls.
        results = [random.randint(1, sides) for _ in range(rolls)]
        return [
            TextContent(
                type="text",
                text=f"Rolled {rolls} d{sides}: {results}",
            )
        ]

    if name == "get_timestamp":
        # Produce an ISO 8601 UTC timestamp.
        now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        return [TextContent(type="text", text=now.isoformat())]

    raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """Run the MCP server over stdio until shutdown."""
    # stdio_server provides JSON-RPC streams over stdin/stdout.
    async with stdio_server() as (read_stream, write_stream):
        # app.run handles initialization and request routing.
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())


