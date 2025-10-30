# Cursor IDE MCP Configuration Examples

This directory contains example Cursor IDE MCP configuration files for the Quick Decision Maker server.

## Configuration Files

- `cursor-settings-macos.json` - macOS configuration example
- `cursor-settings-windows.json` - Windows configuration example

## HTTP Transport Configuration

**Important**: The Quick Decision Maker server uses **HTTP transport with Server-Sent Events (SSE)**. This means:

1. The Docker container runs the HTTP server on port 3333
2. Cursor IDE connects to the server via HTTP URL: `http://localhost:3333/sse`
3. The MCP server inside the container provides the tools over HTTP
4. You need to run the Docker container manually before connecting Cursor

**Before connecting Cursor:**
1. Start the Docker container: `docker run -d -p 3333:3333 jestercharles/mcp-quick-decision:latest`
2. Verify the server is running: `curl http://localhost:3333/sse` (should connect)
3. Configure Cursor to connect to `http://localhost:3333/sse`

## JSON Structure

The configuration uses the `mcpServers` object format:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "http://localhost:3333/sse"
    }
  }
}
```

### Key Fields

- **`mcpServers`**: Top-level object containing all MCP server configurations
- **`server-name`**: Unique identifier for this server (e.g., "quick-decision-maker")
- **`type`**: Transport type, set to `"http"` for HTTP transport
- **`url`**: HTTP URL where the MCP server is running (e.g., "http://localhost:3333/sse")

## Platform Differences

### macOS

- Docker command: `docker` (typically available in PATH or at `/usr/local/bin/docker`)
- Configuration file location: `~/.cursor/mcp.json` (workspace-specific) or global settings

### Windows

- Docker command: `docker.exe` (recommended for explicit path, or use `docker` if in PATH)
- Docker path examples:
  - `C:\Program Files\Docker\Docker\resources\bin\docker.exe` (typical installation path)
  - Or just `docker` if Docker is in your system PATH
- Configuration file location: `%USERPROFILE%\.cursor\mcp.json` (workspace-specific) or global settings

### Absolute Path Examples

If you need to use an absolute path instead of relying on PATH:

**macOS/Windows/Linux:**
```json
{
  "mcpServers": {
    "quick-decision-maker": {
      "type": "http",
      "url": "http://localhost:3333/sse"
    }
  }
}
```

**Note**: The configuration is the same on all platforms since we're using HTTP transport. Just make sure the Docker container is running with the port mapped.

## Configuration Placement

### Workspace-Specific Configuration (Recommended for Demo)

Place the configuration file in your workspace directory:

- **macOS/Linux**: `your-workspace/.cursor/mcp.json`
- **Windows**: `your-workspace\.cursor\mcp.json`

This keeps the configuration with your project and makes it easy to share with others.

### Global Configuration

Alternatively, place it in Cursor's global settings directory:

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Note: File names may vary depending on your Cursor version. Check Cursor's MCP settings UI to confirm the exact path.

## Usage

1. Copy the appropriate configuration file to your Cursor MCP settings location
2. Update the Docker image name if using a different tag or local build
3. Restart Cursor IDE or reload MCP connections
4. Verify the server appears in Cursor's MCP panel with available tools (flip_coin, roll_dice)

## Troubleshooting

- **"docker: command not found"**: Ensure Docker is installed and in your PATH, or use an absolute path
- **Container not starting**: Verify the Docker image exists locally (`docker images`) or can be pulled from Docker Hub
- **Server not appearing in Cursor**: Check that you've restarted Cursor or reloaded MCP connections after adding the configuration

