# Challenge 1: Design a Multi-Server Architecture

Now that you understand how to integrate individual MCP servers, it's time to tackle a more sophisticated challenge: designing and implementing a system that coordinates multiple specialized servers working together.

## Challenge Overview

In real-world applications, splitting functionality across multiple MCP servers often makes more sense than building one monolithic server. This challenge asks you to design and implement a multi-server architecture for a realistic use case, making architectural decisions and handling the complexity of coordinating multiple services.

## Difficulty

Advanced

## Time Estimate

90-120 minutes

## Learning Objectives

By completing this challenge, you will:

1. Analyze when to use multiple servers vs a single combined server
2. Design a coherent multi-server architecture
3. Define clear boundaries and responsibilities for each server
4. Implement servers that work together to solve complex problems
5. Configure multiple servers in Cursor IDE
6. Handle coordination, error propagation, and state management
7. Document your architecture decisions

## Your Mission

Choose ONE of the following scenarios and implement a complete multi-server solution. Each scenario requires 2-3 specialized servers working together.

### Scenario A: Development Workflow Assistant

**Use Case**: Help developers manage their development workflow

**Required Servers**:

1. **Git Server** - Version control operations
   - Tools: `git_status`, `git_diff`, `git_log`, `git_branch`
   - Focuses on read-only git operations
   
2. **Code Analysis Server** - Code quality and metrics
   - Tools: `count_lines`, `find_todos`, `check_style`, `complexity_score`
   - Analyzes code structure and quality
   
3. **Documentation Server** - Generate and manage docs
   - Tools: `generate_docstring`, `extract_api`, `create_readme`
   - Helps maintain project documentation

**Example Workflow**:

A developer asks Claude: "What needs to be documented in my current branch?"

Claude would:
1. Use Git Server to find changed files
2. Use Code Analysis Server to find functions without docstrings
3. Use Documentation Server to generate skeleton documentation
4. Present a comprehensive report

**Architecture Considerations**:

- Each server operates independently
- No direct communication between servers
- Claude/Cursor IDE orchestrates the workflow
- Servers might need to access the same repository

### Scenario B: Content Management System

**Use Case**: Manage a blog or documentation site

**Required Servers**:

1. **File Server** - File system operations
   - Tools: `read_file`, `write_file`, `list_directory`, `delete_file`
   - Manages the content files
   
2. **Markdown Server** - Markdown processing
   - Tools: `render_markdown`, `validate_markdown`, `extract_metadata`, `count_words`
   - Processes markdown content
   
3. **Search Server** - Content search and indexing
   - Tools: `index_content`, `search`, `find_links`, `check_broken_links`
   - Enables content discovery

**Example Workflow**:

A user asks: "Find all blog posts about Python and check if they're valid"

Claude would:
1. Use Search Server to find posts matching "Python"
2. Use File Server to read each post
3. Use Markdown Server to validate formatting
4. Report any issues found

**Architecture Considerations**:

- Search Server needs to access files (through File Server tools in conversation, or directly)
- Markdown Server operates on content, not files directly
- Clear separation between storage, processing, and search

### Scenario C: API Integration Hub

**Use Case**: Integrate with multiple external services

**Required Servers**:

1. **GitHub Server** - GitHub API integration
   - Tools: `list_repos`, `get_issues`, `create_issue`, `search_code`
   - Accesses GitHub data
   
2. **Slack Server** - Slack integration
   - Tools: `send_message`, `list_channels`, `get_messages`, `create_channel`
   - Manages Slack communication
   
3. **Task Manager Server** - Local task tracking
   - Tools: `create_task`, `list_tasks`, `update_task`, `complete_task`
   - Tracks personal tasks and todos

**Example Workflow**:

A user asks: "Create tasks for all open GitHub issues assigned to me and post a summary to Slack"

Claude would:
1. Use GitHub Server to fetch assigned issues
2. Use Task Manager Server to create local tasks
3. Use Slack Server to post summary
4. Return confirmation of all actions

**Architecture Considerations**:

- Each server manages its own authentication
- Operations should be idempotent where possible
- Error handling across multiple external APIs
- Rate limiting for each service

### Scenario D: Data Pipeline Manager

**Use Case**: Process and transform data through multiple stages

**Required Servers**:

