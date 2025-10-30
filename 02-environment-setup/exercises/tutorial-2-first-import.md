# Tutorial 2: First Import and Exploring MCP Types

## Overview

Now that your environment is validated, let's explore the MCP SDK by importing it and examining its core types and structures.

**Estimated Time**: 30-40 minutes

**Prerequisites**: 
- Complete [Tutorial 1: Environment Validation](./tutorial-1-env-validation.md)
- Virtual environment activated

## Learning Objectives

By the end of this tutorial, you will:
- Import and explore MCP SDK components
- Understand MCP's core data types
- Create instances of Tools, Resources, and Prompts
- Explore the Server class
- Write your first (minimal) MCP code

---

## Part 1: Interactive Python Exploration

### Step 1: Start Python Interactive Shell

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Start Python
python3
```

You should see the Python prompt:
```
>>>
```

---

### Step 2: Import MCP Module

```python
>>> import mcp
>>> print(mcp.__version__)
0.9.0

>>> print(mcp.__file__)
/path/to/venv/lib/python3.11/site-packages/mcp/__init__.py

>>> dir(mcp)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', ...]
```

**Question:** What does `dir(mcp)` show you?

**Answer:** All attributes and methods available in the mcp module.

---

### Step 3: Explore MCP Server

```python
>>> from mcp.server import Server
>>> 
>>> # Check Server class
>>> print(Server.__doc__)
>>> 
>>> # See what methods Server has
>>> [m for m in dir(Server) if not m.startswith('_')]
['call_tool', 'get_prompt', 'list_prompts', 'list_resources', 'list_tools', 'read_resource', ...]
```

**Create a Server instance:**

```python
>>> server = Server("my-first-server")
>>> 
>>> print(server)
<mcp.server.Server object at 0x...>
>>> 
>>> print(type(server))
<class 'mcp.server.Server'>
```

**Question:** What is the argument to `Server()`?

**Answer:** The server name (string identifier).

---

### Step 4: Explore MCP Types

```python
>>> from mcp.types import Tool, Resource, Prompt, TextContent
>>> 
>>> # Check Tool structure
>>> help(Tool)
# Press 'q' to exit help
>>> 
>>> # See Tool fields
>>> Tool.__annotations__
{'name': <class 'str'>, 'description': <class 'str'>, 'inputSchema': <class 'dict'>, ...}
```

---

## Part 2: Creating MCP Types

### Step 5: Create a Tool

Exit Python (Ctrl+D or `exit()`) and create a new file:

```bash
cat > explore_tool.py << 'EOF'
"""Exploring MCP Tool type."""

from mcp.types import Tool

# Create a simple tool
calculator_tool = Tool(
    name="add",
    description="Add two numbers together",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            }
        },
        "required": ["a", "b"]
    }
)

# Examine the tool
print("Tool created:")
print(f"  Name: {calculator_tool.name}")
print(f"  Description: {calculator_tool.description}")
print(f"  Input Schema: {calculator_tool.inputSchema}")

# Tools are Pydantic models
print(f"\nTool type: {type(calculator_tool)}")
print(f"Is Pydantic model: {hasattr(calculator_tool, 'model_dump')}")

# Serialize to dict
tool_dict = calculator_tool.model_dump()
print(f"\nAs dictionary:")
print(tool_dict)

# Serialize to JSON
tool_json = calculator_tool.model_dump_json(indent=2)
print(f"\nAs JSON:")
print(tool_json)
EOF

python3 explore_tool.py
```

**Output Analysis:**

- Tools are Pydantic models (data validation library)
- `inputSchema` follows JSON Schema specification
- Can be serialized to dict or JSON

**Questions:**

1. What fields does a Tool require?
2. What is `inputSchema`?
3. Why use JSON Schema format?

---

**Ask the AI:**

Understanding Tools:
- "I see 'inputSchema' uses JSON Schema. Can you explain why MCP uses this standard rather than something custom?"
- "What's the benefit of tools being Pydantic models? What does Pydantic give us?"

---

### Step 6: Create a Resource

```bash
cat > explore_resource.py << 'EOF'
"""Exploring MCP Resource type."""

