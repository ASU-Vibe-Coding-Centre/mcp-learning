# Tutorial 3: Setting Up Docker MCP Gateway

Learn how to set up and configure Docker MCP Gateway to manage multiple MCP servers through a single endpoint.

## Prerequisites

- Docker installed (CLI or Desktop)
- Completed Tutorial 1 or Tutorial 2
- At least 2-3 MCP servers installed
- Basic understanding of Docker networking

## What is MCP Gateway?

The MCP Gateway acts as a centralized proxy between AI clients and multiple MCP servers. Instead of connecting to each server individually, clients connect once to the Gateway, which routes requests to the appropriate servers.

**Benefits:**
- Single endpoint for all servers
- Centralized configuration management
- Simplified client setup
- Better security and access control
- Unified logging and monitoring

---

## Part 1: Gateway Architecture Understanding

### Without Gateway

```
AI Client
├── Connect to MCP Server 1 (localhost:3001)
├── Connect to MCP Server 2 (localhost:3002)
├── Connect to MCP Server 3 (localhost:3003)
└── Connect to MCP Server N (localhost:300N)

Configuration file has N entries
Each server needs individual management
```

### With Gateway

```
AI Client
└── Connect to Gateway (localhost:3000)
    └── Gateway routes to:
        ├── MCP Server 1
        ├── MCP Server 2
        ├── MCP Server 3
        └── MCP Server N

Configuration file has 1 entry
Gateway handles all server management
```

---

## Part 2: Gateway Setup with Docker Desktop

### 2.1 Enable Gateway in Toolkit

If you're using Docker Desktop with MCP Toolkit:

1. Open Docker Desktop
2. Navigate to MCP Toolkit section
3. Go to Settings → Gateway
4. Toggle "Enable Gateway"
5. Note the gateway endpoint: `http://localhost:3000/mcp`

The Gateway is now automatically managing all servers you've enabled in the Toolkit!

### 2.2 Configure AI Client

Update your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "docker-gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

### 2.3 Verify Connection

1. Restart Claude Desktop
2. Check connection status in Docker Desktop MCP Toolkit
3. Ask Claude: "What MCP tools are available?"
4. Claude should list tools from all enabled servers

---

## Part 3: Gateway Setup with Docker CLI

For command-line users, we'll set up a standalone Gateway.

### 3.1 Create Project Directory

```bash
# Create gateway project directory
mkdir -p ~/mcp-gateway
cd ~/mcp-gateway

# Create subdirectories
mkdir -p config data logs
```

### 3.2 Create Gateway Configuration

Create `config/gateway.yml`:

```yaml
# Gateway server configuration
gateway:
  port: 3000
  host: 0.0.0.0
  transport: http-sse
  
  # Logging
  logging:
    level: info
    format: json
    output: /logs/gateway.log
  
  # Security (optional)
  security:
    auth_required: false
    # For production, enable authentication:
    # auth_required: true
    # auth_method: token
    # tokens:
    #   - client: claude_desktop
    #     token: secret-token-123

# MCP servers to manage
servers:
  # Filesystem server
  filesystem:
    image: mcp/filesystem:latest
    enabled: true
    environment:
      ROOT_PATH: /workspace
    volumes:
      - ${HOME}/Documents:/workspace:ro
    resources:
      cpu: 0.5
      memory: 1G
  
  # SQLite server
  sqlite:
    image: mcp/sqlite:latest
    enabled: true
    environment:
      DB_PATH: /data/app.db
    volumes:
      - ./data:/data
    resources:
      cpu: 0.5
      memory: 1G
  
  # GitHub server (requires token)
  github:
    image: mcp/github:latest
    enabled: true
    environment:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    resources:
      cpu: 0.5
      memory: 512M
```

### 3.3 Create Environment File

Create `.env`:

```bash
# GitHub API token
GITHUB_TOKEN=your_github_personal_access_token_here

# Other API keys as needed
# POSTGRES_URL=postgresql://user:pass@localhost:5432/db
```

