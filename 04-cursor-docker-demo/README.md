# Quick Decision Maker - MCP Server Demo

**Instructor Guide for 30-Minute MCP Integration Demo**

This guide provides everything you need to lead a hands-on demonstration of connecting a Docker-based MCP (Model Context Protocol) server to Cursor IDE. The demo uses a simple "Quick Decision Maker" server to illustrate MCP concepts in an engaging, easy-to-understand way.

## Demo Overview

### Learning Objectives

By the end of this demo, students will be able to:
- Understand what MCP is and why it matters for AI assistants
- Connect a Docker-based MCP server to Cursor IDE
- Test MCP tools using natural language prompts
- Explain how Cursor discovers and uses MCP tools
- Understand the Docker → MCP → Cursor architecture

### Prerequisites for Students

- Docker Desktop installed and running
- Cursor IDE installed
- Basic familiarity with Docker (can run containers)
- New to MCP (no prior experience required)

### Materials Needed

- Instructor: Docker Desktop, Cursor IDE, terminal access
- Students: Same as prerequisites
- Optional: Screen sharing capability for remote sessions

### Total Time: 30 minutes

---

## Demo Flow

- [ ] **Section 1: Introduction** (5 min)
- [ ] **Section 2: Docker Setup** (5 min)
- [ ] **Section 3: Cursor Configuration** (5 min)
- [ ] **Section 4: Interactive Testing** (10 min)
- [ ] **Section 5: Wrap-up** (5 min)

---

## Section 1: Introduction (5 minutes)

### Talking Points

**What is MCP?**
- Model Context Protocol is a standard way for AI assistants to discover and use external tools
- Think of it as "plugins for AI" - tools that extend what AI assistants can do
- Cursor IDE uses MCP to connect to servers that provide tools, resources, and prompts

**Why does this matter?**
- AI assistants are powerful, but they can't do everything natively
- MCP allows AI to interact with databases, APIs, file systems, and custom tools
- This makes AI assistants more capable and useful for real-world tasks

**What we'll do today:**
- Connect a pre-built MCP server running in Docker to Cursor IDE
- The server provides decision-making tools (make decisions from lists, generate random numbers)
- We'll test it using natural language prompts in Cursor

**Architecture Overview:**
```
Cursor IDE ←→ Docker Container ←→ MCP Server
    (user)        (transport)        (tools)
```

### Key Concepts to Explain

1. **MCP Server**: A program that provides tools to AI assistants
2. **Docker Container**: Packages the server for easy deployment
3. **HTTP Transport**: Communication over HTTP with Server-Sent Events (SSE) on port 3333
4. **Tool Discovery**: Cursor automatically discovers available tools when connected

### Visual Aids (Optional)

- Show diagram of Cursor → Docker → MCP Server connection
- Demonstrate what Cursor's MCP panel looks like (if screen sharing)

**Transition**: "Let's start by getting the server running in Docker..."

---

## Section 2: Docker Setup (5 minutes)

### Overview

We have two options for getting the server running:
1. **Pull pre-built image** (fastest, recommended for demo)
2. **Build from source** (if you want to show the Dockerfile)

### Option A: Pull Pre-Built Image (Recommended)

**Instructor Steps:**

1. **Pull the Docker image:**
   ```bash
   docker pull jestercharles/mcp-quick-decision:latest
   ```

2. **Verify the image:**
   ```bash
   docker images jestercharles/mcp-quick-decision
   ```

3. **Run the container (required for HTTP transport):**
   ```bash
   docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
   ```
   - The `-d` flag runs the container in the background
   - The `-p 3333:3333` flag maps port 3333 from container to host
   - The container will run the HTTP server on port 3333
   - Verify it's running: `docker ps`
   - Stop it later: `docker stop mcp-quick-decision`

**Student Steps:**

Students should:
1. Pull the same image on their machines
2. Verify they can see the image in their Docker images list

**Platform Notes:**

- **macOS/Windows**: Use Docker Desktop
- **Linux**: Docker Engine should be installed
- If students don't have Docker, they can observe or install during demo

### Option B: Build from Source (Alternative)

If you prefer to build from source:

1. **Navigate to server directory:**
   ```bash
   cd 04-cursor-docker-demo/server
   ```

2. **Build the image:**
   ```bash
   docker build -t mcp-quick-decision:latest .
   ```

3. **Verify build:**
   ```bash
   docker images mcp-quick-decision
   ```

**Key Points to Emphasize:**

