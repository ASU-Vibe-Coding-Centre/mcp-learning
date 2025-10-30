# Module 04 Checkpoint: Advanced MCP Features

This checkpoint validates your understanding of advanced MCP server features: streaming, resources, and prompts. Complete all sections to ensure you're ready for real-world integrations.

## Purpose

This checkpoint helps you:

1. Verify understanding of advanced MCP primitives
2. Confirm you can implement streaming, resources, and prompts
3. Assess ability to combine features effectively
4. Prepare for production-ready server development

## Estimated Time

60-75 minutes

## Prerequisites

Before starting, you should have:

- Completed Module 03 (Basic MCP Server)
- Completed Tutorials 1 and 2
- Attempted at least one challenge
- Reviewed all example servers
- Tested advanced features with MCP Inspector

---

## Part 1: Concept Review

Answer these questions to check your conceptual understanding.

### Question 1: Primitives

**Q:** What are the three core MCP primitives, and what is each one used for?

<details>
<summary>Click to reveal answer</summary>

1. **Tools**: Perform actions or computations (e.g., `calculate()`, `send_email()`)
2. **Resources**: Provide data for context (e.g., `file:///docs/api.md`)
3. **Prompts**: Offer reusable templates for interactions (e.g., `code_review`)

**Key Distinction:**
- **Tools** = actions with side effects
- **Resources** = read-only data access
- **Prompts** = guidance and workflows
</details>

### Question 2: Resources vs Tools

**Q:** A user asks: "What does the API documentation say about authentication?" Should you use a tool or a resource? Why?

<details>
<summary>Click to reveal answer</summary>

**Use a Resource.**

Rationale:
- The AI needs to **read** documentation (data access)
- No action is being performed
- Documentation is static content for context
- A resource like `file:///docs/api-authentication.md` is appropriate

A tool would be appropriate if the request was: "Generate an authentication token" (action with side effect).

**Rule of Thumb:**
- "What does X say?" → Resource
- "Do X" → Tool
</details>

### Question 3: Streaming Purpose

**Q:** When should you implement streaming in an MCP tool?

<details>
<summary>Click to reveal answer</summary>

Implement streaming when:

1. **Long operations**: Taking more than a few seconds
2. **Large datasets**: Processing many items (files, database rows)
3. **Multi-step processes**: Operations with distinct phases
4. **User experience**: When appearing "frozen" would be confusing

**Don't stream when:**
- Operation completes in < 2 seconds
- No clear progress to report
- Overhead outweighs benefits

**Example Good Cases:**
- Processing 1000 files
- Querying database with 10,000 rows
- Multi-step data transformation
- External API calls in sequence

**Example Bad Cases:**
- Simple calculation
- Single file read
- Quick database lookup
</details>

### Question 4: Progress Updates

**Q:** You're processing 10,000 items. How often should you send progress updates?

<details>
<summary>Click to reveal answer</summary>

**Best Practice: Time-based OR count-based, whichever comes first**

```python
# Update every 100 items OR every 1 second
if (count % 100 == 0) or (time.time() - last_update >= 1.0):
    send_progress_update()
```

**Rationale:**
- **Too frequent** (every item): Network overhead, performance impact
- **Too rare** (every 1000 items): Appears frozen
- **Time-based minimum**: Ensures regular feedback even with slow items
- **Count-based maximum**: Prevents flooding with fast items

**Typical Values:**
- Small items (< 100ms each): Every 100-500 items
- Large items (> 1s each): Every 10-50 items
- Time threshold: 1-2 seconds
</details>

### Question 5: Resource URIs

**Q:** What makes a good resource URI scheme?

<details>
<summary>Click to reveal answer</summary>

**Good URI schemes are:**

1. **Consistent**: Follow a pattern across all resources
2. **Descriptive**: Self-documenting structure
3. **Hierarchical**: Reflect logical organization
4. **Stable**: Don't change when content updates

**Examples:**

**Good:**
```
file:///docs/api/authentication.md
file:///config/database.json
api://github/repos/owner/repo
```

**Bad:**
```
file:///1
resource://xyz
file:///tmp/random_name_123.txt
```

**Best Practices:**
- Use standard schemes (`file://`, `http://`, custom like `api://`)
- Include path structure that makes sense
- Avoid temporary or generated IDs when possible
- Make URIs guessable from templates
</details>