### 3.4 Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gateway:
    image: docker/mcp-gateway:latest
    container_name: mcp-gateway
    ports:
      - "3000:3000"
    volumes:
      - ./config/gateway.yml:/config/gateway.yml:ro
      - ./logs:/logs
      - ./data:/data
      - ${HOME}/Documents:/workspace:ro
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    command: --config /config/gateway.yml
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  default:
    name: mcp-gateway-network
```

### 3.5 Start the Gateway

```bash
# Load environment variables
source .env

# Start gateway
docker compose up -d

# Check it's running
docker compose ps

# View logs
docker compose logs -f
```

**Expected output:**
```
[+] Running 1/1
 ✔ Container mcp-gateway  Started
 
NAME           IMAGE                        STATUS          PORTS
mcp-gateway    docker/mcp-gateway:latest    Up 10 seconds   0.0.0.0:3000->3000/tcp
```

### 3.6 Verify Gateway Health

```bash
# Check health endpoint
curl http://localhost:3000/health

# Expected response:
# {"status":"healthy","servers":{"filesystem":"running","sqlite":"running","github":"running"}}

# Check available tools
curl http://localhost:3000/mcp/tools

# Check server list
curl http://localhost:3000/mcp/servers
```

---

## Part 4: Configure AI Clients

### 4.1 Claude Desktop Configuration

Create or update `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

### 4.2 Cursor Configuration

Add to Cursor settings:

```json
{
  "mcp": {
    "servers": {
      "gateway": {
        "url": "http://localhost:3000/mcp"
      }
    }
  }
}
```

### 4.3 Restart Clients

1. Quit and restart Claude Desktop
2. Restart Cursor
3. Verify connection in client logs

---

## Part 5: Testing the Gateway

### 5.1 Test Tool Discovery

In Claude Desktop or Cursor, ask:

```
What MCP tools are available?
```

You should see tools from all three servers:
- Filesystem tools (read_file, write_file, list_directory)
- SQLite tools (query, execute, list_tables)
- GitHub tools (search_code, create_issue, create_pr)

### 5.2 Test Filesystem Access

```
List files in my Documents directory
```

Gateway routes request → Filesystem server → Returns results

### 5.3 Test SQLite Operations

```
List tables in the SQLite database
```

Gateway routes request → SQLite server → Returns results

### 5.4 Test GitHub Integration

```
Search my GitHub repositories for TODO comments
```

Gateway routes request → GitHub server → Returns results

---

## Part 6: Gateway Monitoring

### 6.1 View Gateway Logs

```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f gateway

# Search for errors
docker compose logs gateway | grep ERROR

# View last 50 lines
docker compose logs --tail 50 gateway
```

### 6.2 Monitor Server Status

```bash
# Check which servers are running
curl http://localhost:3000/mcp/servers | jq

# Check server health
docker compose exec gateway ps aux

# View resource usage
docker stats mcp-gateway --no-stream
```

### 6.3 View Request Metrics

```bash
# Gateway logs show routing information
docker compose logs gateway | grep "routing request"

# Example output:
# [INFO] routing request: list_directory -> filesystem server
# [INFO] routing request: query -> sqlite server
# [INFO] routing request: search_code -> github server
```

---

## Part 7: Managing Gateway Servers

### 7.1 Enable/Disable Servers

Edit `config/gateway.yml` to disable a server:

```yaml
servers:
  github:
    image: mcp/github:latest
    enabled: false  # Changed from true
    # ... rest of config
```

Restart gateway:

```bash
docker compose restart gateway
```

### 7.2 Add New Server

Add to `config/gateway.yml`:

```yaml
servers:
  # ... existing servers ...
  
  postgres:
    image: mcp/postgres:latest
    enabled: true
    environment:
      POSTGRES_URL: ${POSTGRES_URL}
    resources:
      cpu: 1.0
      memory: 2G
```

