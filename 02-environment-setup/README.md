# Module 02: Environment Setup

Welcome to Module 02! In this module, you'll set up everything needed to build and run MCP servers.

## Learning Objectives

By the end of this module, you will:

- Have a working Python 3.9+ environment
- Install and configure the MCP Python SDK
- Set up Docker for containerized development
- Configure your IDE for MCP development
- Verify your environment is ready for building MCP servers

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Options](#setup-options)
4. [Python Setup](#python-setup)
5. [Docker Setup](#docker-setup)
6. [IDE Configuration](#ide-configuration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Overview

Setting up your development environment correctly is crucial for a smooth learning experience. This module provides comprehensive instructions for all major operating systems.

**What You'll Install:**

- Python 3.9 or higher
- MCP Python SDK
- Docker (optional but recommended)
- IDE with Python support
- Testing tools (pytest, pytest-asyncio)
- Code quality tools (black, mypy, ruff)

**Estimated Time**: 30-60 minutes

---

## Prerequisites

### Required Knowledge

- Basic command line usage
- Understanding of virtual environments (we'll explain, but familiarity helps)
- Basic Python knowledge (you'll write Python code in later modules)

### System Requirements

**Operating Systems:**
- macOS 10.15 or later
- Linux (Ubuntu 20.04+, Fedora 35+, or equivalent)
- Windows 10/11 with WSL2 (recommended) or native Windows

**Hardware:**
- 4GB RAM minimum (8GB recommended)
- 5GB free disk space
- Internet connection for downloading dependencies

---

## Setup Options

You have three setup options:

### Option 1: Local Python Installation (Recommended for Beginners)

**Best for:**
- Learning and experimentation
- Quick setup
- Don't need containerization

**Pros:**
- Fast to set up
- Easy to debug
- Direct access to tools

**Cons:**
- Can have dependency conflicts
- Environment differences across machines

**Time**: ~20 minutes

### Option 2: Docker-Based Development

**Best for:**
- Consistent environments
- Team development
- Deployment preparation

**Pros:**
- Consistent across all machines
- Isolated from system Python
- Close to production environment

**Cons:**
- Slightly more complex
- Requires Docker knowledge
- Slower initial setup

**Time**: ~40 minutes

### Option 3: Both (Recommended for Advanced Users)

Use local Python for quick development and Docker for testing and deployment.

**Time**: ~60 minutes

---

## Python Setup

### Step 1: Check Python Version

First, check if you have Python 3.9+ installed:

```bash
python3 --version
```

You should see output like:
```
Python 3.11.x
```

If you see version 3.9 or higher, you're good! Skip to Step 3.

If not, continue to Step 2.

### Step 2: Install Python

**For detailed Python installation instructions**, see [python-setup.md](./python-setup.md).

**Quick Links:**
- macOS: Use Homebrew or download from python.org
- Linux: Use package manager (apt, dnf, pacman)
- Windows: Use WSL2 or download from python.org

### Step 3: Create Virtual Environment

Virtual environments isolate your project dependencies from system Python.

**Why virtual environments?**
- Avoid dependency conflicts
- Easy to reset if something breaks
- Different projects can use different package versions

**Create and activate:**

```bash
# Navigate to your projects directory
cd ~/projects

# Create a directory for MCP learning
mkdir mcp-learning
cd mcp-learning

# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You'll see `(venv)` in your prompt when activated.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install MCP SDK

Install the MCP Python SDK:

```bash
pip install mcp
```

Verify installation:

```bash
python -c "import mcp; print(mcp.__version__)"
```

You should see a version number (e.g., `0.9.0`).

### Step 6: Install Development Tools

Install testing and code quality tools:

```bash
pip install pytest pytest-asyncio black mypy ruff
```

**What these tools do:**
- `pytest`: Testing framework
- `pytest-asyncio`: Async testing support
- `black`: Code formatter
- `mypy`: Type checking
- `ruff`: Fast linter

### Step 7: Save Dependencies

Create a `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

This file lists all installed packages. Share it with others or use it to recreate your environment.

---

## Docker Setup

Docker provides a consistent development environment across all machines.

### Why Use Docker?

- **Consistency**: Same environment on all machines
- **Isolation**: Doesn't affect your system
- **Portability**: Easy to share and deploy
- **Learning**: Understand containerization

### Installation Options

You have two options for Docker:

#### Option A: Docker CLI (Command Line Only)

**Best for:** Developers comfortable with CLI

**Pros:**
- Lightweight
- No GUI overhead
- Scriptable

**Installation**: See [docker-setup.md](./docker-setup.md#docker-cli-installation)

#### Option B: Docker Desktop (GUI + CLI)

**Best for:** Developers who prefer GUI management

**Pros:**
- Visual interface
- Easy container management
- Resource monitoring
- Built-in Kubernetes (advanced)

**Cons:**
- Heavier resource usage
- Licensing requirements for some commercial use

**Installation**: See [docker-setup.md](./docker-setup.md#docker-desktop-installation)

### Quick Start with Docker

Once Docker is installed:

```bash
# Navigate to the repository root
cd /path/to/mcp-learning

# Build the development image
docker build -t mcp-learning:dev -f docker/Dockerfile .

# Run a container
docker run -it --rm -v $(pwd):/workspace mcp-learning:dev bash

# Inside container, verify Python and MCP
python --version
python -c "import mcp; print(mcp.__version__)"
```

For detailed Docker setup instructions, see [docker-setup.md](./docker-setup.md).

---

## IDE Configuration

A well-configured IDE makes development much faster.

### Recommended IDEs

#### VS Code (Recommended)

**Why VS Code?**
- Lightweight and fast
- Excellent Python extension
- Great debugging support
- Free and open source

**Setup:**

1. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)

2. Install Python extension:
   - Open VS Code
   - Go to Extensions (Cmd/Ctrl+Shift+X)
   - Search for "Python"
   - Install the official Python extension by Microsoft

3. Configure Python interpreter:
   - Open Command Palette (Cmd/Ctrl+Shift+P)
   - Type "Python: Select Interpreter"
   - Choose your virtual environment (`venv`)

4. Install useful extensions:
   - Python (by Microsoft)
   - Pylance (language server)
   - Python Debugger
   - Black Formatter
   - Ruff

**VS Code Settings** (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

#### Cursor

**Why Cursor?**
- AI-native IDE (based on VS Code)
- Great for learning with AI assistance
- Familiar VS Code interface

**Setup**: Same as VS Code (it's a fork)

#### JetBrains PyCharm

**Why PyCharm?**
- Powerful IDE with advanced features
- Excellent refactoring tools
- Professional debugging

**Setup:**

1. Download from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
   - Community Edition is free
   - Professional has more features

2. Configure interpreter:
   - File → Settings → Project → Python Interpreter
   - Add interpreter → Existing environment
   - Point to `venv/bin/python`

3. Enable plugins:
   - Docker integration
   - Markdown support

### IDE Features to Use

**Debugging:**
- Set breakpoints
- Step through code
- Inspect variables

**Testing:**
- Run tests from IDE
- See test results inline
- Debug failing tests

**Code Quality:**
- See linting errors inline
- Auto-format on save
- Type checking hints

---

## Verification

Let's verify everything is working correctly.

### Python Environment Check

Run this verification script:

```bash
python3 << 'EOF'
import sys
import subprocess

def check_python_version():
    version = sys.version_info
    if version >= (3, 9):
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def check_package(package_name):
    try:
        __import__(package_name)
        print(f"✓ {package_name} installed")
        return True
    except ImportError:
        print(f"✗ {package_name} not installed")
        return False

def check_command(command):
    try:
        result = subprocess.run([command, "--version"], 
                              capture_output=True, 
                              text=True,
                              check=True)
        print(f"✓ {command} available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {command} not found")
        return False

print("=== Environment Verification ===\n")

print("Python:")
check_python_version()

print("\nRequired Packages:")
check_package("mcp")
check_package("pytest")
check_package("pytest_asyncio")

print("\nCode Quality Tools:")
check_package("black")
check_package("mypy")
check_package("ruff")

print("\nCommand Line Tools:")
check_command("pytest")
check_command("black")

print("\n=== Verification Complete ===")
EOF
```

You should see all checks passing (✓).

### Docker Check (If Using Docker)

```bash
docker --version
docker compose version

# Test building the image
docker build -t mcp-test -f docker/Dockerfile .

# Test running a container
docker run --rm mcp-test python -c "import mcp; print('MCP SDK works in Docker!')"
```

### Create a Test MCP Server

Let's create a minimal MCP server to verify everything works:

```bash
# Create a test file
cat > test_server.py << 'EOF'
"""Minimal MCP server to verify setup."""
from mcp.server import Server
from mcp.types import Tool, TextContent

# Create server instance
server = Server("test-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back the input",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool."""
    if name == "echo":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Echo: {message}")]
    
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    print("✓ MCP server script is valid!")
    print("✓ All imports successful!")
    print("✓ Environment setup complete!")
EOF

# Run the test
python test_server.py
```

You should see success messages!

---

## Troubleshooting

### Common Issues

#### Issue: "command not found: python3"

**Solution**: Install Python or use `python` instead of `python3` on Windows.

#### Issue: "No module named 'mcp'"

**Solutions**:
1. Ensure virtual environment is activated (you should see `(venv)`)
2. Install MCP SDK: `pip install mcp`
3. Verify: `pip list | grep mcp`

#### Issue: "Permission denied" on macOS/Linux

**Solution**: Don't use `sudo` with pip in virtual environments. If needed: `python -m pip install --user mcp`

#### Issue: Docker build fails

**Common causes**:
1. Docker not running: Start Docker Desktop or daemon
2. Network issues: Check internet connection
3. Disk space: Free up space (`docker system prune`)

#### Issue: pytest not found

**Solution**: 
```bash
pip install pytest pytest-asyncio
```

### Platform-Specific Issues

**macOS:**
- If Python version is old, install via Homebrew: `brew install python@3.11`
- If command line tools missing: `xcode-select --install`

**Linux:**
- If Python header files missing: `sudo apt install python3-dev` (Ubuntu/Debian)
- If pip missing: `sudo apt install python3-pip`

**Windows:**
- Use WSL2 for best experience
- Or use Git Bash / PowerShell
- Path separators: Use forward slashes or double backslashes

### Getting Help

If you're still stuck:

1. Check the detailed guides:
   - [python-setup.md](./python-setup.md)
   - [docker-setup.md](./docker-setup.md)

2. Search for error messages (include "MCP Python SDK")

3. Ask in community forums

4. Check [official MCP documentation](https://modelcontextprotocol.io)

---

## Next Steps

### Complete the Exercises

1. **Tutorial 1**: [Environment Validation](./exercises/tutorial-1-env-validation.md)
   - Verify all tools work correctly
   - Practice running commands

2. **Tutorial 2**: [First Import](./exercises/tutorial-2-first-import.md)
   - Import MCP SDK
   - Explore basic types
   - Create simple structures

3. **Challenge 1**: [Docker Customization](./exercises/challenge-1-docker-custom.md)
   - Customize Docker setup
   - Add custom tools
   - Optimize image

### Validate Your Setup

Complete the [checkpoint](./checkpoint.md) to ensure your environment is ready.

### Move to Module 03

Once your environment is verified, proceed to:
- [Module 03: Basic MCP Server](../03-basic-mcp-server/README.md)
- Build your first MCP server!

---

## Key Takeaways

- Virtual environments keep your projects isolated
- MCP Python SDK is the foundation for building servers
- Docker provides consistency across development and production
- A well-configured IDE makes development much faster
- Verification ensures everything works before you start coding

---

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [MCP Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)

---

**Estimated Time**: 30-60 minutes (depending on your system and option chosen)

**Prerequisites**: Basic command line knowledge

**Next Module**: [03-basic-mcp-server](../03-basic-mcp-server/README.md)