- The Docker image packages everything needed to run the server
- No need to install Python or dependencies on your machine
- The server runs in isolation inside the container
- We expose port 3333 and map it to the host for HTTP communication
- The server uses HTTP transport with SSE (Server-Sent Events)

**Transition**: "Now that we have the server ready, let's connect it to Cursor IDE..."

---

## Section 3: Cursor Configuration (5 minutes)

### Overview

We need to tell Cursor IDE where to find our MCP server. We'll add a configuration entry that points to the Docker container.

### Configuration File Location

**macOS:**
```
~/.cursor/mcp.json
```
Or workspace-specific:
```
your-workspace/.cursor/mcp.json
```

**Windows:**
```
%USERPROFILE%/.cursor/mcp.json
```
Or workspace-specific:
```
your-workspace/.cursor/mcp.json
```

**Note**: File location may vary by Cursor version. Check Cursor's settings or MCP panel for exact path.

### Configuration Content

**macOS/Windows/Linux Configuration:**

Open or create `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%/.cursor/mcp.json` (Windows) and add:

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

**Important**: Make sure the Docker container is running before connecting Cursor!

```bash
docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
```

### Step-by-Step Instructions

1. **Start the Docker container (if not already running):**
   ```bash
   docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
   ```
   - Verify it's running: `docker ps`
   - Check logs if needed: `docker logs mcp-quick-decision`

2. **Locate or create the configuration file:**
   - Check if `~/.cursor/` directory exists (create if needed)
   - Create `mcp.json` if it doesn't exist
   - If file exists, open it and add to existing `mcpServers` object

3. **Add the server configuration:**
   - Copy the JSON configuration above
   - Ensure proper JSON formatting (commas, brackets)
   - Save the file

4. **Restart Cursor IDE:**
   - Close Cursor completely
   - Reopen Cursor IDE
   - This is required for Cursor to load the new MCP configuration

5. **Verify Connection:**
   - Open Cursor's MCP panel (check settings or extensions menu)
   - Look for "quick-decision-maker" in the list of MCP servers
   - Server should show as "connected" or show available tools

### Configuration Explained

- **`type`**: Transport type, set to `"http"` for HTTP transport
- **`url`**: HTTP URL where the MCP server is running
  - Format: `http://localhost:3333/sse`
  - The `/sse` endpoint is the Server-Sent Events endpoint for MCP communication
  - Port `3333` must match the port where Docker container is exposed

### Troubleshooting: Configuration Issues

**Issue**: Server doesn't appear in Cursor
- **Solution**: Ensure you restarted Cursor after editing the config file
- **Solution**: Check JSON syntax is valid (use a JSON validator)
- **Solution**: Verify Docker is in your PATH or use absolute path

**Issue**: Container not running
- **Solution**: Start the container: `docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest`
- **Solution**: Check container status: `docker ps`
- **Solution**: Check container logs: `docker logs mcp-quick-decision` in terminal

**Issue**: JSON syntax error
- **Solution**: Validate JSON format (no trailing commas, proper quotes)
- **Solution**: Use the example configuration from `config/cursor-settings-macos.json` or `config/cursor-settings-windows.json`

**Issue**: Port already in use
- **Solution**: Check if another container is using port 3333: `docker ps`
- **Solution**: Use a different port: `docker run -d -p 3334:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest`
- **Solution**: Update Cursor config to use the new port: `"url": "http://localhost:3334/sse"`

**Transition**: "Great! Now that Cursor is connected, let's test the server with some example prompts..."

---

## Section 4: Interactive Testing (10 minutes)

### Overview

Now we'll test the MCP server using natural language prompts in Cursor IDE. The server provides two tools:
1. **`make_decision`**: Choose randomly from a list of options
2. **`random_number`**: Generate a random number in a range

### How It Works

**Behind the Scenes:**
1. You type a prompt in Cursor (e.g., "Help me decide between pizza, sushi, and tacos")
2. Cursor's AI sees the `make_decision` tool is available
3. Cursor automatically calls the tool with the list of options
4. The MCP server processes the request and returns a random choice
5. Cursor's AI formats the response for you

**What to Show Students:**
- How Cursor automatically discovers available tools
- How natural language prompts are converted to tool calls
- How tools extend AI capabilities

### Example Prompts and Expected Behavior

#### Test 1: Make Decision from List (5 min)

**Prompt 1:**
```
Help me decide between pizza, sushi, and tacos for dinner.
```

