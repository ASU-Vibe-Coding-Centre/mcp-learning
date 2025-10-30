# Module 02 Checkpoint: Environment Setup

This checkpoint validates that your development environment is correctly set up and you understand the tools before proceeding to build MCP servers.

**Estimated Time**: 30-40 minutes

---

## Purpose

This checkpoint ensures you:
- Have a working Python environment
- Can import and use MCP SDK
- Understand virtual environments
- Know basic Docker operations (if using Docker)
- Can use development tools
- Are ready to build MCP servers

**Passing Criteria**: Complete all validation steps successfully.

---

## Part 1: Python Environment Validation

### Check 1: Python Version

Run this command:

```bash
python3 --version
```

**Required**: Python 3.9.0 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

### Check 2: Virtual Environment

Run these commands:

```bash
# Check if in virtual environment
which python3

# Should show path to venv, not system Python
# Example: /path/to/project/venv/bin/python3
```

**Are you in a virtual environment?** Yes [ ] No [ ]

**If No**: Activate it with `source venv/bin/activate`

**Pass/Fail:** [ ]

---

### Check 3: pip Installation

```bash
pip --version
```

**Required**: pip 20.0 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

### Check 4: MCP SDK Import

Run this Python command:

```bash
python3 -c "import mcp; print(f'MCP SDK version: {mcp.__version__}')"
```

**Expected Output**: `MCP SDK version: 0.9.0` (or similar)

**Your output:** _______________________

**Pass/Fail:** [ ]

---

### Check 5: MCP Components

Run this test:

```bash
python3 << 'EOF'
try:
    from mcp.server import Server
    from mcp.types import Tool, Resource, Prompt, TextContent
    print("✓ All MCP imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    exit(1)
EOF
```

**Expected**: "✓ All MCP imports successful"

**Pass/Fail:** [ ]

---

## Part 2: Development Tools Validation

### Check 6: pytest

```bash
pytest --version
```

**Required**: pytest 7.0 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

### Check 7: black (Formatter)

```bash
black --version
```

**Required**: black 23.0 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

### Check 8: ruff (Linter)

```bash
ruff --version
```

**Required**: ruff 0.1 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

### Check 9: mypy (Type Checker)

```bash
mypy --version
```

**Required**: mypy 1.0 or higher

**Your version:** _______________________

**Pass/Fail:** [ ]

---

## Part 3: Practical Validation

### Check 10: Create and Run Simple Script

Create a file `test_mcp_basic.py`:

```python
"""Test basic MCP functionality."""

from mcp.types import Tool

# Create a tool
tool = Tool(
    name="test",
    description="Test tool",
    inputSchema={
        "type": "object",
        "properties": {
            "input": {"type": "string"}
        }
    }
)

print(f"✓ Created tool: {tool.name}")
print(f"✓ Tool type: {type(tool)}")
print(f"✓ Has description: {tool.description}")

# Serialize
tool_dict = tool.model_dump()
print(f"✓ Serialized to dict with {len(tool_dict)} fields")

print("\n✓✓✓ All basic operations work! ✓✓✓")
```

Run it:

```bash
python3 test_mcp_basic.py
```

**Expected**: All checkmarks and success message

**Pass/Fail:** [ ]

---

### Check 11: Test with pytest

Create `test_simple.py`:

```python
"""Simple pytest test."""

def test_addition():
    assert 1 + 1 == 2

def test_import():
    import mcp
    assert hasattr(mcp, '__version__')
```

Run pytest:

```bash
pytest test_simple.py -v
```

**Expected**: 2 tests passed

**Pass/Fail:** [ ]

---

## Part 4: Docker Validation (Optional but Recommended)

### Check 12: Docker Installation

```bash
docker --version
```

**Required**: Docker 20.0 or higher

**Your version (if installed):** _______________________

**Pass/Fail (if using Docker):** [ ]

**Skip if not using Docker:** [ ]

---

### Check 13: Docker Compose

```bash
docker compose version
```

**Required**: Docker Compose v2.0 or higher

**Your version (if installed):** _______________________

**Pass/Fail (if using Docker):** [ ]

---

### Check 14: Docker Image Build

Build the MCP development image:

