# Module 03: Docker MCP Ecosystem

> **Advanced Content** - This module contains in-depth, comprehensive material. New to MCP? Start with the [simplified learning path](../../01-introduction-quickstart/) for a beginner-friendly introduction.

Welcome to the Docker MCP Ecosystem module! In this module, you'll learn how to leverage Docker's comprehensive MCP infrastructure to discover, deploy, and manage MCP servers at scale.

## Learning Objectives

By the end of this module, you will:

- Understand the Docker MCP ecosystem architecture and components
- Browse and use pre-built servers from the Docker MCP Catalog
- Configure and manage MCP servers using Docker MCP Toolkit
- Set up Docker MCP Gateway for multi-server orchestration
- Know when to use catalog servers vs building custom servers
- Be able to publish your own MCP servers to Docker Hub

## Table of Contents

1. [Why Docker for MCP?](#why-docker-for-mcp)
2. [Docker Desktop vs Docker CLI](#docker-desktop-vs-docker-cli)
3. [Docker MCP Components Overview](#docker-mcp-components-overview)
4. [Docker MCP Catalog](#docker-mcp-catalog)
5. [Docker MCP Toolkit (Desktop)](#docker-mcp-toolkit)
6. [Using MCP Servers with Docker CLI](#using-mcp-servers-with-docker-cli)
7. [Docker MCP Gateway](#docker-mcp-gateway)
8. [Publishing to Docker Hub](#publishing-to-docker-hub)
9. [Best Practices](#best-practices)
10. [Exercises](#exercises)
11. [Next Steps](#next-steps)

---

## Why Docker for MCP?

### The Problem

Traditional MCP server deployment faces several challenges:

**Environment Conflicts**
```
Your Machine:
├── Python 3.9 (for Server A)
├── Python 3.11 (for Server B)  // CONFLICT!
├── Package X v1.0 (for Server A)
├── Package X v2.0 (for Server B)  // CONFLICT!
└── System packages potentially exposed
```

**Setup Complexity**
- Install specific Python versions
- Manage virtual environments
- Configure dependencies manually
- Handle platform-specific issues
- Troubleshoot environment problems

**Security Concerns**
- Servers access host filesystem
- No resource limits
- Shared system resources
- Difficult to isolate

**Platform Inconsistency**
- Works on macOS, breaks on Linux
- Different behavior on Windows
- Dependencies missing on some systems

### The Docker Solution

Docker containerization solves all these problems:

```
Docker Approach:
Your Machine
├── Container 1 (Server A)
│   ├── Python 3.9
│   ├── Package X v1.0
│   └── Isolated filesystem
├── Container 2 (Server B)
│   ├── Python 3.11
│   ├── Package X v2.0
│   └── Isolated filesystem
└── Container 3 (Server C)
    ├── Node.js 18
    ├── TypeScript packages
    └── Isolated filesystem

All isolated, no conflicts!
```

**Benefits:**

1. **Complete Isolation** - Each server has its own environment
2. **No Conflicts** - Dependencies don't clash
3. **Consistent Behavior** - Same everywhere (macOS, Linux, Windows)
4. **Easy Distribution** - Pull and run in seconds
5. **Security** - Resource limits and filesystem isolation
6. **Simple Management** - Start, stop, update easily

---

## Docker Desktop vs Docker CLI

You have two main approaches to working with Docker MCP servers:

### Docker Desktop (GUI Approach)

**What It Is:**
- Full Docker application with graphical interface
- Includes built-in MCP Toolkit for visual management
- Available for macOS, Windows, and Linux

**Best For:**
- Developers who prefer visual interfaces
- Quick discovery and installation of catalog servers
- Teams wanting unified tool across platforms
- Those who want zero-configuration setup

**Pros:**
- **MCP Toolkit Built-in**: Browse catalog, install servers, manage configurations via GUI
- **Visual Management**: See all servers, status, logs in one dashboard
- **Auto-Configuration**: Toolkit generates client configs automatically
- **Integrated Gateway**: Built-in gateway for server aggregation
- **Easy Secret Management**: GUI for adding API keys and tokens

**Cons:**
- Larger resource footprint (~1-2GB RAM)
- Requires license for some commercial use
- Not available in headless/server environments
- GUI might feel slower for CLI experts

**Installation:**
```bash
# Download from: https://www.docker.com/products/docker-desktop
# Install via GUI installer
# MCP Toolkit included automatically in v4.25+
```

---

### Docker CLI (Command-Line Approach)

**What It Is:**
- Docker Engine only, no GUI
- Manage everything via terminal commands
- Available on all platforms, including servers

**Best For:**
- Developers comfortable with command line
- Server/headless environments
- Scriptable workflows and automation
- Minimal resource usage
- Open source preference (Apache 2.0 license)

**Pros:**
- **Lightweight**: Minimal memory usage
- **Scriptable**: Everything is a command
- **Faster**: No GUI overhead
- **Server-Friendly**: Works in SSH/headless environments
- **Free and Open**: No licensing restrictions

**Cons:**
- **Manual Configuration**: Create JSON configs manually
- **No Visual Discovery**: Use `docker search` or browse hub.docker.com
- **More Setup**: Need to configure Gateway separately
- **Steeper Learning Curve**: Must know Docker commands

**Installation:**
```bash
# macOS (with Homebrew)
brew install docker docker-compose
brew install colima  # Docker runtime
colima start

# Linux (Ubuntu/Debian)
sudo apt-get install docker.io docker-compose

# Verify
docker --version
docker compose version
```

---

### Comparison Table

| Feature | Docker Desktop | Docker CLI |
|---------|----------------|------------|
| **MCP Catalog Browser** | ✅ GUI browser | ⚠️ Manual (hub.docker.com or CLI search) |
| **Server Installation** | ✅ One-click install | ⚠️ `docker pull` command |
| **Configuration** | ✅ GUI forms | ⚠️ Manual JSON/YAML editing |
| **Gateway** | ✅ Built-in, auto-configured | ⚠️ Run separately via docker-compose |
| **Client Connection** | ✅ Auto-generates configs | ⚠️ Manual config file creation |
| **Secret Management** | ✅ Secure GUI input | ⚠️ Environment variables or files |
| **Server Monitoring** | ✅ Visual dashboard | ⚠️ `docker ps`, `docker logs` |
| **Resource Usage** | 1-2GB RAM | <100MB RAM |
| **Scripting/Automation** | ⚠️ Limited | ✅ Fully scriptable |
| **Headless/Server Use** | ❌ No | ✅ Yes |
| **License** | Commercial use restrictions | ✅ Open source (Apache 2.0) |

---

### Which Should You Use?

**Use Docker Desktop if:**
- You want the fastest setup experience
- You prefer visual interfaces
- You're learning and want to explore the catalog visually
- You want automatic client configuration
- Resource usage isn't a concern

**Use Docker CLI if:**
- You're comfortable with terminal commands
- You're working on a server without GUI
- You want to script and automate everything
- You prefer minimal resource usage
- You're in an environment requiring open source tools

**Use Both:**
Many developers use Docker Desktop locally for exploration and development, then deploy using Docker CLI in production or CI/CD environments.

---

### This Module Covers Both

Throughout this module, you'll see:
- **Primary examples with Docker Desktop + Toolkit** (most accessible)
- **CLI alternatives in separate sections** (for command-line users)
- **Best practices for both approaches**

Choose the approach that fits your workflow!

---

## Docker MCP Components Overview

Docker's MCP ecosystem consists of four integrated components:

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Ecosystem                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  1. Docker MCP Catalog                                  │ │
│  │     • 200+ pre-built servers                            │ │
│  │     • Verified and versioned                            │ │
│  │     • Local and remote options                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  2. Docker MCP Toolkit (Docker Desktop)                 │ │
│  │     • GUI for server management                         │ │
│  │     • One-click install and configuration               │ │
│  │     • Client integration (Claude, Cursor, etc.)         │ │
│  │     • Built-in Gateway aggregator                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  3. Docker MCP Gateway (Standalone)                     │ │
│  │     • Orchestrates multiple servers                     │ │
│  │     • Centralized configuration                         │ │
│  │     • Routing and load balancing                        │ │
│  │     • Authentication and access control                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  4. Docker Hub MCP Integration                          │ │
│  │     • Distribution platform                             │ │
│  │     • mcp/ namespace for official servers               │ │
│  │     • Version management and tags                       │ │
│  │     • Publishing and contribution                       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Component Relationships

**Catalog → Toolkit → Gateway → Hub**

1. **Catalog** maintains the registry of available servers
2. **Toolkit** provides GUI to browse Catalog and manage servers
3. **Gateway** orchestrates servers (built into Toolkit, available standalone)
4. **Hub** distributes Docker images for all servers

---

## Docker MCP Catalog

The Docker MCP Catalog is a curated, centralized registry of pre-built MCP servers.

### What's in the Catalog?

**200+ Verified Servers** covering:

**Development & DevOps:**
- `mcp/github` - Repository operations, issues, PRs
- `mcp/gitlab` - GitLab project management
- `mcp/git` - Local Git operations
- `mcp/filesystem` - File system access
- `mcp/docker` - Container management

**Databases & Data:**
- `mcp/postgres` - PostgreSQL operations
- `mcp/mysql` - MySQL database access
- `mcp/mongodb` - MongoDB operations
- `mcp/redis` - Redis cache operations
- `mcp/sqlite` - SQLite database access

**Cloud Services:**
- `mcp/aws` - AWS service integrations
- `mcp/gcp` - Google Cloud Platform
- `mcp/azure` - Microsoft Azure operations

**Monitoring & Observability:**
- `mcp/newrelic` - Application monitoring
- `mcp/grafana` - Metrics and dashboards
- `mcp/prometheus` - Metrics collection
- `mcp/datadog` - Infrastructure monitoring

**Business Services:**
- `mcp/stripe` - Payment processing
- `mcp/slack` - Team communication
- `mcp/email` - Email operations
- `mcp/calendar` - Calendar management

**And 180+ more...**

### Server Types

**Local Servers (Docker whale icon)**

Built and digitally signed by Docker:
- Run as containers on your machine
- Work offline once downloaded
- Complete data privacy
- Predictable performance
- All processing happens locally

**Example:** `mcp/filesystem`, `mcp/sqlite`, `mcp/git`

**Remote Servers (Cloud icon)**

Hosted services accessed over internet:
- Maintained by service providers
- Always up-to-date
- Live data access
- No local resources used
- Require internet connectivity

**Example:** `mcp/github` (calls GitHub API), `mcp/stripe` (payment processing)

### Browsing the Catalog

**Method 1: Docker Desktop (Recommended)**

1. Open Docker Desktop
2. Navigate to MCP Toolkit section
3. Click "Browse Catalog"
4. Search or filter by category
5. View server details, capabilities, required configuration

**Method 2: Docker Hub**

Visit: `https://hub.docker.com/u/mcp`

All official servers are under the `mcp/` namespace.

**Method 3: Command Line**

```bash
# Search for MCP servers
docker search mcp/

# Pull a specific server
docker pull mcp/filesystem:latest

# List pulled MCP images
docker images mcp/*
```

### Server Metadata

Each catalog entry includes:

**Basic Information:**
- Server name and description
- Version and release notes
- Publisher (Docker or partner)
- Digital signature verification

**Capabilities:**
- Tools provided
- Resources exposed
- Prompts available
- API requirements

**Configuration:**
- Required environment variables
- Optional settings
- Secret management
- Volume mounts needed

**Example Catalog Entry:**

```yaml
name: mcp/github
version: 1.2.0
publisher: Docker
signature: verified
type: remote

description: >
  GitHub integration providing repository operations,
  issue management, PR creation, and code search.

tools:
  - github_search_code
  - github_create_issue
  - github_create_pr
  - github_get_file
  - github_push_files

configuration:
  required:
    - GITHUB_TOKEN
  optional:
    - GITHUB_API_URL (for Enterprise)
    
resource_limits:
  cpu: 1
  memory: 2GB
  
security:
  filesystem_access: none
  network_access: api.github.com
```

### Using Catalog Servers

**Quick Start (via Docker Desktop):**

1. **Browse** → Find server you need
2. **Install** → One-click pull and configure
3. **Configure** → Add required secrets (API keys)
4. **Enable** → Start the server
5. **Connect** → Link to AI client (Claude, Cursor, etc.)
6. **Use** → Server tools available immediately

**Quick Start (via CLI):**

```bash
# Pull server image
docker pull mcp/github:latest

# Run server with configuration
docker run -d \
  --name mcp-github \
  -e GITHUB_TOKEN=your_token_here \
  mcp/github:latest

# Test server (using MCP Inspector)
npx @modelcontextprotocol/inspector \
  docker run --rm mcp/github:latest
```

---

## Docker MCP Toolkit

The Docker MCP Toolkit is integrated into Docker Desktop and provides a comprehensive GUI for managing MCP servers.

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Docker Desktop (MCP Toolkit)                 │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Catalog Browser                            │ │
│  │  • Search and filter servers                         │ │
│  │  • View capabilities and docs                        │ │
│  │  • One-click installation                            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Server Manager                             │ │
│  │  • Start/stop servers                                │ │
│  │  • Configure settings                                │ │
│  │  • Manage secrets                                    │ │
│  │  • Monitor health                                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Client Configuration                       │ │
│  │  • Cursor IDE                                    │ │
│  │  • Cursor                                            │ │
│  │  • Continue.dev                                      │ │
│  │  • Gordon                                            │ │
│  │  • Custom clients                                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Built-in MCP Gateway                       │ │
│  │  • Aggregates all servers                            │ │
│  │  • Single endpoint for clients                       │ │
│  │  • Routing and orchestration                         │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────┬────────────────────────────────────┘
                       │ HTTP SSE / stdio
         ┌─────────────┼─────────────┐
         │             │             │
    Container 1   Container 2   Container 3
    (Server A)    (Server B)    (Server C)
```

### Key Features

#### 1. Zero Manual Setup

**Traditional Approach:**
```bash
# Install Python version
pyenv install 3.11.0

# Create virtual environment
python3 -m venv mcp-env
source mcp-env/bin/activate

# Install dependencies
pip install github-mcp-server requests PyGithub

# Configure environment
export GITHUB_TOKEN=...
export GITHUB_API_URL=...

# Run server
python -m github_mcp_server
```

**Docker Toolkit Approach:**
```
1. Click "GitHub" in catalog
2. Click "Install"
3. Enter GitHub token
4. Click "Enable"
Done! (30 seconds)
```

#### 2. Cross-LLM Compatibility

Configure once, use everywhere:

```yaml
# Toolkit generates this configuration automatically
clients:
  claude_desktop:
    enabled: true
    endpoint: http://localhost:3000/mcp
  
  cursor:
    enabled: true
    endpoint: http://localhost:3000/mcp
  
  continue_dev:
    enabled: true
    endpoint: http://localhost:3000/mcp
```

All clients connect to the same Gateway endpoint, accessing all servers.

#### 3. Secret Management

**Secure secret storage:**
- Encrypted at rest
- Never logged or exposed
- Automatically injected into containers
- Rotatable without redeployment

**GUI Workflow:**
```
Server Settings → Secrets →
├── Add Secret
│   ├── Key: GITHUB_TOKEN
│   ├── Value: ghp_xxxxxxxxxxxx (hidden)
│   └── Description: GitHub API access
└── Save (encrypted)
```

#### 4. Resource Management

**Default Limits (Configurable):**
- CPU: 1 core
- Memory: 2GB RAM
- Disk: No host access (except explicit mounts)
- Network: Restricted to necessary endpoints

**Security Features:**
- Image signature verification
- Attestation checking
- No root access in containers
- Isolated networking

### Using the Toolkit

#### Installation

**Prerequisites:**
- Docker Desktop 4.25+ (includes MCP Toolkit)
- Available on macOS, Windows, Linux

**Steps:**
1. Download Docker Desktop: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install following platform instructions
3. Launch Docker Desktop
4. Navigate to MCP section (sidebar)

#### Workflow Example: Adding GitHub Server

**Step 1: Browse Catalog**
```
Docker Desktop → MCP → Catalog → Search "github"
```

**Step 2: Review Details**
- Tools: `github_search_code`, `github_create_issue`, `github_create_pr`
- Requires: `GITHUB_TOKEN`
- Type: Remote (calls GitHub API)
- Security: Verified, signed by Docker

**Step 3: Install**
```
Click "Install" → Docker pulls mcp/github:latest
```

**Step 4: Configure**
```
Server Settings →
  Secrets →
    Add Secret:
      Key: GITHUB_TOKEN
      Value: [your GitHub personal access token]
      
  Options →
    Enable on startup: ✓
    Resource limits: Default (1 CPU, 2GB)
```

**Step 5: Enable**
```
Toggle "Enabled" → Server starts
Status: Running ✓
```

**Step 6: Connect Client**
```
Client Configuration →
  Cursor IDE →
    Status: Connected ✓
    Endpoint: http://localhost:3000/mcp
    
  Cursor →
    Status: Not configured
    Click "Configure" → Follow prompts
```

**Step 7: Test**
```
Open Cursor IDE
Ask: "Search my GitHub repos for TODO comments"
GitHub server tools are now available!
```

#### Managing Multiple Servers

**Dashboard View:**
```
┌─────────────────────────────────────────────┐
│  Enabled MCP Servers (5)                    │
├─────────────────────────────────────────────┤
│  ✓ mcp/github         Running      [Stop]   │
│  ✓ mcp/filesystem     Running      [Stop]   │
│  ✓ mcp/postgres       Running      [Stop]   │
│  ○ mcp/stripe         Stopped      [Start]  │
│  ○ mcp/slack          Stopped      [Start]  │
└─────────────────────────────────────────────┘
```

**Bulk Operations:**
- Start all
- Stop all
- Update all
- Export configuration
- Import configuration

---

## Using MCP Servers with Docker CLI

For developers who prefer command-line tools or work in headless environments, here's how to work with MCP servers using Docker CLI.

### Prerequisites

```bash
# Verify Docker CLI is installed
docker --version

# Verify Docker Compose
docker compose version

# Ensure Docker daemon is running
docker ps
```

### Discovering MCP Servers

**Method 1: Search Docker Hub**

```bash
# Search for official MCP servers
docker search mcp/

# Search for specific server
docker search mcp/github

# View server details on Docker Hub
# Visit: https://hub.docker.com/u/mcp
```

**Method 2: Browse Catalog Online**

Visit [hub.docker.com/u/mcp](https://hub.docker.com/u/mcp) to see:
- All available servers
- Documentation for each server
- Required configuration
- Usage examples

### Installing (Pulling) Servers

```bash
# Pull a specific server
docker pull mcp/filesystem:latest

# Pull multiple servers at once
docker pull mcp/github:latest
docker pull mcp/postgres:latest
docker pull mcp/sqlite:latest

# Verify downloaded images
docker images mcp/*
```

**Output Example:**
```
REPOSITORY           TAG       IMAGE ID       CREATED        SIZE
mcp/filesystem       latest    abc123def456   2 days ago     120MB
mcp/github           latest    def456ghi789   3 days ago     95MB
mcp/postgres         latest    ghi789jkl012   1 week ago     150MB
```

### Running Individual Servers

**Example 1: Filesystem Server**

```bash
# Run filesystem server
docker run -d \
  --name mcp-filesystem \
  -e ROOT_PATH=/workspace \
  -v ${HOME}/Documents:/workspace \
  mcp/filesystem:latest

# Check it's running
docker ps | grep mcp-filesystem

# View logs
docker logs mcp-filesystem

# Follow logs in real-time
docker logs -f mcp-filesystem
```

**Example 2: GitHub Server**

```bash
# Run GitHub server with token
docker run -d \
  --name mcp-github \
  -e GITHUB_TOKEN=your_github_token_here \
  mcp/github:latest

# Verify
docker ps | grep mcp-github

# Check environment is set correctly
docker inspect mcp-github | grep GITHUB_TOKEN
```

**Example 3: SQLite Server**

```bash
# Run SQLite server with database file
docker run -d \
  --name mcp-sqlite \
  -v ${HOME}/databases:/data \
  -e DB_PATH=/data/mydb.sqlite \
  mcp/sqlite:latest
```

### Managing Server Lifecycle

```bash
# Stop a server
docker stop mcp-github

# Start a stopped server
docker start mcp-github

# Restart a server
docker restart mcp-github

# Remove a server (stops and deletes)
docker rm -f mcp-github

# View resource usage
docker stats mcp-github

# View detailed information
docker inspect mcp-github
```

### Using Docker Compose for Multiple Servers

Create `mcp-servers-compose.yml`:

```yaml
version: '3.8'

services:
  # GitHub integration
  github:
    image: mcp/github:latest
    container_name: mcp-github
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
    
  # File system access
  filesystem:
    image: mcp/filesystem:latest
    container_name: mcp-filesystem
    environment:
      - ROOT_PATH=/workspace
    volumes:
      - ${HOME}/Documents:/workspace:ro  # Read-only
    restart: unless-stopped
    
  # PostgreSQL integration
  postgres:
    image: mcp/postgres:latest
    container_name: mcp-postgres
    environment:
      - POSTGRES_URL=${POSTGRES_URL}
    restart: unless-stopped
    
  # SQLite database
  sqlite:
    image: mcp/sqlite:latest
    container_name: mcp-sqlite
    environment:
      - DB_PATH=/data/app.db
    volumes:
      - ./data:/data
    restart: unless-stopped

networks:
  default:
    name: mcp-network
```

**Create `.env` file for secrets:**

```bash
# .env
GITHUB_TOKEN=ghp_your_token_here
POSTGRES_URL=postgresql://user:pass@localhost:5432/dbname
```

**Manage all servers:**

```bash
# Start all servers
docker compose -f mcp-servers-compose.yml up -d

# Check status
docker compose -f mcp-servers-compose.yml ps

# View logs for all services
docker compose -f mcp-servers-compose.yml logs

# View logs for specific service
docker compose -f mcp-servers-compose.yml logs github

# Follow logs
docker compose -f mcp-servers-compose.yml logs -f

# Stop all servers
docker compose -f mcp-servers-compose.yml stop

# Start all servers
docker compose -f mcp-servers-compose.yml start

# Remove all servers
docker compose -f mcp-servers-compose.yml down

# Remove servers and volumes
docker compose -f mcp-servers-compose.yml down -v
```

### Setting Up MCP Gateway with Docker CLI

**Step 1: Create Gateway Configuration**

Create `gateway-config.yml`:

```yaml
servers:
  github:
    image: mcp/github:latest
    environment:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    enabled: true
    
  filesystem:
    image: mcp/filesystem:latest
    environment:
      ROOT_PATH: /workspace
    volumes:
      - ${HOME}/Documents:/workspace
    enabled: true
    
  postgres:
    image: mcp/postgres:latest
    environment:
      POSTGRES_URL: ${POSTGRES_URL}
    enabled: true

gateway:
  port: 3000
  transport: http-sse
  
  logging:
    level: info
    format: json
```

**Step 2: Create Docker Compose for Gateway**

Create `gateway-compose.yml`:

```yaml
version: '3.8'

services:
  gateway:
    image: docker/mcp-gateway:latest
    container_name: mcp-gateway
    ports:
      - "3000:3000"
    volumes:
      - ./gateway-config.yml:/config/gateway.yml:ro
      - ${HOME}/Documents:/workspace
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - POSTGRES_URL=${POSTGRES_URL}
    command: --config /config/gateway.yml
    restart: unless-stopped
    
networks:
  default:
    name: mcp-gateway-network
```

**Step 3: Run Gateway**

```bash
# Start gateway
docker compose -f gateway-compose.yml up -d

# Check it's running
docker compose -f gateway-compose.yml ps

# View logs
docker compose -f gateway-compose.yml logs -f

# Test endpoint
curl http://localhost:3000/health
```

### Connecting AI Clients to CLI-Managed Servers

**Option 1: Direct Connection (Single Server)**

Create Cursor IDE config (`~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` on macOS):

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "GITHUB_TOKEN=your_token",
        "mcp/github:latest"
      ]
    }
  }
}
```

**Option 2: Gateway Connection (Multiple Servers)**

```json
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

This connects to the Gateway you set up with Docker Compose, giving access to all configured servers.

### Monitoring and Debugging

**View Running Servers:**

```bash
# List MCP containers
docker ps --filter "name=mcp-"

# Show resource usage
docker stats $(docker ps --filter "name=mcp-" -q)

# Formatted output
docker ps --filter "name=mcp-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Check Logs:**

```bash
# Last 100 lines
docker logs --tail 100 mcp-github

# Last 10 minutes
docker logs --since 10m mcp-github

# Follow logs with timestamps
docker logs -f --timestamps mcp-github

# Search logs for errors
docker logs mcp-github 2>&1 | grep -i error
```

**Execute Commands in Running Container:**

```bash
# Open shell in container
docker exec -it mcp-github sh

# Run single command
docker exec mcp-github ps aux

# Check environment variables
docker exec mcp-github env

# Test network connectivity
docker exec mcp-github ping -c 3 api.github.com
```

**Inspect Container Configuration:**

```bash
# Full inspection
docker inspect mcp-github

# Specific information
docker inspect mcp-github --format='{{.Config.Env}}'
docker inspect mcp-github --format='{{.NetworkSettings.IPAddress}}'
docker inspect mcp-github --format='{{.State.Status}}'
```

### Updating Servers

```bash
# Pull latest version
docker pull mcp/github:latest

# Stop old container
docker stop mcp-github

# Remove old container
docker rm mcp-github

# Start new container with same config
docker run -d \
  --name mcp-github \
  -e GITHUB_TOKEN=your_token \
  mcp/github:latest

# Or use docker-compose
docker compose -f mcp-servers-compose.yml pull
docker compose -f mcp-servers-compose.yml up -d
```

### Cleanup and Maintenance

```bash
# Stop all MCP servers
docker stop $(docker ps -q --filter "name=mcp-")

# Remove all stopped MCP containers
docker rm $(docker ps -aq --filter "name=mcp-")

# Remove unused MCP images
docker images "mcp/*" -q | xargs docker rmi

# Clean up everything (use with caution)
docker system prune -a

# Remove only MCP-related items
docker ps -a --filter "name=mcp-" -q | xargs docker rm -f
docker images "mcp/*" -q | xargs docker rmi -f
```

### Best Practices for CLI Usage

**1. Use Docker Compose for Multiple Servers**

Instead of managing multiple `docker run` commands, use docker-compose.yml:
- Easier to manage
- Configuration in one place
- Simple start/stop all servers
- Automatic network creation

**2. Use Environment Files for Secrets**

Never hardcode secrets in compose files:

```yaml
# ❌ Bad
environment:
  - GITHUB_TOKEN=ghp_abc123

# ✅ Good
environment:
  - GITHUB_TOKEN=${GITHUB_TOKEN}
```

Then use `.env` file or:
```bash
export GITHUB_TOKEN=ghp_abc123
docker compose up -d
```

**3. Pin Image Versions in Production**

```yaml
# ❌ Development: latest
image: mcp/github:latest

# ✅ Production: pinned version
image: mcp/github:1.2.0
```

**4. Use Named Volumes for Data**

```yaml
services:
  sqlite:
    image: mcp/sqlite:latest
    volumes:
      - sqlite-data:/data  # Named volume, survives container removal

volumes:
  sqlite-data:
    driver: local
```

**5. Set Resource Limits**

```yaml
services:
  github:
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

**6. Use Health Checks**

```yaml
services:
  github:
    image: mcp/github:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Automation and Scripting

**Create a management script (`manage-mcp.sh`):**

```bash
#!/bin/bash

COMPOSE_FILE="mcp-servers-compose.yml"

case "$1" in
  start)
    echo "Starting MCP servers..."
    docker compose -f $COMPOSE_FILE up -d
    ;;
  stop)
    echo "Stopping MCP servers..."
    docker compose -f $COMPOSE_FILE stop
    ;;
  restart)
    echo "Restarting MCP servers..."
    docker compose -f $COMPOSE_FILE restart
    ;;
  status)
    echo "MCP Server Status:"
    docker compose -f $COMPOSE_FILE ps
    ;;
  logs)
    docker compose -f $COMPOSE_FILE logs -f ${2:-}
    ;;
  update)
    echo "Updating MCP servers..."
    docker compose -f $COMPOSE_FILE pull
    docker compose -f $COMPOSE_FILE up -d
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs|update} [service]"
    exit 1
    ;;
esac
```

**Make executable and use:**

```bash
chmod +x manage-mcp.sh

./manage-mcp.sh start
./manage-mcp.sh status
./manage-mcp.sh logs github
./manage-mcp.sh update
```

### Comparison: CLI vs Desktop Toolkit

| Task | Docker Desktop Toolkit | Docker CLI |
|------|----------------------|------------|
| **Discover Servers** | Visual catalog browser | `docker search mcp/` or hub.docker.com |
| **Install Server** | Click "Install" button | `docker pull mcp/server:latest` |
| **Configure Server** | GUI forms for env vars | Create .env file or pass -e flags |
| **Start Server** | Toggle "Enabled" switch | `docker run` or `docker compose up` |
| **View Logs** | Click "View Logs" | `docker logs container-name` |
| **Monitor Resources** | Visual dashboard | `docker stats` command |
| **Update Server** | Click "Update" | `docker pull` + restart container |
| **Multiple Servers** | Managed automatically | docker-compose.yml file |
| **Gateway Setup** | Built-in, automatic | Manual docker-compose setup |
| **Client Config** | Auto-generated | Manual JSON editing |

**Choose CLI when:**
- Working on servers/VMs without GUI
- Automating with scripts
- Managing production deployments
- Need full control and customization
- Prefer terminal workflows

**Choose Desktop when:**
- Learning and exploring
- Want visual management
- Need quick setup
- Prefer GUI over commands
- Working on local development machine

---

## Docker MCP Gateway

The Docker MCP Gateway is an open-source orchestration layer for MCP servers. It's built into the Toolkit but also available as a standalone component.

### What is the Gateway?

The Gateway acts as a **centralized proxy** between AI clients and MCP servers:

```
Without Gateway:                With Gateway:

AI Client                       AI Client
├── Connect to Server 1             │ Single connection
├── Connect to Server 2             ↓
├── Connect to Server 3         Gateway
└── Connect to Server N         ├── Route to Server 1
                                ├── Route to Server 2
Multiple connections            ├── Route to Server 3
Different configs               └── Route to Server N
Hard to manage
                                Single config
                                Easy management
```

### Architecture

```
┌──────────────────────────────────────────────┐
│  AI Clients                                   │
│  (Claude, Cursor, Custom Apps)                │
└───────────────────┬──────────────────────────┘
                    │ Single endpoint
                    │ http://localhost:3000/mcp
                    │
┌───────────────────▼──────────────────────────┐
│            Docker MCP Gateway                 │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │  Configuration Management                │ │
│  │  • Load server configs                   │ │
│  │  • Manage secrets                        │ │
│  │  • Handle updates                        │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │  Routing & Orchestration                 │ │
│  │  • Discover available tools              │ │
│  │  • Route tool calls to servers           │ │
│  │  • Aggregate responses                   │ │
│  │  • Load balance requests                 │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │  Security & Access Control               │ │
│  │  • Authenticate clients                  │ │
│  │  • Authorize tool access                 │ │
│  │  • Rate limiting                         │ │
│  │  • Audit logging                         │ │
│  └─────────────────────────────────────────┘ │
└──────┬──────────┬──────────┬─────────────────┘
       │          │          │
       ▼          ▼          ▼
  MCP Server  MCP Server  MCP Server
       1          2          N
```

### Gateway Benefits

**1. Simplified Client Configuration**

**Without Gateway:**
```json
// Client must configure each server individually
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "mcp/github"],
      "env": {"GITHUB_TOKEN": "..."}
    },
    "postgres": {
      "command": "docker",
      "args": ["run", "mcp/postgres"],
      "env": {"DB_URL": "..."}
    },
    "filesystem": {
      "command": "docker",
      "args": ["run", "mcp/filesystem"],
      "env": {"ROOT_PATH": "..."}
    }
  }
}
```

**With Gateway:**
```json
// Client connects to single endpoint
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

Gateway handles all server connections internally.

**2. Centralized Security**

```yaml
# gateway-config.yml
security:
  authentication:
    enabled: true
    method: token
    tokens:
      - client: claude_desktop
        token: "secret-token-1"
      - client: cursor
        token: "secret-token-2"
  
  authorization:
    github_tools:
      allowed_clients: [claude_desktop, cursor]
    postgres_tools:
      allowed_clients: [claude_desktop]
    
  rate_limiting:
    requests_per_minute: 60
    requests_per_hour: 1000
```

**3. Unified Observability**

```
Gateway Dashboard:
├── Request Metrics
│   ├── Total requests: 1,245
│   ├── Successful: 1,180
│   ├── Failed: 65
│   └── Average latency: 245ms
├── Server Health
│   ├── mcp/github: ✓ Healthy
│   ├── mcp/postgres: ✓ Healthy
│   └── mcp/filesystem: ⚠ Degraded
└── Recent Activity
    ├── 10:45:23 - github_search_code (Claude)
    ├── 10:45:20 - postgres_query (Cursor)
    └── 10:45:18 - fs_read_file (Claude)
```

### Setting Up Gateway (Standalone)

**Installation:**

```bash
# Pull Gateway image
docker pull docker/mcp-gateway:latest

# Create configuration
mkdir -p ~/mcp-gateway/config
```

**Configuration File (`config/gateway.yml`):**

```yaml
# Server definitions
servers:
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
  
  filesystem:
    image: mcp/filesystem:latest
    volumes:
      - ${HOME}/Documents:/workspace
    enabled: true

# Gateway settings
gateway:
  port: 3000
  transport: http-sse
  
  security:
    auth_required: false
    
  logging:
    level: info
    format: json
```

**Run Gateway:**

```bash
# Start Gateway
docker run -d \
  --name mcp-gateway \
  -p 3000:3000 \
  -v ~/mcp-gateway/config:/config \
  -e GITHUB_TOKEN=your_token \
  -e POSTGRES_URL=postgresql://... \
  docker/mcp-gateway:latest \
  --config /config/gateway.yml

# Check status
docker logs mcp-gateway

# Test endpoint
curl http://localhost:3000/health
```

**Client Configuration:**

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

Now Cursor IDE connects to Gateway, which provides access to all configured servers.

### Gateway Use Cases

**Development Teams:**
- Centralized server management
- Shared configuration
- Team-wide server availability

**Production Deployments:**
- Single point of control
- Simplified monitoring
- Easier updates and rollbacks

**Enterprise Environments:**
- Fine-grained access control
- Compliance and audit logging
- Policy enforcement

**Multi-Tenant Systems:**
- Isolate clients from each other
- Per-client resource limits
- Usage tracking and billing

---

## Publishing to Docker Hub

You can publish your custom MCP servers to Docker Hub for distribution.

### Building MCP Server Images

**Project Structure:**
```
my-mcp-server/
├── Dockerfile
├── requirements.txt
├── server.py
├── README.md
└── .dockerignore
```

**Dockerfile Example:**

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app
USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import sys; sys.exit(0)"

# Run server
CMD ["python", "server.py"]
```

**Build and Tag:**

```bash
# Build image
docker build -t myusername/my-mcp-server:1.0.0 .

# Tag as latest
docker tag myusername/my-mcp-server:1.0.0 \
           myusername/my-mcp-server:latest

# Test locally
docker run --rm myusername/my-mcp-server:latest
```

### Publishing to Docker Hub

**Step 1: Create Docker Hub Account**
- Visit: [hub.docker.com](https://hub.docker.com)
- Sign up or log in

**Step 2: Login from CLI**

```bash
docker login
# Enter username and password
```

**Step 3: Push Image**

```bash
# Push versioned tag
docker push myusername/my-mcp-server:1.0.0

# Push latest tag
docker push myusername/my-mcp-server:latest
```

**Step 4: Document Your Server**

Create detailed Docker Hub repository documentation:

```markdown
# My MCP Server

Description of what your server does.

## Tools Provided

- `tool_name_1` - Description
- `tool_name_2` - Description

## Configuration

### Required Environment Variables

- `API_KEY` - Your API key
- `API_URL` - API endpoint URL

### Optional Environment Variables

- `LOG_LEVEL` - Logging level (default: info)

## Usage

### With Docker CLI:

\`\`\`bash
docker run -d \
  -e API_KEY=your_key \
  myusername/my-mcp-server:latest
\`\`\`

### With Docker Compose:

\`\`\`yaml
services:
  mcp-server:
    image: myusername/my-mcp-server:latest
    environment:
      API_KEY: ${API_KEY}
\`\`\`

## Testing

\`\`\`bash
# Using MCP Inspector
npx @modelcontextprotocol/inspector \
  docker run --rm myusername/my-mcp-server:latest
\`\`\`
```

### Contributing to Docker MCP Catalog

To have your server included in the official Docker MCP Catalog:

**Step 1: Prepare Your Server**

Requirements:
- Follows MCP specification
- Dockerized with proper Dockerfile
- Comprehensive documentation
- Tests included
- Security best practices followed
- License specified (prefer MIT or Apache 2.0)

**Step 2: Submit to MCP Registry**

1. Fork repository: [github.com/docker/mcp-registry](https://github.com/docker/mcp-registry)

2. Create server definition file:

```yaml
# registry/servers/my-server.yml
name: myserver
title: My MCP Server
description: >
  Comprehensive description of what your server does
  and why it's useful.

version: 1.0.0
author: Your Name
homepage: https://github.com/yourusername/my-mcp-server
license: MIT

docker_image: yourusername/my-mcp-server:1.0.0

category: development  # or: databases, cloud, monitoring, business

tools:
  - name: example_tool
    description: What this tool does
    
environment_variables:
  required:
    - name: API_KEY
      description: API key for service
  optional:
    - name: LOG_LEVEL
      description: Logging verbosity

security:
  filesystem_access: read-only
  network_access: api.example.com
  
resource_limits:
  cpu: 1
  memory: 2GB
```

3. Submit pull request to `docker/mcp-registry`

**Step 3: Review Process**

Docker team reviews:
- Code quality and security
- Documentation completeness
- Functionality testing
- Compliance with standards

**Step 4: Publication**

Once approved:
- Server appears in Docker MCP Catalog
- Available in Docker Desktop within 24 hours
- Listed on Docker Hub under `mcp/` namespace (if accepted as official)
- Accessible to all Docker Desktop users

---

## Best Practices

### 1. Choosing Between Catalog and Custom

**Use Catalog Servers When:**
- Standard integration exists (GitHub, databases, etc.)
- You want immediate availability
- Security and maintenance are important
- You don't need customization

**Build Custom Servers When:**
- Unique business logic required
- Internal/proprietary integrations
- Specific customization needed
- Learning MCP fundamentals

**Hybrid Approach:**
```
Project Setup:
├── Catalog Servers (80%)
│   ├── mcp/github (version control)
│   ├── mcp/postgres (database)
│   └── mcp/slack (notifications)
└── Custom Servers (20%)
    ├── internal-erp-server (proprietary)
    └── custom-workflow-server (specific logic)
```

### 2. Server Organization

**Development:**
```yaml
# docker-compose.yml for development
services:
  # Catalog servers
  github:
    image: mcp/github:latest
    environment:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
  
  # Custom server (local development)
  custom:
    build: ./custom-server
    volumes:
      - ./custom-server:/app
    command: python -m debugpy --listen 0.0.0.0:5678 server.py
```

**Production:**
```yaml
# Production deployment
services:
  gateway:
    image: docker/mcp-gateway:latest
    volumes:
      - ./config/gateway.yml:/config/gateway.yml
    ports:
      - "3000:3000"
  
  github:
    image: mcp/github:1.2.0  # Pinned version
    environment:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
  
  custom:
    image: mycompany/custom-server:2.1.0  # Pinned version
    environment:
      API_KEY: ${API_KEY}
```

### 3. Security Considerations

**Secret Management:**

```yaml
# Don't hardcode secrets
services:
  server:
    environment:
      API_KEY: my-secret-key  # BAD!

# Use environment variables
services:
  server:
    environment:
      API_KEY: ${API_KEY}  # GOOD - from .env file

# Or use Docker secrets
secrets:
  api_key:
    file: ./secrets/api_key.txt

services:
  server:
    secrets:
      - api_key  # BEST - encrypted, managed
```

**Resource Limits:**

```yaml
services:
  untrusted-server:
    image: third-party/server
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

**Network Isolation:**

```yaml
networks:
  mcp-internal:
    internal: true  # No external access
  
  mcp-external:
    # Can access internet

services:
  database-server:
    networks:
      - mcp-internal  # Isolated
  
  api-server:
    networks:
      - mcp-internal
      - mcp-external  # Can call external APIs
```

### 4. Monitoring and Logging

**Structured Logging:**

```python
# In your MCP server
import logging
import json

logger = logging.getLogger(__name__)

def log_tool_call(tool_name: str, args: dict, user: str):
    logger.info(json.dumps({
        "event": "tool_call",
        "tool": tool_name,
        "args": args,
        "user": user,
        "timestamp": datetime.now().isoformat()
    }))
```

**Docker Logging Driver:**

```yaml
services:
  mcp-server:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 5. Testing Containerized Servers

**Unit Tests:**

```bash
# Test server in container
docker run --rm \
  -e API_KEY=test_key \
  myserver:latest \
  python -m pytest tests/
```

**Integration Tests:**

```bash
# Use MCP Inspector
npx @modelcontextprotocol/inspector \
  docker run --rm myserver:latest

# Automated testing
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## Exercises

See the [exercises](./exercises/) directory for hands-on practice:

- **[Tutorial 1: Using Catalog Servers](./exercises/tutorial-1-catalog-usage.md)** - Browse and use pre-built servers
- **[Tutorial 2: Docker MCP Toolkit](./exercises/tutorial-2-toolkit-setup.md)** - Set up and manage servers with GUI
- **[Tutorial 3: Gateway Configuration](./exercises/tutorial-3-gateway-setup.md)** - Deploy standalone Gateway
- **[Challenge 1: Multi-Server Setup](./exercises/challenge-1-multi-server.md)** - Configure complex multi-server environment
- **[Challenge 2: Publishing Your Server](./exercises/challenge-2-publishing.md)** - Build and publish your own MCP server

---

## Next Steps

### Continue Learning

1. **[Module 04: Basic MCP Server](../04-basic-mcp-server/)** - Build custom servers from scratch
2. **[Module 05: Advanced Features](../05-advanced-features/)** - Streaming, resources, and prompts
3. **[Module 06: Integration Patterns](../06-integration-patterns/)** - Real-world integrations

### Practice Projects

**Beginner:**
- Use 3 catalog servers with Cursor IDE
- Set up Gateway for local development
- Create documentation for your server setup

**Intermediate:**
- Build and publish your first custom MCP server
- Integrate catalog and custom servers via Gateway
- Implement monitoring and logging

**Advanced:**
- Contribute a server to Docker MCP Catalog
- Set up multi-environment deployment (dev, staging, prod)
- Implement advanced security with Gateway

---

## Additional Resources

**Official Documentation:**
- [Docker MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
- [Docker MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)
- [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
- [Docker Hub MCP](https://docs.docker.com/ai/mcp-catalog-and-toolkit/hub-mcp/)

**Repositories:**
- [MCP Registry](https://github.com/docker/mcp-registry) - Submit your servers
- [Docker Hub MCP](https://hub.docker.com/u/mcp) - Browse official servers

**Community:**
- [E2B Sandboxes + MCP](https://e2b.dev/docs/mcp) - MCP Catalog integration
- [Docker Community Forums](https://forums.docker.com/)

---

**Time to Complete**: 2-3 hours (tutorials + exercises)

**Prerequisites**: [Module 02: Environment Setup](../02-environment-setup/)

**Next Module**: [04-basic-mcp-server](../04-basic-mcp-server/)

