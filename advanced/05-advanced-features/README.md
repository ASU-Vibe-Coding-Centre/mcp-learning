# Module 05: Advanced MCP Features

> **Advanced Content** - This module contains in-depth, comprehensive material. New to MCP? Start with the [simplified learning path](../../01-introduction-quickstart/) for a beginner-friendly introduction.

Welcome to advanced MCP server development. In this module, you'll expand beyond basic tools to implement sophisticated capabilities: streaming responses for long-running operations, resources for exposing data, and prompts for reusable interaction templates.

## Module Overview

Building on the foundation of basic MCP servers from Module 03, this module explores three additional primitives that make MCP servers truly powerful: **streaming**, **resources**, and **prompts**. These features transform simple tool servers into comprehensive integration platforms that can handle complex, real-world scenarios.

By the end of this module, you'll understand how to build servers that not only execute functions but also provide structured access to data, stream progress updates for long operations, and offer templated workflows for common tasks.

## Learning Objectives

By completing this module, you will be able to:

1. **Implement Streaming Responses**
   - Understand when and why to use streaming
   - Send progress notifications during long-running operations
   - Provide incremental results for better user experience
   - Handle streaming in database queries and file processing

2. **Expose Resources**
   - Define resources with URIs and metadata
   - Implement resource templates for dynamic discovery
   - Provide read access to files, databases, and APIs
   - Understand the difference between tools (actions) and resources (data)

3. **Create Prompt Templates**
   - Build reusable prompts with variable substitution
   - Design prompts that encode expert knowledge
   - Structure multi-turn conversations
   - Provide context and guidance for common tasks

4. **Combine All Features**
   - Build servers that integrate tools, resources, and prompts
   - Understand how these primitives complement each other
   - Design cohesive server capabilities
   - Implement real-world integration patterns

5. **Negotiate Capabilities**
   - Declare server capabilities during initialization
   - Understand feature detection and capability negotiation
   - Build servers that gracefully handle capability differences

## What You'll Build

Throughout this module, you'll create increasingly sophisticated servers:

1. **Streaming Server** - Database query server with streaming results
2. **Resource Server** - File system server exposing files as resources
3. **Prompt Server** - Server providing templates for code review and debugging
4. **Combined Server** - Full-featured server demonstrating all primitives together

Each implementation demonstrates real-world patterns you can apply to your own integrations.

## Prerequisites

Before starting this module, ensure you have:

- Completed Module 03 (Basic MCP Server Implementation)
- Solid understanding of basic MCP server patterns
- Ability to implement tools with proper schemas
- Familiarity with async/await in Python
- Understanding of JSON-RPC communication flow

## Module Structure

### Core Concepts

#### 1. Streaming Responses

**What is Streaming?**

Streaming allows servers to send progress updates and incremental results during long-running operations, rather than making clients wait for a complete response.

**Why Stream?**

- **User Experience**: Show progress instead of appearing frozen
- **Large Datasets**: Return results incrementally rather than all at once
- **Long Operations**: Provide feedback during multi-step processes
- **Transparency**: Let users see what's happening in real-time

**When to Use Streaming:**

- Database queries returning many rows
- File processing operations
- External API calls with multiple requests
- Long computations with intermediate results
- Any operation taking more than a few seconds

**How Streaming Works in MCP:**

MCP uses JSON-RPC notifications to send progress updates:

```python
# During a long-running tool call, send progress notifications
await request_context.send_progress(
    progress_token="query-123",
    progress=50,
    total=100
)

# Continue with incremental results
await request_context.send_progress(
    progress_token="query-123", 
    progress=75,
    total=100
)

# Finally return the complete result
return [TextContent(type="text", text="Operation complete")]
```

**Key Concepts:**

- **Progress Tokens**: Unique identifiers linking progress updates to requests
- **Progress/Total**: Current progress and expected total (optional)
- **Notifications**: One-way messages that don't expect responses
- **Final Result**: Always return a complete result at the end

