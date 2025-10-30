# Module 06: Integration Patterns

> **Advanced Content** - This module contains in-depth, comprehensive material. New to MCP? Start with the [simplified learning path](../../01-introduction-quickstart/) for a beginner-friendly introduction.

Welcome to real-world MCP integration. In this module, you'll learn how to connect your MCP servers to actual AI applications, debug effectively, and implement production-ready integration patterns.

## Module Overview

Building MCP servers is one thing - integrating them into real applications is another. This module bridges the gap between development and deployment, showing you how to:

- Connect servers to Cursor IDE and other MCP clients
- Use MCP Inspector for effective debugging
- Implement real-world integration patterns
- Design multi-server architectures
- Handle production considerations

By the end of this module, you'll be able to deploy MCP servers that work seamlessly with AI applications in production environments.

## Learning Objectives

By completing this module, you will be able to:

1. **Integrate with Cursor IDE**
   - Configure MCP servers in Cursor IDE
   - Test server functionality with real AI interactions
   - Debug connection and communication issues
   - Optimize performance for desktop integration

2. **Use MCP Inspector Effectively**
   - Set up Inspector for testing
   - Interpret request/response messages
   - Debug protocol-level issues
   - Profile server performance

3. **Implement Real-World Patterns**
   - Build GitHub integration for repository operations
   - Create Git server for version control workflows
   - Wrap external APIs as MCP servers
   - Design domain-specific integrations

4. **Design Multi-Server Architectures**
   - Understand when to split functionality across servers
   - Implement server composition patterns
   - Handle server dependencies
   - Manage configuration for multiple servers

5. **Apply Production Best Practices**
   - Implement proper error handling and logging
   - Handle rate limiting and caching
   - Secure sensitive data and credentials
   - Monitor server health and performance

## What You'll Build

Throughout this module, you'll create production-ready integrations:

1. **GitHub Integration Server** - Repository operations, issue management, file access
2. **Git Server** - Local repository operations (status, log, diff, commit)
3. **Web Scraper Server** - Extract data from websites
4. **Multi-Server Application** - Combining multiple servers for complex workflows

Each implementation demonstrates patterns you can apply to your own integrations.

## Prerequisites

Before starting this module, ensure you have:

- Completed Module 03 (Basic MCP Server)
- Completed Module 04 (Advanced Features) recommended
- Understanding of Git and version control
- Familiarity with REST APIs
- Basic understanding of web technologies

## Module Structure

### Core Integration Concepts

#### 1. Cursor IDE Integration

**What is Cursor IDE?**

Cursor IDE is Anthropic's AI assistant application that supports MCP. It's one of the primary ways users interact with MCP servers.

**Integration Flow:**

```
User ─> Cursor IDE ─> MCP Client ─> Your MCP Server ─> External System
            (AI)           (Protocol)      (Your Code)      (API/DB/Files)
```

**Configuration:**

Cursor IDE uses a JSON configuration file to discover and launch MCP servers:

**Location:**
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

**Example Configuration:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/my_server.py"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    },
    "another-server": {
      "command": "node",
      "args": ["/path/to/server.js"]
    }
  }
}
```

**Key Components:**

- **Server ID**: Unique identifier (`my-server`)
- **Command**: How to launch the server (`python`, `node`, etc.)
- **Args**: Command-line arguments (path to your server script)
- **Env**: Environment variables (API keys, config)

**How It Works:**

1. Cursor IDE reads configuration on startup
2. Launches each server as a subprocess
3. Connects via stdio transport
4. AI can now use your server's tools, resources, and prompts

#### 2. MCP Inspector

**What is MCP Inspector?**

MCP Inspector is an official debugging tool that provides a web UI for testing MCP servers. Think of it as Postman for MCP.

**Installation:**

```bash
npm install -g @modelcontextprotocol/inspector
```

**Usage:**

```bash
# Launch inspector with your server
mcp-inspector python my_server.py

# Or with arguments
mcp-inspector python my_server.py --arg value