```bash
cd /path/to/mcp-learning
docker build -t mcp-test:dev -f docker/Dockerfile .
```

**Expected**: Build completes without errors

**Pass/Fail:** [ ]

---

### Check 15: Run MCP in Docker

```bash
docker run --rm mcp-test:dev python -c "import mcp; print('MCP works in Docker!')"
```

**Expected**: "MCP works in Docker!"

**Pass/Fail:** [ ]

---

## Part 5: IDE Validation

### Check 16: IDE Setup

**Which IDE are you using?**
- [ ] VS Code
- [ ] PyCharm
- [ ] Cursor
- [ ] Other: ______________

**Is Python interpreter configured?** Yes [ ] No [ ]

**Can you see MCP imports without errors?** Yes [ ] No [ ]

**Do you have autocomplete for MCP types?** Yes [ ] No [ ]

**Pass/Fail:** [ ]

---

## Part 6: Workflow Validation

### Check 17: Complete Workflow Test

This tests your entire workflow:

```bash
# 1. Create project directory
mkdir test-mcp-workflow
cd test-mcp-workflow

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install MCP
pip install mcp

# 5. Create test script
cat > workflow_test.py << 'EOF'
from mcp.types import Tool

tool = Tool(
    name="workflow_test",
    description="Testing complete workflow",
    inputSchema={"type": "object", "properties": {}}
)

print(f"✓ Workflow test passed: {tool.name}")
EOF

# 6. Run it
python workflow_test.py

# 7. Deactivate
deactivate

# 8. Clean up
cd ..
rm -rf test-mcp-workflow
```

**Expected**: Each step completes successfully

**Pass/Fail:** [ ]

---

## Part 7: Knowledge Check

### Question 1: Virtual Environments

**Why use virtual environments?**

Your answer:
```




```

**Key points to include:**
- Isolate project dependencies
- Avoid version conflicts
- Easy to recreate
- Different projects can have different package versions

**Self-check:** Does your answer cover these points? [ ]

---

### Question 2: MCP Types

**What are the three main MCP capability types?**

1. _______________________
2. _______________________
3. _______________________

**Correct answers**: Tools, Resources, Prompts

**Self-check:** Did you get all three? [ ]

---

### Question 3: JSON Schema

**What is JSON Schema used for in MCP?**

Your answer:
```



```

**Key point**: Defines the structure and validation rules for tool input parameters

**Self-check:** Does your answer match? [ ]

---

### Question 4: Docker Benefits

**List 3 benefits of using Docker for MCP development:**

1. _______________________
2. _______________________
3. _______________________

**Example answers**: Consistency across machines, isolation, portability, production-like environment

**Self-check:** Do your answers make sense? [ ]

---

## Part 8: Troubleshooting Practice

### Scenario 1: Import Error

You run `python script.py` and get:
```
ImportError: No module named 'mcp'
```

**What are 3 possible causes and solutions?**

1. Cause: _______________________
   Solution: _______________________

2. Cause: _______________________
   Solution: _______________________

3. Cause: _______________________
   Solution: _______________________

**Example answers:**
1. Cause: Virtual environment not activated / Solution: `source venv/bin/activate`
2. Cause: MCP not installed / Solution: `pip install mcp`
3. Cause: Using wrong Python interpreter / Solution: Use `python3` or check `which python`

---

### Scenario 2: Pytest Not Found

You run `pytest` and get:
```
bash: pytest: command not found
```

**What's the problem and how do you fix it?**

Your answer:
```


```

**Solution**: pytest not installed or not in PATH. Fix: `pip install pytest` (with venv activated)

---

## Part 9: Final Validation Script

### Run Comprehensive Validation

Save this as `final_validation.py`:

```python
#!/usr/bin/env python3
"""Comprehensive environment validation."""

import sys
import subprocess
from pathlib import Path

def check(condition, message):
    if condition:
        print(f"✓ {message}")
        return True
    else:
        print(f"✗ {message}")
        return False

def main():
    print("=" * 60)
    print("FINAL ENVIRONMENT VALIDATION")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Python version
    version = sys.version_info
    all_passed &= check(
        version >= (3, 9),
        f"Python {version.major}.{version.minor}.{version.micro} >= 3.9"
    )
    
    # Virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    all_passed &= check(in_venv, "Running in virtual environment")
    
    # MCP SDK
    try:
        import mcp
        all_passed &= check(True, f"MCP SDK {mcp.__version__} installed")
    except ImportError:
        all_passed &= check(False, "MCP SDK installed")
    
    # MCP components
    try:
        from mcp.server import Server
        from mcp.types import Tool, Resource, Prompt, TextContent
        all_passed &= check(True, "All MCP components importable")
    except ImportError as e:
        all_passed &= check(False, f"MCP components importable: {e}")
    
    # Development tools
    tools = [
        ("pytest", "Testing"),
        ("black", "Formatting"),
        ("ruff", "Linting"),
        ("mypy", "Type checking"),
    ]
    
    for cmd, name in tools:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                timeout=5
            )
            all_passed &= check(result.returncode == 0, f"{name} ({cmd})")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            all_passed &= check(False, f"{name} ({cmd})")
    
    # Docker (optional)
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5
        )
        check(result.returncode == 0, "Docker (optional)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        check(False, "Docker (optional - skip if not using)")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✓✓✓ ENVIRONMENT READY FOR MCP DEVELOPMENT! ✓✓✓")
        print()
        print("Next steps:")
        print("  → Complete the checkpoint questions")
        print("  → Proceed to Module 03: Basic MCP Server")
        return 0
    else:
        print("✗✗✗ SOME CHECKS FAILED ✗✗✗")
        print()
        print("Review the failed checks and:")
        print("  → Re-read the setup guides")
        print("  → Fix the issues")
        print("  → Run this script again")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Run it:

```bash
python3 final_validation.py
```

**Expected**: All checks pass

**Pass/Fail:** [ ]

---

## Completion Summary

### Validation Results

**Total checks:** 17 (19 with Docker)

**Passed:** _____ / _____

**Percentage:** _____%

### Ready to Proceed?

**If you passed 90%+ of checks:**
- [ ] You're ready for Module 03!
- [ ] Proceed to [03-basic-mcp-server](../03-basic-mcp-server/README.md)

**If you passed 70-89% of checks:**
- [ ] Review the failed areas
- [ ] Re-read relevant setup guides
- [ ] Retry the checkpoint

**If you passed less than 70%:**
- [ ] Something is significantly wrong
- [ ] Start over with [python-setup.md](../python-setup.md)
- [ ] Ask for help if needed

---

## Checklist Before Moving On

Before proceeding to Module 03, ensure:

- [ ] Python 3.9+ installed and working
- [ ] Virtual environment created and activated
- [ ] MCP SDK installed and importable
- [ ] All MCP types (Tool, Resource, Prompt) understood
- [ ] pytest, black, ruff, mypy installed
- [ ] Can create and run Python scripts
- [ ] Can run tests with pytest
- [ ] IDE configured with Python interpreter
- [ ] Docker working (if using Docker)
- [ ] Understand troubleshooting basics
- [ ] Completed all exercises or reviewed solutions
- [ ] Final validation script passes

---

## Additional Notes

### If You're Stuck

1. **Re-read the module**: [README.md](./README.md)
2. **Check troubleshooting**: [python-setup.md](./python-setup.md#troubleshooting)
3. **Review exercises**: Complete any you skipped
4. **Ask for help**: Use community or AI assistance

### Common Issues

**Issue**: "Virtual environment not activating"
- **Solution**: Ensure you're in the right directory, try recreating it

**Issue**: "MCP not found even after install"
- **Solution**: Verify venv is activated, try `python3 -m pip install mcp`

**Issue**: "Docker commands fail"
- **Solution**: Ensure Docker is running, check Docker Desktop status

---

## Next Steps

1. **Save your environment configuration**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Commit to git** (if using version control):
   ```bash
   git add .
   git commit -m "feat: complete environment setup"
   ```

3. **Celebrate**: Your environment is ready!

4. **Move to Module 03**: [Basic MCP Server](../03-basic-mcp-server/README.md)

---

**Congratulations on completing Module 02!**

You now have a fully functional MCP development environment and are ready to build your first MCP server!

---

**Time to Complete**: 30-40 minutes

**Next Module**: [03-basic-mcp-server](../03-basic-mcp-server/README.md)