1. **Data Source Server** - Fetch data from various sources
   - Tools: `fetch_csv`, `fetch_json`, `fetch_api`, `read_database`
   - Retrieves raw data
   
2. **Data Transform Server** - Process and clean data
   - Tools: `clean_data`, `transform_schema`, `aggregate`, `filter_rows`
   - Transforms data
   
3. **Data Export Server** - Export to various formats
   - Tools: `export_csv`, `export_json`, `export_excel`, `send_to_database`
   - Outputs processed data

**Example Workflow**:

A user asks: "Fetch sales data from the API, aggregate by region, and export as Excel"

Claude would:
1. Use Data Source Server to fetch from API
2. Use Data Transform Server to aggregate by region
3. Use Data Export Server to create Excel file
4. Report the output file location

**Architecture Considerations**:

- Data passes through conversation (or temp storage)
- Each server has single responsibility
- Pipeline can be reconfigured for different workflows
- Handle large data efficiently

### Scenario E: Your Own Multi-Server System

Have a different idea? Design your own!

**Requirements**:

- At least 2 servers (3 recommended)
- Clear separation of concerns
- Realistic use case
- Servers work together to solve a problem
- Document your design decisions

## Design Phase (Required)

Before coding, create a design document addressing:

### 1. Architecture Overview

Create a diagram or description showing:

```
[User] → [Cursor IDE/Claude] → [Server 1: Purpose]
                              → [Server 2: Purpose]  
                              → [Server 3: Purpose]
                              ↓
                          [External Systems/Data]
```

### 2. Server Responsibilities

For each server, define:

- **Name**: What is it called?
- **Purpose**: What is its single responsibility?
- **Tools**: What tools does it expose?
- **Dependencies**: What external resources does it need?
- **State**: Does it maintain state? Where?

### 3. Interaction Patterns

Describe how servers work together:

- **Independent**: Do they ever need each other's data?
- **Orchestration**: How does Claude coordinate them?
- **Data Flow**: How does data move through the system?
- **Error Handling**: What happens if one server fails?

### 4. Design Decisions

Justify your choices:

**Why Multiple Servers?**

- What would be the downside of a single server?
- What are the benefits of splitting functionality?
- How does this improve maintainability?

**Boundary Decisions**:

- Why did you draw boundaries where you did?
- What functionality belongs in each server?
- Did you consider alternative splits?

**Trade-offs**:

- What are the downsides of your design?
- Where might it break down?
- What would you improve with more time?

## Implementation Phase

### Step 1: Implement Each Server

For each server in your architecture:

**Create the server file** (e.g., `git_server.py`):

```python
#!/usr/bin/env python3
"""
[Server Name] MCP Server
[Brief description of purpose]
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server with descriptive name
app = Server("[server-name]")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register tools for this server."""
    return [
        # Define your tools
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    # Implement tool logic
    pass

async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Requirements for each server**:

- [ ] At least 2-3 tools per server
- [ ] Clear, specific tool descriptions
- [ ] Comprehensive input validation
- [ ] Proper error handling
- [ ] Type hints and docstrings
- [ ] Each server works independently

### Step 2: Configure in Cursor IDE

Create configuration for all servers:

**File**: `cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "server-1": {
      "command": "python",
      "args": ["/full/path/to/server1.py"],
      "env": {
        "CONFIG_VAR": "value"
      }
    },
    "server-2": {
      "command": "python",
      "args": ["/full/path/to/server2.py"]
    },
    "server-3": {
      "command": "python",
      "args": ["/full/path/to/server3.py"]
    }
  }
}
```

**Configuration Checklist**:

- [ ] All servers listed with unique IDs
- [ ] Full paths to server scripts
- [ ] Environment variables configured
- [ ] JSON syntax is valid
- [ ] Paths use correct separators for OS

### Step 3: Test Each Server Independently

Before testing together, verify each server works alone:

```bash
# Test with MCP Inspector
mcp-inspector python server1.py
mcp-inspector python server2.py
mcp-inspector python server3.py