# Opens browser at http://localhost:5173
```

**Features:**

- **Interactive Testing**: Call tools, read resources, get prompts
- **Message Inspection**: See raw JSON-RPC messages
- **Real-Time**: Watch requests and responses as they happen
- **Schema Validation**: Verify your schemas are correct
- **Performance**: Measure response times

**Workflow:**

1. **Start Server**: Inspector launches your server
2. **Discover**: Lists available tools, resources, prompts
3. **Test**: Call tools with custom parameters
4. **Inspect**: View request/response JSON
5. **Debug**: Identify issues before production

**When to Use Inspector:**

- Developing new tools or features
- Debugging protocol issues
- Validating schemas and responses
- Performance profiling
- Before connecting to Cursor IDE

#### 3. Real-World Integration Patterns

**Pattern 1: Version Control Integration**

Integrate with Git for AI-assisted development:

```python
# Git Server Example
@app.list_tools()
async def list_tools():
    return [
        Tool(name="git_status", ...),
        Tool(name="git_log", ...),
        Tool(name="git_diff", ...),
        Tool(name="git_commit", ...),
    ]
```

**Use Cases:**
- "Show me uncommitted changes"
- "What changed in the last 5 commits?"
- "Create a commit with these changes"

**Pattern 2: API Integration**

Wrap external APIs as MCP servers:

```python
# GitHub API Server
@app.list_tools()
async def list_tools():
    return [
        Tool(name="github_create_issue", ...),
        Tool(name="github_search_repos", ...),
        Tool(name="github_get_readme", ...),
    ]
```

**Use Cases:**
- "Create an issue for this bug"
- "Find popular Python ML libraries"
- "Show me the README for project X"

**Pattern 3: Data Access**

Provide AI with access to databases, files, or APIs:

```python
# Database Server
@app.list_resources()
async def list_resources():
    return [
        Resource(uri="db://schema/users", ...),
        Resource(uri="db://schema/orders", ...),
    ]

@app.list_tools()
async def list_tools():
    return [
        Tool(name="query_database", ...),
        Tool(name="export_data", ...),
    ]
```

**Use Cases:**
- "What's in the users table?"
- "Show me today's orders"
- "Export sales data to CSV"

**Pattern 4: Content Management**

Manage documents, wikis, or content:

```python
# Documentation Server
@app.list_resources()
async def list_resources():
    # Expose documentation as resources
    return [Resource(uri=f"file:///docs/{doc}", ...) for doc in docs]

@app.list_prompts()
async def list_prompts():
    # Provide content creation templates
    return [
        Prompt(name="write_api_doc", ...),
        Prompt(name="create_tutorial", ...),
    ]
```

**Use Cases:**
- "What does the API documentation say?"
- "Create a tutorial for feature X"
- "Update the troubleshooting guide"

#### 4. Multi-Server Architectures

**When to Use Multiple Servers:**

Use separate servers when:

1. **Different Domains**: Database, Git, API integrations
2. **Different Teams**: Each team owns their server
3. **Different Languages**: Python server + Node.js server
4. **Security Boundaries**: Separate sensitive operations
5. **Performance**: Distribute load across servers

**Design Patterns:**

**Pattern A: Functional Separation**

```
User ─> Cursor IDE ─> Git Server (version control)
                      └─> Database Server (data access)
                      └─> API Server (external APIs)
```

Each server handles a distinct domain.

**Pattern B: Layered Architecture**

```
User ─> Cursor IDE ─> Orchestration Server
                             ├─> Backend Server
                             ├─> Frontend Server
                             └─> Data Server
```

One server coordinates others.

**Pattern C: Microservices**

```
User ─> Cursor IDE ─> User Service Server
                      └─> Order Service Server
                      └─> Notification Service Server