**Example Use Case - Database Query:**

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict, request_context):
    if name == "query_database":
        query = arguments["query"]
        results = []
        
        # Execute query with cursor
        cursor = await database.execute(query)
        total_rows = await cursor.count()
        
        # Stream results as they're fetched
        for i, row in enumerate(cursor):
            results.append(row)
            
            # Send progress every 100 rows
            if i % 100 == 0:
                await request_context.send_progress(
                    progress_token=f"query-{request_context.request_id}",
                    progress=i,
                    total=total_rows
                )
        
        # Return complete results
        return [TextContent(
            type="text",
            text=json.dumps(results, indent=2)
        )]
```

#### 2. Resources

**What are Resources?**

Resources are data and content that servers expose for LLMs to read and understand. Unlike tools (which perform actions), resources provide information.

**Key Characteristics:**

- **URI-based**: Each resource has a unique URI (e.g., `file:///docs/api.md`)
- **Read-only**: Resources are for reading context, not executing actions
- **Metadata**: Include name, description, and MIME type
- **Templates**: Support patterns for dynamic resource discovery

**Resources vs Tools:**

| Aspect | Tools | Resources |
|--------|-------|-----------|
| **Purpose** | Perform actions | Provide data |
| **Invocation** | Called by AI with arguments | Read by AI for context |
| **Side Effects** | Can modify state | Read-only |
| **Examples** | calculate(), send_email() | Documentation files, config data |
| **Return Value** | Action results | Content (text, JSON, binary) |

**When to Use Resources:**

- **Documentation**: Expose docs for the AI to reference
- **Configuration**: Provide current settings and options
- **Database Schemas**: Let AI understand data structure
- **Sample Data**: Show examples of expected formats
- **Log Files**: Provide debugging context
- **API Definitions**: Expose available endpoints

**Resource Definition:**

```python
from mcp.types import Resource

Resource(
    uri="file:///logs/app.log",
    name="Application Log",
    description="Current application log file with error details",
    mimeType="text/plain"
)
```

**Resource Implementation Pattern:**

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources"""
    return [
        Resource(
            uri="file:///config/settings.json",
            name="Configuration",
            description="Application configuration settings",
            mimeType="application/json"
        ),
        Resource(
            uri="file:///docs/README.md",
            name="Documentation",
            description="Project documentation",
            mimeType="text/markdown"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource by URI"""
    if uri == "file:///config/settings.json":
        with open("config/settings.json") as f:
            return f.read()
    elif uri == "file:///docs/README.md":
        with open("docs/README.md") as f:
            return f.read()
    else:
        raise ValueError(f"Unknown resource: {uri}")
```

**Resource Templates:**

Templates enable dynamic resource discovery using URI patterns:

```python
from mcp.types import ResourceTemplate

ResourceTemplate(
    uriTemplate="file:///{path}",
    name="File System",
    description="Access any file in the workspace",
    mimeType="text/plain"
)
```

Clients can then construct URIs like `file:///src/main.py` dynamically.

#### 3. Prompts

**What are Prompts?**

Prompts are reusable templates that structure interactions with the AI. They encode expert knowledge, best practices, and common workflows into templates that guide AI behavior.

**Why Use Prompts?**

- **Consistency**: Ensure the same approach is used every time
- **Expert Knowledge**: Embed domain expertise into templates
- **Convenience**: Save users from writing detailed instructions
- **Quality**: Well-crafted prompts lead to better AI responses
- **Reusability**: Write once, use many times

**Prompt Characteristics:**

- **Named**: Each prompt has a unique identifier
- **Parameterized**: Accept arguments for customization
- **Structured**: Define clear roles and message sequences
- **Context-Rich**: Include relevant background information

**When to Use Prompts:**

- **Code Review**: Standard checklist and criteria
- **Debugging**: Systematic troubleshooting workflow
- **Documentation**: Consistent documentation style
- **Testing**: Test case generation patterns
- **Refactoring**: Safe refactoring guidelines
- **Analysis**: Structured analytical frameworks

