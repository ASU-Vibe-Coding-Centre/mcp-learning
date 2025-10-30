# Module 03 Validation Checklist

This checklist ensures Module 03 is complete and functional before committing to git.

## Content Validation

### Documentation

- [x] README.md created with complete module overview
- [x] README.md includes learning objectives
- [x] README.md explains server anatomy and lifecycle
- [x] README.md includes best practices and troubleshooting
- [x] checkpoint.md created with comprehensive assessment

### Example Servers

- [x] minimal_server.py created with extensive comments
- [x] calculator_server.py created with error handling
- [x] file_server.py created with security considerations
- [x] All examples include type hints and docstrings
- [x] test_calculator_server.py created with pytest examples

### Exercises

- [x] tutorial-1-hello-world.md created (step-by-step first server)
- [x] tutorial-2-simple-tools.md created (multi-tool calculator)
- [x] challenge-1-custom-tool.md created (open-ended design)
- [x] challenge-2-text-tools.md created (text manipulation)
- [x] challenge-3-data-tools.md created (JSON/CSV processing)

### Solutions

- [x] tutorial-1-solution.md created
- [x] tutorial-2-solution.md created
- [x] challenge-1-solution.md created (with multiple options)

## Functional Validation

### Example Servers

Run each example server to verify it starts without errors:

```bash
# From the project root

# Test minimal_server
python 03-basic-mcp-server/examples/minimal_server.py
# Should start and wait for input (Ctrl+C to stop)

# Test calculator_server
python 03-basic-mcp-server/examples/calculator_server.py
# Should start and wait for input (Ctrl+C to stop)

# Test file_server
python 03-basic-mcp-server/examples/file_server.py
# Should start and wait for input (Ctrl+C to stop)
```

**Expected Result**: Each server starts without errors and waits for stdin input.

### Example Servers with Inspector

Test each server with MCP Inspector:

```bash
# Test minimal_server with Inspector
npx @modelcontextprotocol/inspector python 03-basic-mcp-server/examples/minimal_server.py

# Test calculator_server with Inspector
npx @modelcontextprotocol/inspector python 03-basic-mcp-server/examples/calculator_server.py

# Test file_server with Inspector
npx @modelcontextprotocol/inspector python 03-basic-mcp-server/examples/file_server.py
```

**Validation Steps**:
1. Inspector opens in browser
2. Server connects successfully
3. Tools appear in the Inspector interface
4. Tool schemas are correct
5. Test calling each tool with valid inputs
6. Test calling each tool with invalid inputs (verify error handling)

### Unit Tests

Run the pytest suite:

```bash
# From project root
cd 03-basic-mcp-server/examples

# Run all tests
pytest test_calculator_server.py

# Run with verbose output
pytest test_calculator_server.py -v

# Run with coverage (if pytest-cov installed)
pytest test_calculator_server.py --cov=calculator_server
```

**Expected Result**: All tests pass (should be 50+ tests)

### Tutorial Validation

Complete Tutorial 1 following only the tutorial instructions:

```bash
# Create working directory
mkdir -p mcp_exercises
cd mcp_exercises

# Follow tutorial-1-hello-world.md step by step
# Time how long it takes (should be < 30 minutes)
```

**Validation Criteria**:
- Tutorial instructions are clear and complete
- No steps are missing or unclear
- Resulting server works when tested with Inspector
- Time to complete is reasonable (30-45 minutes)

Complete Tutorial 2:

```bash
# Follow tutorial-2-simple-tools.md step by step
# Time how long it takes (should be < 45 minutes)
```

**Validation Criteria**:
- Tutorial builds on Tutorial 1 appropriately
- Instructions are clear for all three refactoring phases
- Resulting server works with all four operations
- Error handling works correctly
- Time to complete is reasonable (45-60 minutes)

**Combined Time**: Tutorial 1 + Tutorial 2 should be < 1 hour combined

## Docker Validation

Test in Docker environment:

```bash
# Build the Docker image (from project root)
docker build -t mcp-learning:dev -f docker/Dockerfile .

# Run container and test
docker-compose -f docker/docker-compose.yml run --rm dev bash

# Inside container, test servers
python 03-basic-mcp-server/examples/minimal_server.py
python 03-basic-mcp-server/examples/calculator_server.py
python 03-basic-mcp-server/examples/file_server.py

# Run tests
cd 03-basic-mcp-server/examples
pytest test_calculator_server.py
```

**Expected Result**: All servers start and all tests pass in Docker environment

## Content Quality Checks

### Code Quality

