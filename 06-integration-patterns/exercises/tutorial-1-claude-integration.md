# Tutorial 1: Connecting Your Server to Claude Desktop

Welcome to your first real-world MCP integration! In this tutorial, you'll connect an MCP server to Claude Desktop, enabling Claude to use your tools in live conversations. This is where MCP truly comes to life - giving AI assistants access to your custom capabilities.

## Learning Objectives

By completing this tutorial, you will:

1. Understand how Claude Desktop discovers and launches MCP servers
2. Configure a server in Claude Desktop's settings
3. Test server functionality through conversational AI interaction
4. Debug common integration issues
5. Verify tools are working correctly in production

## Time Estimate

20-30 minutes

## Prerequisites

Before starting, ensure you have:

- **Claude Desktop installed** (download from anthropic.com)
- **A working MCP server** (we'll use the calculator from Module 03)
- **Python 3.9+** with MCP SDK installed
- **Basic understanding** of JSON configuration files

Verify Claude Desktop is installed:

```bash
# macOS
ls ~/Library/Application\ Support/Claude/

# Windows
dir %APPDATA%\Claude\

# Linux
ls ~/.config/Claude/
```

You should see Claude's application directory exists.

## What You'll Accomplish

You'll:

1. Locate Claude Desktop's configuration file
2. Add a calculator server to the configuration
3. Restart Claude Desktop to load the server
4. Interact with Claude using your server's tools
5. Verify and debug the integration

By the end, you'll be able to ask Claude to perform calculations using your custom server!

## Overview: How Claude Desktop Integration Works

Before diving in, let's understand the architecture:

```
You → Claude Desktop → MCP Client → Your Server → Tool Logic
      (User Chat)     (Protocol)    (Python)      (Calculator)
```

**The Flow:**

1. You configure which servers Claude should use
2. Claude Desktop launches these servers on startup
3. Claude discovers available tools from each server
4. When you chat, Claude decides when to use tools
5. Your server receives tool calls and returns results
6. Claude incorporates results into its responses

**Key Point:** Your server runs as a subprocess, communicating via stdio (standard input/output).

## Step 1: Prepare Your MCP Server

First, let's create a simple calculator server to integrate.

Create a file called `calculator_server.py`:

```python
#!/usr/bin/env python3
"""
Calculator MCP Server
Provides basic arithmetic operations for Claude Desktop.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server
app = Server("calculator-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register calculator tools."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Numerator"},
                    "b": {"type": "number", "description": "Denominator"}
                },
                "required": ["a", "b"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle calculator operations."""
    
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [TextContent(
            type="text",
            text=f"{arguments['a']} + {arguments['b']} = {result}"
        )]
    
    elif name == "multiply":
        result = arguments["a"] * arguments["b"]
        return [TextContent(
            type="text",
            text=f"{arguments['a']} × {arguments['b']} = {result}"
        )]
    
    elif name == "divide":
        if arguments["b"] == 0:
            return [TextContent(
                type="text",
                text="Error: Cannot divide by zero"
            )]
        result = arguments["a"] / arguments["b"]
        return [TextContent(
            type="text",
            text=f"{arguments['a']} ÷ {arguments['b']} = {result}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


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

**Save this file** and note the full path. You'll need it in the next step.

For example:
- macOS/Linux: `/Users/yourname/mcp_servers/calculator_server.py`
- Windows: `C:\Users\yourname\mcp_servers\calculator_server.py`

### Test Your Server (Optional but Recommended)

Before integrating with Claude, verify your server works:

```bash
# Test with MCP Inspector
mcp-inspector python calculator_server.py

# Or test directly
python calculator_server.py
```

If using Inspector, try calling the `add` tool with `{"a": 5, "b": 3}`. You should get a result.

## Step 2: Locate Claude Desktop Configuration

Claude Desktop uses a JSON file to configure MCP servers.

**Find the configuration file location:**

### macOS

```bash
# Configuration file location
~/Library/Application Support/Claude/claude_desktop_config.json

# Navigate there
cd ~/Library/Application\ Support/Claude/
```

### Windows

```powershell
# Configuration file location
%APPDATA%\Claude\claude_desktop_config.json

# Navigate there
cd %APPDATA%\Claude
```

### Linux

```bash
# Configuration file location
~/.config/Claude/claude_desktop_config.json

# Navigate there
cd ~/.config/Claude
```

**If the file doesn't exist**, create it! This is normal for fresh installations.

## Step 3: Edit the Configuration File

Open `claude_desktop_config.json` in your text editor.

If the file is **empty or doesn't exist**, start with this basic structure:

```json
{
  "mcpServers": {}
}
```

Now **add your calculator server**:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/FULL/PATH/TO/calculator_server.py"]
    }
  }
}
```

**Important:** Replace `/FULL/PATH/TO/calculator_server.py` with the actual full path to your server file.

### macOS/Linux Example

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/Users/john/mcp_servers/calculator_server.py"]
    }
  }
}
```

### Windows Example

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["C:\\Users\\john\\mcp_servers\\calculator_server.py"]
    }
  }
}
```