from mcp.types import Resource

# Create a file resource
file_resource = Resource(
    uri="file:///logs/app.log",
    name="Application Log",
    description="Main application log file",
    mimeType="text/plain"
)

print("Resource created:")
print(f"  URI: {file_resource.uri}")
print(f"  Name: {file_resource.name}")
print(f"  Description: {file_resource.description}")
print(f"  MIME Type: {file_resource.mimeType}")

# Create a database resource with template
db_resource = Resource(
    uri="db://users/{user_id}",
    name="User Record",
    description="Access user data by ID",
    mimeType="application/json"
)

print("\nTemplated resource:")
print(f"  URI Pattern: {db_resource.uri}")
print(f"  Note: {{user_id}} is a variable")

# Resources as dict
print(f"\nResource as dict:")
print(file_resource.model_dump())
EOF

python3 explore_resource.py
```

**Key Observations:**

- Resources use URI format
- Can be templated (with variables like `{user_id}`)
- Include metadata (name, description, mimeType)
- Represent read-only data access

**Questions:**

1. What's the difference between a Tool and a Resource?
2. When would you use a templated URI?
3. What is `mimeType` used for?

---

**Ask the AI:**

Understanding Resources:
- "Can you give me examples of when I'd use a templated URI like 'db://users/{id}' versus separate resources?"
- "Resources are read-only. If I need to update data, what would I use instead?"

---

### Step 7: Create Content Types

```bash
cat > explore_content.py << 'EOF'
"""Exploring MCP Content types."""

from mcp.types import TextContent, ImageContent, EmbeddedResource

# Text content (most common)
text = TextContent(
    type="text",
    text="Hello from MCP!"
)

print("Text Content:")
print(f"  Type: {text.type}")
print(f"  Text: {text.text}")

# Image content
image = ImageContent(
    type="image",
    data="base64-encoded-image-data-here",
    mimeType="image/png"
)

print("\nImage Content:")
print(f"  Type: {image.type}")
print(f"  MIME Type: {image.mimeType}")
print(f"  Data length: {len(image.data)} characters")

# Embedded resource
embedded = EmbeddedResource(
    type="resource",
    resource=Resource(
        uri="file:///data.json",
        name="Data File",
        mimeType="application/json"
    )
)

print("\nEmbedded Resource:")
print(f"  Type: {embedded.type}")
print(f"  Resource URI: {embedded.resource.uri}")

print("\n--- Content Types Summary ---")
print("TextContent: Plain text responses")
print("ImageContent: Binary image data (base64)")
print("EmbeddedResource: Reference to a resource")
EOF

python3 explore_content.py
```

**Understanding Content Types:**

- **TextContent**: For text responses (most common)
- **ImageContent**: For images/binary data
- **EmbeddedResource**: For referencing resources

---

### Step 8: Create a Prompt

```bash
cat > explore_prompt.py << 'EOF'
"""Exploring MCP Prompt type."""

from mcp.types import Prompt, PromptArgument

# Create a prompt template
code_review_prompt = Prompt(
    name="code_review",
    description="Review code for quality and best practices",
    arguments=[
        PromptArgument(
            name="language",
            description="Programming language",
            required=True
        ),
        PromptArgument(
            name="code",
            description="Code to review",
            required=True
        ),
        PromptArgument(
            name="focus",
            description="Specific focus area (security, performance, style)",
            required=False
        )
    ]
)

print("Prompt created:")
print(f"  Name: {code_review_prompt.name}")
print(f"  Description: {code_review_prompt.description}")
print(f"\nArguments:")
for arg in code_review_prompt.arguments:
    required = "required" if arg.required else "optional"
    print(f"  - {arg.name} ({required}): {arg.description}")

# Prompts as dict
print(f"\nPrompt as dict:")
print(code_review_prompt.model_dump())
EOF

