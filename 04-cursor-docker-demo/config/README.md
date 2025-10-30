# Cursor IDE MCP Configuration Examples

This directory contains example Cursor IDE MCP configuration files for the Quick Decision Maker server.

## Configuration Files

- `cursor-settings-macos.json` - macOS configuration example
- `cursor-settings-windows.json` - Windows configuration example

## JSON Structure

The configuration uses the `mcpServers` object format:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "image-name:tag"]
    }
  }
}
```

### Key Fields

- **`mcpServers`**: Top-level object containing all MCP server configurations
- **`server-name`**: Unique identifier for this server (e.g., "quick-decision-maker")
- **`command`**: The executable to run (e.g., "docker" or "docker.exe" on Windows)
- **`args`**: Array of command-line arguments
  - `run`: Docker run command
  - `--rm`: Automatically remove container when it stops
  - `-i`: Interactive mode (required for stdio transport)
  - `image-name:tag`: Docker image to run (e.g., "jestercharles/mcp-quick-decision:latest")

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

**macOS:**
```json
{
  "mcpServers": {
    "quick-decision-maker": {
      "command": "/usr/local/bin/docker",
      "args": ["run", "--rm", "-i", "jestercharles/mcp-quick-decision:latest"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "quick-decision-maker": {
      "command": "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe",
      "args": ["run", "--rm", "-i", "jestercharles/mcp-quick-decision:latest"]
    }
  }
}
```

Note: On Windows, use double backslashes (`\\`) in JSON paths.

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

