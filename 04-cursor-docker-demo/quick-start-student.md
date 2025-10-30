# Quick Decision Maker - Quick Start Guide

**One-Page Reference for Students**

This guide helps you quickly connect the Quick Decision Maker MCP server to Cursor IDE.

## Prerequisites

- Docker Desktop installed and running
- Cursor IDE installed
- Basic Docker knowledge (can run containers)

## Step 1: Pull Docker Image (1 minute)

```bash
docker pull jestercharles/mcp-quick-decision:latest
```

Verify it's there:
```bash
docker images jestercharles/mcp-quick-decision
```

## Step 2: Run Docker Container (1 minute)

Start the container:

```bash
docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
```

Verify it's running:
```bash
docker ps
```

## Step 3: Configure Cursor IDE (2 minutes)

### macOS/Linux

Create or edit: `~/.cursor/mcp.json`

### Windows

Create or edit: `%USERPROFILE%/.cursor/mcp.json`

**Configuration (same for all platforms):**

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

**Important:** 
1. Make sure the Docker container is running before configuring Cursor
2. Restart Cursor IDE after saving the configuration file

## Step 4: Verify Connection (1 minute)

1. Open Cursor IDE
2. Check MCP panel/settings
3. Look for "quick-decision-maker" in the list
4. Server should show as "connected"

## Step 5: Test the Server (2 minutes)

Try these prompts in Cursor's chat:

### Test 1: Make Decision
```
Help me decide between pizza, sushi, and tacos for dinner.
```

### Test 2: Random Number
```
Pick a random number between 1 and 100.
```

### Test 3: Custom Range
```
Generate a random number between 50 and 200.
```

## Troubleshooting

**Container won't start?**
- Check Docker is running: `docker ps`
- Verify image exists: `docker images | grep mcp-quick-decision`
- Try pulling again: `docker pull jestercharles/mcp-quick-decision:latest`
- Check container logs: `docker logs mcp-quick-decision`

**Cursor can't connect?**
- Verify the Docker container is running: `docker ps`
- Check port 3333 is available: `curl http://localhost:3333/sse`
- Verify configuration file location and name (`mcp.json`)
- Check JSON syntax is valid (no trailing commas)
- Restart Cursor IDE completely

**Tools don't work?**
- Verify server appears in Cursor's MCP panel
- Check container is running: `docker ps`
- Try restarting Cursor again

## Student Verification Checklist

Before you finish, verify you can:

- [ ] Pull or build the Docker image successfully
- [ ] Run the container and verify it starts
- [ ] Locate and edit Cursor IDE configuration file
- [ ] Restart Cursor and see the server connected
- [ ] Use natural language to invoke `make_decision` tool
- [ ] Use natural language to invoke `random_number` tool with parameters
- [ ] Explain what happens when you make a request
- [ ] Understand how Cursor discovers tools automatically
- [ ] Explain the Docker → MCP → Cursor architecture in your own words

**Success Criteria:**
- ✅ You can connect the server to Cursor
- ✅ You can test at least one tool successfully
- ✅ You can explain what MCP is and why it matters

## What's Next?

- Explore more example prompts: `examples/test-prompts.md`
- Learn to build your own server: See Module 03
- Check server code: `server/server.py`

**Questions?** See the full instructor guide in `README.md`