python3 explore_prompt.py
```

**Key Points about Prompts:**

- Define reusable prompt templates
- Can have required and optional arguments
- Help standardize AI interactions

---

## Part 3: Putting It Together

### Step 9: Create Complete Type Examples

Create a comprehensive example:

```bash
cat > complete_types_example.py << 'EOF'
"""Complete example of all MCP types."""

from mcp.types import (
    Tool,
    Resource,
    Prompt,
    PromptArgument,
    TextContent
)

print("=" * 60)
print("MCP Types Complete Example")
print("=" * 60)

# 1. Tools (actions the AI can perform)
print("\n1. TOOLS (Actions)")
print("-" * 60)

tools = [
    Tool(
        name="get_weather",
        description="Get current weather for a city",
        inputSchema={
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    ),
    Tool(
        name="send_email",
        description="Send an email message",
        inputSchema={
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    )
]

for tool in tools:
    print(f"Tool: {tool.name}")
    print(f"  {tool.description}")
    print(f"  Parameters: {list(tool.inputSchema['properties'].keys())}")

# 2. Resources (data the AI can read)
print("\n2. RESOURCES (Data)")
print("-" * 60)

resources = [
    Resource(
        uri="file:///config/settings.json",
        name="Application Settings",
        mimeType="application/json"
    ),
    Resource(
        uri="db://products/{product_id}",
        name="Product Information",
        mimeType="application/json"
    ),
    Resource(
        uri="api://weather/{city}",
        name="Weather Data",
        mimeType="application/json"
    )
]

for resource in resources:
    print(f"Resource: {resource.uri}")
    print(f"  {resource.name}")
    templated = "{" in resource.uri
    print(f"  Templated: {templated}")

# 3. Prompts (reusable templates)
print("\n3. PROMPTS (Templates)")
print("-" * 60)

prompts = [
    Prompt(
        name="summarize",
        description="Summarize a document",
        arguments=[
            PromptArgument(name="document", description="Document to summarize", required=True),
            PromptArgument(name="length", description="Summary length", required=False)
        ]
    ),
    Prompt(
        name="translate",
        description="Translate text",
        arguments=[
            PromptArgument(name="text", description="Text to translate", required=True),
            PromptArgument(name="target_language", description="Target language", required=True)
        ]
    )
]

for prompt in prompts:
    print(f"Prompt: {prompt.name}")
    print(f"  {prompt.description}")
    print(f"  Arguments: {[arg.name for arg in prompt.arguments]}")

# 4. Content (responses from tools)
print("\n4. CONTENT (Responses)")
print("-" * 60)

contents = [
    TextContent(type="text", text="The weather in Tokyo is 22°C and sunny."),
    TextContent(type="text", text="Email sent successfully to user@example.com"),
]

for i, content in enumerate(contents, 1):
    print(f"Content {i}: {content.text}")

print("\n" + "=" * 60)
print("All MCP types demonstrated successfully!")
print("=" * 60)
EOF

python3 complete_types_example.py
```

---

## Part 4: Understanding JSON Schema

### Step 10: JSON Schema Exploration

JSON Schema defines the structure of tool inputs. Let's explore:

```bash
cat > json_schema_examples.py << 'EOF'
"""Understanding JSON Schema for MCP tools."""

from mcp.types import Tool

# Example 1: Simple parameters
simple_tool = Tool(
    name="greet",
    description="Greet a person",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Person's name"
            }
        },
        "required": ["name"]
    }
)

print("Example 1: Simple String Parameter")
print(f"Parameters: {list(simple_tool.inputSchema['properties'].keys())}")
print(f"Required: {simple_tool.inputSchema['required']}")

# Example 2: Multiple types
math_tool = Tool(
    name="calculate",
    description="Perform calculation",
    inputSchema={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "Operation to perform"
            },
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            }
        },
        "required": ["operation", "a", "b"]
    }
)