### Question 6: Resource Templates

**Q:** What's the difference between listing resources and providing resource templates?

<details>
<summary>Click to reveal answer</summary>

**list_resources()**: Returns actual, specific resources
```python
Resource(uri="file:///post-1.md", ...)
Resource(uri="file:///post-2.md", ...)
Resource(uri="file:///post-3.md", ...)
```

**list_resource_templates()**: Returns patterns for discovering resources
```python
ResourceTemplate(uriTemplate="file:///post-{id}.md", ...)
```

**When to use each:**

**List Resources:**
- Enumerate known, fixed resources
- Provide metadata-rich catalog
- Limited, well-defined set

**Templates:**
- Enable dynamic discovery
- Handle large or infinite sets
- Allow clients to construct URIs
- Reduce server memory/processing

**Example:**
- **List**: All modules in a course (fixed: 01-07)
- **Template**: Any file in project (`file:///{path}`)
</details>

### Question 7: Prompts

**Q:** What makes a prompt template effective?

<details>
<summary>Click to reveal answer</summary>

**Effective prompts:**

1. **Clear Purpose**: Specific task or workflow
2. **Parameterized**: Accept relevant arguments
3. **Structured**: Well-organized sections
4. **Context-Rich**: Include necessary background
5. **Actionable**: Guide to concrete actions
6. **Expert Knowledge**: Encode best practices

**Example Structure:**
```
1. Clear objective statement
2. Context and constraints
3. Step-by-step process
4. Specific criteria or checklist
5. Output format guidance
6. Examples (when helpful)
```

**Bad Prompt:**
"Review this code."

**Good Prompt:**
"Review this {language} code for:
1. Correctness: Logic errors?
2. Security: Vulnerabilities?
3. Performance: Inefficiencies?
4. Style: Best practices?
5. Maintainability: Clarity?

For each issue, provide:
- Severity level
- Specific location
- Clear explanation
- Fix suggestion"
</details>

### Question 8: Capability Negotiation

**Q:** What happens during MCP capability negotiation?

<details>
<summary>Click to reveal answer</summary>

**During initialization:**

1. **Client sends `initialize` request** with its capabilities
2. **Server responds** with its capabilities
3. **Client sends `initialized` notification** confirming

**Server declares:**
```python
{
    "capabilities": {
        "tools": {},           # Provides tools
        "resources": {         # Provides resources
            "subscribe": true  # Supports subscriptions
        },
        "prompts": {}          # Provides prompts
    }
}
```

