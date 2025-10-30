# Cursor IDE MCP Implementation Research

**Date:** October 30, 2025  
**Source:** https://cursor.com/docs/context/mcp  
**Purpose:** Document Cursor's MCP implementation for migration task

---

## Configuration File Paths

### macOS
```
~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

### Windows
```
%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

### Linux
```
~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

**Note:** The MCP configuration in Cursor is managed through the Cline extension (formerly Claude Dev), stored in the extension's global storage area.

---

## JSON Configuration Schema

Based on the Cursor MCP documentation, the configuration format is:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-api-key",
        "OTHER_VAR": "value"
      }
    },
    "another-server": {
      "command": "node",
      "args": ["/path/to/server.js"]
    }
  }
}
```

**Key Points:**
- Top-level key is `mcpServers` (object)
- Each server has a unique name as the key
- Required fields: `command`, `args`
- Optional field: `env` (for environment variables)

---

## Differences from Standard MCP Client Configuration

**Similarities with Claude Desktop:**
- Same JSON structure (`mcpServers` object)
- Same field names (`command`, `args`, `env`)
- Same transport mechanism (stdio by default)

**Differences:**
1. **File Location:** Cursor stores config in extension's global storage, not app support directory
2. **Extension Dependency:** Requires Cline extension to be installed
3. **Configuration Access:** Through Cursor's settings/extension UI, not direct file editing (though file can be edited)

---

## How Cursor Exposes MCP Tools to Users

### Access Points

1. **Cline Chat Interface:**
   - MCP tools are available in Cline's chat panel
   - Tools appear automatically when servers are configured
   - AI can invoke tools during conversations

2. **Tool Discovery:**
   - Cursor automatically discovers available tools from configured servers
   - Tools are listed in the Cline extension interface
   - Users can see tool descriptions and parameters

3. **Integration with Workflow:**
   - Tools integrate seamlessly with code editing
   - Can operate on open files, workspace context
   - Results appear in chat interface and can trigger code changes

### UI/UX Elements

- **Cline Extension Panel:** Primary interface for MCP interaction
- **Settings Access:** Cursor Settings → Extensions → Cline → MCP Servers
- **Tool Invocation:** Through natural language in Cline chat
- **Visual Indicators:** Server connection status, tool availability

---

## Environment Variable Handling

**In Configuration:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "${API_KEY}",
        "CUSTOM_VAR": "hardcoded-value"
      }
    }
  }
}
```

**Key Points:**
- Environment variables can be hardcoded in `env` object
- Can reference system environment variables using `${VAR_NAME}` syntax
- Variables are passed to the server process at startup
- No special escaping required

---

## Server Lifecycle

1. **Startup:**
   - Servers start when Cursor launches (if configured)
   - Or when Cline extension activates
   - Runs as child process of Cursor

2. **Communication:**
   - Uses stdio transport (stdin/stdout)
   - JSON-RPC 2.0 messages
   - Managed by Cline extension

3. **Shutdown:**
   - Servers terminate when Cursor closes
   - Or when extension is disabled/reloaded

4. **Auto-Restart:**
   - Servers restart if they crash (with backoff)
   - Configuration changes may require Cursor reload

---

## Testing Recommendations

### Basic Test Setup

1. **Create Simple Server:**
```python
# test_server.py
from mcp.server import Server
from mcp.types import Tool

app = Server("test-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="test_tool",
            description="A simple test tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    return [{"type": "text", "text": f"Received: {arguments.get('message')}"}]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

2. **Configure in Cursor:**
```json
{
  "mcpServers": {
    "test-server": {
      "command": "python",
      "args": ["/absolute/path/to/test_server.py"]
    }
  }
}
```

3. **Verify:**
   - Reload Cursor window (Cmd+R or Ctrl+R)
   - Open Cline extension
   - Check server connection status
   - Try invoking the test tool in chat

---

## Key Differences for Documentation

### What to Emphasize in Cursor Context

1. **Development-Focused:**
   - Code analysis, refactoring, testing tools
   - Integration with workspace files
   - Git operations and version control
   - Documentation generation

2. **Cline Extension:**
   - Explain that MCP requires Cline extension
   - How to access settings through extension
   - Extension-specific features

3. **Workspace Integration:**
   - Tools can access workspace context
   - File operations relative to workspace root
   - Integration with Cursor's file explorer

### Example Use Cases for Cursor

**Instead of (Claude Desktop - General):**
- "Summarize this email"
- "Help me plan my day"
- "Translate this text"

**Use (Cursor IDE - Development):**
- "Analyze the complexity of this function"
- "Suggest refactorings for this code"
- "Generate unit tests for this module"
- "Find security issues in this file"
- "Update documentation for these changes"

---

## Configuration Tips

### Best Practices

1. **Use Absolute Paths:**
   ```json
   "args": ["/Users/username/projects/server/server.py"]
   ```
   Not: `"args": ["./server.py"]` or `"args": ["server.py"]`

2. **Virtual Environments:**
   If using Python venv:
   ```json
   {
     "command": "/path/to/venv/bin/python",
     "args": ["/path/to/server.py"]
   }
   ```

3. **Debugging:**
   - Check Cursor's Developer Console: Help → Toggle Developer Tools
   - Look for MCP-related errors in console
   - Verify server can run standalone: `python /path/to/server.py`

4. **Reload After Changes:**
   - Configuration changes require window reload
   - Cmd+Shift+P → "Developer: Reload Window"

---

## Common Issues & Solutions

### Server Not Appearing

**Problem:** Server configured but not showing in Cline  
**Solutions:**
- Verify Cline extension is installed and enabled
- Check file path is absolute, not relative
- Reload Cursor window after config changes
- Check Developer Console for errors

### Server Crashes on Startup

**Problem:** Server starts but immediately exits  
**Solutions:**
- Test server runs standalone: `python server.py`
- Check for missing dependencies
- Verify Python/Node version compatibility
- Look for errors in Developer Console

### Environment Variables Not Working

**Problem:** Server can't access environment variables  
**Solutions:**
- Use `env` object in configuration
- Hardcode values for testing
- Check if system env vars are available to Cursor
- Consider using config files instead of env vars

---

## Implementation Notes for Migration

### Priority Updates

1. **High Priority:**
   - Configuration file paths (different from Claude Desktop)
   - Example configurations (same format, different location)
   - UI/UX references (Cline extension, not standalone app)
   - Installation instructions (extension + Cursor)

2. **Medium Priority:**
   - Example use cases (development-focused)
   - Workflow descriptions (code editing context)
   - Troubleshooting guides (Cursor-specific)

3. **Low Priority:**
   - General MCP concepts (unchanged)
   - Server implementation code (unchanged)
   - Protocol details (unchanged)

### Text Replacement Strategy

**Safe Replacements:**
- "Claude Desktop" → "Cursor IDE"
- "Claude Desktop app" → "Cursor IDE with Cline extension"
- "Claude's interface" → "Cline's interface"

**Context-Dependent:**
- "Claude" → "Cursor" (only when referring to the client)
- Keep "Claude" when referring to the AI model itself
- "AI application" can remain generic

---

## Summary

**Key Findings:**
1. Configuration format is identical to Claude Desktop
2. File location is different (extension storage vs app support)
3. Requires Cline extension to be installed
4. Access through Cline chat interface
5. Development-focused use cases are most relevant
6. Window reload required after configuration changes

**Ready for Implementation:** ✅

All necessary information has been gathered to proceed with the migration tasks.

---

**References:**
- [Cursor MCP Documentation](https://cursor.com/docs/context/mcp)
- MCP Protocol Specification
- Cline Extension Documentation