**Prompt Definition:**

```python
from mcp.types import Prompt, PromptArgument

Prompt(
    name="code_review",
    description="Review code for quality, security, and best practices",
    arguments=[
        PromptArgument(
            name="language",
            description="Programming language (python, javascript, etc.)",
            required=True
        ),
        PromptArgument(
            name="code",
            description="The code to review",
            required=True
        )
    ]
)
```

**Prompt Implementation Pattern:**

```python
from mcp.types import PromptMessage

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompt templates"""
    return [
        Prompt(
            name="code_review",
            description="Comprehensive code review",
            arguments=[
                PromptArgument(name="language", required=True),
                PromptArgument(name="code", required=True)
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    """Get a specific prompt with arguments"""
    if name == "code_review":
        language = arguments["language"]
        code = arguments["code"]
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please review the following {language} code for:

1. Correctness: Does it work as intended?
2. Security: Are there any vulnerabilities?
3. Performance: Any obvious inefficiencies?
4. Style: Does it follow {language} best practices?
5. Maintainability: Is it clear and well-structured?

Code to review:
```{language}
{code}
```

Provide specific, actionable feedback for each area."""
                }
            )
        ]
    
    raise ValueError(f"Unknown prompt: {name}")
```

#### 4. Combining All Features

**Cohesive Server Design:**

The most powerful MCP servers combine tools, resources, and prompts to provide comprehensive capabilities:

**Example: Documentation Server**

- **Tools**: 
  - `search_docs(query)` - Search documentation
  - `create_doc(path, content)` - Create new documentation
  
- **Resources**:
  - `file:///docs/{path}` - Access any documentation file
  - `file:///docs/index.json` - Documentation index
  
- **Prompts**:
  - `write_api_docs(endpoint)` - Template for API documentation
  - `explain_concept(topic)` - Structured explanation template

**How They Work Together:**

1. User asks: "How do I use the authentication API?"
2. AI uses `search_docs("authentication")` tool to find relevant docs
3. AI reads `file:///docs/auth/guide.md` resource for details
4. AI applies `explain_concept("authentication")` prompt to structure response
5. User receives comprehensive, well-structured answer

**Design Patterns:**

**Pattern 1: Tools + Resources**
- Tools perform actions
- Resources provide context for those actions
- Example: Git server with `commit` tool + `file:///repo/README.md` resource

**Pattern 2: Prompts + Resources**
- Prompts structure analysis
- Resources provide data to analyze
- Example: Code review prompt + source file resources

**Pattern 3: Tools + Prompts**
- Tools perform operations
- Prompts guide how to use tools effectively
- Example: Database query tool + SQL optimization prompt

**Pattern 4: All Three**
- Comprehensive integration platform
- Example: Development server with file tools, code resources, and development workflow prompts

#### 5. Capability Negotiation

**What is Capability Negotiation?**

During initialization, clients and servers exchange information about what features they support. This allows servers to declare their capabilities and clients to understand what they can use.

**Server Capabilities:**

```python
{
    "capabilities": {
        "tools": {},                    # Server provides tools
        "resources": {
            "subscribe": True,          # Supports resource subscriptions
            "listChanged": True         # Can notify when resource list changes
        },
        "prompts": {
            "listChanged": True         # Can notify when prompt list changes
        },
        "logging": {}                   # Can send log messages
    }
}
```

**Why Capability Negotiation Matters:**

- **Forward Compatibility**: New features don't break old clients
- **Feature Detection**: Clients know what's available
- **Graceful Degradation**: Servers work with varying client capabilities
- **Version Independence**: Protocol can evolve without breaking changes

**Implementation Pattern:**

```python
from mcp.server import Server

# Server automatically handles capability negotiation
server = Server("my-server")

# Capabilities are inferred from which handlers you implement
@server.list_tools()        # Enables "tools" capability
async def list_tools():
    ...

@server.list_resources()    # Enables "resources" capability
async def list_resources():
    ...

@server.list_prompts()      # Enables "prompts" capability
async def list_prompts():
    ...
```

