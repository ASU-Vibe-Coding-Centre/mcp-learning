# Python Setup Guide

This guide provides detailed instructions for installing Python 3.9+ and setting up your Python environment for MCP development.

## Table of Contents

1. [Overview](#overview)
2. [Python Installation by Operating System](#python-installation-by-operating-system)
3. [Virtual Environments](#virtual-environments)
4. [Installing MCP Python SDK](#installing-mcp-python-sdk)
5. [Dependency Management](#dependency-management)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### Why Python 3.9+?

The MCP Python SDK requires Python 3.9 or higher because it uses:
- Modern type hints (PEP 585, PEP 604)
- Async/await improvements
- Dictionary merge operators
- Better performance

### What You'll Install

1. **Python 3.9+**: The programming language
2. **pip**: Python package installer
3. **venv**: Virtual environment tool (included with Python)
4. **MCP SDK**: The Model Context Protocol Python library

---

## Python Installation by Operating System

### macOS

#### Option 1: Homebrew (Recommended)

Homebrew is a package manager for macOS.

**Step 1: Install Homebrew** (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Python**

```bash
# Install Python 3.11 (or latest)
brew install python@3.11

# Verify installation
python3.11 --version
```

**Step 3: Set up symlinks** (optional but convenient)

```bash
# If you want 'python3' to point to Python 3.11
brew link python@3.11
```

#### Option 2: Official Installer

**Step 1: Download**

Visit [python.org/downloads](https://www.python.org/downloads/) and download the macOS installer for Python 3.11 or later.

**Step 2: Install**

- Open the downloaded `.pkg` file
- Follow the installation wizard
- Check "Add Python to PATH" if prompted

**Step 3: Verify**

```bash
python3 --version
```

#### Option 3: pyenv (For Managing Multiple Versions)

If you need multiple Python versions:

```bash
# Install pyenv
brew install pyenv

# Install Python 3.11
pyenv install 3.11.6

# Set as global default
pyenv global 3.11.6

# Add to shell profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

### Linux

#### Ubuntu / Debian

**For Python 3.11:**

```bash
# Update package list
sudo apt update

# Install Python 3.11 and related tools
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip

# Verify
python3.11 --version
```

**If Python 3.11 isn't available in default repos:**

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**Set Python 3.11 as default** (optional):

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --config python3
```

#### Fedora

```bash
# Install Python 3.11
sudo dnf install python3.11 python3.11-devel

# Verify
python3.11 --version
```

#### Arch Linux

```bash
# Install Python
sudo pacman -S python

# Verify (Arch usually has latest)
python --version
```

### Windows

#### Option 1: WSL2 (Recommended)

Windows Subsystem for Linux provides a Linux environment on Windows.

**Step 1: Enable WSL2**

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart your computer.

**Step 2: Install Ubuntu from Microsoft Store**

Open Microsoft Store, search for "Ubuntu", and install.

**Step 3: Install Python in Ubuntu**

Open Ubuntu terminal:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

python3 --version
```

#### Option 2: Native Windows

**Step 1: Download**

Visit [python.org/downloads](https://www.python.org/downloads/) and download the Windows installer.

**Step 2: Install**

- Run the installer
- **Important**: Check "Add Python to PATH"
- Choose "Customize installation"
- Ensure "pip" and "py launcher" are selected
- Click "Install"

**Step 3: Verify**

Open Command Prompt or PowerShell:

```cmd
python --version
# or
py --version
```

**Note**: On Windows, you may use `python` instead of `python3`.

---

## Virtual Environments

### Why Virtual Environments?

Virtual environments are isolated Python environments that:
- Keep project dependencies separate
- Prevent version conflicts
- Make projects reproducible
- Easy to reset if something breaks

**Analogy**: Think of virtual environments like separate sandboxes - each project has its own toys (packages), and they don't interfere with each other.

### Creating a Virtual Environment

**Step 1: Create a project directory**

```bash
# Create and enter your project directory
mkdir ~/mcp-learning
cd ~/mcp-learning
```

**Step 2: Create virtual environment**

```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# This creates a 'venv' directory with:
# - Python interpreter copy
# - pip
# - Isolated package installation directory
```

**Directory structure after creation:**

```
mcp-learning/
└── venv/
    ├── bin/          # Executables (Linux/macOS)
    ├── Scripts/      # Executables (Windows)
    ├── lib/          # Installed packages
    └── pyvenv.cfg    # Configuration
```

### Activating the Virtual Environment

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**If you get an execution policy error on Windows:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**How to tell if it's activated?**

Your prompt will change to show `(venv)`:

```
(venv) user@machine:~/mcp-learning$
```

### Deactivating

To exit the virtual environment:

```bash
deactivate
```

The `(venv)` prefix will disappear.

### Best Practices

1. **Always activate before installing packages**
   ```bash
   source venv/bin/activate
   pip install package-name
   ```

2. **Don't commit `venv/` to git**
   Add to `.gitignore`:
   ```
   venv/
   ```

3. **Use `requirements.txt` to share dependencies**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Name your virtual environment descriptively** (optional)
   ```bash
   python3 -m venv .venv-mcp-dev
   ```

---

## Installing MCP Python SDK

### Installation

**Ensure virtual environment is activated** (you should see `(venv)` in your prompt).

**Install MCP SDK:**

```bash
pip install mcp
```

**What gets installed:**

- `mcp`: Core MCP library
- Dependencies (automatically installed):
  - `pydantic`: Data validation
  - `anyio`: Async I/O
  - Other required packages

### Verifying Installation

**Method 1: Check version**

```bash
pip show mcp
```

Output should show:
```
Name: mcp
Version: 0.9.0 (or similar)
Summary: Model Context Protocol Python SDK
...
```

**Method 2: Import in Python**

```bash
python -c "import mcp; print(f'MCP version: {mcp.__version__}')"
```

**Method 3: Interactive Python**

```python
python3
>>> import mcp
>>> from mcp.server import Server
>>> from mcp.types import Tool, Resource, TextContent
>>> print("All imports successful!")
>>> exit()
```

### Exploring MCP Types

Let's explore what MCP provides:

```python
python3 << 'EOF'
from mcp.types import Tool, Resource, Prompt, TextContent

# Example Tool structure
example_tool = Tool(
    name="example",
    description="An example tool",
    inputSchema={
        "type": "object",
        "properties": {
            "input": {"type": "string"}
        }
    }
)

print("Tool structure:")
print(f"  Name: {example_tool.name}")
print(f"  Description: {example_tool.description}")

# Example Resource structure
example_resource = Resource(
    uri="file:///example.txt",
    name="Example File",
    mimeType="text/plain"
)

print("\nResource structure:")
print(f"  URI: {example_resource.uri}")
print(f"  Name: {example_resource.name}")

print("\n✓ MCP types imported successfully!")
EOF
```

---

## Dependency Management

### Using requirements.txt

**Create requirements.txt:**

```bash
pip freeze > requirements.txt
```

This creates a file listing all installed packages:

```
mcp==0.9.0
pydantic==2.5.0
anyio==4.0.0
...
```

**Install from requirements.txt:**

On another machine or fresh environment:

```bash
pip install -r requirements.txt
```

### Development vs Production Dependencies

Create separate requirements files:

**requirements.txt** (production):
```
mcp==0.9.0
pydantic>=2.0.0
```

**requirements-dev.txt** (development):
```
-r requirements.txt
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
mypy==1.7.0
ruff==0.1.6
```

**Install development dependencies:**

```bash
pip install -r requirements-dev.txt
```

### Pinning Versions

**Exact pinning** (reproducible but inflexible):
```
mcp==0.9.0
```

**Minimum version** (flexible but may break):
```
mcp>=0.9.0
```

**Compatible release** (recommended):
```
mcp~=0.9.0  # Allows 0.9.x but not 0.10.0
```

### Upgrading Packages

**Upgrade specific package:**

```bash
pip install --upgrade mcp
```

**Upgrade all packages** (be careful!):

```bash
pip list --outdated
pip install --upgrade package-name
```

### Uninstalling

**Uninstall specific package:**

```bash
pip uninstall mcp
```

**Uninstall all packages** (nuclear option):

```bash
pip freeze | xargs pip uninstall -y
```

---

## Troubleshooting

### Issue: "python3: command not found"

**macOS/Linux:**
- Install Python using instructions above
- Check if `python` works instead of `python3`

**Windows:**
- Use `python` or `py` instead of `python3`
- Reinstall Python and check "Add to PATH"

### Issue: "No module named 'venv'"

On some Linux systems, venv isn't installed by default:

```bash
# Ubuntu/Debian
sudo apt install python3.11-venv

# Fedora
sudo dnf install python3-venv
```

### Issue: "pip: command not found"

**Install pip:**

```bash
# macOS/Linux with Python 3
python3 -m ensurepip --upgrade

# Ubuntu/Debian
sudo apt install python3-pip

# Or download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Issue: "Permission denied" when installing packages

**Never use sudo with pip in virtual environments.**

**If outside virtual environment:**

```bash
# Use --user flag
pip install --user mcp

# Or better: create and use virtual environment
```

### Issue: SSL Certificate errors

```bash
# Upgrade pip
pip install --upgrade pip

# Or use --trusted-host (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org mcp
```

### Issue: "mcp module not found" even after installation

**Possible causes:**

1. **Wrong Python interpreter**
   ```bash
   # Check which Python
   which python3
   
   # Check which pip
   which pip
   
   # They should be in the same venv
   ```

2. **Virtual environment not activated**
   ```bash
   # Activate it
   source venv/bin/activate
   
   # Verify with (venv) in prompt
   ```

3. **Installed in different environment**
   ```bash
   # Install in current environment
   python -m pip install mcp
   ```

### Issue: Slow pip installs

**Use a faster mirror** (for users in China, etc.):

```bash
# Temporary
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mcp

# Permanent
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Quick Reference

### Common Commands

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install package
pip install mcp

# Install from requirements
pip install -r requirements.txt

# Save dependencies
pip freeze > requirements.txt

# Upgrade package
pip install --upgrade mcp

# Uninstall package
pip uninstall mcp

# List installed packages
pip list

# Show package info
pip show mcp

# Deactivate virtual environment
deactivate
```

### Verification Script

Save this as `verify_setup.py`:

```python
"""Verify Python environment setup."""
import sys
import subprocess

def main():
    print("=== Python Environment Verification ===\n")
    
    # Check Python version
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 9):
        print("✓ Python version OK (3.9+)")
    else:
        print("✗ Python version too old (need 3.9+)")
        return False
    
    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✓ Running in virtual environment")
    else:
        print("⚠ Not in virtual environment (recommended)")
    
    # Check MCP import
    try:
        import mcp
        print(f"✓ MCP SDK installed (version {mcp.__version__})")
    except ImportError:
        print("✗ MCP SDK not installed")
        print("  Run: pip install mcp")
        return False
    
    # Check key modules
    modules = [
        ('mcp.server', 'Server'),
        ('mcp.types', 'Tool'),
        ('mcp.types', 'Resource'),
    ]
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✓ Can import {module}.{name}")
        except ImportError as e:
            print(f"✗ Cannot import {module}.{name}: {e}")
            return False
    
    print("\n=== All checks passed! ===")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

Run it:

```bash
python verify_setup.py
```

---

## Next Steps

1. **Complete environment setup**: Return to [README.md](./README.md)
2. **Install Docker** (optional): See [docker-setup.md](./docker-setup.md)
3. **Configure IDE**: Set up VS Code or PyCharm
4. **Run exercises**: Complete [tutorial-1-env-validation.md](./exercises/tutorial-1-env-validation.md)
5. **Build first server**: Move to [Module 03](../03-basic-mcp-server/README.md)

---

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [MCP Python SDK on GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [Python Packaging Guide](https://packaging.python.org/)

---

**You're now ready to develop MCP servers with Python!**