print("\nExample 2: Enum and Number Types")
print(f"Operations allowed: {math_tool.inputSchema['properties']['operation']['enum']}")

# Example 3: Nested objects
search_tool = Tool(
    name="search",
    description="Search database",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string"
            },
            "filters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "min_price": {"type": "number"},
                    "max_price": {"type": "number"}
                }
            },
            "limit": {
                "type": "integer",
                "default": 10,
                "minimum": 1,
                "maximum": 100
            }
        },
        "required": ["query"]
    }
)

print("\nExample 3: Nested Objects and Defaults")
print(f"Has nested object: 'filters'")
print(f"Default limit: {search_tool.inputSchema['properties']['limit']['default']}")

# Example 4: Arrays
list_tool = Tool(
    name="process_items",
    description="Process a list of items",
    inputSchema={
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1,
                "description": "List of items to process"
            }
        },
        "required": ["items"]
    }
)

print("\nExample 4: Array Parameters")
print(f"Accepts array of: {list_tool.inputSchema['properties']['items']['items']['type']}")
print(f"Minimum items: {list_tool.inputSchema['properties']['items']['minItems']}")

print("\n--- JSON Schema Types ---")
print("string: Text values")
print("number: Numeric values (int or float)")
print("integer: Whole numbers only")
print("boolean: true/false")
print("object: Nested structure")
print("array: List of values")
print("enum: Restricted set of values")
EOF

python3 json_schema_examples.py
```

---

**Ask the AI:**

Understanding JSON Schema:
- "When should I use 'number' versus 'integer' in JSON Schema? Does it matter?"
- "I want to restrict a parameter to specific values. Should I use 'enum' or is there another way?"
- "Can you explain nested objects in JSON Schema? When would I need them?"

---

## Part 5: Practical Exercise

### Step 11: Build Your Own Type Instances

Create a file with your own MCP types:

```bash
cat > my_mcp_types.py << 'EOF'
"""My custom MCP types."""

from mcp.types import Tool, Resource, Prompt, PromptArgument

# TODO: Create a tool for your favorite functionality
my_tool = Tool(
    name="",  # Fill in
    description="",  # Fill in
    inputSchema={
        "type": "object",
        "properties": {
            # Add your parameters here
        },
        "required": []
    }
)

# TODO: Create a resource for data you'd want to access
my_resource = Resource(
    uri="",  # Fill in (e.g., "file:///...", "db://...", "api://...")
    name="",  # Fill in
    mimeType=""  # Fill in
)

# TODO: Create a prompt template for a common task
my_prompt = Prompt(
    name="",  # Fill in
    description="",  # Fill in
    arguments=[
        # Add PromptArgument instances
    ]
)

# Print your creations
print("My Tool:")
print(f"  Name: {my_tool.name}")
print(f"  Description: {my_tool.description}")

print("\nMy Resource:")
print(f"  URI: {my_resource.uri}")
print(f"  Name: {my_resource.name}")

print("\nMy Prompt:")
print(f"  Name: {my_prompt.name}")
print(f"  Description: {my_prompt.description}")
EOF

# Edit the file with your values
echo "Edit my_mcp_types.py and fill in the TODOs"
echo "Then run: python3 my_mcp_types.py"
```

**Exercise:** 
1. Edit `my_mcp_types.py`
2. Create a tool, resource, and prompt for something useful to you
3. Run it and verify it works

---

## Part 6: Type Validation

### Step 12: Understanding Pydantic Validation

MCP uses Pydantic for validation. Let's see it in action:

```bash
cat > test_validation.py << 'EOF'
"""Testing Pydantic validation in MCP types."""

from mcp.types import Tool

print("Testing MCP type validation...")

# Valid tool
try:
    valid_tool = Tool(
        name="test",
        description="Test tool",
        inputSchema={"type": "object", "properties": {}}
    )
    print("✓ Valid tool created")
except Exception as e:
    print(f"✗ Error: {e}")

