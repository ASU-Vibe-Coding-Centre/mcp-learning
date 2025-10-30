# Docker Setup Guide

This guide covers setting up Docker for the MCP Learning Repository using either **command-line Docker** or **Docker Desktop**.

---

## Table of Contents

- [Option 1: Command-Line Docker (Recommended for Developers)](#option-1-command-line-docker-recommended-for-developers)
- [Option 2: Docker Desktop (GUI Option)](#option-2-docker-desktop-gui-option)
- [Using Docker with MCP Learning](#using-docker-with-mcp-learning)
- [Troubleshooting](#troubleshooting)

---

## Option 1: Command-Line Docker (Recommended for Developers)

Command-line Docker provides a lightweight Docker experience without the GUI overhead of Docker Desktop.

### macOS Installation

1. **Install Docker via Homebrew:**
   ```bash
   brew install docker docker-compose
   ```

2. **Install Docker Machine (for VM management):**
   ```bash
   brew install docker-machine
   ```

3. **Install a VM driver (recommended: VirtualBox or HyperKit):**
   ```bash
   # Option A: VirtualBox (more stable, larger footprint)
   brew install --cask virtualbox
   
   # Option B: HyperKit (native macOS, lighter)
   brew install hyperkit
   ```

4. **Create a Docker Machine:**
   ```bash
   docker-machine create --driver virtualbox default
   # OR for HyperKit:
   # docker-machine create --driver hyperkit default
   ```

5. **Configure your shell to use the Docker Machine:**
   ```bash
   eval $(docker-machine env default)
   ```
   
   Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent:
   ```bash
   echo 'eval $(docker-machine env default)' >> ~/.zshrc
   ```

6. **Verify installation:**
   ```bash
   docker --version
   docker-compose --version
   docker ps
   ```

### Linux Installation

1. **Install Docker Engine:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   
   # Fedora/RHEL
   sudo dnf install -y docker docker-compose
   ```

2. **Start Docker service:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Add your user to docker group (avoid using sudo):**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

4. **Verify installation:**
   ```bash
   docker --version
   docker-compose --version
   docker ps
   ```

### Windows Installation (Command-Line)

For Windows, we recommend using WSL2 (Windows Subsystem for Linux):

1. **Enable WSL2:**
   ```powershell
   wsl --install
   ```

2. **Install Docker in WSL2:**
   Follow the Linux installation steps above within your WSL2 terminal.

3. **Verify installation:**
   ```bash
   docker --version
   docker-compose --version
   ```

---

## Option 2: Docker Desktop (GUI Option)

Docker Desktop provides a graphical interface and is easier to install but has a larger footprint.

### macOS Installation

1. **Download Docker Desktop:**
   - Visit [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download the macOS version (Intel or Apple Silicon)

2. **Install Docker Desktop:**
   - Open the `.dmg` file
   - Drag Docker to Applications folder
   - Launch Docker from Applications

3. **Wait for Docker to start:**
   - Look for the Docker whale icon in the menu bar
   - Click it and ensure "Docker Desktop is running"

4. **Verify installation:**
   ```bash
   docker --version
   docker-compose --version
   docker ps
   ```

### Linux Installation

1. **Download Docker Desktop for Linux:**
   - Visit [https://docs.docker.com/desktop/install/linux-install/](https://docs.docker.com/desktop/install/linux-install/)
   - Follow distribution-specific instructions

2. **Install the package:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ./docker-desktop-<version>-<arch>.deb
   ```

3. **Launch Docker Desktop:**
   ```bash
   systemctl --user start docker-desktop
   ```

### Windows Installation

1. **Ensure WSL2 is enabled** (Docker Desktop requires it):
   ```powershell
   wsl --install
   ```

2. **Download Docker Desktop for Windows:**
   - Visit [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download the Windows version

3. **Run the installer:**
   - Follow the installation wizard
   - Ensure "Use WSL 2 instead of Hyper-V" is selected

4. **Restart your computer**

5. **Launch Docker Desktop** and wait for it to start

6. **Verify installation:**
   ```powershell
   docker --version
   docker-compose --version
   ```

---

## Using Docker with MCP Learning

Once Docker is installed, you can use the MCP Learning environment:

### Build the Docker Image

From the repository root:

```bash
docker build -t mcp-learning:dev -f docker/Dockerfile .
```

### Verify Docker Compose Configuration

```bash
docker-compose -f docker/docker-compose.yml config
```

### Start the Development Container

```bash
# Interactive shell for development
docker-compose -f docker/docker-compose.yml run --rm dev

# Or using shorthand (if in docker/ directory)
cd docker
docker-compose run --rm dev
```

### Run Tests

```bash
docker-compose -f docker/docker-compose.yml run --rm test
```

### Run a Specific Example Server

```bash
docker-compose -f docker/docker-compose.yml run --rm dev python 03-basic-mcp-server/examples/minimal_server.py
```

### Check Python Version

```bash
docker-compose -f docker/docker-compose.yml run --rm dev python --version
```

### Stop All Containers

```bash
docker-compose -f docker/docker-compose.yml down
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Cannot connect to the Docker daemon"

**Symptoms:** `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

**Solutions:**

- **macOS (Command-Line):**
  ```bash
  # Start Docker Machine
  docker-machine start default
  eval $(docker-machine env default)
  ```

- **macOS (Docker Desktop):**
  - Ensure Docker Desktop is running (check menu bar for whale icon)
  - Try restarting Docker Desktop

- **Linux:**
  ```bash
  # Start Docker service
  sudo systemctl start docker
  
  # Check Docker service status
  sudo systemctl status docker
  ```

- **Windows:**
  - Ensure Docker Desktop is running
  - Ensure WSL2 is properly configured

#### 2. "Permission denied while trying to connect to the Docker daemon socket"

**Symptoms:** Permission errors when running Docker commands

**Solution (Linux):**
```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

#### 3. Docker Build Fails with "failed to compute cache key"

**Symptoms:** Build errors related to copying files

**Solutions:**
```bash
# Ensure you're building from the repository root
cd /path/to/mcp-server
docker build -t mcp-learning:dev -f docker/Dockerfile .

# Clear Docker build cache
docker builder prune -a
```

#### 4. Slow Docker Performance on macOS

**Symptoms:** Docker containers running slowly, especially file I/O

**Solutions:**

- **Docker Desktop:** 
  - Increase resources: Docker Desktop → Settings → Resources
  - Recommended: 4 CPUs, 8GB RAM
  
- **Command-Line Docker:**
  - Recreate Docker Machine with more resources:
    ```bash
    docker-machine rm default
    docker-machine create --driver virtualbox --virtualbox-cpu-count=4 --virtualbox-memory=8192 default
    ```

#### 5. Port Already in Use

**Symptoms:** `Error starting userland proxy: listen tcp 0.0.0.0:3000: bind: address already in use`

**Solutions:**
```bash
# Find what's using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port in docker-compose.yml
# Change "3000:3000" to "3001:3000"
```

#### 6. Volume Mount Issues on Windows

**Symptoms:** Files not syncing between host and container

**Solutions:**
```bash
# Ensure your project is in a WSL2 filesystem, not Windows filesystem
# Move project to WSL2 home directory
mv /mnt/c/Users/YourName/project ~/project

# Or enable WSL2 integration in Docker Desktop:
# Docker Desktop → Settings → Resources → WSL Integration
```

#### 7. "docker-compose: command not found"

**Symptoms:** `docker-compose` command doesn't work

**Solutions:**

- **If using Docker Desktop:** Ensure Docker Desktop is running (it includes docker-compose)

- **If using command-line Docker:**
  ```bash
  # macOS
  brew install docker-compose
  
  # Linux
  sudo apt-get install docker-compose
  
  # Or install via pip
  pip install docker-compose
  ```

#### 8. Image Build Takes Forever

**Symptoms:** Docker build hangs at "Downloading..." or takes very long

**Solutions:**
```bash
# Check internet connection
curl -I https://pypi.org

# Use a different Python base image mirror (edit Dockerfile)
# FROM python:3.11-slim
# to
# FROM --platform=linux/amd64 python:3.11-slim

# Clear and rebuild without cache
docker builder prune -a
docker build --no-cache -t mcp-learning:dev -f docker/Dockerfile .
```

---

## Platform-Specific Notes

### macOS (Apple Silicon)

If you're on an M1/M2/M3 Mac:

```bash
# Build for ARM architecture (faster)
docker build --platform linux/arm64 -t mcp-learning:dev -f docker/Dockerfile .

# Or for compatibility with other platforms
docker build --platform linux/amd64 -t mcp-learning:dev -f docker/Dockerfile .
```

### Windows WSL2

- Always work inside WSL2 filesystem (`/home/username/`) for best performance
- Avoid working in `/mnt/c/` (Windows filesystem) as it's significantly slower
- Use Windows Terminal for better experience

### Linux

- If using SELinux (Fedora/RHEL), you may need to adjust volume mount permissions:
  ```bash
  # Add :z flag to volume mounts in docker-compose.yml
  volumes:
    - ..:/app:z
  ```

---

## Next Steps

Once Docker is set up and working:

1. ✅ Verify installation: `docker --version` and `docker-compose --version`
2. ✅ Build the image: `docker build -t mcp-learning:dev -f docker/Dockerfile .`
3. ✅ Test the container: `docker-compose -f docker/docker-compose.yml run --rm dev python --version`
4. 🚀 Continue to [Quick Start Guide](../QUICK_START.md) to build your first MCP server!

---

**Need more help?** Check the [main README](../README.md) or open an issue on GitHub.