The SDK handles the initialization handshake automatically based on which handlers you provide.

## Development Workflow

When building advanced MCP servers, follow this workflow:

### 1. Design Phase

**Identify the Right Primitives:**

- **Need to perform actions?** → Use tools
- **Need to provide data?** → Use resources
- **Need to guide interactions?** → Use prompts
- **Long operations?** → Add streaming to tools

**Plan Your API:**

- List all tools with their parameters
- Identify data sources for resources
- Define prompts that would be valuable
- Consider how primitives work together

### 2. Implementation Phase

**Start Simple:**

- Implement tools first (most familiar from Module 03)
- Add resources for data access
- Layer on prompts for guidance
- Add streaming to long-running tools

**Incremental Building:**

1. Basic server with one tool
2. Add resource support
3. Implement streaming for appropriate tools
4. Create prompt templates
5. Test integration of all features

### 3. Testing Phase

**Test Each Primitive:**

- **Tools**: Verify correct execution with various inputs
- **Resources**: Confirm all URIs resolve correctly
- **Prompts**: Test argument substitution and message structure
- **Streaming**: Verify progress notifications work properly

**Test Integration:**

- Verify tools can access resources
- Confirm prompts reference appropriate resources
- Check that capabilities are correctly declared

## Best Practices

### Streaming Best Practices

1. **Use Meaningful Progress Tokens**: Make them debuggable
   - Good: `f"query-{query_id}-{timestamp}"`
   - Bad: `"x"`

2. **Balance Update Frequency**: Not too often, not too rare
   - Too frequent: Overhead from many notifications
   - Too rare: Appears frozen to users
   - Good rule: Every 1-2 seconds or every significant step

3. **Provide Total When Possible**: Helps clients show percentage
   ```python
   await request_context.send_progress(
       progress_token="task-123",
       progress=50,
       total=100  # Client can show "50%"
   )
   ```

4. **Always Return Final Result**: Even with streaming updates
   ```python
   # Send progress updates...
   await request_context.send_progress(...)
   
   # Always return complete result
   return [TextContent(type="text", text="Final result")]
   ```

### Resource Best Practices

1. **Use Descriptive URIs**: Make them self-documenting
   - Good: `file:///logs/app-2024-10-30.log`
   - Bad: `file:///1`

2. **Provide Rich Metadata**: Help AI understand content
   ```python
   Resource(
       uri="file:///config/database.json",
       name="Database Configuration",
       description="Current database connection settings including host, port, and credentials",
       mimeType="application/json"
   )
   ```

3. **Use Appropriate MIME Types**: Signal content format
   - Text files: `text/plain`
   - JSON: `application/json`
   - Markdown: `text/markdown`
   - Images: `image/png`, `image/jpeg`

4. **Consider Resource Templates**: Enable dynamic discovery
   ```python
   ResourceTemplate(
       uriTemplate="file:///{category}/{name}.md",
       name="Documentation Files",
       description="Access any documentation file by category and name"
   )
   ```

5. **Handle Missing Resources Gracefully**: Return clear errors
   ```python
   @app.read_resource()
   async def read_resource(uri: str) -> str:
       if not resource_exists(uri):
           raise ValueError(f"Resource not found: {uri}")
       return load_resource(uri)
   ```

### Prompt Best Practices

1. **Design for Clarity**: Prompts should be self-explanatory
   ```python
   Prompt(
       name="debug_error",
       description="Systematic debugging workflow for error messages"
   )
   ```

2. **Use Required Arguments Appropriately**: Only require what's essential
   ```python
   arguments=[
       PromptArgument(name="error_message", required=True),
       PromptArgument(name="context", required=False)  # Optional
   ]
   ```