# Missing required field
try:
    invalid_tool = Tool(
        name="test"
        # Missing description and inputSchema
    )
    print("✗ Should have failed!")
except Exception as e:
    print(f"✓ Validation caught missing field: {type(e).__name__}")

# Wrong type
try:
    wrong_type = Tool(
        name=123,  # Should be string
        description="Test",
        inputSchema={}
    )
    print("✗ Should have failed!")
except Exception as e:
    print(f"✓ Validation caught wrong type: {type(e).__name__}")

print("\nPydantic validation ensures type safety!")
EOF

python3 test_validation.py
```

**Key Learning:** Pydantic automatically validates that:
- Required fields are present
- Types are correct
- Data structure matches expectations

---

## Part 7: Cleanup and Summary

### Step 13: Review What You've Learned

Create a summary script:

```bash
cat > learning_summary.py << 'EOF'
"""Summary of MCP types learned."""

print("=" * 60)
print("MCP SDK Types Summary")
print("=" * 60)

print("\nCore Imports:")
print("  from mcp.server import Server")
print("  from mcp.types import Tool, Resource, Prompt, TextContent")

print("\nTool - Functions the AI can call:")
print("  - name: str")
print("  - description: str")
print("  - inputSchema: dict (JSON Schema)")
print("  Example: get_weather, send_email, calculate")

print("\nResource - Data the AI can read:")
print("  - uri: str (file://, db://, api://)")
print("  - name: str")
print("  - mimeType: str")
print("  Example: file:///logs/app.log, db://users/{id}")

print("\nPrompt - Reusable templates:")
print("  - name: str")
print("  - description: str")
print("  - arguments: list[PromptArgument]")
print("  Example: code_review, summarize, translate")

print("\nContent - Response types:")
print("  - TextContent: Plain text")
print("  - ImageContent: Images/binary")
print("  - EmbeddedResource: Resource references")

print("\nKey Concepts:")
print("  1. All types are Pydantic models")
print("  2. Automatic validation")
print("  3. Can serialize to dict/JSON")
print("  4. JSON Schema for tool inputs")

print("\nNext Steps:")
print("  → Build your first MCP server!")
print("  → Module 03: Basic MCP Server")

print("=" * 60)
EOF