**Expected Behavior:**
- Cursor recognizes this as a decision-making request
- Calls the `make_decision` tool with options: `["pizza", "sushi", "tacos"]`
- Returns: `"Decision: [random choice]"`
- Example output: "Decision: sushi"

**Prompt 2:**
```
I can't decide where to go on vacation: Hawaii, Paris, Tokyo, or Bali.
```

**Expected Behavior:**
- Calls `make_decision` with all four options
- Returns a randomly selected destination

**Instructor Demonstration:**

1. Open Cursor IDE
2. Open the chat/assistant panel
3. Type the first prompt
4. Show how Cursor uses the tool
5. Explain what's happening behind the scenes

**Student Activity:**

Students should:
1. Try their own decision prompts (what to have for lunch, which movie to watch, etc.)
2. Experiment with different numbers of options (2, 3, 5+ options)
3. Notice how Cursor automatically formats the tool call

#### Test 2: Random Number Generation (5 min)

**Prompt 1:**
```
Pick a random number between 1 and 100.
```

**Expected Behavior:**
- Cursor calls the `random_number` tool with `min: 1, max: 100`
- Returns a random number in that range

**Prompt 2:**
```
Generate a random number between 50 and 200.
```

**Expected Behavior:**
- Calls `random_number` with custom range
- Returns number between 50 and 200

**Instructor Demonstration:**

1. Show default behavior (1-100 range)
2. Show custom range usage
3. Explain how tools accept parameters

**Student Activity:**

Students should:
1. Try different number ranges
2. Notice how the tool accepts min/max parameters
3. See how AI understands numeric requests

### Key Teaching Moments

**Tool Discovery:**
- "Notice how Cursor knew to use the make_decision tool? That's because Cursor discovered it when we connected the server."

**Natural Language to Tool Calls:**
- "When you say 'help me decide between X, Y, Z', Cursor translates that into a tool call with those options."

**Extending AI Capabilities:**
- "Before connecting this server, Cursor couldn't make random decisions. Now it can because we added that capability."

### Interactive Q&A During Testing

Encourage questions about:
- How Cursor knows which tool to use
- What happens if the tool fails
- Can you see the actual tool calls being made?

**Transition**: "Excellent! Let's wrap up and review what we learned..."

---

## Section 5: Wrap-up (5 minutes)

### Review Points

**What We Accomplished:**
1. ✅ Connected a Docker-based MCP server to Cursor IDE
2. ✅ Tested MCP tools using natural language
3. ✅ Understood how Cursor discovers and uses tools
4. ✅ Saw the Docker → MCP → Cursor architecture in action

**Key Concepts:**
- **MCP Server**: Provides tools to AI assistants
- **Docker Packaging**: Makes servers easy to deploy
- **HTTP Transport**: Communication over HTTP on port 3333 with SSE
- **Tool Discovery**: Cursor automatically finds available tools

**Architecture Recap:**
```
Your Prompt → Cursor AI → MCP Server → Tool Execution → Result → You
```

### What's Next?

**For Students Who Want to Build Their Own Servers:**

Point to **Module 03: Building with Docker**:
- Phase 2: Build a simple custom server
- Learn how to write MCP server code
- Package your own server with Docker
- Connect it to Cursor IDE

**Resources:**
- Server code: `04-cursor-docker-demo/server/server.py`
- Dockerfile: `04-cursor-docker-demo/server/Dockerfile`
- Configuration examples: `04-cursor-docker-demo/config/`

### Quick Q&A (3 minutes)

Common questions:
- "Can I modify the server tools?"
  - Yes! See the server code and Module 03 for how to build your own
  
- "Can I run multiple MCP servers at once?"
  - Yes! Add multiple entries to your `mcp.json` file
  
- "What other MCP servers exist?"
  - Check out Docker's MCP Catalog and the MCP Registry
  - See Module 03, Phase 1 for running catalog servers

### Closing

**Instructor Summary:**
"You've now seen how MCP extends AI assistant capabilities. The Quick Decision Maker is just one example - you can build servers for databases, APIs, file systems, and any tool you need. The power of MCP is in its simplicity: standard protocol, easy packaging, automatic discovery."

**Next Steps:**
- Students can continue experimenting with the demo server
- Those interested can explore Module 03 to build their own
- All students should understand the core MCP concepts

**Thank students for their participation!**

---

## Troubleshooting Section

### Common Issues and Quick Fixes

#### Issue: Container Won't Start

