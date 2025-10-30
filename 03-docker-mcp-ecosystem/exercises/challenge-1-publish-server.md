# Challenge 1: Build and Publish an MCP Server to Docker Hub

Build a custom MCP server, containerize it with Docker, and publish it to Docker Hub.

## Challenge Overview

Create a functional MCP server that provides useful tools, package it as a Docker image following best practices, and publish it to Docker Hub for others to use.

## Difficulty: Intermediate

**Prerequisites:**
- Completed Tutorials 1-3
- Basic Python knowledge
- Docker Hub account (free at [hub.docker.com](https://hub.docker.com))
- Familiarity with Dockerfile basics

**Time Estimate:** 2-3 hours

---

## Requirements

### Functional Requirements

Your MCP server must:

1. **Provide at least 2 useful tools** that perform distinct operations
2. **Accept configuration** via environment variables
3. **Include error handling** for invalid inputs
4. **Log operations** for debugging
5. **Follow MCP specification** correctly

### Docker Requirements

Your Docker image must:

1. **Use an official base image** (e.g., `python:3.11-slim`)
2. **Run as non-root user** for security
3. **Include a health check** to verify server is running
4. **Be optimized for size** (under 200MB if possible)
5. **Use multi-stage build** if applicable
6. **Include proper labels** for metadata

### Documentation Requirements

You must provide:

1. **README.md** with:
   - Clear description of what the server does
   - List of tools provided
   - Required environment variables
   - Usage examples
   - Testing instructions

2. **Inline code comments** explaining key logic

3. **Docker Hub description** summarizing the server

---

## Suggested Server Ideas

Choose one or create your own:

### Option 1: Weather MCP Server

Tools:
- `get_current_weather(location)` - Get current weather for a location
- `get_forecast(location, days)` - Get weather forecast

Uses: OpenWeatherMap API (free tier available)

### Option 2: Calculator MCP Server

Tools:
- `calculate(expression)` - Evaluate mathematical expressions
- `convert_units(value, from_unit, to_unit)` - Convert between units
- `solve_equation(equation)` - Solve simple equations

Uses: Python's `eval()` with safety constraints, `pint` library

### Option 3: Text Tools MCP Server

Tools:
- `analyze_sentiment(text)` - Analyze sentiment of text
- `summarize_text(text, max_words)` - Summarize long text
- `translate_text(text, target_lang)` - Translate text

Uses: TextBlob, NLTK, or similar libraries

### Option 4: System Monitor MCP Server

Tools:
- `get_cpu_usage()` - Get current CPU usage
- `get_memory_info()` - Get memory statistics
- `get_disk_usage(path)` - Get disk space info

Uses: `psutil` library

---

## Step-by-Step Guide

### Phase 1: Build the MCP Server

#### 1.1 Create Project Structure

```bash
mkdir my-mcp-server
cd my-mcp-server

# Create files
touch server.py
touch requirements.txt
touch Dockerfile
touch .dockerignore
touch README.md
```

#### 1.2 Implement Server (server.py)

```python
#!/usr/bin/env python3
"""
Your MCP Server
Description of what it does
"""

import asyncio
import os
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("my-mcp-server")

# Initialize server
app = Server("my-mcp-server")

# TODO: Implement your tools here
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="example_tool",
            description="Example tool description",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Input parameter"
                    }
                },
                "required": ["input"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool"""
    if name == "example_tool":
        # TODO: Implement your tool logic
        result = f"Processed: {arguments.get('input', 'none')}"
        return [TextContent(type="text", text=result)]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

#### 1.3 Create requirements.txt

```txt
mcp>=0.1.0
# Add your specific dependencies here
```

#### 1.4 Test Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test server
python server.py
```

---

### Phase 2: Containerize the Server

#### 2.1 Create Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /build

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Metadata labels
LABEL org.opencontainers.image.title="My MCP Server"
LABEL org.opencontainers.image.description="Description of what your server does"
LABEL org.opencontainers.image.authors="your-email@example.com"
LABEL org.opencontainers.image.source="https://github.com/yourusername/my-mcp-server"
LABEL org.opencontainers.image.licenses="MIT"

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash mcpuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/mcpuser/.local

# Copy application code
COPY --chown=mcpuser:mcpuser server.py .

# Switch to non-root user
USER mcpuser

# Add .local/bin to PATH
ENV PATH=/home/mcpuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Run server
CMD ["python", "server.py"]
```

#### 2.2 Create .dockerignore

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
*.md
.git/
.gitignore
tests/
.pytest_cache/
```

#### 2.3 Build Image Locally

```bash
# Build image
docker build -t my-mcp-server:test .

# Check image size
docker images my-mcp-server:test

# Test image
docker run --rm -i my-mcp-server:test

# Test with environment variables
docker run --rm -i \
  -e LOG_LEVEL=DEBUG \
  my-mcp-server:test
```

---

### Phase 3: Write Documentation

#### 3.1 Create README.md

```markdown
# My MCP Server

Brief description of what your server does.

## Features

- Tool 1: Description
- Tool 2: Description

## Tools Provided

### tool_name_1

Description of what this tool does.

**Parameters:**
- `param1` (string, required): Description
- `param2` (number, optional): Description

**Example:**
\`\`\`
Tool call: tool_name_1
Arguments: {"param1": "value"}
Result: ...
\`\`\`

### tool_name_2

Description of what this tool does.

## Configuration

### Required Environment Variables

- `API_KEY`: Your API key (if applicable)

### Optional Environment Variables

- `LOG_LEVEL`: Logging level (default: INFO)

## Usage

### With Docker CLI

\`\`\`bash
docker run -d \
  --name my-mcp-server \
  -e API_KEY=your_key \
  yourusername/my-mcp-server:latest
\`\`\`

### With Docker Compose

\`\`\`yaml
services:
  mcp-server:
    image: yourusername/my-mcp-server:latest
    environment:
      API_KEY: ${API_KEY}
\`\`\`

### With Cursor IDE

\`\`\`json
{
  "mcpServers": {
    "my-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "API_KEY=your_key",
        "yourusername/my-mcp-server:latest"
      ]
    }
  }
}
\`\`\`

## Testing

\`\`\`bash
# Using MCP Inspector
npx @modelcontextprotocol/inspector \
  docker run --rm -i yourusername/my-mcp-server:latest
\`\`\`

## Building from Source

\`\`\`bash
git clone https://github.com/yourusername/my-mcp-server
cd my-mcp-server
docker build -t my-mcp-server .
\`\`\`

## License

MIT License - see LICENSE file for details
```

---

### Phase 4: Publish to Docker Hub

#### 4.1 Create Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for free account
3. Verify email

#### 4.2 Create Repository

1. Click "Create Repository"
2. Name: `my-mcp-server`
3. Description: Brief summary
4. Visibility: Public
5. Create

#### 4.3 Tag and Push Image

```bash
# Login to Docker Hub
docker login
# Enter username and password

# Tag image with your username
docker tag my-mcp-server:test yourusername/my-mcp-server:1.0.0
docker tag my-mcp-server:test yourusername/my-mcp-server:latest

# Push to Docker Hub
docker push yourusername/my-mcp-server:1.0.0
docker push yourusername/my-mcp-server:latest

# Verify on Docker Hub
# Visit: https://hub.docker.com/r/yourusername/my-mcp-server
```

#### 4.4 Update Docker Hub Description

1. Go to your repository on Docker Hub
2. Click "Edit" on description
3. Paste your README content
4. Save

---

### Phase 5: Test Published Image

#### 5.1 Pull and Test

```bash
# Remove local images
docker rmi yourusername/my-mcp-server:latest

# Pull from Docker Hub
docker pull yourusername/my-mcp-server:latest

# Test it works
docker run --rm -i yourusername/my-mcp-server:latest
```

#### 5.2 Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector \
  docker run --rm -i yourusername/my-mcp-server:latest
```

#### 5.3 Test with AI Client

Add to Cursor IDE config and test all tools.

---

## Evaluation Criteria

Your solution will be evaluated on:

### Functionality (40 points)
- [ ] Server implements at least 2 working tools (20 pts)
- [ ] Tools handle errors gracefully (10 pts)
- [ ] Configuration via environment variables works (10 pts)

### Docker Implementation (30 points)
- [ ] Uses official base image (5 pts)
- [ ] Runs as non-root user (10 pts)
- [ ] Includes health check (5 pts)
- [ ] Image size is reasonable (<200MB preferred) (5 pts)
- [ ] Build is reproducible (5 pts)

### Documentation (20 points)
- [ ] README is clear and comprehensive (10 pts)
- [ ] Code includes helpful comments (5 pts)
- [ ] Usage examples are provided (5 pts)

### Publishing (10 points)
- [ ] Successfully published to Docker Hub (5 pts)
- [ ] Docker Hub description is complete (3 pts)
- [ ] Image can be pulled and used by others (2 pts)

**Total: 100 points**

---

## Bonus Challenges

Want to go further?

### Bonus 1: Automated Testing (+10 pts)

Add automated tests:
- Unit tests for tool logic
- Integration tests for MCP protocol
- CI/CD pipeline (GitHub Actions)

### Bonus 2: Multi-Architecture (+10 pts)

Build for multiple platforms:
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t yourusername/my-mcp-server:latest \
  --push .
```

### Bonus 3: Contribute to Catalog (+20 pts)

Submit your server to Docker MCP Catalog:
1. Fork [docker/mcp-registry](https://github.com/docker/mcp-registry)
2. Create server definition YAML
3. Submit pull request

---

## Common Issues and Solutions

### Issue: Image too large

**Solutions:**
- Use `python:3.11-slim` instead of `python:3.11`
- Use multi-stage build
- Remove unnecessary files
- Use `.dockerignore`

### Issue: Permission denied

**Solutions:**
- Ensure files are owned by non-root user
- Check file permissions in Dockerfile
- Verify USER directive is set correctly

### Issue: Dependencies not found

**Solutions:**
- Ensure requirements.txt is complete
- Check Python path with non-root user
- Verify COPY commands in Dockerfile

---

## Solution Template

A complete solution template is available in:
`03-docker-mcp-ecosystem/exercises/solutions/challenge-1-solution/`

This includes:
- Working server implementation
- Optimized Dockerfile
- Comprehensive documentation
- Testing instructions

**Try to complete the challenge before looking at the solution!**

---

## Share Your Work

Once completed, share your server:

1. **GitHub**: Create repository with your code
2. **Docker Hub**: Ensure good documentation
3. **Community**: Share on MCP Discord/forums
4. **Feedback**: Ask others to test and review

---

## What You'll Learn

- Building complete MCP servers from scratch
- Docker best practices for production images
- Publishing and distributing Docker images
- Writing user-facing documentation
- Complete server development lifecycle

Good luck!