python3 learning_summary.py
```

---

## Completion Checklist

Before moving to the next module, ensure you can:

- [ ] Import MCP SDK components
- [ ] Create Tool instances with proper JSON Schema
- [ ] Create Resource instances with URIs
- [ ] Create Prompt instances with arguments
- [ ] Understand different Content types
- [ ] Explain what Pydantic validation does
- [ ] Serialize MCP types to dict/JSON
- [ ] Understand the difference between Tools and Resources

---

## Next Steps

1. **Clean up** test files (optional):
   ```bash
   rm explore_*.py test_*.py complete_types_example.py json_schema_examples.py learning_summary.py
   # Keep my_mcp_types.py if you want
   ```

2. **Try the challenge**: [Challenge 1: Docker Customization](./challenge-1-docker-custom.md)

3. **Complete checkpoint**: [Module 02 Checkpoint](../checkpoint.md)

4. **Move to Module 03**: [Basic MCP Server](../../03-basic-mcp-server/README.md)
   - You're now ready to build real MCP servers!

---

## How to Use AI Assistance

Learning the MCP SDK types works well with AI guidance. Here's how to ask effectively:

### Understanding Type Structure

When exploring types:

```
I'm looking at the Tool type. Can you explain what each field (name, 
description, inputSchema) is used for, but don't write example code yet? 
I want to understand the purpose first.
```

```
What's the relationship between Tool, Resource, and Prompt in MCP? 
Give me a mental model without diving into code.
```

### JSON Schema Questions

For schema understanding:

```
I'm confused by JSON Schema. Can you explain what "type": "object" and 
"properties" mean in simple terms?
```

```
I see 'required' in the inputSchema. How does this work, and what happens 
if a required field is missing?
```

```
The tutorial uses 'enum' in the JSON Schema. What does this accomplish 
and when should I use it?
```

### Pydantic Validation

To understand validation:

```
Step 12 mentions Pydantic validation. What is Pydantic and why does MCP 
use it? Explain at a high level.
```

```
The validation caught a missing field error. How does Pydantic know what's 
required vs optional? Don't show me code, explain the concept.
```

### Type Usage Questions

When designing your own types:

```
I want to create a tool that [does X]. What parameters should I consider 
including? Guide my thinking, don't design it for me.
```

```
I'm trying to decide if [operation] should be a Tool or a Resource. 
What questions should I ask myself to make this decision?
```

### Working with URIs

For resource URIs:

```
I see URIs like "file://" and "db://". Are these standard protocols or 
MCP-specific? How do I choose what to use?
```

```
The tutorial shows templated URIs with {variable}. When would I use a 
template vs a fixed URI?
```

### Content Types

Understanding responses:

```
There are TextContent, ImageContent, and EmbeddedResource types. Can you 
explain when to use each one?
```

```
Why would I return an EmbeddedResource instead of just text?
```

### Debugging Type Issues

When things go wrong:

```
I'm trying to create a Tool instance but getting [error]. What does this 
error mean, and what should I check in my code?
```

```
My Tool's inputSchema isn't validating correctly. Rather than fix it for 
me, what are common schema mistakes I should look for?
```

### Understanding Examples

To learn from code:

```
In the complete_types_example.py, the get_weather tool uses an enum for 
'units'. Why is this better than just accepting any string?
```

```
Can you walk me through what happens when I call tool.model_dump()? 
What's the purpose of this method?
```

### Step-by-Step Exploration

For the exercises:

```
I'm working on Step 11 (creating my own types). Can you help me brainstorm 
what kind of tool would be interesting to create, without actually 
designing it?
```

```
I'm filling out my_mcp_types.py. For my tool, I'm thinking of [idea]. 
What parameters would make sense? Let me think it through with your guidance.
```

### Testing Understanding

Verify your knowledge:

```
I think Resources are read-only and Tools can modify things. Is this 
correct, or am I misunderstanding?
```

```
I believe JSON Schema is how the AI knows what parameters a tool needs. 
Is my understanding accurate?
```

### What NOT to Ask

Avoid these shortcuts:

- "Write a complete Tool for me"
- "Fill in all the TODOs in my_mcp_types.py"
- "Give me 10 example tools"
- "Debug my code" (without showing effort to understand)

### Example Learning Conversation

**Effective:**

1. "I'm creating a tool for temperature conversion. What parameters would it logically need?"
2. Think about the response (input temperature, units, etc.)
3. "OK, I have temperature and units. How do I represent the units parameter so only valid values are accepted?"
4. Learn about enum
5. "Let me try implementing this... [shows code]... Does this make sense?"

**Less effective:**

1. "Create a temperature conversion tool for me"
2. Copy the result
3. Move on without understanding

### Deepening Understanding

After completing steps:

```
I've completed all the type examples. Can you quiz me on the differences 
between Tools, Resources, and Prompts? I'll answer, then you tell me if 
I'm right.
```

```
I notice all the types are Pydantic models. What advantages does this give 
us versus plain dictionaries?
```

### Conceptual Questions

For big-picture understanding:

```
Why does MCP need all these different types? Why not just have "functions" 
like a regular API?
```

```
How do these type definitions help an AI understand what it can do?
```

---

## Key Takeaways

- MCP SDK provides structured types for servers, tools, resources, and prompts
- All types are Pydantic models with automatic validation
- JSON Schema defines tool input parameters
- Tools perform actions, Resources provide data access
- Content types define response formats
- Understanding these types is essential for building MCP servers

**You're now familiar with the MCP SDK structure and ready to build servers!**

---

**Estimated Time**: 30-40 minutes

**Next**: [Challenge 1: Docker Customization](./challenge-1-docker-custom.md) or [Module 03](../../03-basic-mcp-server/README.md)