**Note for Windows:** Use double backslashes (`\\`) or forward slashes (`/`) in paths.

### Understanding the Configuration

```json
{
  "mcpServers": {
    "calculator": {              // Server identifier (choose any name)
      "command": "python",       // How to run the server
      "args": ["path/to/file"],  // Arguments to the command
      "env": {}                  // Optional environment variables
    }
  }
}
```

- **Server ID** (`calculator`): A unique name for this server
- **Command**: The executable to run (`python`, `python3`, `node`, etc.)
- **Args**: Command-line arguments (typically just the path to your server)
- **Env**: Optional environment variables (API keys, config values)

### Adding Multiple Servers (Optional)

You can configure multiple servers:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/path/to/calculator_server.py"]
    },
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"],
      "env": {
        "WEATHER_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

For now, **just add the calculator server**.

## Step 4: Restart Claude Desktop

Changes to the configuration file only take effect when Claude Desktop starts.

**Restart Claude Desktop:**

1. **Quit Claude Desktop completely** (don't just close the window)
   - macOS: `Cmd + Q` or Claude Desktop → Quit
   - Windows: Right-click taskbar icon → Quit
   - Linux: Use your window manager's quit option

2. **Wait a few seconds** for the process to fully terminate

3. **Launch Claude Desktop again**

Claude will:
- Read the configuration file
- Launch your calculator server
- Discover available tools
- Make them available for use

**What's Happening Behind the Scenes:**

When Claude Desktop starts, it:
1. Reads `claude_desktop_config.json`
2. Spawns `python calculator_server.py` as a subprocess
3. Sends an initialization request
4. Receives the list of tools (add, multiply, divide)
5. Keeps the server running for the duration of the session

## Step 5: Verify the Integration

Now let's verify Claude can see and use your server!

### Check Server Status

In Claude Desktop, **look for indicators** that your server loaded:

- Some versions show MCP server status in settings
- Check Claude's developer console (if available)
- The most reliable way: just try using it!

### Test with a Simple Calculation

Start a new conversation with Claude and try:

**You:** "Can you add 42 and 17 for me?"

**Expected:** Claude should use your calculator server's `add` tool and respond with the result.

### What Claude Sees

When you ask for a calculation, Claude:

1. Analyzes your request
2. Recognizes it needs the `add` tool
3. Calls your server: `{"name": "add", "arguments": {"a": 42, "b": 17}}`
4. Receives the response: `"42 + 17 = 59"`
5. Incorporates this into its response to you

### More Test Queries

Try these to verify different tools:

```
"What's 7 times 8?"          → Should use multiply
"Divide 100 by 4"            → Should use divide
"Calculate 15 + 23"          → Should use add
"What's 5 divided by 0?"     → Should handle error gracefully
```

## Step 6: Debugging Common Issues

If things aren't working, here's how to troubleshoot.

### Issue 1: Claude Doesn't Use Your Tools

**Symptom:** Claude responds without calling your server.

**Possible Causes:**

1. **Server didn't start** - Check configuration file syntax
2. **Tools not relevant** - Try more specific requests
3. **Path incorrect** - Verify full path to server file

**Debug Steps:**

```bash
# Test server manually
python /path/to/calculator_server.py

# Verify with Inspector
mcp-inspector python /path/to/calculator_server.py
```

### Issue 2: Configuration File Syntax Error

**Symptom:** Claude Desktop won't start or shows an error.

**Common Mistakes:**

```json
// Bad: Missing comma
{
  "mcpServers": {
    "calculator": {
      "command": "python"
      "args": ["path"]  // Missing comma above!
    }
  }
}

// Bad: Extra comma
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["path"],  // Extra comma!
    }
  }
}

// Good: Valid JSON
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["path"]
    }
  }
}
```

**Validate Your JSON:**

Use an online JSON validator or:

```bash
# Python validation
python -m json.tool claude_desktop_config.json

# If valid, it will pretty-print the JSON
# If invalid, it will show the error
```

### Issue 3: Python Not Found

**Symptom:** Error about Python not being found.

**Solution:** Use the full path to Python:

```bash
# Find your Python path
which python    # macOS/Linux
where python    # Windows
```

Then use that path in the config:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "/usr/local/bin/python3",  // Full path
      "args": ["/path/to/calculator_server.py"]
    }
  }
}
```

### Issue 4: Module Not Found (MCP SDK)

**Symptom:** Error that `mcp` module can't be imported.

**Cause:** Python can't find the MCP SDK.

**Solution:** Ensure MCP is installed and use the same Python that has it:

```bash
# Install MCP SDK if needed
pip install mcp

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install mcp