**Symptom**: Container exits immediately or port 3333 is not accessible

**Possible Causes:**
1. Docker not running
2. Image not found
3. Port 3333 already in use
4. Container crashed

**Solutions:**
```bash
# Check Docker is running
docker ps

# Verify image exists
docker images | grep mcp-quick-decision

# Try pulling image again
docker pull jestercharles/mcp-quick-decision:latest

# Check container logs
docker logs mcp-quick-decision

# Check if port 3333 is in use
lsof -i :3333  # macOS/Linux
netstat -ano | findstr :3333  # Windows

# Restart container
docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
```

#### Issue: Cursor Can't Connect to Server

**Symptom**: Server doesn't appear in Cursor's MCP panel

**Possible Causes:**
1. Configuration file not found
2. JSON syntax error
3. Cursor not restarted
4. Docker not in PATH

**Solutions:**
1. Verify configuration file location and content
2. Validate JSON syntax (use JSON validator)
3. Restart Cursor IDE completely
4. Use absolute path to Docker in configuration

#### Issue: Tool Calls Fail

**Symptom**: Cursor shows error when trying to use tools

**Possible Causes:**
1. Container stopped
2. Invalid parameters sent to tool
3. Server error
4. HTTP connection issue

**Solutions:**
1. Check if container is running: `docker ps`
2. Verify HTTP endpoint is accessible: `curl http://localhost:3333/sse`
3. Check container logs: `docker logs mcp-quick-decision`
4. Verify tool parameters match the schema
5. Restart the container if needed

#### Issue: Wrong Docker Path (Windows/macOS)

**Symptom**: "docker: command not found" error

**Solution:**
Verify the container is running and the port is mapped correctly:
```bash
# Check if container is running
docker ps

# Check if port 3333 is listening
curl http://localhost:3333/sse

# Restart the container if needed
docker stop mcp-quick-decision
docker rm mcp-quick-decision
docker run -d -p 3333:3333 --name mcp-quick-decision jestercharles/mcp-quick-decision:latest
```

#### Issue: JSON Configuration Syntax Error

**Symptom**: Cursor won't load configuration

**Solution:**
- Validate JSON using an online JSON validator
- Ensure no trailing commas
- Ensure all quotes are proper JSON quotes (not curly quotes)
- Check the example files in `config/` directory

---

## Instructor Success Checklist

Use this checklist to verify students have successfully completed the demo:

### Pre-Demo Setup
- [ ] Docker Desktop is running
- [ ] Cursor IDE is installed
- [ ] Demo materials are prepared
- [ ] Configuration examples are ready

### During Demo
- [ ] All students can pull/build the Docker image
- [ ] All students can locate their Cursor configuration file
- [ ] All students successfully add the server configuration
- [ ] All students restart Cursor and see the server connected

### Post-Demo Verification

Students should be able to:
- [ ] Pull or build the Docker image
- [ ] Run the container with correct flags
- [ ] Locate and edit Cursor IDE configuration
- [ ] Restart Cursor and see the server connected
- [ ] Use natural language to invoke `make_decision` tool
- [ ] Use natural language to invoke `random_number` tool with parameters
- [ ] Explain what happens when they make a request
- [ ] Understand how Cursor discovers tools
- [ ] Explain the Docker → MCP → Cursor architecture

### Success Metrics

**Immediate Success (During Demo):**
- 90%+ of students successfully connect server to Cursor
- 100% of students can test at least one tool successfully
- Students can articulate what MCP is in their own words

**Post-Demo Success:**
- Students can reproduce the setup on their own later
- Students understand how to modify the Cursor configuration
- Students can explain the role of Docker in the setup

---

## Additional Resources

### For Students

- **Quick Start Guide**: See `quick-start-student.md` for one-page reference
- **Example Prompts**: See `examples/test-prompts.md` for more testing ideas
- **Configuration Examples**: See `config/` directory for copy-paste ready configs

### For Instructors

- **Server Code**: `server/server.py` - Show students how tools are implemented
- **Dockerfile**: `server/Dockerfile` - Explain Docker packaging
- **Module 03**: Point students here for building their own servers

### Related Modules

- **Module 01**: Introduction & QuickStart (using existing servers)
- **Module 03**: Building with Docker (build your own servers)
- **Advanced**: Deep dive into MCP protocol and advanced features

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-27  
**Target Audience:** Instructors leading 30-minute MCP integration demo  
**Estimated Demo Time:** 30 minutes

