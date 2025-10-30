# Module 03 Checkpoint: Basic MCP Server Implementation

This checkpoint validates your understanding of Module 03. Complete all sections to ensure you're ready to move on to advanced features.

## Purpose

This checkpoint helps you:

1. Verify you understand core MCP server concepts
2. Confirm you can build servers independently
3. Identify any gaps in knowledge before advancing
4. Build confidence in your MCP development skills

## Estimated Time

45-60 minutes

## Prerequisites

Before starting, you should have:

- Completed Tutorials 1 and 2
- Attempted at least one challenge
- Reviewed the example servers
- Tested servers with MCP Inspector

---

## Part 1: Concept Review

Answer these questions to check your conceptual understanding. Don't just guess - if you're unsure, review the module content.

### Question 1: Server Components

**Q:** What are the three essential components every MCP server must have?

<details>
<summary>Click to reveal answer</summary>

1. **Server Instance**: The `Server()` object that coordinates functionality
2. **Tool Registration**: The `@app.list_tools()` handler that declares available tools
3. **Tool Handler**: The `@app.call_tool()` handler that executes tool requests

All three are required for a functioning MCP server.
</details>

### Question 2: Tool Schemas

**Q:** Why do tools need an `inputSchema` even if they don't take any parameters?

<details>
<summary>Click to reveal answer</summary>

The `inputSchema` is part of the tool contract. It tells clients (and LLMs) what parameters are expected. Even for tools with no parameters, you should provide a schema:

```python
inputSchema={
    "type": "object",
    "properties": {},
    "required": []
}
```

This makes the tool's interface explicit and follows JSON Schema standards.
</details>

### Question 3: Return Values

**Q:** Why do tool handlers return a *list* of `TextContent` instead of a single `TextContent` object?

<details>
<summary>Click to reveal answer</summary>

MCP supports returning multiple content items in a single response. This allows tools to:
- Return multiple pieces of information
- Mix content types (text, images, embedded resources)
- Provide structured, multi-part responses

Even if you're only returning one item, it must be wrapped in a list for consistency with the protocol.
</details>

### Question 4: Error Handling

**Q:** What's the difference between raising a `ValueError` and returning an error message as `TextContent`?

<details>
<summary>Click to reveal answer</summary>

**Raising ValueError:**
- Used for unknown tools or severe programming errors
- Results in a protocol-level error
- Should be rare in production

**Returning error as TextContent:**
- Used for user/input errors (invalid parameters, failed operations)
- Provides user-friendly error messages
- Allows the client to display the error gracefully
- The preferred method for handling expected error conditions

Example:
```python
# Raise ValueError for unknown tools
if name not in ["tool1", "tool2"]:
    raise ValueError(f"Unknown tool: {name}")

# Return TextContent for input errors
if value < 0:
    return [TextContent(type="text", text="Error: Value must be positive")]
```
</details>

### Question 5: Async/Await

**Q:** Why must tool handlers be async functions (use `async def`)?

<details>
<summary>Click to reveal answer</summary>

MCP is built on async I/O to:
- Handle multiple concurrent requests efficiently
- Support streaming responses (covered in Module 04)
- Work with async transport layers (stdio, SSE, HTTP)
- Follow modern Python async patterns

All handler functions must be async, even if they don't use `await` internally, because they're called by the async MCP framework.
</details>

---

## Part 2: Code Reading