- [x] All Python files use consistent formatting
- [x] All Python files include docstrings
- [x] All Python files use type hints
- [x] Comments explain complex logic
- [x] No placeholder or TODO comments in examples

### Documentation Quality

- [x] All Markdown files use consistent formatting
- [x] All code blocks have language tags
- [x] All links work (internal references)
- [x] Examples are clear and complete
- [x] No typos in headings or major sections

### Learning Path

- [x] Module builds on Modules 01-02 appropriately
- [x] Concepts are introduced in logical order
- [x] Difficulty progresses gradually (Tutorial 1 → Tutorial 2 → Challenges)
- [x] Each exercise has clear learning objectives
- [x] Checkpoint validates all key concepts

## Edge Case Testing

### minimal_server.py

Test with Inspector:
- Call "echo" with normal message
- Call "echo" with empty message
- Call "echo" with very long message (1000+ chars)
- Call unknown tool (should error)

### calculator_server.py

Test with Inspector:
- All four operations with positive numbers
- Operations with negative numbers
- Operations with floats
- Division by zero (should error with clear message)
- Invalid parameter types (should error)
- Missing parameters (should error)

### file_server.py

Test with Inspector:
- list_directory with empty workspace
- write_file to create a new file
- read_file to read the created file
- list_directory again (should show the file)
- write_file to create file in subdirectory (should auto-create dir)
- read_file on non-existent file (should error)
- Attempt to write_file with path traversal "../../../etc/passwd" (should be blocked)

## Performance Checks

### Server Startup

- Servers start in < 2 seconds
- No warnings or errors on startup
- Memory usage is reasonable (< 100MB per server)

### Response Time

- Tool calls return in < 100ms for simple operations
- Error handling is fast (< 50ms)

### Resource Cleanup

- Servers shut down cleanly with Ctrl+C
- No zombie processes left behind
- No file descriptors leaked

## Accessibility and Usability

### Tutorial Clarity

- [ ] Have a new learner follow Tutorial 1
- [ ] Observe where they get stuck
- [ ] Verify tutorial completion time
- [ ] Gather feedback on clarity

### Example Readability

- [ ] Have someone review an example server
- [ ] Can they understand it without explanation?
- [ ] Are the comments helpful?
- [ ] Is the code organization logical?

### Error Messages

- All error messages are helpful and specific
- Error messages suggest how to fix the problem
- No cryptic error codes or internal details exposed

## Final Checks

Before committing to git:

- [ ] All content validation items complete
- [ ] All functional validation tests pass
- [ ] All Docker validation tests pass
- [ ] All edge cases handled
- [ ] No broken links or references
- [ ] No typos in critical sections
- [ ] All files are included (nothing missing)
- [ ] File structure matches the task list

## Known Issues

Document any issues found during validation:

- None identified (to be filled during validation)

## Sign-Off

Module 03 is ready for commit when:

- [x] All content is created
- [ ] All validation tests pass
- [ ] At least one person has tested the tutorials
- [ ] No critical issues remain

**Validated by**: _________________  
**Date**: _________________  
**Notes**: _________________

---

## Running the Full Validation

To run all validations at once:

```bash
#!/bin/bash
# validate_module_03.sh

echo "Module 03 Validation Script"
echo "=========================="

echo "\n1. Testing minimal_server.py..."
timeout 2s python 03-basic-mcp-server/examples/minimal_server.py &
if [ $? -eq 124 ]; then
    echo "✓ minimal_server.py starts successfully"
else
    echo "✗ minimal_server.py failed to start"
    exit 1
fi

echo "\n2. Testing calculator_server.py..."
timeout 2s python 03-basic-mcp-server/examples/calculator_server.py &
if [ $? -eq 124 ]; then
    echo "✓ calculator_server.py starts successfully"
else
    echo "✗ calculator_server.py failed to start"
    exit 1
fi

echo "\n3. Testing file_server.py..."
timeout 2s python 03-basic-mcp-server/examples/file_server.py &
if [ $? -eq 124 ]; then
    echo "✓ file_server.py starts successfully"
else
    echo "✗ file_server.py failed to start"
    exit 1
fi

echo "\n4. Running unit tests..."
cd 03-basic-mcp-server/examples
pytest test_calculator_server.py -v
if [ $? -eq 0 ]; then
    echo "✓ All tests pass"
else
    echo "✗ Some tests failed"
    exit 1
fi

echo "\n=========================="
echo "All validations passed!"
echo "Module 03 is ready for commit"
```

Save as `scripts/validate_module_03.sh` and run with `bash scripts/validate_module_03.sh`