# Then use the venv Python in config
{
  "mcpServers": {
    "calculator": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/calculator_server.py"]
    }
  }
}
```

### Issue 5: Server Crashes

**Symptom:** Server works in Inspector but not in Claude.

**Debug Strategy:**

Add logging to your server:

```python
import sys

# At the start of your server
print("Calculator server starting...", file=sys.stderr)

# After tool registration
print("Tools registered", file=sys.stderr)

# In tool handler
print(f"Handling tool: {name}", file=sys.stderr)
```

Check Claude Desktop's logs:
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\Logs\`
- Linux: `~/.config/Claude/logs/`

## Step 7: Advanced Configuration

Once basic integration works, try these enhancements:

### Add Environment Variables

Useful for API keys, configuration, etc.:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/path/to/calculator_server.py"],
      "env": {
        "LOG_LEVEL": "DEBUG",
        "MAX_PRECISION": "10"
      }
    }
  }
}
```

Access in your server:

```python
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")
max_precision = int(os.environ.get("MAX_PRECISION", "5"))
```

### Use Virtual Environment

For better dependency isolation:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/calculator_server.py"]
    }
  }
}
```

### Add Multiple Related Servers

Organize by functionality:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/path/to/calculator_server.py"]
    },
    "file-tools": {
      "command": "python",
      "args": ["/path/to/file_server.py"]
    },
    "git-tools": {
      "command": "python",
      "args": ["/path/to/git_server.py"],
      "env": {
        "GIT_REPO_PATH": "/path/to/your/repo"
      }
    }
  }
}
```

## Best Practices

### 1. Server Naming

Choose clear, descriptive server IDs:

```json
// Good
"calculator"
"github-integration"
"database-tools"

// Avoid
"server1"
"my_server"
"test"
```

### 2. Tool Descriptions

Write descriptions that help Claude understand when to use each tool:

```python
Tool(
    name="add",
    description="Add two numbers together. Use this for addition operations.",
    # ...
)
```

Better descriptions = better tool selection.

### 3. Error Handling

Always handle errors gracefully:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        # Tool logic
        result = process(arguments)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
```

### 4. Security

Never hardcode sensitive data in configuration:

```json
// Bad
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "ghp_actualtoken123"  // Don't do this!
      }
    }
  }
}

// Good - Reference environment variables
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"  // Reads from system env
      }
    }
  }
}
```

### 5. Testing Workflow

1. **Develop** with MCP Inspector
2. **Test** configuration with simple queries
3. **Deploy** to Claude Desktop
4. **Monitor** for issues in real conversations

## Verification Checklist

Before moving on, verify:

- [ ] Configuration file is valid JSON
- [ ] Server path is correct (full, absolute path)
- [ ] Python command works from terminal
- [ ] MCP SDK is installed and accessible
- [ ] Claude Desktop successfully restarted
- [ ] Claude can discover your tools
- [ ] Tools respond correctly to requests
- [ ] Error cases are handled gracefully

## What You've Learned

Congratulations! You now understand:

1. How Claude Desktop discovers and launches MCP servers
2. The configuration file format and location
3. How to add and configure servers
4. Testing and debugging integration issues
5. Best practices for production deployment

## Next Steps

Now that you have basic integration working:

1. **Try the GitHub server** from the examples
2. **Build a custom server** for your specific needs
3. **Complete Tutorial 2** to implement GitHub operations
4. **Experiment** with multi-server configurations

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Server not starting | Check config syntax and paths |
| Tools not being used | Make descriptions more specific |
| Python not found | Use full path to Python executable |
| MCP module error | Install SDK in correct Python environment |
| Server crashes | Add logging and check Claude's log files |

## Additional Resources

- **Claude Desktop Docs**: Official integration guide
- **MCP Inspector**: `mcp-inspector python your_server.py`
- **Example Servers**: Check `05-integration-patterns/examples/`
- **Module 05 README**: Detailed integration patterns

## Challenge Exercise

Now that you can integrate servers, try this:

1. Create a "time server" with tools for:
   - Getting current time
   - Converting time zones
   - Calculating time differences

2. Configure it in Claude Desktop

3. Test by asking Claude:
   - "What time is it in Tokyo?"
   - "How many hours until midnight?"
   - "What's the time difference between NYC and London?"

This reinforces the complete cycle: develop → configure → test → use.

## Summary

You've successfully integrated an MCP server with Claude Desktop! This is a major milestone - you can now give Claude access to any capability you can code. The pattern you learned applies to any server:

1. Write the server code
2. Test with Inspector
3. Configure in `claude_desktop_config.json`
4. Restart Claude Desktop
5. Verify and debug

This foundation enables endless possibilities: database access, API integrations, file operations, custom business logic, and more.

Ready to build something more complex? Continue to Tutorial 2!

