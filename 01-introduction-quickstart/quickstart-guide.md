## QuickStart — Connect a Free MCP Server (≈10 minutes)

This guide walks you through connecting a free MCP server to your IDE and testing a few calls.

### Prerequisites
- Cursor IDE installed (or another MCP‑aware client)
- Internet access

### Finding MCP Servers
Browse the MCP catalog at `https://mcp.so`. Use the search bar or tags (e.g., "weather", "time", "calculator"). Prefer servers that:
- Do not require API keys (for fastest start)
- Have simple, clearly documented capabilities
- Are actively maintained

Recommended for this module: an Open‑Meteo weather server (no API key). You can switch to any other server later.

### 1) Finding MCP Servers
Browse available servers on the MCP catalog (`https://mcp.so`). Look for simple, anonymous servers such as time, calculator, or weather. Pick one that does not require API keys to start.

What to note:
- Server name and purpose
- How it runs (command to start, Docker image, or hosted)
- Any configuration the client needs

### 2) Connect the Server in Cursor (step‑by‑step)
You connect MCP servers to Cursor using the MCP config file. Follow these steps:

1. Create or open the config file:
   - macOS/Linux: `~/.cursor/mcp.json`
   - Windows: `%USERPROFILE%/.cursor/mcp.json`

2. Add a server entry. If your chosen server is a local executable, use the `command` form:

   ```json
   {
     "mcpServers": {
       "open-meteo-weather": {
         "command": "open-meteo-mcp-server",
         "args": []
       }
     }
   }
   ```

3. If your server runs via Docker, use a wrapper script or `docker run` in `command` with args. Example pattern:

   ```json
   {
     "mcpServers": {
       "weather-docker": {
         "command": "docker",
         "args": ["run", "--rm", "your/weather-image:latest"]
       }
     }
   }
   ```

4. Save the file, then reload MCP in Cursor:
   - Close and reopen Cursor, or
   - Use the MCP panel to refresh connections

5. Verify the server appears with its capabilities (tools/resources/prompts) in the MCP panel.

#### Additional `mcp.json` examples

- Multiple servers in one file:

```json
{
  "mcpServers": {
    "open-meteo-weather": { "command": "open-meteo-mcp-server", "args": [] },
    "calculator-local":   { "command": "calculator-mcp", "args": [] }
  }
}
```

- Passing arguments to a server:

```json
{
  "mcpServers": {
    "weather-with-locale": {
      "command": "open-meteo-mcp-server",
      "args": ["--units", "imperial", "--lang", "en"]
    }
  }
}
```

- Using environment variables (if the server supports them):

```json
{
  "mcpServers": {
    "weather-env": {
      "command": "open-meteo-mcp-server",
      "args": [],
      "env": { "APP_LOG_LEVEL": "info" }
    }
  }
}
```

### 3) Test Your Connection
Open the MCP panel in Cursor and verify that the server appears with its capabilities (tools/resources/prompts). Try a few simple calls:
- "Call tool: current_time" (if available)
- "Get current weather for New York using weather tool"
- "Fetch resource: server_info" (if provided)

Example prompts to paste into the chat:
- "What tools does the server expose?"
- "Use the weather tool to get the temperature for San Francisco."
- "List available resources from the connected server."

Expected results:
- Listing tools: You see a list of tool names with short descriptions and input schemas.
- Weather tool call: Returns current conditions (e.g., temperature, summary) as structured data or a formatted message.
- Listing resources: You see resource identifiers (e.g., `server_info`) that can be read or listed.

Expected behavior:
- The tool calls return structured outputs
- The resource read returns a small JSON object or text response
- Errors are clear if inputs are invalid

### 4) Troubleshooting
Common issues and fixes:
- Server not listed
  - Confirm config path: macOS/Linux `~/.cursor/mcp.json`, Windows `%USERPROFILE%/.cursor/mcp.json`
  - Validate JSON (no trailing commas, matching braces)
  - Reload MCP connections or restart Cursor
- Command not found
  - Ensure the server binary is installed and on PATH (`which <command>`)
  - For Docker, verify `docker` runs from your shell and the image exists
- Server not responding
  - Try running the server command manually in a terminal to check logs
  - Check network/firewall settings if the server binds to a port
  - Kill orphaned processes and retry
- Permission or path issues
  - On macOS, grant Terminal/IDE Full Disk Access if required
  - Use absolute paths in `args` when referencing files

### 5) What You Just Did
You connected an MCP‑aware client (Cursor) to an MCP server, discovered its capabilities, and executed a few calls. You now have a working baseline to build on in later modules.

### Time Estimate
≈10 minutes (5 minutes to configure, 5 minutes to test).

### What You Just Did (recap)
- Picked a simple server from the MCP catalog
- Added a connection in `~/.cursor/mcp.json`
- Reloaded the IDE and verified capabilities
- Called a tool and listed resources end‑to‑end

### Verification checklist
- MCP panel shows your server with tools/resources/prompts
- Listing tools returns at least one tool with schema
- Running a tool returns a structured response without errors
- Listing resources returns identifiers (if supported), and reading one succeeds
- No errors in the Cursor logs after reload

### Alternative: Use an n8n MCP Server
If you’re building along with Module 02, you can point Cursor directly to an n8n workflow that exposes MCP tools. See Module 02’s section “Using Cursor IDE with Workflow A (n8n MCP Server)” for the JSON config and steps.