# Test each tool
# Verify error handling
# Check edge cases
```

**Testing Checklist** (per server):

- [ ] Server starts without errors
- [ ] All tools are registered
- [ ] Tools respond correctly
- [ ] Errors are handled gracefully
- [ ] Edge cases work as expected

### Step 4: Test Multi-Server Integration

Restart Cursor IDE and test workflows that use multiple servers:

**Test Queries**:

Create 3-5 test questions that require using multiple servers together:

1. **Simple Coordination**: Uses 2 servers sequentially
   - Example: "Get git status and analyze the changed files"
   
2. **Complex Workflow**: Uses all servers
   - Example: "Find all Python files, check for missing docs, generate them"
   
3. **Error Handling**: Tests failure scenarios
   - Example: "Process a file that doesn't exist"
   
4. **Data Flow**: Tests passing data between operations
   - Example: "Read data from X, transform with Y, export with Z"
   
5. **Independent Operations**: Tests parallel server use
   - Example: "Check git status AND search for todos"

**Integration Testing Checklist**:

- [ ] Servers load successfully in Cursor IDE
- [ ] Claude discovers all tools
- [ ] Multi-server workflows complete successfully
- [ ] Errors in one server don't crash others
- [ ] Data flows correctly between operations
- [ ] Performance is acceptable

### Step 5: Create Documentation

Document your multi-server system:

**Create** `ARCHITECTURE.md`:

```markdown
# [System Name] Multi-Server Architecture

## Overview

[Brief description of what the system does]

## Servers

### Server 1: [Name]

**Purpose**: [Single responsibility]

**Tools**:
- `tool_name`: Description
- `tool_name`: Description

**Dependencies**: [External resources needed]

### Server 2: [Name]

[Same structure]

### Server 3: [Name]

[Same structure]

## Example Workflows

### Workflow 1: [Name]

**User Goal**: [What user wants to achieve]

**Steps**:
1. Server 1: [Action]
2. Server 2: [Action]
3. Server 3: [Action]
4. Result: [Outcome]

## Configuration

[How to configure all servers]

## Design Decisions

### Why Multiple Servers?

[Explain the benefits]

### Boundaries

[Explain how you divided functionality]

### Trade-offs

[Discuss downsides and limitations]

## Future Improvements

[What you would add/change]
```

## Success Criteria

Your solution should demonstrate:

### Architecture

- [ ] **Clear separation of concerns** - Each server has one responsibility
- [ ] **Minimal coupling** - Servers don't depend on each other
- [ ] **Complete coverage** - Together, servers solve the full use case
- [ ] **Sensible boundaries** - Division makes logical sense

### Implementation

- [ ] **All servers functional** - Each works independently
- [ ] **Tools well-designed** - Clear parameters and responses
- [ ] **Error handling** - Failures are graceful and informative
- [ ] **Production quality** - Code is clean, documented, tested

### Integration

- [ ] **Configuration correct** - All servers load in Cursor IDE
- [ ] **Workflows successful** - Multi-server operations work
- [ ] **Performance acceptable** - No unnecessary delays
- [ ] **User experience good** - Claude can coordinate effectively

### Documentation

- [ ] **Design explained** - Architecture decisions documented
- [ ] **Usage clear** - Examples show how to use the system
- [ ] **Trade-offs discussed** - Honest about limitations
- [ ] **Future-thinking** - Considers improvements

## Evaluation Questions

After completing your implementation, answer these:

### Design Evaluation

1. **Could this have been one server?** Why or why not?

2. **Where are the boundaries between your servers?** What principle did you use to draw them?

3. **What would happen if you needed to add new functionality?** Which server would it belong in?

4. **How does your design handle failures?** What if one server is unavailable?

5. **What assumptions did you make?** How might they limit your design?

### Implementation Evaluation

6. **What was the hardest part to implement?** Why?

7. **What would you refactor given more time?** Why?

8. **How would your servers handle concurrent requests?** Do they maintain state?

9. **What security concerns exist?** How did you address them?

10. **How would you test this system thoroughly?** What test cases are critical?

### Comparison

11. **Single Server Alternative**: Sketch what a single-server implementation would look like. What would be different?

12. **Different Split**: How else could you have divided the functionality? What would change?

## Common Pitfalls to Avoid

### 1. Too Much Coupling

**Bad**: Server A directly calls Server B

```python
# Don't do this
def tool_in_server_a():
    result_from_b = call_server_b()  # Direct dependency!