**Why it matters:**
- Forward compatibility (new features don't break old clients)
- Feature detection (clients know what's available)
- Graceful degradation (works with varying client capabilities)

**In Python SDK:**
The SDK infers capabilities from which handlers you implement:
- Implement `list_tools()` → tools capability
- Implement `list_resources()` → resources capability
- Implement `list_prompts()` → prompts capability
</details>

### Question 9: Combining Features

**Q:** You're building a documentation assistant. How would you use tools, resources, and prompts together?

<details>
<summary>Click to reveal answer</summary>

**Effective Combination:**

**Resources:**
- `file:///docs/**/*.md` - Documentation files
- `file:///examples/**/*.py` - Code examples
- `api://docserver/search` - Search index

**Tools:**
- `search_docs(query)` - Find relevant documentation
- `validate_example(code)` - Check code correctness
- `create_doc(topic, content)` - Add new documentation

**Prompts:**
- `write_api_docs(endpoint)` - Template for API documentation
- `explain_concept(topic, level)` - Explanation workflow
- `troubleshoot_error(error)` - Debugging guide

**Workflow Example:**

1. User: "How do I authenticate?"
2. AI uses `search_docs("authentication")` tool
3. AI reads `file:///docs/auth-guide.md` resource
4. AI applies `explain_concept("authentication", "beginner")` prompt
5. AI provides comprehensive, well-structured answer

**Key Insight:** Each primitive serves a distinct role, and they work together to provide comprehensive functionality.
</details>

### Question 10: Security

**Q:** What security considerations are important when implementing resources?

<details>
<summary>Click to reveal answer</summary>

**Critical Security Checks:**

1. **Path Traversal Prevention:**
```python
# Validate path is within allowed directory
if not file_path.resolve().is_relative_to(BASE_DIR.resolve()):
    raise PermissionError("Access denied")
```

2. **URI Validation:**
```python
# Only accept expected schemes
if not uri.startswith("file:///"):
    raise ValueError("Invalid URI scheme")
```

3. **File Type Restrictions:**
```python
# Only serve text files, not binaries
allowed_extensions = ['.md', '.txt', '.json', '.py']
if file_path.suffix not in allowed_extensions:
    raise ValueError("File type not allowed")
```

4. **Access Control:**
```python
# Check permissions
if not has_permission(user, file_path):
    raise PermissionError("Access denied")
```

5. **Error Message Safety:**
```python
# Don't leak path information
# Bad: "File not found: /Users/admin/secrets.txt"
# Good: "Resource not found"
```

**Never trust user input** - always validate paths, URIs, and access permissions.
</details>

---

## Part 2: Practical Exercise

Build a working server that demonstrates all three advanced primitives.

### Exercise: Project Analyzer Server

**Requirements:**

Create an MCP server that analyzes a code project with:

**Tools (with streaming):**
1. `analyze_directory(path)` - Analyze all files in directory with progress
2. `count_lines(path)` - Count lines across project files

**Resources:**
1. List all Python files in a directory
2. Provide resource template for any file: `file:///{path}`

**Prompts:**
1. `code_review_file(file_path)` - Prompt for reviewing a specific file

**Specifications:**

- **Streaming**: `analyze_directory` must stream progress every 5 files
- **Resources**: List at least 5 Python files with accurate URIs
- **Resource Reading**: Read file content when requested
- **Prompts**: Provide structured code review template
- **Security**: Validate all paths to prevent directory traversal

**Starter Template:**

```python
#!/usr/bin/env python3
"""
Checkpoint Exercise: Project Analyzer Server
"""

import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, Resource, ResourceTemplate, 
    Prompt, PromptArgument, PromptMessage,
    TextContent
)

app = Server("project-analyzer")
PROJECT_ROOT = Path(__file__).parent.parent

# TODO: Implement handlers

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Time Limit:** 45 minutes

**Testing:**

1. Run with MCP Inspector
2. List tools, resources, prompts
3. Call `analyze_directory` with a test directory
4. Read a resource
5. Get the `code_review_file` prompt

### Success Criteria

Your server should:

- [ ] Start without errors
- [ ] Declare all three capability types
- [ ] List 2 tools with proper schemas
- [ ] List at least 5 resources
- [ ] Provide at least 1 resource template
- [ ] List 1 prompt with arguments
- [ ] Stream progress during analysis
- [ ] Read file content correctly
- [ ] Return formatted prompt messages
- [ ] Handle errors gracefully
- [ ] Include security checks

---

## Part 3: Debugging Scenarios

Identify and fix issues in these code snippets.

### Scenario 1: Streaming Not Working

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "process_files":
        files = get_files()
        
        for i, f in enumerate(files):
            process(f)
            # Send progress
            print(f"Progress: {i+1}/{len(files)}")
        
        return [TextContent(type="text", text="Done")]
```

**Q:** Why doesn't progress appear in the client?

<details>
<summary>Click to reveal answer</summary>

**Problem:** Using `print()` instead of MCP progress notifications.

**Fix:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict, request_context: Any) -> list[TextContent]:
    if name == "process_files":
        files = get_files()
        progress_token = f"process-{id(request_context)}"
        
        for i, f in enumerate(files):
            process(f)
            
            # Send MCP progress notification (conceptual)
            # await request_context.send_progress(
            #     progress_token=progress_token,
            #     progress=i+1,
            #     total=len(files)
            # )
            
            # Allow other tasks to run
            await asyncio.sleep(0)
        
        return [TextContent(type="text", text="Done")]
```

**Key Changes:**
1. Accept `request_context` parameter
2. Use MCP progress API (not print)
3. Include `await asyncio.sleep(0)` to yield control
</details>

### Scenario 2: Resource Not Found

```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    path = uri.replace("file:///", "")
    with open(path, 'r') as f:
        return f.read()
```

**Q:** Resources are listed but reading fails. Why?

<details>
<summary>Click to reveal answer</summary>

**Problems:**

1. **Incomplete URI parsing**: `replace()` doesn't handle all cases
2. **No path validation**: Security vulnerability
3. **No error handling**: Crashes on missing files
4. **Absolute path assumption**: May not work on all systems

**Fix:**
```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    # Validate URI scheme
    if not uri.startswith("file:///"):
        raise ValueError(f"Invalid URI: {uri}")
    
    # Properly extract path
    path_str = uri[8:]  # Remove "file:///"
    file_path = PROJECT_ROOT / path_str
    
    # Security: validate path is within PROJECT_ROOT
    try:
        file_path.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        raise PermissionError("Access denied")
    
    # Check file exists
    if not file_path.exists():
        raise ValueError(f"Resource not found: {uri}")
    
    # Read with error handling
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError("Binary file cannot be read as text")
```
</details>

### Scenario 3: Prompt Not Helpful

```python
@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    if name == "review_code":
        code = arguments["code"]
        return [PromptMessage(
            role="user",
            content={"type": "text", "text": f"Review: {code}"}
        )]
```

**Q:** Prompt works but AI responses are generic. What's wrong?

<details>
<summary>Click to reveal answer</summary>

**Problem:** Prompt lacks structure, guidance, and specificity.

**Fix:**
```python
@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    if name == "review_code":
        code = arguments["code"]
        language = arguments.get("language", "python")
        
        return [PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"""Please conduct a comprehensive code review.

Code to review ({language}):
```{language}
{code}
```

Review across these dimensions:

1. CORRECTNESS
   - Are there any bugs or logic errors?
   - Will it work as intended?
   - Are edge cases handled?

2. SECURITY
   - Any security vulnerabilities?
   - Is input properly validated?
   - Are there injection risks?

3. PERFORMANCE
   - Any obvious inefficiencies?
   - Appropriate algorithmic complexity?

4. READABILITY
   - Clear variable/function names?
   - Proper structure and organization?
   - Adequate comments?

5. BEST PRACTICES
   - Follows {language} conventions?
   - Good error handling?
   - Maintainable?

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Specific location
- Clear explanation
- Concrete fix suggestion

Also note what the code does well."""
            }
        )]
