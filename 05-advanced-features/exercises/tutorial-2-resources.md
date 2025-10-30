# Tutorial 2: Exposing Data as Resources

## Overview

In this tutorial, you'll learn how to expose data as MCP resources. Resources allow AI models to read and understand context from your data sources without executing actions. This is fundamentally different from tools, which perform actions.

**Estimated Time:** 60 minutes

**Difficulty:** Intermediate

**Prerequisites:**
- Completed Module 03 (Basic MCP Server)
- Understanding of URIs and file paths
- Familiarity with JSON Schema

## Learning Objectives

By the end of this tutorial, you will be able to:

1. Understand the difference between resources and tools
2. Define resources with URIs, names, descriptions, and MIME types
3. Implement resource templates for dynamic discovery
4. Read and return resource content
5. Implement security checks for resource access
6. Test resources with MCP Inspector

## Scenario

You'll build a **Documentation Resource Server** that exposes project documentation as resources. This allows AI models to:

- Read documentation for context
- Reference configuration files
- Access code examples
- Understand project structure

This is a common pattern for AI-assisted development tools.

## Resources vs Tools: Key Differences

Before we begin, understand this crucial distinction:

| Aspect | Tools | Resources |
|--------|-------|-----------|
| **Purpose** | Perform actions | Provide data |
| **Invocation** | AI calls with arguments | AI reads for context |
| **Side Effects** | Can modify state | Read-only |
| **When Used** | "Do something" | "What does this say?" |
| **Example** | `create_file()` | `file:///docs/README.md` |

**Example:**
- **Tool**: "Create a new user account" → `create_user(name, email)`
- **Resource**: "What are the user requirements?" → Read `file:///docs/user-requirements.md`

## Step 1: Set Up Your Server File

Create `documentation_server.py`:

```python
#!/usr/bin/env python3
"""
Documentation Resource Server

Exposes project documentation as MCP resources.
"""

import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceTemplate, TextContent, Tool

# Server instance
app = Server("documentation-resource-server")

# Define project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "resources"

# We'll add handlers here

async def main():
    """Run the MCP server."""
    print("Starting Documentation Resource Server...")
    print(f"Serving documentation from: {DOCS_DIR}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Implement list_resources

Resources start with discovery. Implement the handler that lists available resources:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available resources.
    
    This tells clients what documentation is available.
    Each resource needs:
    - URI: Unique identifier (file:// for files)
    - Name: Human-readable name
    - Description: What this resource contains
    - MIME Type: Content type
    """
    resources = []
    
    # Find all markdown files in docs directory
    if DOCS_DIR.exists() and DOCS_DIR.is_dir():
        md_files = sorted(DOCS_DIR.rglob("*.md"))
        
        for md_file in md_files:
            # Create relative path from project root
            try:
                relative_path = md_file.relative_to(PROJECT_ROOT)
                
                # Create resource
                resources.append(Resource(
                    uri=f"file:///{relative_path.as_posix()}",
                    name=f"Documentation: {md_file.stem}",
                    description=f"Project documentation: {relative_path}",
                    mimeType="text/markdown"
                ))
            except ValueError:
                # Skip files outside project root
                continue
    
    # Add key project files
    key_files = [
        ("README.md", "Main project README", "text/markdown"),
        ("LEARNING_PATH.md", "Learning path guide", "text/markdown"),
        ("QUICK_START.md", "Quick start guide", "text/markdown"),
    ]
    
    for filename, description, mime_type in key_files:
        file_path = PROJECT_ROOT / filename
        if file_path.exists():
            resources.append(Resource(
                uri=f"file:///{filename}",
                name=filename,
                description=description,
                mimeType=mime_type
            ))
    
    return resources
```

**Key Points:**

- **URI Format**: `file:///path/to/file` (three slashes for absolute paths)
- **Relative Paths**: Paths are relative to project root
- **MIME Types**: Help clients understand content format
- **Descriptive Names**: Help AI understand what each resource contains

## Step 3: Implement read_resource

Now implement the handler that reads resource content:

```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read the content of a resource.
    
    Args:
        uri: Resource URI (e.g., "file:///README.md")
    
    Returns:
        Resource content as string
    
    Raises:
        ValueError: If resource not found or invalid URI
    """
    # Validate URI format
    if not uri.startswith("file:///"):
        raise ValueError(f"Invalid URI scheme. Expected 'file:///', got '{uri}'")
    
    # Extract path from URI
    # Remove 'file:///' prefix (7 characters)
    path_str = uri[8:]
    
    # Construct full path
    file_path = PROJECT_ROOT / path_str
    
    # SECURITY: Ensure path is within PROJECT_ROOT
    # This prevents directory traversal attacks
    try:
        file_path.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        raise PermissionError(f"Access denied: {uri} is outside project directory")
    
    # Check file exists
    if not file_path.exists():
        raise ValueError(f"Resource not found: {uri}")
    
    if not file_path.is_file():
        raise ValueError(f"Resource is not a file: {uri}")
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        raise ValueError(f"Resource is not a text file: {uri}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading: {uri}")
```

