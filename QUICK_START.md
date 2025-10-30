# Quick Start Guide

Get your first MCP server connected in under 10 minutes! This guide will take you from zero to a working MCP connection.

> **Note:** This repository has been restructured with simplified beginner-friendly modules. For the most up-to-date quickstart, see **[Module 01: Introduction & QuickStart](01-introduction-quickstart/)**. This guide provides Docker-based quickstart alternatives.

## Repository Structure

This repository now has two learning paths:

### Simplified Learning Path (Recommended for Beginners)
- **Module 01**: Introduction & QuickStart (10-minute connection guide)
- **Module 02**: Building with n8n (workflow automation)
- **Module 03**: Building with Docker (custom servers)

**Total time:** 4-6 hours | [See Learning Path →](LEARNING_PATH.md)

### Advanced Learning Path (For Deep Dives)
- **8 comprehensive modules** covering protocol details, advanced features, security, and debugging

**Total time:** 16-23 hours | [See Advanced Content →](advanced/)

---

Get your first MCP server running in under 10 minutes using existing server options.

## Prerequisites Check

Before starting, verify you have these installed:

```bash
# Check Python (need 3.9+)
python3 --version

# Check Docker
docker --version

# Check Git
git --version
```

If any command fails, see the [Prerequisites section in README.md](README.md#prerequisites) for installation instructions.

## Step 1: Clone the Repository (1 minute)

```bash
# Clone the repository
git clone https://github.com/ASU-Vibe-Coding-Centre/mcp-learning.git

# Navigate into the directory
cd mcp-learning
```

## Step 2: Choose Your Path

You have two options for getting started. Choose the one that fits your preference:

### Option A: Docker (Recommended)

Easiest setup, consistent environment across all platforms.

### Option B: Local Python

If you prefer working directly on your machine without Docker.

---

## Option A: Docker Quick Start (5 minutes)

### A1. Build the Docker Image

```bash
docker build -t mcp-learning:dev -f docker/Dockerfile .
```

This will take 2-3 minutes the first time as it downloads dependencies.

### A2. Start the Development Container

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### A3. Verify the Container is Running

```bash
docker-compose -f docker/docker-compose.yml ps
```

You should see the `dev` service with status "Up".

### A4. Enter the Container

```bash
docker-compose -f docker/docker-compose.yml exec dev bash
```

You're now inside the development environment!

### A5. Run Your First MCP Server

```bash
# Inside the container
python 04-basic-mcp-server/examples/minimal_server.py
```

**Success!** Your MCP server is now running. You should see initialization messages.

### A6. Test the Server

Open a new terminal (keep the server running in the first one):

```bash
# Enter the container in a new terminal
docker-compose -f docker/docker-compose.yml exec dev bash

# Test the server (instructions coming in Module 04)
# For now, just verify it started without errors
```

### A7. Stop and Clean Up

When you're done:

```bash
# Exit the container
exit

# Stop the container
docker-compose -f docker/docker-compose.yml down
```

**Jump to:** [What's Next?](#whats-next)

---

## Option B: Local Python Quick Start (5 minutes)

### B1. Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### B2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 1-2 minutes to install all packages.

### B3. Verify Installation

```bash
# Check that mcp is installed
python -c "import mcp; print(f'MCP SDK version: {mcp.__version__}')"
```

### B4. Run Your First MCP Server

```bash
python 04-basic-mcp-server/examples/minimal_server.py
```

**Success!** Your MCP server is now running.

### B5. Test the Server

Open a new terminal (keep the server running in the first one) and activate the virtual environment again:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Test commands will be covered in Module 04
```

### B6. Deactivate When Done

```bash
deactivate
```

---

## What's Next?

You've successfully run your first MCP server! Here's what to do next:

### Recommended Next Steps

**New Beginner-Friendly Path:**
1. **[Module 01: Introduction & QuickStart](01-introduction-quickstart/)** - 10-minute connection guide using free servers
2. **[Module 02: Building with n8n](02-building-with-n8n/)** - Build workflow-based MCP servers (45 min)
3. **[Module 03: Building with Docker](03-building-with-docker/)** - Build custom Python servers (3-4 hours)

**For Complete Understanding:**
- Read the conceptual overview in Module 01
- Connect a free server from mcp.so to Cursor IDE
- Follow the step-by-step testing guide

**For Code Examples:**
- Browse [advanced/04-basic-mcp-server/](advanced/04-basic-mcp-server/examples/) for Python examples
- Explore [advanced/03-docker-mcp-ecosystem/](advanced/03-docker-mcp-ecosystem/) for Docker patterns

### Learning Paths

**If you want the simplified experience:**
- Follow the **[new 3-module learning path](LEARNING_PATH.md)**
- Total time: 4-6 hours
- Perfect for beginners

**If you want comprehensive content:**
- Explore the **[advanced directory](advanced/)**
- Total time: 16-23 hours
- Deep-dive into all topics

### Recommended Learning Options

**Fastest Path (2 hours):**
- [Module 01 QuickStart](01-introduction-quickstart/) - Connect to existing server (10 min)
- [Module 03 Phase 2](03-building-with-docker/phase-2-simple-custom-server.md) - Build simple server (60-90 min)

**Complete Beginner Path (4-6 hours):**
- All three modules in sequence
- See [LEARNING_PATH.md](LEARNING_PATH.md) for details

**Advanced & Comprehensive (16-23 hours):**
- All advanced modules
- See [advanced/README.md](advanced/README.md)

---

## Troubleshooting

### Docker Issues

**Error: "Cannot connect to Docker daemon"**
```bash
# Make sure Docker is running
# On macOS/Windows: Start Docker Desktop
# On Linux: sudo systemctl start docker
```

**Error: "Port already in use"**
```bash
# Stop the conflicting container
docker ps  # Find the container ID
docker stop <container-id>
```

**Container won't start**
```bash
# Check logs
docker-compose -f docker/docker-compose.yml logs

# Rebuild from scratch
docker-compose -f docker/docker-compose.yml down -v
docker build --no-cache -t mcp-learning:dev -f docker/Dockerfile .
```

### Python Issues

**Error: "No module named 'mcp'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "Python version too old"**
```bash
# Check your Python version
python3 --version

# You need Python 3.9 or higher
# Download from: https://www.python.org/downloads/
```

**Import errors or missing dependencies**
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### General Issues

**Server starts but nothing happens**
- This is normal! The server is waiting for client connections
- You'll learn how to test it properly in Module 03
- For now, seeing no errors means it's working

**Can't find example files**
- Make sure you're in the `mcp-learning` directory
- Run `ls` to see available folders
- Example files are in Module 04

**Still stuck?**
- Check [Module 08: Debugging & Troubleshooting](08-debugging-troubleshooting/README.md)
- Review the [Docker setup guide](docker/README.md) for detailed Docker help
- Open an issue on GitHub with your error message

---

## Quick Reference Commands

### Docker Commands

```bash
# Build image
docker build -t mcp-learning:dev -f docker/Dockerfile .

# Start container
docker-compose -f docker/docker-compose.yml up -d

# Enter container
docker-compose -f docker/docker-compose.yml exec dev bash

# Check container status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs

# Stop container
docker-compose -f docker/docker-compose.yml down
```

### Python Commands

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run a server
python path/to/server.py

# Deactivate
deactivate
```

---

## Success Checklist

- [ ] Repository cloned
- [ ] Docker running OR virtual environment activated
- [ ] Dependencies installed
- [ ] Minimal server runs without errors
- [ ] Ready to start Module 01 or Module 04

**Congratulations!** You're ready to learn MCP server development!

---

**Time to completion:** 5-10 minutes

**Next:** [Module 01: Introduction](01-introduction/README.md) OR [Module 03: Docker MCP Ecosystem](03-docker-mcp-ecosystem/README.md) OR [Module 04: Basic MCP Server](04-basic-mcp-server/README.md)