```

**Improvements:**
- Structured sections
- Clear criteria
- Specific guidance
- Expected output format
- Context (language)
</details>

---

## Part 4: Self-Assessment

Rate your confidence (1-5, where 5 is very confident):

### Streaming
- [ ] I understand when to use streaming
- [ ] I can implement progress notifications correctly
- [ ] I know how to balance update frequency
- [ ] I can test streaming with MCP Inspector

### Resources
- [ ] I understand resources vs tools distinction
- [ ] I can design good URI schemes
- [ ] I know when to use resource templates
- [ ] I can implement secure resource access

### Prompts
- [ ] I understand prompt purpose and benefits
- [ ] I can create effective prompt templates
- [ ] I know how to structure prompts well
- [ ] I can parameterize prompts appropriately

### Integration
- [ ] I can combine all three primitives effectively
- [ ] I understand capability negotiation
- [ ] I can build production-ready servers
- [ ] I'm ready for Module 05 (Integration Patterns)

**If any rating is < 3:** Review that section of Module 04 before proceeding.

---

## Part 5: Next Steps

### Before Moving to Module 05

Ensure you can:

1. **Build complete servers** with streaming, resources, and prompts
2. **Test thoroughly** using MCP Inspector
3. **Handle errors** gracefully across all features
4. **Implement security** properly (especially for resources)
5. **Design cohesive systems** where features complement each other

### Recommended Practice

If you need more practice:

1. Complete any remaining challenges
2. Review all example servers
3. Build a server combining features for your own use case
4. Test extensively with real AI clients
5. Consider security implications in your implementations

### Module 05 Preview

Next, you'll learn:

- Integrating with Claude Desktop
- Using MCP Inspector for debugging
- Real-world patterns (GitHub, Git, APIs)
- Multi-server architectures
- Production deployment

---

## Completion Certificate

Once you've successfully:

- ✓ Answered all concept questions correctly
- ✓ Completed the practical exercise
- ✓ Debugged all scenarios
- ✓ Rated yourself 3+ on all self-assessment items

**You're ready for Module 05: Integration Patterns!**

Keep your checkpoint exercise code - you'll enhance it in the next module.

---

**Well done on completing the advanced features module!**

You now have the knowledge to build sophisticated MCP servers that leverage all three core primitives effectively.