Review this code and answer the questions:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="process_data",
            description="Process data",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string"}
                },
                "required": ["data"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "process_data":
        data = arguments["data"]
        result = data.upper()
        return [TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")
```

### Question 6: What issues do you see?

<details>
<summary>Click to reveal issues and fixes</summary>

**Issues:**

1. **No input validation**
   - What if `data` is empty?
   - What if `arguments` doesn't contain "data"?

2. **Generic description**
   - "Process data" doesn't tell LLMs what the tool actually does

3. **No error handling**
   - If `data.upper()` fails (though unlikely), there's no try/except

**Improved version:**

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="process_data",
            description="Convert text to uppercase letters. Useful for normalizing text input.",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The text to convert to uppercase"
                    }
                },
                "required": ["data"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "process_data":
        # Validate parameter exists
        data = arguments.get("data")
        if data is None:
            return [TextContent(
                type="text",
                text="Error: 'data' parameter is required"
            )]
        
        # Validate parameter is not empty
        if not data.strip():
            return [TextContent(
                type="text",
                text="Error: 'data' cannot be empty"
            )]
        
        # Process and return
        result = data.upper()
        return [TextContent(type="text", text=result)]
    
    raise ValueError(f"Unknown tool: {name}")
```
</details>

---

## Part 3: Hands-On Exercise

Now build a server from scratch to prove your skills!

### The Challenge

Create an MCP server called "string-utils" with THREE tools:

#### Tool 1: count_characters

- **Parameters**: `text` (string, required)
- **Returns**: Character count, including and excluding spaces
- **Example**: "hello world" → "11 characters (9 without spaces)"

#### Tool 2: find_substring

- **Parameters**:
  - `text` (string, required)
  - `substring` (string, required)
  - `case_sensitive` (boolean, optional, default: true)
- **Returns**: Number of occurrences and positions
- **Example**: Find "the" in "The cat and the dog" (case_insensitive) → "Found 2 times at positions: 0, 12"

#### Tool 3: replace_spaces

- **Parameters**:
  - `text` (string, required)
  - `replacement` (string, optional, default: "_")
- **Returns**: Text with spaces replaced
- **Example**: "hello world" with "-" → "hello-world"

### Requirements

Your server must:

1. Validate all inputs appropriately
2. Handle edge cases (empty strings, substring not found, etc.)
3. Return helpful error messages
4. Include clear tool descriptions
5. Use helper functions where appropriate
6. Include type hints and docstrings

### Starter Template

```python
#!/usr/bin/env python3
"""String Utilities MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("string-utils")

# TODO: Add helper functions here

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return available string utility tools."""
    # TODO: Implement tool registration
    pass

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle string utility tool calls."""
    # TODO: Implement tool routing and handlers
    pass

async def main():
    """Run the string utilities server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### Testing Checklist

Test your server with these cases:

#### count_characters
- [ ] Normal text: "hello world"
- [ ] Empty string: ""
- [ ] Only spaces: "   "
- [ ] Special characters: "hello! @#$"

#### find_substring
- [ ] Found once: text="hello", substring="ll"
- [ ] Found multiple times: text="hello hello", substring="he"
- [ ] Not found: text="hello", substring="xyz"
- [ ] Case sensitive: text="Hello", substring="hello", case_sensitive=true
- [ ] Case insensitive: text="Hello", substring="hello", case_sensitive=false
- [ ] Empty substring

#### replace_spaces
- [ ] Normal text: "hello world"
- [ ] Multiple spaces: "hello    world"
- [ ] No spaces: "helloworld"
- [ ] Only spaces: "   "
- [ ] Custom replacement: replacement="-"
- [ ] Empty replacement: replacement=""

### Success Criteria

Your checkpoint is complete when:

- [ ] All three tools are implemented
- [ ] Server starts without errors
- [ ] All tools appear in MCP Inspector
- [ ] All test cases pass
- [ ] Error handling works correctly
- [ ] Code includes helper functions, type hints, and docstrings

---

## Part 4: Self-Assessment

Rate your confidence (1-5) for each skill:

1 = Not confident, need to review  
5 = Very confident, ready to move on

### Core Skills

- [ ] I can create a basic MCP server from scratch
- [ ] I understand tool schemas and how to define parameters
- [ ] I can implement tool handlers with proper routing
- [ ] I know how to validate input parameters
- [ ] I can handle errors and return appropriate messages
- [ ] I understand when to use helper functions
- [ ] I can test my servers with the MCP Inspector

### Code Quality

- [ ] I write clear, descriptive tool names and descriptions
- [ ] I include input validation for all parameters
- [ ] I use type hints and docstrings
- [ ] I extract helper functions to avoid duplication
- [ ] I write helpful error messages

### Concepts

- [ ] I understand the MCP server lifecycle
- [ ] I know the difference between list_tools() and call_tool()
- [ ] I understand why async/await is required
- [ ] I can explain the role of JSON Schema in tool definitions
- [ ] I know when to group tools in one server vs. separate servers

**If any rating is below 3, review that section of Module 03 before continuing.**

---

## Part 5: Troubleshooting Challenge

Imagine a learner shows you this error. How would you help them fix it?

### Scenario

```
Error: My server starts, but when I try to call the 'greet' tool in the Inspector, 
I get an error: "Unknown tool: greet"

My code:
@app.list_tools()
async def list_tools():
    return [Tool(name="hello", description="...", inputSchema={...})]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        # ...handle greeting...
```

### Your Diagnosis

<details>
<summary>Click to reveal solution</summary>

**Problem**: Tool name mismatch

- In `list_tools()`: Tool is named "hello"
- In `call_tool()`: Handler checks for "greet"

**Solution**: Make the names match:

```python
# Either change list_tools:
Tool(name="greet", ...)

# Or change call_tool:
if name == "hello":
```

**Key Lesson**: Tool names must match exactly (including case) between registration and handling.
</details>

---

## Part 6: Reflection

Before moving on, reflect on these questions:

1. **What was the most challenging concept in this module?**
   - How did you overcome it?
   - What resources helped?

2. **What patterns do you see emerging in MCP server code?**
   - Input validation
   - Helper functions
   - Error handling
   - Routing patterns

3. **How would you explain MCP servers to someone else?**
   - Can you explain it in one or two sentences?
   - What's the simplest example you could give?

4. **What questions do you still have?**
   - Write them down
   - Ask the AI assistant or review the docs
   - Don't move on with unresolved confusion

---

## Completion

Once you've:

- [ ] Answered all concept questions
- [ ] Reviewed the code reading section
- [ ] Completed the hands-on exercise
- [ ] Tested your server thoroughly
- [ ] Rated yourself 3+ on all self-assessment items
- [ ] Reflected on your learning

You're ready for **Module 04: Advanced Features**!

---

## Need Help?

### Stuck on the Hands-On Exercise?

Ask the AI assistant:
- "How do I find substring positions in Python?"
- "What's the best way to validate string inputs?"
- "Can you explain how case-insensitive matching works?"

### Concepts Still Unclear?

- Re-read the relevant section in README.md
- Review the example servers
- Look at the solution files
- Try explaining it out loud (rubber duck debugging)

### Want More Practice?

Before moving on, try:
- Adding more tools to your checkpoint server
- Implementing one of the challenge exercises
- Building a server for a problem you've encountered

---

## What's Next?

Module 04 covers:
- Streaming responses for long operations
- Resources for exposing data
- Prompt templates
- Combining multiple features

But first, make sure you've mastered the basics here. Advanced features build on these foundations!

Good luck with your checkpoint!

