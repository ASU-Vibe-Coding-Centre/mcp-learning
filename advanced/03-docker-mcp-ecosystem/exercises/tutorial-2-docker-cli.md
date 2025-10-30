# Tutorial 2: Using MCP Servers with Docker CLI

Learn how to discover, install, and manage MCP servers using Docker CLI commands.

## Prerequisites

- Docker CLI installed and running
- Docker Compose installed
- Basic command-line familiarity
- Terminal access

## Verify Installation

```bash
# Check Docker is installed
docker --version

# Check Docker Compose
docker compose version

# Test Docker daemon is running
docker ps
```

Expected output:
```
Docker version 24.0.0 or higher
Docker Compose version v2.20.0 or higher
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```

---

## Part 1: Discovering MCP Servers

### 1.1 Search Docker Hub from CLI

```bash
# Search for all MCP servers
docker search mcp/

# Search for specific functionality
docker search mcp/github
docker search mcp/postgres
docker search mcp/filesystem
```

### 1.2 Browse Online Catalog

Visit [hub.docker.com/u/mcp](https://hub.docker.com/u/mcp) in your browser.

**Note down:**
- Available servers
- Required environment variables
- Documentation links

---

## Part 2: Installing and Running Individual Servers

### 2.1 Pull a Server Image

```bash
# Pull the filesystem server
docker pull mcp/filesystem:latest

# Verify it downloaded
docker images mcp/filesystem
```

**Expected output:**
```
REPOSITORY         TAG       IMAGE ID       CREATED       SIZE
mcp/filesystem     latest    abc123def456   2 days ago    120MB
```

### 2.2 Run Your First Server

```bash
# Create a test directory
mkdir -p ~/mcp-test-workspace
echo "Hello from MCP!" > ~/mcp-test-workspace/test.txt

# Run filesystem server
docker run -d \
  --name mcp-filesystem \
  -e ROOT_PATH=/workspace \
  -v ~/mcp-test-workspace:/workspace \
  mcp/filesystem:latest

# Check it's running
docker ps | grep mcp-filesystem
```

### 2.3 View Server Logs

```bash
# View all logs
docker logs mcp-filesystem

# Follow logs in real-time
docker logs -f mcp-filesystem
# Press Ctrl+C to stop following

# View last 20 lines
docker logs --tail 20 mcp-filesystem
```

**What to look for:**
- Server initialization messages
- "MCP Server Ready" or similar confirmation
- No error messages

### 2.4 Check Server Resource Usage

```bash
# View resource consumption
docker stats mcp-filesystem --no-stream

# View detailed information
docker inspect mcp-filesystem
```

### 2.5 Stop and Remove Server

```bash
# Stop the server
docker stop mcp-filesystem

# Verify it stopped
docker ps -a | grep mcp-filesystem

# Remove the container
docker rm mcp-filesystem

# Verify removal
docker ps -a | grep mcp-filesystem
# Should return nothing
```

---

## Part 3: Managing Multiple Servers with Docker Compose

### 3.1 Create Docker Compose Configuration

Create a file named `mcp-servers.yml`:

```yaml
version: '3.8'

services:
  # Filesystem access
  filesystem:
    image: mcp/filesystem:latest
    container_name: mcp-filesystem
    environment:
      - ROOT_PATH=/workspace
    volumes:
      - ~/mcp-test-workspace:/workspace:ro
    restart: unless-stopped
    
  # SQLite database
  sqlite:
    image: mcp/sqlite:latest
    container_name: mcp-sqlite
    environment:
      - DB_PATH=/data/test.db
    volumes:
      - ./sqlite-data:/data
    restart: unless-stopped

networks:
  default:
    name: mcp-network
```

### 3.2 Create Environment File

Create `.env` file for secrets (if needed):

```bash
# .env
LOG_LEVEL=info
```

### 3.3 Start All Servers

```bash
# Pull all images
docker compose -f mcp-servers.yml pull

# Start all services
docker compose -f mcp-servers.yml up -d

# Check status
docker compose -f mcp-servers.yml ps
```

**Expected output:**
```
NAME                IMAGE                  STATUS          PORTS
mcp-filesystem      mcp/filesystem:latest  Up 5 seconds
mcp-sqlite          mcp/sqlite:latest      Up 5 seconds
```

### 3.4 View Logs for All Services

```bash
# View all logs
docker compose -f mcp-servers.yml logs

# Follow logs in real-time
docker compose -f mcp-servers.yml logs -f

# View logs for specific service
docker compose -f mcp-servers.yml logs filesystem

# View last 10 lines for each service
docker compose -f mcp-servers.yml logs --tail 10
```

### 3.5 Manage Services

```bash
# Stop all services
docker compose -f mcp-servers.yml stop

# Start all services
docker compose -f mcp-servers.yml start

# Restart specific service
docker compose -f mcp-servers.yml restart sqlite

# Stop and remove all services
docker compose -f mcp-servers.yml down

# Stop and remove including volumes
docker compose -f mcp-servers.yml down -v
```

---

## Part 4: Working with Secrets and Environment Variables

### 4.1 Add Server Requiring Credentials

Update `mcp-servers.yml` to add GitHub server:

```yaml
services:
  # ... existing services ...
  
  github:
    image: mcp/github:latest
    container_name: mcp-github
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
```

### 4.2 Configure Secrets

Option 1: Using `.env` file (for development):

```bash
# Add to .env file
echo "GITHUB_TOKEN=your_github_token_here" >> .env
```

Option 2: Export environment variable:

```bash
export GITHUB_TOKEN=your_github_token_here
```

Option 3: Pass directly (not recommended for production):

```bash
docker compose -f mcp-servers.yml up -d \
  -e GITHUB_TOKEN=your_token
```

### 4.3 Verify Secret is Set

```bash
# Start the service
docker compose -f mcp-servers.yml up -d github

# Check environment variables (token will be visible)
docker exec mcp-github env | grep GITHUB_TOKEN
```

**Security Warning:** Secrets in environment variables are visible in `docker inspect`. For production, use Docker secrets or external secret managers.

---

## Part 5: Monitoring and Debugging

### 5.1 Monitor Resource Usage

```bash
# Monitor all MCP containers
docker stats $(docker ps -q --filter "name=mcp-")

# Monitor specific container
docker stats mcp-filesystem --no-stream
```

### 5.2 Execute Commands in Running Container

```bash
# Open interactive shell
docker exec -it mcp-filesystem sh

# Inside container:
ls -la /workspace
cat /workspace/test.txt
exit

# Run single command
docker exec mcp-filesystem ls -la /workspace
```

### 5.3 Troubleshooting Common Issues

**Issue: Container won't start**

```bash
# Check recent logs
docker logs --tail 50 mcp-filesystem

# Check container exit code
docker inspect mcp-filesystem --format='{{.State.ExitCode}}'

# Try running interactively
docker run --rm -it mcp/filesystem:latest sh
```

**Issue: Can't connect to server**

```bash
# Check container is running
docker ps | grep mcp-filesystem

# Check network settings
docker inspect mcp-filesystem --format='{{.NetworkSettings.Networks}}'

# Test network connectivity
docker exec mcp-filesystem ping -c 3 google.com
```

**Issue: Permission denied errors**

```bash
# Check volume mounts
docker inspect mcp-filesystem --format='{{.Mounts}}'

# Check file permissions on host
ls -la ~/mcp-test-workspace
```

---

## Part 6: Updating and Maintaining Servers

### 6.1 Update Server to Latest Version

```bash
# Pull latest image
docker pull mcp/filesystem:latest

# Using docker-compose (recommended)
docker compose -f mcp-servers.yml pull
docker compose -f mcp-servers.yml up -d
```

Docker Compose will automatically:
- Detect image updates
- Stop old container
- Start new container with same config

### 6.2 Cleanup Unused Resources

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup (use with caution)
docker system prune -a --volumes
```

### 6.3 Backup and Restore

**Backup server configuration:**

```bash
# Export docker-compose config
cp mcp-servers.yml mcp-servers.backup.yml

# Backup environment file
cp .env .env.backup

# Backup volumes
docker run --rm \
  -v mcp_sqlite-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/sqlite-backup.tar.gz /data
```

**Restore configuration:**

```bash
# Restore files
cp mcp-servers.backup.yml mcp-servers.yml
cp .env.backup .env

# Restore volume
docker run --rm \
  -v mcp_sqlite-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/sqlite-backup.tar.gz -C /
```

---

## Part 7: Creating a Management Script

### 7.1 Create Management Script

Create `manage-mcp.sh`:

```bash
#!/bin/bash

COMPOSE_FILE="mcp-servers.yml"

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
    echo ""
    echo "Resource Usage:"
    docker stats $(docker compose -f $COMPOSE_FILE ps -q) --no-stream
    ;;
  logs)
    if [ -z "$2" ]; then
      docker compose -f $COMPOSE_FILE logs -f
    else
      docker compose -f $COMPOSE_FILE logs -f $2
    fi
    ;;
  update)
    echo "Updating MCP servers..."
    docker compose -f $COMPOSE_FILE pull
    docker compose -f $COMPOSE_FILE up -d
    echo "Update complete!"
    ;;
  clean)
    echo "Cleaning up..."
    docker compose -f $COMPOSE_FILE down
    docker system prune -f
    echo "Cleanup complete!"
    ;;
  *)
    echo "MCP Server Manager"
    echo ""
    echo "Usage: $0 {command} [service]"
    echo ""
    echo "Commands:"
    echo "  start    - Start all MCP servers"
    echo "  stop     - Stop all MCP servers"
    echo "  restart  - Restart all MCP servers"
    echo "  status   - Show server status and resource usage"
    echo "  logs     - View logs (optionally for specific service)"
    echo "  update   - Pull latest images and restart servers"
    echo "  clean    - Stop servers and clean up resources"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs filesystem"
    echo "  $0 status"
    exit 1
    ;;
