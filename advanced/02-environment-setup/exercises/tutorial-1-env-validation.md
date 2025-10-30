# Tutorial 1: Environment Validation

## Overview

This tutorial walks you through validating your development environment to ensure everything is set up correctly for MCP development.

**Estimated Time**: 20-30 minutes

**Prerequisites**: Complete the setup instructions in [README.md](../README.md)

## Learning Objectives

By the end of this tutorial, you will:
- Verify Python installation and version
- Confirm MCP SDK is installed correctly
- Test all development tools
- Understand how to troubleshoot common issues
- Create a simple test script

---

## Part 1: Python Environment Validation

### Step 1: Check Python Version

Open your terminal and run:

```bash
python3 --version
```

**Expected Output:**
```
Python 3.11.x (or 3.9+)
```

**Questions:**
1. What version of Python do you have?
2. Is it 3.9 or higher?

**If not 3.9+**: Review [python-setup.md](../python-setup.md) to install a newer version.

---

### Step 2: Verify Virtual Environment

Check if you're in a virtual environment:

```bash
which python3
# or
which python
```

**Expected Output (in virtual environment):**
```
/path/to/your/project/venv/bin/python3
```

**If you see system Python** (like `/usr/bin/python3`):

Activate your virtual environment:

```bash
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

**Question:** How can you tell if a virtual environment is active?

**Answer:** Your prompt should show `(venv)` prefix.

---

**Ask the AI:**

If you're having issues with virtual environments:
- "What's the difference between system Python and a virtual environment? Why use venv?"
- "I ran the activation command but still see system Python. What should I check?"

---

### Step 3: Check pip

Verify pip is working:

```bash
pip --version
```

**Expected Output:**
```
pip 23.x.x from /path/to/venv/lib/python3.11/site-packages/pip (python 3.11)
```

**Upgrade pip if needed:**

```bash
pip install --upgrade pip
```

---

## Part 2: MCP SDK Validation

### Step 4: Verify MCP Installation

Check if MCP is installed:

```bash
pip show mcp
```

**Expected Output:**
```
Name: mcp
Version: 0.9.0 (or similar)
Summary: Model Context Protocol Python SDK
Home-page: https://github.com/modelcontextprotocol/python-sdk
Author: Anthropic
...
```

**If "Package not found":**

```bash
pip install mcp
```

---

### Step 5: Test MCP Import

Test importing MCP in Python:

```bash
python3 -c "import mcp; print(f'MCP version: {mcp.__version__}')"
```

**Expected Output:**
```
MCP version: 0.9.0
```

**If you see an ImportError:**

1. Ensure virtual environment is activated
2. Reinstall MCP: `pip install mcp`
3. Check you're using the right Python: `which python3`

---

### Step 6: Test MCP Components

Create a test script to verify all MCP components:

```bash
cat > test_mcp_imports.py << 'EOF'
"""Test all MCP imports."""

print("Testing MCP imports...")

# Test basic import
try:
    import mcp
    print("✓ mcp module imported")
except ImportError as e:
    print(f"✗ Failed to import mcp: {e}")
    exit(1)

# Test Server
try:
    from mcp.server import Server
    print("✓ Server class imported")
except ImportError as e:
    print(f"✗ Failed to import Server: {e}")
    exit(1)

# Test Types
try:
    from mcp.types import Tool, Resource, Prompt, TextContent
    print("✓ Tool, Resource, Prompt, TextContent imported")
except ImportError as e:
    print(f"✗ Failed to import types: {e}")
    exit(1)

# Create a simple server instance
try:
    server = Server("test-server")
    print("✓ Server instance created")
except Exception as e:
    print(f"✗ Failed to create server: {e}")
    exit(1)

# Create type instances
try:
    test_tool = Tool(
        name="test",
        description="Test tool",
        inputSchema={"type": "object", "properties": {}}
    )
    print("✓ Tool instance created")
    
    test_resource = Resource(
        uri="test://resource",
        name="Test Resource",
        mimeType="text/plain"
    )
    print("✓ Resource instance created")
    
    test_content = TextContent(type="text", text="Test")
    print("✓ TextContent instance created")
except Exception as e:
    print(f"✗ Failed to create type instances: {e}")
    exit(1)

print("\n✓✓✓ All MCP components working! ✓✓✓")
EOF

python3 test_mcp_imports.py
```

**Expected Output:**
```
Testing MCP imports...
✓ mcp module imported
✓ Server class imported
✓ Tool, Resource, Prompt, TextContent imported
✓ Server instance created
✓ Tool instance created
✓ Resource instance created
✓ TextContent instance created

