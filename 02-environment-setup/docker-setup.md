# Docker Setup Guide

This guide provides comprehensive instructions for setting up Docker for MCP development, covering both Docker CLI (command-line only) and Docker Desktop (with GUI).

## Table of Contents

1. [Overview](#overview)
2. [Which Docker Option Should You Choose?](#which-docker-option-should-you-choose)
3. [Docker CLI Installation](#docker-cli-installation)
4. [Docker Desktop Installation](#docker-desktop-installation)
5. [Verifying Installation](#verifying-installation)
6. [Using Docker for MCP Development](#using-docker-for-mcp-development)
7. [Docker Compose Setup](#docker-compose-setup)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Docker?

Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, portable, and consistent across different environments.

**Benefits for MCP Development:**

- **Consistency**: Same environment on all machines
- **Isolation**: Doesn't interfere with your system Python
- **Portability**: Easy to share your setup
- **Production-like**: Similar to how you'd deploy in production

### Docker vs Virtual Machines

| Aspect | Docker Container | Virtual Machine |
|--------|------------------|-----------------|
| **Size** | Megabytes | Gigabytes |
| **Startup** | Seconds | Minutes |
| **Performance** | Near-native | Slower |
| **Isolation** | Process-level | Full OS |
| **Use Case** | Apps & services | Full systems |

---

## Which Docker Option Should You Choose?

### Docker CLI (Command-Line)

**Best for:**
- Developers comfortable with terminal
- Servers and CI/CD environments
- Lightweight installations
- Scriptable workflows

**Pros:**
- Lighter resource usage
- No GUI overhead
- Faster startup
- Open source (Apache 2.0)

**Cons:**
- No visual interface
- Harder for beginners
- Manual container management

**Licensing**: Free and open source

---

### Docker Desktop

**Best for:**
- Developers who prefer GUI
- Visual container management
- Integrated development experience
- Kubernetes development (advanced)

**Pros:**
- Visual interface
- Easy container management
- Resource limits in GUI
- Integrated Kubernetes

**Cons:**
- Higher resource usage
- Slower on some machines
- Licensing for commercial use

**Licensing**: 
- Free for personal use, education, small businesses
- Requires license for larger companies (check [Docker pricing](https://www.docker.com/pricing/))

---

## Docker CLI Installation

### macOS

#### Method 1: Homebrew

```bash
# Install Docker
brew install docker

# Install Docker Compose
brew install docker-compose

# Install colima (Docker runtime for macOS)
brew install colima

# Start colima
colima start

# Verify
docker --version
docker compose version
```

**What is Colima?**
- Container runtime for macOS
- Alternative to Docker Desktop
- Lightweight and free

#### Method 2: Docker Engine (via Docker Desktop CLI)

If you have Docker Desktop but want CLI-only:

```bash
# Docker Desktop includes CLI tools
# Just don't start the GUI
docker --version
```

### Linux

#### Ubuntu / Debian

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
sudo docker --version
```

**Add your user to docker group** (avoid using sudo):

```bash
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or use:
newgrp docker

# Verify you can run without sudo
docker run hello-world
```

#### Fedora

```bash
# Install prerequisites
sudo dnf -y install dnf-plugins-core

# Add Docker repository
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Verify
docker --version
```

#### Arch Linux

```bash
# Install Docker
sudo pacman -S docker docker-compose

# Start and enable Docker service
sudo systemctl start docker.service
sudo systemctl enable docker.service

# Add user to docker group
sudo usermod -aG docker $USER

# Verify
docker --version
```

### Windows

#### WSL2 (Recommended)

**Step 1: Enable WSL2**

Open PowerShell as Administrator:

```powershell
wsl --install
wsl --set-default-version 2
```

Restart your computer.

**Step 2: Install Ubuntu from Microsoft Store**

**Step 3: Install Docker in Ubuntu**

Open Ubuntu terminal and follow the Ubuntu instructions above.

**Step 4: Configure WSL integration**

Ensure Docker can access WSL:

```bash
# In Ubuntu
sudo service docker start
```

#### Native Windows (Without WSL)

**Not recommended for MCP development** - use WSL2 for better compatibility with Python tooling.

---

## Docker Desktop Installation

### macOS

**Step 1: Download**

Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) and download the appropriate version:
- **Apple Silicon** (M1, M2, M3): ARM64 version
- **Intel**: AMD64 version

**Step 2: Install**

1. Open the downloaded `.dmg` file
2. Drag Docker icon to Applications folder
3. Open Docker from Applications
4. Grant permissions when prompted
5. Wait for Docker to start (whale icon in menu bar)

**Step 3: Configure** (optional)

Click the Docker icon in menu bar → Preferences:

- **Resources**: Adjust CPU, Memory, Disk
- **File Sharing**: Ensure your projects folder is shared
- **Docker Engine**: Use default settings

**Step 4: Verify**

```bash
docker --version
docker compose version
docker run hello-world
```

### Linux

**Step 1: Download**

Visit [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)

For Ubuntu/Debian:

```bash
# Download DEB package
curl -O https://desktop.docker.com/linux/main/amd64/docker-desktop-<version>-amd64.deb

# Install
sudo apt install ./docker-desktop-<version>-amd64.deb
```

For Fedora:

```bash
# Download RPM package
curl -O https://desktop.docker.com/linux/main/amd64/docker-desktop-<version>-x86_64.rpm

# Install
sudo dnf install ./docker-desktop-<version>-x86_64.rpm
```

**Step 2: Start Docker Desktop**

```bash
systemctl --user start docker-desktop
```

Or launch from applications menu.

**Step 3: Verify**

```bash
docker --version
docker run hello-world
```

### Windows

**Step 1: Prerequisites**

- Windows 10/11 64-bit
- WSL2 installed and enabled
- Virtualization enabled in BIOS

**Step 2: Download**

Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

**Step 3: Install**

1. Run the installer
2. Ensure "Use WSL 2 instead of Hyper-V" is checked
3. Follow the installation wizard
4. Restart when prompted

**Step 4: Configure WSL Integration**

Open Docker Desktop:
- Settings → Resources → WSL Integration
- Enable integration with your Ubuntu distribution

**Step 5: Verify**

In WSL Ubuntu terminal:

```bash
docker --version
docker compose version
docker run hello-world
```

---

## Verifying Installation

### Basic Verification

```bash
# Check Docker version
docker --version
# Should show: Docker version 24.x.x

# Check Docker Compose version
docker compose version
# Should show: Docker Compose version v2.x.x

# Check Docker is running
docker ps
# Should show: CONTAINER ID   IMAGE   ... (empty table is fine)
```

### Run Test Container

```bash
# Run hello-world image
docker run hello-world

# You should see:
# "Hello from Docker!"
# "This message shows that your installation appears to be working correctly."
```

### Run Interactive Container

```bash
# Run Ubuntu container interactively
docker run -it --rm ubuntu:22.04 bash

# Inside container:
cat /etc/os-release
# Should show Ubuntu 22.04 info

# Exit container
exit
```

### Test with Python

```bash
# Run Python container
docker run -it --rm python:3.11 python

# Inside Python:
>>> print("Hello from Docker!")
>>> exit()
```

---

## Using Docker for MCP Development

### The MCP Development Image

This repository includes a Dockerfile for MCP development.

**Location**: `docker/Dockerfile`

**What's included:**
- Python 3.11
- MCP Python SDK
- Development tools (pytest, black, mypy, ruff)
- Volume mounting for live code editing

### Building the Image

```bash
# Navigate to repository root
cd /path/to/mcp-learning

# Build the image
docker build -t mcp-learning:dev -f docker/Dockerfile .

# This will:
# 1. Download Python 3.11 base image
# 2. Install system dependencies
# 3. Install Python packages
# 4. Set up working directory
```

**Build time**: 2-5 minutes (first time), then cached.

### Running the Development Container

**Interactive shell:**

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  mcp-learning:dev \
  bash
```

**Breakdown:**
- `-it`: Interactive terminal
- `--rm`: Remove container when done
- `-v $(pwd):/workspace`: Mount current directory
- `-w /workspace`: Set working directory
- `bash`: Run bash shell

**Inside container:**

```bash
# Verify Python
python --version

# Verify MCP
python -c "import mcp; print(mcp.__version__)"

# Run tests
pytest

# Format code
black .

# Type check
mypy .
```

### Running MCP Servers in Docker

**Run a specific server:**

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  mcp-learning:dev \
  python 03-basic-mcp-server/examples/minimal_server.py
```

**With environment variables:**

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  -e DATABASE_URL=postgresql://localhost/mydb \
  mcp-learning:dev \
  python my_server.py
```

---

## Docker Compose Setup

Docker Compose simplifies multi-container setups.

### The Compose File

**Location**: `docker/docker-compose.yml`

**What it defines:**
- Development container
- Volume mounts
- Environment variables
- Network configuration

### Using Docker Compose

**Start services:**

```bash
# In repository root
cd /path/to/mcp-learning

# Start dev container
docker compose -f docker/docker-compose.yml run --rm dev bash
```

**Run commands:**

```bash
# Run tests
docker compose -f docker/docker-compose.yml run --rm dev pytest

# Format code
docker compose -f docker/docker-compose.yml run --rm dev black .

# Run a server
docker compose -f docker/docker-compose.yml run --rm dev python my_server.py
```

**Create alias for convenience:**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias mcp-docker="docker compose -f docker/docker-compose.yml run --rm dev"

# Then use:
mcp-docker bash
mcp-docker pytest
mcp-docker python my_server.py
```

### Advanced Docker Compose Usage

**Background services:**

```bash
# Start in background
docker compose -f docker/docker-compose.yml up -d

# View logs
docker compose -f docker/docker-compose.yml logs -f

# Stop services
docker compose -f docker/docker-compose.yml down
```

**Multiple services:**

If you have multiple MCP servers, add them to compose file:

```yaml
services:
  server1:
    build:
      context: .
      dockerfile: docker/Dockerfile
    volumes:
      - .:/workspace
    command: python server1.py
  
  server2:
    build:
      context: .
      dockerfile: docker/Dockerfile
    volumes:
      - .:/workspace
    command: python server2.py
```

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Cause**: Docker service not running

**Solution (Linux):**

```bash
sudo systemctl start docker
```

**Solution (macOS with colima):**

```bash
colima start
```

**Solution (Docker Desktop):**

Start Docker Desktop application

### Issue: "Permission denied" on Linux

**Cause**: User not in docker group

**Solution:**

```bash
sudo usermod -aG docker $USER
newgrp docker

# Or log out and back in
```

### Issue: Docker build fails with network error

**Cause**: Network connectivity or DNS issues

**Solutions:**

1. **Check internet connection**

2. **Use different DNS:**
   ```bash
   # Edit /etc/docker/daemon.json
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   
   # Restart Docker
   sudo systemctl restart docker
   ```

3. **Use proxy if behind firewall:**
   ```bash
   docker build --build-arg HTTP_PROXY=http://proxy.example.com:8080 .
   ```

### Issue: "No space left on device"

**Cause**: Docker images/containers filling disk

**Solution:**

```bash
# See disk usage
docker system df

# Clean up
docker system prune -a

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune
```

### Issue: Docker Desktop uses too much memory

**Solution:**

Docker Desktop → Preferences → Resources:
- Reduce Memory limit (default is high)
- Reduce CPU count if needed
- Reduce Disk size

### Issue: Slow performance on macOS

**Causes:**
- File sharing overhead
- Resource limits

**Solutions:**

1. **Use :delegated mount option:**
   ```bash
   docker run -v $(pwd):/workspace:delegated ...
   ```

2. **Increase resources:**
   Docker Desktop → Preferences → Resources → Increase CPU/Memory

3. **Use colima instead of Docker Desktop:**
   ```bash
   brew install colima
   colima start --cpu 4 --memory 8
   ```

### Issue: WSL2 integration not working

**Solution (Windows):**

1. Ensure WSL2 is default:
   ```powershell
   wsl --set-default-version 2
   ```

2. Docker Desktop → Settings → Resources → WSL Integration
   - Enable integration with Ubuntu

3. Restart Docker Desktop

### Issue: Image build is slow

**Cause**: Not using layer caching effectively

**Solutions:**

1. **Order Dockerfile for caching:**
   ```dockerfile
   # Install dependencies first (changes less often)
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   # Copy code last (changes often)
   COPY . .
   ```

2. **Use BuildKit:**
   ```bash
   DOCKER_BUILDKIT=1 docker build -t myimage .
   ```

3. **Use cache mount:**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.cache/pip \
       pip install -r requirements.txt
   ```

---

## Docker Best Practices

### 1. Use .dockerignore

Create `.dockerignore` in project root:

```
venv/
__pycache__/
*.pyc
.git/
.env
*.log
node_modules/
```

### 2. Keep Images Small

```dockerfile
# Use specific version tags
FROM python:3.11-slim

# Combine RUN commands
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# Clean up in same layer
RUN pip install package && rm -rf /root/.cache/pip
```

### 3. Don't Run as Root

```dockerfile
# Create user
RUN useradd -m -u 1000 mcpuser

# Switch to user
USER mcpuser

# Run command
CMD ["python", "server.py"]
```

### 4. Use Multi-Stage Builds

```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "server.py"]
```

### 5. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

---

## Quick Reference

### Common Commands

```bash
# Build image
docker build -t name:tag .

# Run container
docker run -it --rm name:tag

# List containers
docker ps        # Running
docker ps -a     # All

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# List images
docker images

# Remove image
docker rmi <image_id>

# Clean up everything
docker system prune -a

# View logs
docker logs <container_id>

# Execute command in running container
docker exec -it <container_id> bash

# Copy files
docker cp file.txt <container_id>:/path/
docker cp <container_id>:/path/file.txt .
```

### Docker Compose Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Run one-off command
docker compose run service command

# Rebuild images
docker compose build

# List services
docker compose ps
```

---

## Next Steps

1. **Verify your Docker setup**: Run the verification commands above
2. **Build the MCP image**: `docker build -t mcp-learning:dev -f docker/Dockerfile .`
3. **Complete exercises**: Return to [README.md](./README.md)
4. **Explore Docker Compose**: Try running services together
5. **Learn more**: Check [official Docker docs](https://docs.docker.com/)

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/) - Find pre-built images
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker for Development](https://docs.docker.com/develop/)

---

**You're now ready to use Docker for MCP development!**