esac
```

### 7.2 Make Script Executable

```bash
chmod +x manage-mcp.sh
```

### 7.3 Use Management Script

```bash
# Start all servers
./manage-mcp.sh start

# Check status
./manage-mcp.sh status

# View logs for specific service
./manage-mcp.sh logs filesystem

# Update all servers
./manage-mcp.sh update

# Stop all servers
./manage-mcp.sh stop
```

---

## Part 8: Verification

### 8.1 Verify Everything Works

```bash
# Start all servers
./manage-mcp.sh start

# Check all are running
docker ps --filter "name=mcp-" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

# Test filesystem server can access files
docker exec mcp-filesystem ls -la /workspace

# Check logs are clean (no errors)
./manage-mcp.sh logs | grep -i error
```

### 8.2 Performance Check

```bash
# Check resource usage
docker stats $(docker ps -q --filter "name=mcp-") --no-stream

# Check disk usage
docker system df
```

---

## Challenge Exercises

### Challenge 1: Add Monitoring

Add a monitoring container that tracks MCP server health.

Hint: Look into Prometheus or similar monitoring tools.

### Challenge 2: Automated Backups

Create a script that automatically backs up all MCP server data and configurations daily.

### Challenge 3: High Availability

Modify the docker-compose configuration to include:
- Health checks for each service
- Automatic restart on failure
- Resource limits

Example:
```yaml
services:
  filesystem:
    image: mcp/filesystem:latest
    healthcheck:
      test: ["CMD", "test", "-f", "/tmp/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
```

---

## What You've Learned

- How to search for and pull MCP server images
- Running individual servers with `docker run`
- Managing multiple servers with Docker Compose
- Working with environment variables and secrets
- Monitoring and debugging running servers
- Updating and maintaining servers
- Creating automation scripts for management
- Best practices for CLI-based workflows

---

## Next Steps

- **Tutorial 3**: Set up MCP Gateway with Docker CLI
- **Tutorial 4**: Build and publish your own MCP server
- **Module 04**: Learn to build custom MCP servers from scratch

For troubleshooting, see [Module 08: Debugging & Troubleshooting](../../08-debugging-troubleshooting/)

---

## Quick Reference

```bash
# Essential Commands
docker ps --filter "name=mcp-"                    # List MCP containers
docker logs -f mcp-filesystem                     # View logs
docker stats mcp-filesystem --no-stream           # Resource usage
docker compose -f mcp-servers.yml up -d           # Start all servers
docker compose -f mcp-servers.yml logs -f         # Follow all logs
docker compose -f mcp-servers.yml down            # Stop and remove

# Troubleshooting
docker inspect mcp-filesystem                     # Detailed info
docker exec -it mcp-filesystem sh                 # Interactive shell
docker system df                                  # Disk usage
docker system prune -a                            # Cleanup (careful!)
```