✓✓✓ All MCP components working! ✓✓✓
```

**Clean up:**
```bash
rm test_mcp_imports.py
```

---

**Ask the AI:**

If MCP imports are failing:
- "I'm getting 'ModuleNotFoundError: No module named mcp'. What are the three most common causes?"
- "The validation script shows 'Server instance created' but I don't understand what that means. Can you explain?"

---

## Part 3: Development Tools Validation

### Step 7: Check pytest

Verify pytest is installed:

```bash
pytest --version
```

**Expected Output:**
```
pytest 7.4.x
```

**If not installed:**

```bash
pip install pytest pytest-asyncio
```

**Test pytest works:**

```bash
# Create a simple test
cat > test_example.py << 'EOF'
def test_simple():
    assert 1 + 1 == 2
    
def test_string():
    assert "hello".upper() == "HELLO"
EOF

# Run test
pytest test_example.py -v

# Clean up
rm test_example.py
```

**Expected Output:**
```
test_example.py::test_simple PASSED
test_example.py::test_string PASSED
```

---

### Step 8: Check Code Formatting Tools

**Black (formatter):**

```bash
black --version
```

**Expected:** `black, version 23.x.x`

**If not installed:** `pip install black`

**Test black:**

```bash
# Create poorly formatted file
cat > ugly_code.py << 'EOF'
def    add(  a,b  ):
    return    a+b
EOF

# Format it
black ugly_code.py

# Check result
cat ugly_code.py
# Should be properly formatted

# Clean up
rm ugly_code.py
```

---

**Ruff (linter):**

```bash
ruff --version
```

**Expected:** `ruff 0.x.x`

**If not installed:** `pip install ruff`

**Test ruff:**

```bash
# Create code with issues
cat > bad_code.py << 'EOF'
import os
import sys

def unused_function():
    pass

x = 1
EOF

# Lint it
ruff check bad_code.py

# Clean up
rm bad_code.py
```

---

**Mypy (type checker):**

```bash
mypy --version
```

**Expected:** `mypy 1.x.x`

**If not installed:** `pip install mypy`

---

## Part 4: Docker Validation (Optional)

**If you installed Docker**, validate it:

### Step 9: Check Docker

```bash
docker --version
```

**Expected Output:**
```
Docker version 24.x.x
```

**Check Docker is running:**

```bash
docker ps
```

**Expected:** Should show empty table (or running containers), not an error.

---

### Step 10: Check Docker Compose

```bash
docker compose version
```

**Expected Output:**
```
Docker Compose version v2.x.x
```

---

### Step 11: Test Docker with Python

Run a simple Python command in Docker:

```bash
docker run --rm python:3.11 python -c "print('Hello from Docker!')"
```

**Expected Output:**
```
Hello from Docker!
```

---

### Step 12: Build MCP Development Image

Build the MCP development Docker image:

```bash
# Navigate to repository root
cd /path/to/mcp-learning

# Build image
docker build -t mcp-learning:dev -f docker/Dockerfile .
```

**This will take 2-5 minutes the first time.**

**Verify image was built:**

```bash
docker images | grep mcp-learning
```

**Expected:** You should see `mcp-learning` image listed.

---

### Step 13: Test MCP in Docker

Run MCP import test in Docker:

```bash
docker run --rm mcp-learning:dev python -c "import mcp; print(f'MCP {mcp.__version__} works in Docker!')"
```

**Expected Output:**
```
MCP 0.9.0 works in Docker!
```

---

**Ask the AI:**

If you're having Docker issues:
- "Docker build succeeded but when I run the container I get 'command not found'. What does this usually mean?"
- "What's the difference between 'docker build' and 'docker run'? When do I use each?"

---

## Part 5: IDE Validation

### Step 14: Check IDE Setup

**If using VS Code:**

1. Open VS Code
2. Open the Command Palette (Cmd/Ctrl+Shift+P)
3. Type "Python: Select Interpreter"
4. Verify your virtual environment is listed
5. Select it

**Verify in VS Code:**

1. Create a new Python file
2. Type: `from mcp.server import Server`
3. You should see autocomplete suggestions
4. No red underlines should appear

**If using PyCharm:**

1. Open PyCharm
2. File → Settings → Project → Python Interpreter
3. Verify your virtual environment is selected
4. Check that `mcp` package is listed

---

## Part 6: Comprehensive Validation Script

### Step 15: Run Full Validation

Create a comprehensive validation script:

```bash
cat > validate_environment.py << 'EOF'
#!/usr/bin/env python3
"""Comprehensive environment validation script."""

import sys
import subprocess
from pathlib import Path

def check(condition, message):
    """Check a condition and print result."""
    if condition:
        print(f"✓ {message}")
        return True
    else:
        print(f"✗ {message}")
        return False