```

Each server is an independent service.

**Configuration Example:**

```json
{
  "mcpServers": {
    "git": {
      "command": "python",
      "args": ["./servers/git_server.py"]
    },
    "database": {
      "command": "python",
      "args": ["./servers/db_server.py"],
      "env": {
        "DB_CONNECTION": "postgresql://..."
      }
    },
    "github": {
      "command": "python",
      "args": ["./servers/github_server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

**Benefits:**
- Clear separation of concerns
- Independent deployment
- Technology flexibility
- Easier testing and debugging

**Challenges:**
- More complex configuration
- Coordination between servers
- Duplicate functionality risk

#### 5. Production Considerations

**Error Handling:**

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        result = perform_operation(arguments)
        return [TextContent(type="text", text=result)]
    except NetworkError as e:
        # Network issues - provide helpful message
        return [TextContent(
            type="text",
            text=f"Network error: {e}. Please check your connection and try again."
        )]
    except AuthenticationError as e:
        # Auth issues - guide user to fix
        return [TextContent(
            type="text",
            text=f"Authentication failed: {e}. Please verify your credentials."
        )]
    except Exception as e:
        # Unexpected errors - log but don't expose details
        logger.error(f"Unexpected error in {name}: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text="An unexpected error occurred. Please try again later."
        )]
```

**Logging:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name} with args: {arguments}")
    # ... implementation ...
    logger.info(f"Tool {name} completed successfully")
```

**Rate Limiting:**

```python
from collections import deque
import time

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def is_allowed(self) -> bool:
        now = time.time()
        # Remove old calls
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

rate_limiter = RateLimiter(max_calls=100, time_window=60)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if not rate_limiter.is_allowed():
        return [TextContent(
            type="text",
            text="Rate limit exceeded. Please wait before trying again."
        )]
    # ... implementation ...
```

**Caching:**

```python
from functools import lru_cache
import time

class Cache:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache = {}
    
    def get(self, key: str):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value):
        self.cache[key] = (value, time.time())

cache = Cache(ttl=300)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "fetch_data":
        cache_key = f"data:{arguments['id']}"
        
        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return [TextContent(type="text", text=cached)]
        
        # Fetch and cache
        data = fetch_from_api(arguments['id'])
        cache.set(cache_key, data)
        return [TextContent(type="text", text=data)]
```

**Security:**

```python
import os
from pathlib import Path

# Use environment variables for secrets
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

# Validate paths to prevent traversal
def is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False

# Sanitize user input
def sanitize_filename(filename: str) -> str:
    # Remove dangerous characters
    return "".join(c for c in filename if c.isalnum() or c in "._- ")

# Validate operations
ALLOWED_OPERATIONS = ["read", "list", "search"]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    operation = arguments.get("operation")
    if operation not in ALLOWED_OPERATIONS:
        return [TextContent(
            type="text",
            text=f"Operation '{operation}' not allowed"
        )]
```

---

## Docker-Based Integration Patterns

In addition to direct Cursor IDE integration, you can use Docker's MCP ecosystem for more scalable and production-ready deployments.

### Integration Pattern 1: Docker Desktop with MCP Toolkit

**What is the MCP Toolkit?**

Docker Desktop 4.25+ includes the MCP Toolkit - a GUI for managing MCP servers. This is ideal for:
- Quick access to pre-built servers from the Docker MCP Catalog
- Visual management of multiple servers
- Zero-configuration client setup
- Centralized secret management

**When to Use:**
- You want quick access to catalog servers
- Managing multiple servers visually
- Local development with Docker Desktop
- Team environments with standardized tooling

**Configuration Example:**

Instead of configuring Cursor IDE directly, use the MCP Toolkit:

1. **Open Docker Desktop** → Navigate to MCP section
2. **Install Servers** from catalog (GitHub, PostgreSQL, etc.)
3. **Configure** via GUI (API keys, settings)
4. **Enable** servers
5. **Connect Cursor IDE** to Gateway endpoint

**Toolkit generates this configuration automatically:**

```json
{
  "mcpServers": {
    "docker-gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

**Benefits:**
- One configuration for all servers
- Visual server management
- Built-in gateway orchestration
- Automatic updates for catalog servers

### Integration Pattern 2: Docker CLI with Manual Gateway

**When to Use:**
- Headless/server environments
- CI/CD pipelines
- Scriptable deployments
- Production environments without GUI

**Setup:**

**Step 1: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  # MCP Gateway
  gateway:
    image: docker/mcp-gateway:latest
    container_name: mcp-gateway
    ports:
      - "3000:3000"
    volumes:
      - ./gateway-config.yml:/config/gateway.yml:ro
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - POSTGRES_URL=${POSTGRES_URL}
    command: --config /config/gateway.yml
    restart: unless-stopped
  
  # Your custom server (alongside catalog servers)
  my-custom-server:
    build:
      context: ./my-server
    container_name: mcp-custom
    environment:
      - API_KEY=${MY_API_KEY}
    restart: unless-stopped
```

**Step 2: Create gateway-config.yml**

```yaml
servers:
  # Catalog servers
  github:
    image: mcp/github:latest
    environment:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    enabled: true
  
  postgres:
    image: mcp/postgres:latest
    environment:
      POSTGRES_URL: ${POSTGRES_URL}
    enabled: true
  
  # Your custom server
  my-custom:
    url: http://mcp-custom:8080
    enabled: true

gateway:
  port: 3000
  transport: http-sse
  logging:
    level: info
```

**Step 3: Start Services**

```bash
docker compose up -d
```

**Step 4: Configure Client**

```json
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

**Benefits:**
- Scriptable and automatable
- Works in any environment
- Full control over configuration
- Integrates with existing Docker workflows

### Integration Pattern 3: Hybrid Catalog + Custom Servers

**Combining pre-built and custom servers:**

**Use Case:** You need GitHub integration (from catalog) plus a custom internal API server.

**Architecture:**

```
AI Client (Cursor IDE)
    │
    └─> Docker MCP Gateway
            ├─> mcp/github (catalog server)
            ├─> mcp/postgres (catalog server)
            └─> custom/internal-api (your server)
```

**Implementation:**

**1. Use Docker Toolkit for catalog servers:**
- Install GitHub and PostgreSQL from catalog via GUI
- Configure secrets through Toolkit

**2. Add your custom server via CLI:**

```yaml
# docker-compose.yml (in addition to Toolkit)
version: '3.8'

services:
  internal-api:
    build:
      context: ./internal-api-server
    container_name: mcp-internal-api
    environment:
      - INTERNAL_API_KEY=${INTERNAL_API_KEY}
    ports:
      - "8081:8080"
    restart: unless-stopped
```

**3. Update Gateway configuration:**

Add your custom server to the existing gateway:

```json
// Toolkit manages github and postgres
// Manually add internal-api
{
  "servers": {
    "internal-api": {
      "url": "http://localhost:8081",
      "enabled": true
    }
  }
}
```

**Benefits:**
- Best of both worlds: catalog + custom
- Catalog servers: maintained, updated automatically
- Custom servers: full control, internal integrations
- Single gateway endpoint for all

### Integration Pattern 4: Multi-Environment Deployment

**Deploy the same servers across dev, staging, and production:**

**Development (Docker Desktop + Toolkit):**

```bash
# Use Toolkit GUI
# Quick server installation
# Visual debugging
# Local development
```

**Staging (Docker Compose):**

```yaml
# docker-compose.staging.yml
version: '3.8'

services:
  gateway:
    image: docker/mcp-gateway:latest
    ports:
      - "3000:3000"
    volumes:
      - ./config/staging-gateway.yml:/config/gateway.yml:ro
    environment:
      - GITHUB_TOKEN=${STAGING_GITHUB_TOKEN}
      - LOG_LEVEL=DEBUG
```

**Production (Kubernetes/Cloud):**

```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-gateway
  template:
    spec:
      containers:
      - name: gateway
        image: docker/mcp-gateway:latest
        env:
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: github-token
```

**Configuration Management:**

```bash
# .env.development
GITHUB_TOKEN=dev_token_here
LOG_LEVEL=DEBUG

# .env.staging
GITHUB_TOKEN=staging_token_here
LOG_LEVEL=INFO

# .env.production
GITHUB_TOKEN=${PROD_GITHUB_TOKEN_FROM_SECRET_MANAGER}
LOG_LEVEL=WARNING
```

**Benefits:**
- Consistent configuration across environments
- Easy promotion: dev → staging → production
- Environment-specific settings
- Same Docker images everywhere

### Integration Pattern 5: Scaling with Gateway

**Scenario:** Multiple AI clients (users) connecting to shared servers.

**Architecture:**

```
Cursor IDE (User 1) ─┐
Cursor IDE (User 2) ─┼─> Gateway (Load Balancer)
Cursor (User 3) ─────────┘      ├─> Server Instance 1
Custom App (User 4) ─────────────├─> Server Instance 2
                                 └─> Server Instance 3
```

**Implementation with Docker:**

```yaml
version: '3.8'

services:
  gateway:
    image: docker/mcp-gateway:latest
    ports:
      - "3000:3000"
    volumes:
      - ./gateway-config.yml:/config/gateway.yml:ro
    environment:
      - GATEWAY_AUTH=true
      - RATE_LIMIT_PER_CLIENT=100
    deploy:
      replicas: 2  # Gateway redundancy

  github-server:
    image: mcp/github:latest
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    deploy:
      replicas: 3  # Scale based on load
      
  postgres-server:
    image: mcp/postgres:latest
    environment:
      - POSTGRES_URL=${POSTGRES_URL}
    deploy:
      replicas: 2
```

**Gateway Configuration:**

```yaml
gateway:
  port: 3000
  
  # Authentication
  security:
    auth_required: true
    auth_method: token
    tokens:
      - client: user1
        token: token1
      - client: user2
        token: token2
  
  # Rate limiting per client
  rate_limiting:
    enabled: true
    requests_per_minute: 100
    per_client: true
  
  # Load balancing
  load_balancing:
    strategy: round_robin
    health_check_interval: 30s

servers:
  github:
    instances: 3  # Gateway manages 3 instances
    image: mcp/github:latest
  
  postgres:
    instances: 2
    image: mcp/postgres:latest
```

**Client Configuration:**

```json
{
  "mcpServers": {
    "gateway": {
      "url": "http://gateway.example.com:3000/mcp",
      "headers": {
        "Authorization": "Bearer user1_token"
      }
    }
  }
}
```

**Benefits:**
- Central access control
- Per-client rate limiting
- Load distribution
- High availability
- Easy scaling

### Docker Integration Best Practices

**1. Use Catalog Servers First**

Before building custom servers, check the Docker MCP Catalog:
- 200+ pre-built, tested servers
- Maintained by Docker and partners
- Regular security updates
- Battle-tested in production

**2. Version Pinning**

**Development:**
```yaml
image: mcp/github:latest  # Get latest features
```

**Production:**
```yaml
image: mcp/github:1.2.3  # Pin specific version
```

**3. Secret Management**

**Don't:**
```yaml
# Bad: Secrets in compose file
environment:
  - GITHUB_TOKEN=ghp_hardcoded_token_here
```

**Do:**
```yaml
# Good: Secrets from environment
environment:
  - GITHUB_TOKEN=${GITHUB_TOKEN}

# Or use Docker secrets
secrets:
  - github_token

services:
  server:
    secrets:
      - github_token
```

**4. Health Checks**

```yaml
services:
  github-server:
    image: mcp/github:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**5. Resource Limits**

```yaml
services:
  github-server:
    image: mcp/github:latest
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

**6. Logging**

```yaml
services:
  gateway:
    image: docker/mcp-gateway:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Comparing Integration Approaches

| Aspect | Direct Cursor IDE | Docker Toolkit | Docker CLI + Gateway |
|--------|---------------------|----------------|----------------------|
| **Setup Complexity** | Low | Very Low | Medium |
| **Server Discovery** | Manual | GUI Catalog | Manual/Scripted |
| **Management** | JSON config | Visual GUI | docker-compose |
| **Scalability** | Limited | Medium | High |
| **Multi-User** | No | Limited | Yes (with auth) |
| **CI/CD** | Difficult | Limited | Excellent |
| **Production** | Not recommended | Small teams | Enterprise-ready |
| **Best For** | Development | Local dev teams | Production deployments |

### Migration Path

**Start:** Direct Cursor IDE integration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

**Grow:** Docker Toolkit (visual management)

1. Containerize your server
2. Install Docker Desktop
3. Use MCP Toolkit GUI
4. Connect Cursor IDE to Gateway

**Scale:** Docker CLI + Gateway (production)

1. Create docker-compose.yml
2. Deploy to staging/production
3. Add monitoring and logging
4. Implement load balancing

### Learning More

- **Module 03**: [Docker MCP Ecosystem](../03-docker-mcp-ecosystem/) - Complete Docker MCP coverage
- **Tutorial**: [Gateway Setup](../03-docker-mcp-ecosystem/exercises/tutorial-3-gateway-setup.md)
- **Tutorial**: [Docker CLI Workflows](../03-docker-mcp-ecosystem/exercises/tutorial-2-docker-cli.md)
- **Challenge**: [Build and Publish Server](../03-docker-mcp-ecosystem/exercises/challenge-1-publish-server.md)

---

## Development Workflow

### Building an Integration

**Step 1: Design**
- Identify what the AI needs to do
- Map external API/system to MCP primitives
- Plan error handling and edge cases

**Step 2: Implement**
- Build basic server with core tools
- Add resources for data access
- Create prompts for common workflows

**Step 3: Test with Inspector**
- Verify all tools work correctly
- Test error conditions
- Check performance

**Step 4: Integrate with Cursor IDE**
- Add to configuration file
- Test with real AI interactions
- Refine based on user experience

**Step 5: Production Hardening**
- Add comprehensive error handling
- Implement logging and monitoring
- Apply rate limiting and caching
- Security review

## Best Practices

### Configuration Management

**Use Environment Variables:**
```python
import os

config = {
    "api_key": os.environ.get("API_KEY"),
    "api_url": os.environ.get("API_URL", "https://api.example.com"),
    "debug": os.environ.get("DEBUG", "false").lower() == "true"
}
```

**Cursor IDE Config:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "${API_KEY}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Error Messages

**Good Error Messages:**
- Clear and actionable
- Don't leak sensitive information
- Suggest solutions
- Appropriate detail level

**Examples:**

```python
# Good
"GitHub API rate limit exceeded. Limit resets at 14:30 UTC. Try again in 15 minutes."

# Bad
"Error 403"

# Good
"File 'config.json' not found. Please ensure the file exists in the project root."

# Bad
"FileNotFoundError: [Errno 2] No such file or directory: '/Users/admin/secret/config.json'"
```

### Performance

**Optimize Tool Execution:**
- Cache expensive operations
- Use async/await effectively
- Batch operations when possible
- Stream large results

**Monitor:**
- Log execution times
- Track success/failure rates
- Monitor resource usage
- Set up alerts for issues

## Examples in This Module

All example code is in the `examples/` directory:

- `github_server.py` - GitHub API integration with auth
- `git_server.py` - Local Git operations
- `web_scraper_server.py` - Web scraping with BeautifulSoup
- `claude_desktop_config.json` - Example Cursor IDE configuration

## Exercises

The `exercises/` directory contains hands-on practice:

### Tutorials

1. **tutorial-1-cursor-integration.md** - Connect server to Cursor IDE
   - Estimated time: 30 minutes
   - Difficulty: Beginner
   - Configure and test your first integration

2. **tutorial-2-github-api.md** - Build GitHub integration
   - Estimated time: 60 minutes
   - Difficulty: Intermediate
   - Implement repository and issue operations

### Challenges

3. **challenge-1-multi-server.md** - Design multi-server architecture
   - Estimated time: 90 minutes
   - Difficulty: Advanced
   - Combine multiple servers for complex workflow

4. **challenge-2-api-integration.md** - Integrate with API of choice
   - Estimated time: 90 minutes
   - Difficulty: Advanced
   - Build production-ready API integration

All exercises include solutions and detailed explanations.

## Checkpoint

After completing this module, work through `checkpoint.md` to validate your understanding. You should be able to:

- Configure and test MCP servers with Cursor IDE
- Use MCP Inspector effectively for debugging
- Build real-world integrations (Git, GitHub, APIs)
- Design multi-server architectures
- Apply production best practices

## Next Steps

After mastering integration patterns, you'll move to:

**Module 06: Security & Best Practices**
- Authentication and authorization
- Input validation and sanitization
- Secure secrets management
- Production security hardening

## Getting Help

### Ask the AI Assistant

Throughout your exercises, you can ask questions like:

- "How do I configure Cursor IDE to use my server?"
- "Why isn't my server appearing in MCP Inspector?"
- "How should I handle API rate limits?"
- "What's the best way to structure multiple servers?"

### Review Examples

The example servers demonstrate complete, production-ready implementations with proper error handling, logging, and security.

### Check the Cheat Sheet

See `resources/cheatsheets/mcp-cheatsheet.md` for quick reference on:
- Cursor IDE configuration
- MCP Inspector commands
- Common integration patterns
- Debugging techniques

## Key Takeaways

By the end of this module, remember these core principles:

1. **Test Early**: Use Inspector before Cursor IDE
2. **Handle Errors**: Comprehensive error handling is critical
3. **Security First**: Never expose sensitive data
4. **Log Thoughtfully**: Balance detail with privacy
5. **Design for Users**: Think about the AI/user experience

Start with `examples/github_server.py` to see a complete integration, then work through the tutorials to build your own.

Happy integrating!