**Security is Critical:**

1. **Validate URI scheme**: Only accept `file://`
2. **Check path boundaries**: Prevent `../../etc/passwd` attacks
3. **Verify file exists**: Clear error messages
4. **Handle encoding**: Gracefully handle binary files

## Step 4: Add Resource Templates

Templates allow dynamic resource discovery:

```python
@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """
    List resource templates for dynamic discovery.
    
    Templates use URI patterns with variables.
    Clients can substitute values to construct URIs.
    """
    return [
        ResourceTemplate(
            uriTemplate="file:///{path}",
            name="Project Files",
            description=(
                "Access any file in the project by path. "
                "Path should be relative to project root. "
                "Example: file:///03-basic-mcp-server/README.md"
            ),
            mimeType="text/plain"  # Generic, actual type determined at read time
        ),
        ResourceTemplate(
            uriTemplate="file:///resources/{category}/{filename}",
            name="Resource Files by Category",
            description=(
                "Access resource files by category. "
                "Categories: cheatsheets, prompts, references. "
                "Example: file:///resources/cheatsheets/mcp-cheatsheet.md"
            ),
            mimeType="text/markdown"
        ),
        ResourceTemplate(
            uriTemplate="file:///{module}/README.md",
            name="Module README Files",
            description=(
                "Access README for any module. "
                "Modules: 01-introduction, 02-environment-setup, 03-basic-mcp-server, etc. "
                "Example: file:///03-basic-mcp-server/README.md"
            ),
            mimeType="text/markdown"
        )
    ]
```

**Template Benefits:**

- **Scalability**: Don't need to list every possible resource
- **Discovery**: Clients can construct URIs based on patterns
- **Flexibility**: Works with dynamic content

**Variables in Templates:**
- `{path}`: Any file path
- `{category}`: Category name
- `{filename}`: File name
- `{module}`: Module directory name

## Step 5: Add Helper Tools

