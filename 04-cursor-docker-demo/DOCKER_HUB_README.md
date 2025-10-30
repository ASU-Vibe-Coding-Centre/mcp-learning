# Quick Decision Maker - MCP Server

**Docker Image:** `jestercharles/mcp-quick-decision:latest`

A simple MCP (Model Context Protocol) server for making quick decisions. Provides tools for choosing from lists and generating random numbers.

## Quick Start

### Pull the Image

```bash
docker pull jestercharles/mcp-quick-decision:latest
```

### Run the Container

```bash
docker run --rm -i jestercharles/mcp-quick-decision:latest
```

### Connect to Cursor IDE

1. Create or edit `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%/.cursor/mcp.json` (Windows)

2. Add configuration:

```json
{
  "mcpServers": {
    "quick-decision-maker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "jestercharles/mcp-quick-decision:latest"
      ]
    }
  }
}
```

3. Restart Cursor IDE

4. Test with prompts like:
   - "Help me decide between pizza, sushi, and tacos"
   - "Pick a random number between 1 and 100"

## Tools

- **`make_decision`**: Choose randomly from a list of options
- **`random_number`**: Generate a random number in a range

## Image Details

- **Base Image**: Python 3.11-slim
- **Size**: ~181MB
- **Transport**: stdio (standard input/output)
- **Platform**: Linux/amd64

## Documentation

For complete documentation and examples, see the repository:
- Instructor Guide: `README.md`
- Student Quick Start: `quick-start-student.md`
- Example Prompts: `examples/test-prompts.md`

## License

See repository for license information.