Add to `.env`:

```bash
POSTGRES_URL=postgresql://user:pass@host:5432/dbname
```

Restart:

```bash
docker compose down
docker compose up -d
```

### 7.3 Update Server Images

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d

# Verify update
docker compose logs -f
```

---

## Part 8: Advanced Gateway Configuration

### 8.1 Enable Authentication

Edit `config/gateway.yml`:

```yaml
gateway:
  security:
    auth_required: true
    auth_method: token
    tokens:
      - client: claude_desktop
        token: claude-secret-token-123
      - client: cursor
        token: cursor-secret-token-456
```

Update client configs to include token:

```json
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer claude-secret-token-123"
      }
    }
  }
}
```

### 8.2 Configure Rate Limiting

```yaml
gateway:
  rate_limiting:
    enabled: true
    requests_per_minute: 60
    requests_per_hour: 1000
    per_client: true
```

### 8.3 Set Up Access Control

```yaml
gateway:
  access_control:
    github_tools:
      allowed_clients: [claude_desktop, cursor]
    postgres_tools:
      allowed_clients: [claude_desktop]
    filesystem_tools:
      allowed_paths: ["/workspace/safe/*"]
```

---

## Part 9: Troubleshooting

### Issue: Gateway won't start

```bash
# Check logs for errors
docker compose logs gateway

# Common issues:
# - Port 3000 already in use
# - Config file syntax error
# - Missing environment variables

# Test config syntax
docker compose config

# Check port availability
lsof -i :3000
```

### Issue: Can't connect from client

```bash
# Verify gateway is running
docker compose ps

# Test endpoint manually
curl http://localhost:3000/health

# Check firewall isn't blocking
# Check client config file syntax
```

### Issue: Server not responding

```bash
# Check server status in gateway
curl http://localhost:3000/mcp/servers

# Restart specific server (edit gateway.yml, restart gateway)
docker compose restart gateway

# Check server logs
docker compose logs gateway | grep "server_name"
```

---

## Challenge Exercises

### Challenge 1: Multi-Environment Setup

Create separate gateway configurations for:
- Development (all servers, verbose logging)
- Staging (selected servers, moderate logging)
- Production (minimal servers, error logging only)

### Challenge 2: Custom Health Checks

Implement custom health check endpoints for each server that verify:
- Server is responding
- Required external services are accessible
- Resource usage is within limits

### Challenge 3: Gateway Dashboard

Create a simple web dashboard that displays:
- Gateway status
- List of active servers
- Recent request history
- Error rates and latency metrics

Hint: Use gateway logs and health endpoints as data sources.

---

## What You've Learned

- How Gateway simplifies multi-server management
- Setting up Gateway with Docker Desktop Toolkit
- Setting up standalone Gateway with Docker CLI
- Configuring AI clients to use Gateway
- Monitoring and debugging Gateway operations
- Managing servers through Gateway configuration
- Advanced features: authentication, rate limiting, access control

---

## Next Steps

- **Tutorial 4**: Build and publish your own MCP server
- **Module 04**: Learn to build custom MCP servers from scratch
- **Module 05**: Advanced integration patterns

For troubleshooting, see [Module 08: Debugging & Troubleshooting](../../08-debugging-troubleshooting/)

---

## Quick Reference

```bash
# Gateway Management
docker compose up -d                    # Start gateway
docker compose ps                       # Check status
docker compose logs -f gateway          # View logs
docker compose restart gateway          # Restart gateway
docker compose down                     # Stop gateway

# Health Checks
curl http://localhost:3000/health       # Gateway health
curl http://localhost:3000/mcp/servers  # Server status
curl http://localhost:3000/mcp/tools    # Available tools

# Configuration
vim config/gateway.yml                  # Edit config
docker compose config                   # Validate config
docker compose restart gateway          # Apply changes
```