While resources are read-only, tools can help discover them:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List tools for resource discovery."""
    return [
        Tool(
            name="search_documentation",
            description="Search for documentation files containing specific text",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for in documentation"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="list_categories",
            description="List available documentation categories",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for resource discovery."""
    
    if name == "search_documentation":
        query = arguments["query"].lower()
        results = []
        
        # Search markdown files
        if DOCS_DIR.exists():
            for md_file in DOCS_DIR.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if query in content.lower():
                        relative_path = md_file.relative_to(PROJECT_ROOT)
                        results.append({
                            "file": str(relative_path),
                            "uri": f"file:///{relative_path.as_posix()}"
                        })
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No documentation found containing '{query}'"
            )]
        
        return [TextContent(
            type="text",
            text=f"""Found {len(results)} documentation files containing '{query}':

{chr(10).join(f"  - {r['file']}" for r in results)}

Use read_resource() to read any file by its URI.
"""
        )]
    
    elif name == "list_categories":
        categories = set()
        
        if DOCS_DIR.exists():
            for item in DOCS_DIR.iterdir():
                if item.is_dir():
                    categories.add(item.name)
        
        return [TextContent(
            type="text",
            text=f"""Documentation Categories:

{chr(10).join(f"  - {cat}" for cat in sorted(categories))}

Use resource template: file:///resources/{{category}}/{{filename}}
"""
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]
```

## Step 6: Test Your Server

Test the server:

```bash
# Run directly
python documentation_server.py
```

### Test with MCP Inspector

```bash
mcp-inspector python documentation_server.py
```

In the Inspector:

1. **List Resources**: See all available documentation
2. **Read Resource**: Try reading a resource:
   - URI: `file:///README.md`
   - Verify content is returned
3. **List Templates**: Check available patterns
4. **Use Tools**: Search for documentation

## Step 7: Enhance with Metadata

Add more useful metadata to resources:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    """Enhanced resource listing with metadata."""
    resources = []
    
    if DOCS_DIR.exists() and DOCS_DIR.is_dir():
        md_files = sorted(DOCS_DIR.rglob("*.md"))
        
        for md_file in md_files:
            try:
                relative_path = md_file.relative_to(PROJECT_ROOT)
                
                # Get file size for description
                size_kb = md_file.stat().st_size / 1024
                
                # Read first line for better description
                first_line = ""
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        # Remove markdown header syntax
                        first_line = first_line.lstrip('#').strip()
                except:
                    pass
                
                description = f"{relative_path}"
                if first_line:
                    description = f"{first_line} ({relative_path})"
                
                resources.append(Resource(
                    uri=f"file:///{relative_path.as_posix()}",
                    name=md_file.stem.replace('-', ' ').title(),
                    description=description,
                    mimeType="text/markdown"
                ))
            except ValueError:
                continue
    
    return resources
```

## Challenge Extensions

### Challenge 1: Add JSON Resources

Expose configuration files as resources:

```python
# Find and expose JSON files
for json_file in PROJECT_ROOT.glob("*.json"):
    resources.append(Resource(
        uri=f"file:///{json_file.name}",
        name=f"Config: {json_file.stem}",
        description=f"Configuration: {json_file.name}",
        mimeType="application/json"
    ))
```

### Challenge 2: Add Content Preview

Include content preview in description:

```python
# Read first 100 characters
with open(file_path, 'r') as f:
    preview = f.read(100)

description = f"{relative_path}: {preview}..."
```

### Challenge 3: Implement Subscriptions

Allow clients to subscribe to resource changes (advanced):

```python
@app.subscribe_resource()
async def subscribe_resource(uri: str):
    """Notify clients when resource changes."""
    # Watch file for changes
    # Send notifications when modified
    pass
```

### Challenge 4: Add Binary Resources

Support image resources:

```python
# For images, return base64 encoded data
if mime_type.startswith("image/"):
    with open(file_path, 'rb') as f:
        import base64
        content = base64.b64encode(f.read()).decode('utf-8')
    return content
```

## Testing Checklist

Verify your implementation:

- [ ] Lists all markdown files in docs directory
- [ ] Reads resource content correctly
- [ ] Handles missing resources with clear errors
- [ ] Prevents directory traversal attacks
- [ ] Resource templates are accessible
- [ ] Tools help discover resources
- [ ] MIME types are correct
- [ ] URIs follow correct format

## Common Issues and Solutions

### Issue: "Resource not found" for Existing Files

**Problem:** Files exist but read_resource fails.

**Solution:** Check:
- URI format is correct (`file:///` with three slashes)
- Path is relative to PROJECT_ROOT
- No extra slashes or incorrect separators
- File permissions allow reading

**Debug:**
```python
print(f"Looking for: {file_path}")
print(f"Exists: {file_path.exists()}")
print(f"Is file: {file_path.is_file()}")
```

### Issue: Security Check Failing

**Problem:** legitimate files are blocked.

**Solution:** Verify path resolution:
```python
print(f"File path: {file_path.resolve()}")
print(f"Project root: {PROJECT_ROOT.resolve()}")
print(f"Is relative: {file_path.resolve().is_relative_to(PROJECT_ROOT.resolve())}")
```

### Issue: Templates Not Working

**Problem:** Template variables aren't substituted.

**Solution:** Templates are discovered by clients, not the server. The server just needs to:
1. List templates with `list_resource_templates()`
2. Handle any valid URI in `read_resource()`

## Understanding Resource Flow

Here's how resources are used:

```
1. CLIENT DISCOVERY
   Client: list_resources()
   Server: Returns list of Resource objects
   
2. CLIENT READS RESOURCE
   Client: read_resource("file:///README.md")
   Server: Validates URI, reads file, returns content
   
3. AI USES CONTENT
   AI reads resource content to understand context
   AI uses this knowledge to answer user questions
```

**Example Interaction:**

```
User: "What are the learning objectives for Module 03?"

AI: 
  1. Calls list_resources()
  2. Finds "file:///03-basic-mcp-server/README.md"
  3. Calls read_resource("file:///03-basic-mcp-server/README.md")
  4. Reads content
  5. Extracts learning objectives section
  6. Answers user's question with specific details
```

## Key Takeaways

1. **Resources ≠ Tools**: Resources provide data, tools perform actions
2. **URIs are Identifiers**: Use consistent, descriptive URI schemes
3. **Security Matters**: Always validate paths and prevent traversal
4. **MIME Types Help**: Specify correct content types
5. **Templates Enable Scale**: Dynamic access without listing everything
6. **Discovery Tools**: Tools can help find relevant resources

## Next Steps

- Try Challenge 1 (SQLite with Streaming)
- Complete Challenge 2 (API Resources)
- Review resource_server.py example for more patterns
- Build a server that combines resources with tools

## Solution

A complete solution is available in `solutions/tutorial-2-solution.py`.

Compare your implementation to see additional patterns and optimizations.

Excellent work! You now understand how to expose data as MCP resources.