```

**Good**: Servers are independent, Claude orchestrates

```python
# Server A and B are independent
# Claude/user coordinates them in conversation
```

### 2. Unclear Boundaries

**Bad**: Each server does a little of everything

```
Server 1: Read file, parse, format, write
Server 2: Read file, parse, transform, write
Server 3: Read file, validate, write
```

**Good**: Each server has clear responsibility

```
Server 1: File I/O only
Server 2: Data transformation only  
Server 3: Validation only
```

### 3. Monolithic Tools

**Bad**: One tool that does everything

```python
Tool(name="do_everything", description="Does the whole workflow")
```

**Good**: Focused, composable tools

```python
Tool(name="fetch_data", ...)
Tool(name="transform_data", ...)
Tool(name="export_data", ...)
```

### 4. Ignoring Failure Modes

**Bad**: Assume everything works

```python
data = fetch_from_api()  # What if this fails?
result = process(data)    # Now what?
```

**Good**: Handle failures gracefully

```python
try:
    data = fetch_from_api()
except APIError as e:
    return [TextContent(type="text", text=f"Failed to fetch: {e}")]
```

### 5. Over-Engineering

**Bad**: 10 servers for a simple task

**Good**: Use as many servers as needed, no more

Ask: "Does this split make the system simpler or more complex?"

## Advanced Extensions

If you finish early, try these enhancements:

### 1. Shared Configuration

Create a shared config file that multiple servers read:

```json
{
  "workspace": "/path/to/project",
  "log_level": "INFO",
  "cache_enabled": true
}
```

Each server reads this on startup.

### 2. State Coordination

Implement a simple way for servers to share state:

- Shared file-based state
- Environment variables
- Temporary files with agreed naming

### 3. Health Checks

Add a health check tool to each server:

```python
Tool(
    name="health_check",
    description="Check if server is operating normally"
)
```

### 4. Metrics and Logging

Add consistent logging across all servers:

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='[%(name)s] %(levelname)s: %(message)s'
)

logger = logging.getLogger("server-name")
```

### 5. Configuration Validation

Create a script that validates your full multi-server configuration:

```python
# validate_config.py
def validate_servers():
    # Check all servers start
    # Verify tools are registered
    # Test basic workflows
```

## Example Solution Structure

```
multi-server-challenge/
├── servers/
│   ├── server1_name.py
│   ├── server2_name.py
│   └── server3_name.py
├── config/
│   ├── cline_mcp_settings.json
│   └── shared_config.json (optional)
├── tests/
│   ├── test_server1.py
│   ├── test_server2.py
│   ├── test_server3.py
│   └── test_integration.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── WORKFLOWS.md
├── README.md
└── requirements.txt
```

## Resources

### Helpful Examples

- **Module 06 examples/**: See `github_server.py`, `git_server.py`, etc.
- **Module 04 examples/**: Review `combined_server.py` for tool patterns
- **Tutorial 1**: Review Cursor IDE integration

### Debugging Tips

1. **Test servers individually first** before configuring together
2. **Check Cursor IDE logs** for startup errors
3. **Use MCP Inspector** to verify each server
4. **Add logging** to understand orchestration flow
5. **Start simple** then add complexity

### Questions?

**Ask Claude** (via Cline):

- "How should I split responsibilities between these servers?"
- "What's a good boundary between X and Y functionality?"
- "Help me debug why servers aren't coordinating correctly"

**Remember**: This is about design thinking as much as coding!

## Submission Checklist

Before considering this challenge complete:

- [ ] Design document created and thorough
- [ ] All servers implemented and tested independently
- [ ] Configuration file created and valid
- [ ] Multi-server workflows tested in Cursor IDE
- [ ] Architecture documentation written
- [ ] Evaluation questions answered
- [ ] Code is clean, documented, and follows best practices
- [ ] Trade-offs and limitations documented honestly

## What You've Learned

After completing this challenge, you understand:

1. **When to use multiple servers** vs a single server
2. **How to design server boundaries** and responsibilities
3. **Patterns for server coordination** through orchestration
4. **Real-world complexity** of multi-server systems
5. **Trade-offs and design decisions** in architecture
6. **Configuration and deployment** of complex systems

This is the kind of architectural thinking needed for production MCP deployments!

## Next Steps

- Try **Challenge 2** to integrate with a real external API
- Review **Module 07** for security considerations across multiple servers
- Explore **Module 08** for debugging multi-server systems
- Consider **combining your servers** with others from the examples

You're now ready to design and build sophisticated MCP integrations for real-world use cases!