3. **Structure Prompts for Quality**: Include context and guidance
   ```python
   return [
       PromptMessage(
           role="user",
           content={
               "type": "text",
               "text": f"""Analyze this error:

Error: {error_message}

Please provide:
1. Root cause analysis
2. Immediate fix suggestions
3. Prevention strategies

{f'Additional context: {context}' if context else ''}"""
           }
       )
   ]
   ```

4. **Encode Best Practices**: Use prompts to share expertise
   - Include checklists
   - Reference standards
   - Provide examples
   - Suggest systematic approaches

### Combined Server Best Practices

1. **Maintain Consistency**: Use similar patterns across primitives
   - Consistent naming (e.g., all tools use verb_noun pattern)
   - Similar error handling approaches
   - Uniform documentation style

2. **Document Relationships**: Explain how features work together
   ```python
   # In README or tool descriptions
   """
   This server provides:
   - Tools: For executing git commands
   - Resources: For reading repository files
   - Prompts: For commit message templates
   
   Use the 'commit' tool with the 'write_commit_message' prompt
   and reference files using resources.
   """
   ```

3. **Design for Discoverability**: Make it easy to understand capabilities
   - Clear tool names and descriptions
   - Well-organized resource hierarchies
   - Prompt names that indicate their purpose

## Examples in This Module

All example code is in the `examples/` directory:

- `streaming_server.py` - Database server with streaming query results
- `resource_server.py` - File system exposed as resources
- `prompt_server.py` - Templates for code review and debugging
- `combined_server.py` - Full-featured server with all primitives

## Exercises

The `exercises/` directory contains hands-on practice:

### Tutorials (Step-by-Step Guidance)

1. **tutorial-1-streaming.md** - Add streaming to a long-running operation
   - Estimated time: 60 minutes
   - Difficulty: Intermediate
   - Implement progress notifications for file processing

2. **tutorial-2-resources.md** - Expose data as resources
   - Estimated time: 60 minutes
   - Difficulty: Intermediate
   - Build resource server with templates

### Challenges (Test Your Skills)

3. **challenge-1-sqlite-stream.md** - Database server with streaming
   - Estimated time: 90 minutes
   - Difficulty: Advanced
   - Implement SQLite server with streaming queries

4. **challenge-2-api-resources.md** - Wrap external API as resources
   - Estimated time: 90 minutes
   - Difficulty: Advanced
   - Expose REST API responses as MCP resources

All exercises include solutions in `exercises/solutions/` with multiple approaches and detailed explanations.

## Checkpoint

After completing this module, work through `checkpoint.md` to validate your understanding. You should be able to:

- Implement streaming for appropriate operations
- Design and expose resources effectively
- Create useful prompt templates
- Combine all primitives in a cohesive server
- Understand capability negotiation

## Next Steps

After mastering advanced features, you'll move to:

**Module 05: Integration Patterns**
- Connecting to Cursor IDE
- Using MCP Inspector for debugging
- Real-world integration examples (GitHub, Git, APIs)
- Multi-server architectures
- Production deployment patterns

## Getting Help

### Ask the AI Assistant

Throughout your exercises, you can ask questions like:

- "When should I use resources instead of tools?"
- "How do I implement streaming with progress updates?"
- "What makes a good prompt template?"
- "Can you explain capability negotiation?"

### Review Examples

The example servers demonstrate complete implementations with detailed comments explaining design decisions.

### Quick Reference

For quick reference on:
- Resource URI patterns
- Prompt message structure
- Streaming notification format

See the examples in this module for complete working implementations.
- Capability declaration syntax

## Key Takeaways

By the end of this module, remember these core principles:

1. **Choose the Right Primitive**: Tools for actions, resources for data, prompts for guidance
2. **Stream When Appropriate**: Long operations deserve progress updates
3. **Resources Provide Context**: Help AI understand before acting
4. **Prompts Encode Expertise**: Share knowledge through templates
5. **Combine Thoughtfully**: Features should complement each other

Start with `examples/streaming_server.py` to see streaming in action, then explore resources and prompts before combining everything.

Happy building!