def main():
    print("=" * 60)
    print("MCP Development Environment Validation")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Python version
    print("1. Python Environment")
    print("-" * 60)
    version = sys.version_info
    all_passed &= check(
        version >= (3, 9),
        f"Python version {version.major}.{version.minor}.{version.micro} (need 3.9+)"
    )
    
    # Virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    all_passed &= check(
        in_venv,
        "Running in virtual environment"
    )
    
    print()
    
    # MCP SDK
    print("2. MCP SDK")
    print("-" * 60)
    try:
        import mcp
        all_passed &= check(True, f"MCP SDK installed (version {mcp.__version__})")
    except ImportError:
        all_passed &= check(False, "MCP SDK installed")
    
    # MCP components
    imports = [
        ("mcp.server", "Server"),
        ("mcp.types", "Tool"),
        ("mcp.types", "Resource"),
        ("mcp.types", "TextContent"),
    ]
    
    for module, name in imports:
        try:
            __import__(module)
            all_passed &= check(True, f"Can import {module}.{name}")
        except ImportError:
            all_passed &= check(False, f"Can import {module}.{name}")
    
    print()
    
    # Development tools
    print("3. Development Tools")
    print("-" * 60)
    
    tools = [
        ("pytest", "Testing framework"),
        ("black", "Code formatter"),
        ("ruff", "Linter"),
        ("mypy", "Type checker"),
    ]
    
    for tool, description in tools:
        try:
            result = subprocess.run(
                [tool, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            all_passed &= check(
                result.returncode == 0,
                f"{description} ({tool})"
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            all_passed &= check(False, f"{description} ({tool})")
    
    print()
    
    # Docker (optional)
    print("4. Docker (Optional)")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        docker_installed = result.returncode == 0
        check(docker_installed, "Docker installed")
        
        if docker_installed:
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            check(result.returncode == 0, "Docker Compose installed")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        check(False, "Docker installed (optional)")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✓✓✓ All checks passed! You're ready to develop MCP servers! ✓✓✓")
        return 0
    else:
        print("✗✗✗ Some checks failed. Please review the output above. ✗✗✗")
        print()
        print("Common solutions:")
        print("  - Activate virtual environment: source venv/bin/activate")
        print("  - Install MCP: pip install mcp")
        print("  - Install dev tools: pip install pytest black ruff mypy")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x validate_environment.py
python3 validate_environment.py
```

**Save this script** - it's useful for checking your environment anytime!

---

## Part 7: Troubleshooting Practice

### Exercise 1: Intentional Breakage

Let's practice troubleshooting by intentionally breaking things:

**Break 1: Deactivate virtual environment**

```bash
deactivate
python3 -c "import mcp"
```

**Question:** What error do you see?

**Fix:**
```bash
source venv/bin/activate
```

---

**Break 2: Wrong Python version**

```bash
# If you have Python 2 or old Python 3
python2 --version  # or older python3
```

**Question:** Why won't this work for MCP?

**Answer:** MCP requires Python 3.9+ for modern type hints and async features.

---

### Exercise 2: Debug Common Issues

For each scenario, identify the problem and solution:

**Scenario A:**
```bash
$ python3 script.py
ImportError: No module named 'mcp'
```

**Problem:**
**Solution:**

---

**Scenario B:**
```bash
$ pip install mcp
Requirement already satisfied: mcp
$ python3 -c "import mcp"
ImportError: No module named 'mcp'
```

**Problem:**
**Solution:**

---

**Scenario C:**
```bash
$ pytest test_server.py
bash: pytest: command not found
```

**Problem:**
**Solution:**

---

## Part 8: Create Your Environment Checklist

Create a personal checklist file:

```bash
cat > MY_ENVIRONMENT_CHECKLIST.md << 'EOF'
# My MCP Development Environment Checklist

## Setup Complete

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] MCP SDK installed
- [ ] pytest installed
- [ ] black installed
- [ ] ruff installed
- [ ] mypy installed
- [ ] IDE configured
- [ ] Docker installed (optional)
- [ ] Docker image built (optional)

## Daily Checklist (Before Starting Work)

- [ ] Activate virtual environment
- [ ] Verify in correct directory
- [ ] Run `python3 validate_environment.py`
- [ ] Git status clean (or known changes)

## Troubleshooting Notes

(Add your own notes as you encounter and solve issues)

### Issue 1:


### Issue 2:


EOF

echo "Checklist created: MY_ENVIRONMENT_CHECKLIST.md"
```

---

## Completion Checklist

Before moving to the next tutorial, ensure you can:

- [ ] Check Python version from command line
- [ ] Activate and deactivate virtual environment
- [ ] Install packages with pip
- [ ] Import MCP SDK in Python
- [ ] Run pytest tests
- [ ] Format code with black
- [ ] Lint code with ruff
- [ ] Run the validation script successfully
- [ ] Troubleshoot common issues

---

## Next Steps

1. **If all checks passed**: Great! Move to [Tutorial 2: First Import](./tutorial-2-first-import.md)

2. **If some checks failed**: 
   - Review the specific setup guides ([python-setup.md](../python-setup.md), [docker-setup.md](../docker-setup.md))
   - Check the troubleshooting sections
   - Run validation script again

3. **Save your validation script**: You'll use `validate_environment.py` regularly

4. **Complete the challenge**: Try [Challenge 1: Docker Customization](./challenge-1-docker-custom.md)

---

## How to Use AI Assistance

Environment setup can be tricky. Here's how to get effective help:

### General Troubleshooting

When something isn't working:

```
I'm running [command] and getting [error message]. What does this error 
typically mean, and what should I check first?
```

```
My Python version check shows 3.8, but MCP requires 3.9+. What's the 
best way to install a newer Python version on [your OS]?
```

### Virtual Environment Issues

For venv problems:

```
I activated my virtual environment but 'which python' still shows the 
system Python. What am I doing wrong?
```

```
I'm on Windows and the virtual environment activation command isn't 
working. What's the correct Windows syntax?
```

### Import Errors

When imports fail:

```
I installed mcp with pip but Python can't import it. I'm getting 
[specific error]. What are the common causes and how do I diagnose this?
```

```
The validation script at Step 6 is failing on [specific import]. 
Can you help me understand what this means without just giving me the fix?
```

### Docker Issues

For Docker problems:

```
Docker build is failing with [error]. I'm on [Mac/Linux/Windows]. 
What should I check?
```

```
The MCP image built successfully but when I try to run it, I get [error]. 
What does this typically indicate?
```

### Understanding Commands

To learn what commands do:

```
The tutorial uses 'pip install --no-cache-dir'. What does --no-cache-dir 
do and why would we use it in Docker?
```

```
Can you explain what 'which python3' tells me and why it's useful for 
diagnosing virtual environment issues?
```

### Debugging Validation Scripts

When validation fails:

```
My validation script is failing at [specific check]. Rather than tell me 
how to fix it, can you help me understand what that check is testing and 
why it might fail?
```

### Platform-Specific Help

For OS-specific issues:

```
I'm on [Mac/Linux/Windows] and [specific step] isn't working as described. 
What's the equivalent command or approach for my platform?
```

### Progressive Problem Solving

Work through issues systematically:

```
Step 1: I've confirmed Python 3.9 is installed but not being used.
Can you give me the first thing to check?
```

Then continue:

```
OK, I checked [X] and found [Y]. What should I check next?
```

### What NOT to Ask

Avoid these as they skip understanding:

- "Fix my environment"
- "Give me all the commands to run"
- "Here's my error, tell me exactly what to type"

### Example Debugging Conversation

**Effective:**

1. "Import mcp is failing. What are the typical causes?"
2. Get list of causes
3. "OK, I checked my venv and it's not activated. How do I verify it's activated after running the activation command?"
4. Learn the indicators
5. "Now I see (venv) in my prompt. Let me try the import again..."

**Less effective:**

1. "Import mcp not working, what do I do?"
2. Get specific commands
3. Run them without understanding
4. Still don't know how to diagnose future issues

### Asking for Explanations

Learn as you troubleshoot:

```
The tutorial says to run 'pip show mcp'. I got it working, but what 
information does this command show and how is it useful?
```

```
Why do we need to upgrade pip? What problems does an old pip cause?
```

---

## Summary

You've validated:
- Python environment is correctly set up
- MCP SDK is installed and working
- Development tools are available
- Docker is ready (if installed)
- IDE is configured

**You're ready to start building MCP servers!**

---

## Solutions to Exercises

### Exercise 2: Debug Common Issues

**Scenario A:**
- **Problem:** MCP not installed or virtual environment not activated
- **Solution:** `source venv/bin/activate` then `pip install mcp`

**Scenario B:**
- **Problem:** Multiple Python environments; pip installing to different environment than python3 is using
- **Solution:** Use `python3 -m pip install mcp` to ensure consistency

**Scenario C:**
- **Problem:** pytest not installed or virtual environment not activated
- **Solution:** `source venv/bin/activate` then `pip install pytest`

---

**Estimated Time**: 20-30 minutes

**Next**: [Tutorial 2: First Import](./tutorial-2-first-import.md)

