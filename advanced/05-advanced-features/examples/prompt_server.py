#!/usr/bin/env python3
"""
MCP Server with Prompts - Template Example

This example demonstrates how to implement prompts in an MCP server.
Prompts are reusable templates that structure interactions with AI,
encoding expert knowledge and best practices into templated workflows.

Key Concepts Demonstrated:
1. Defining prompts with names, descriptions, and arguments
2. Creating parameterized prompt templates
3. Structuring multi-message conversations
4. Encoding domain expertise into prompts
5. Providing context and guidance for common tasks

Usage:
    python prompt_server.py

Test with MCP Inspector:
    mcp-inspector python prompt_server.py
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent, Tool


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create the MCP server instance
app = Server("prompt-template-server")


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """
    List all available prompt templates.
    
    This server provides prompts for common software development tasks:
    1. Code review - Systematic code quality analysis
    2. Debug error - Structured debugging workflow
    3. Write tests - Test case generation guidance
    4. Refactor code - Safe refactoring recommendations
    5. Explain code - Code explanation template
    6. Write documentation - Documentation generation
    7. Optimize performance - Performance analysis workflow
    
    Returns:
        List of Prompt definitions with arguments
    """
    return [
        # ====================================================================
        # Prompt 1: Code Review
        # ====================================================================
        Prompt(
            name="code_review",
            description=(
                "Comprehensive code review covering correctness, security, "
                "performance, style, and maintainability. Provides structured "
                "feedback with specific recommendations."
            ),
            arguments=[
                PromptArgument(
                    name="language",
                    description="Programming language (e.g., python, javascript, rust)",
                    required=True
                ),
                PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True
                ),
                PromptArgument(
                    name="context",
                    description="Additional context about the code's purpose (optional)",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 2: Debug Error
        # ====================================================================
        Prompt(
            name="debug_error",
            description=(
                "Systematic debugging workflow for error messages. "
                "Analyzes root cause, suggests immediate fixes, and provides "
                "prevention strategies."
            ),
            arguments=[
                PromptArgument(
                    name="error_message",
                    description="The error message or stack trace",
                    required=True
                ),
                PromptArgument(
                    name="code",
                    description="The code that produced the error (optional)",
                    required=False
                ),
                PromptArgument(
                    name="context",
                    description="What you were trying to do when the error occurred (optional)",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 3: Write Tests
        # ====================================================================
        Prompt(
            name="write_tests",
            description=(
                "Generate comprehensive test cases for code. "
                "Covers normal cases, edge cases, error cases, and "
                "includes setup and teardown guidance."
            ),
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to write tests for",
                    required=True
                ),
                PromptArgument(
                    name="framework",
                    description="Testing framework (e.g., pytest, jest, junit)",
                    required=True
                ),
                PromptArgument(
                    name="test_type",
                    description="Type of tests (unit, integration, e2e)",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 4: Refactor Code
        # ====================================================================
        Prompt(
            name="refactor_code",
            description=(
                "Suggest safe refactoring improvements. "
                "Focuses on code clarity, maintainability, and best practices "
                "while preserving functionality."
            ),
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to refactor",
                    required=True
                ),
                PromptArgument(
                    name="goals",
                    description="Refactoring goals (e.g., 'improve readability', 'reduce complexity')",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 5: Explain Code
        # ====================================================================
        Prompt(
            name="explain_code",
            description=(
                "Explain code in clear, understandable terms. "
                "Breaks down complex logic into digestible explanations "
                "suitable for different audience levels."
            ),
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to explain",
                    required=True
                ),
                PromptArgument(
                    name="audience",
                    description="Target audience (e.g., 'beginner', 'intermediate', 'expert')",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 6: Write Documentation
        # ====================================================================
        Prompt(
            name="write_documentation",
            description=(
                "Generate documentation for code. "
                "Creates clear docstrings, API documentation, or README sections "
                "following best practices."
            ),
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to document",
                    required=True
                ),
                PromptArgument(
                    name="doc_type",
                    description="Documentation type (e.g., 'docstring', 'api', 'readme')",
                    required=True
                ),
                PromptArgument(
                    name="style",
                    description="Documentation style (e.g., 'google', 'numpy', 'sphinx')",
                    required=False
                )
            ]
        ),
        
        # ====================================================================
        # Prompt 7: Optimize Performance
        # ====================================================================
        Prompt(
            name="optimize_performance",
            description=(
                "Analyze code for performance bottlenecks and suggest optimizations. "
                "Focuses on algorithmic improvements, resource usage, and efficiency."
            ),
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to optimize",
                    required=True
                ),
                PromptArgument(
                    name="performance_data",
                    description="Performance measurements or profiling data (optional)",
                    required=False
                )
            ]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    """
    Get a specific prompt template with arguments filled in.
    
    This handler returns a list of messages that structure the conversation
    with the AI. Each message has a role (user/assistant) and content.
    
    Args:
        name: Prompt name
        arguments: Prompt arguments to substitute into template
    
    Returns:
        List of PromptMessage objects
    
    Raises:
        ValueError: If prompt name is unknown or required arguments are missing
    """
    
    # ========================================================================
    # Prompt 1: Code Review
    # ========================================================================
    if name == "code_review":
        language = arguments.get("language")
        code = arguments.get("code")
        context = arguments.get("context", "")
        
        if not language or not code:
            raise ValueError("Missing required arguments: language and code")
        
        context_section = f"\n\nContext: {context}" if context else ""
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please conduct a comprehensive code review of the following {language} code.

{context_section}

Analyze the code across these dimensions:

1. CORRECTNESS
   - Does the code work as intended?
   - Are there any logical errors or bugs?
   - Are edge cases handled properly?

2. SECURITY
   - Are there any security vulnerabilities?
   - Is input validation adequate?
   - Are there any injection risks (SQL, XSS, etc.)?

3. PERFORMANCE
   - Are there obvious inefficiencies?
   - Is the algorithmic complexity appropriate?
   - Are resources (memory, CPU) used efficiently?

4. STYLE & READABILITY
   - Does it follow {language} best practices and conventions?
   - Is the code clear and easy to understand?
   - Are variable and function names descriptive?
   - Is the code properly formatted?

5. MAINTAINABILITY
   - Is the code well-structured?
   - Is it easy to modify and extend?
   - Are there appropriate comments?
   - Is there excessive complexity?

Code to review:
```{language}
{code}
```

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Specific location in code
- Clear explanation of the problem
- Concrete suggestion for improvement
- Example of better code (when applicable)

Also highlight what the code does well."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 2: Debug Error
    # ========================================================================
    elif name == "debug_error":
        error_message = arguments.get("error_message")
        code = arguments.get("code", "")
        context = arguments.get("context", "")
        
        if not error_message:
            raise ValueError("Missing required argument: error_message")
        
        code_section = f"\n\nRelevant code:\n```\n{code}\n```" if code else ""
        context_section = f"\n\nContext: {context}" if context else ""
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""I need help debugging the following error.

Error message:
```
{error_message}
```
{code_section}
{context_section}

Please help me debug this systematically:

1. ERROR ANALYSIS
   - What type of error is this?
   - What is the immediate cause?
   - What does the error message tell us?

2. ROOT CAUSE
   - What is the underlying issue?
   - Why did this error occur?
   - Are there multiple contributing factors?

3. IMMEDIATE FIX
   - What's the quickest way to fix this specific error?
   - Provide specific code changes
   - Explain why this fix works

4. PROPER SOLUTION
   - Is the immediate fix the best long-term solution?
   - Are there better approaches?
   - What's the most robust fix?

5. PREVENTION
   - How can we prevent this error in the future?
   - What defensive programming practices apply?
   - Should we add tests, validation, or error handling?

6. RELATED ISSUES
   - Are there similar errors that might occur?
   - Are there related code areas to check?

Please be specific and provide code examples where helpful."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 3: Write Tests
    # ========================================================================
    elif name == "write_tests":
        code = arguments.get("code")
        framework = arguments.get("framework")
        test_type = arguments.get("test_type", "unit")
        
        if not code or not framework:
            raise ValueError("Missing required arguments: code and framework")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please write comprehensive {test_type} tests for the following code using {framework}.

Code to test:
```
{code}
```

Create tests that cover:

1. HAPPY PATH
   - Normal, expected use cases
   - Valid inputs with expected outputs
   - Typical user workflows

2. EDGE CASES
   - Boundary values (min, max, zero, empty)
   - Special values (null, undefined, infinity)
   - Unusual but valid inputs

3. ERROR CASES
   - Invalid inputs
   - Missing required parameters
   - Type mismatches
   - Out-of-range values

4. STATE TESTING (if applicable)
   - Initial state
   - State transitions
   - Final state verification

5. INTEGRATION POINTS (if applicable)
   - Mocking external dependencies
   - Testing interactions with other components

For each test, provide:
- Clear, descriptive test name
- Arrange (setup) section
- Act (execution) section
- Assert (verification) section
- Comments explaining what's being tested and why

Follow {framework} best practices and conventions."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 4: Refactor Code
    # ========================================================================
    elif name == "refactor_code":
        code = arguments.get("code")
        goals = arguments.get("goals", "improve overall code quality")
        
        if not code:
            raise ValueError("Missing required argument: code")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please suggest refactoring improvements for the following code.

Refactoring goals: {goals}

Code to refactor:
```
{code}
```

Provide refactoring suggestions in these areas:

1. CODE STRUCTURE
   - Function/method organization
   - Separation of concerns
   - Single Responsibility Principle
   - Extract functions/classes where appropriate

2. NAMING
   - Variable names
   - Function names
   - Class names
   - Use clear, self-documenting names

3. COMPLEXITY REDUCTION
   - Simplify complex conditionals
   - Reduce nesting
   - Break down large functions
   - Improve control flow

4. DUPLICATION
   - Identify repeated code
   - Suggest DRY (Don't Repeat Yourself) improvements
   - Extract common patterns

5. BEST PRACTICES
   - Apply design patterns where appropriate
   - Follow language idioms
   - Improve error handling
   - Add appropriate comments

For each suggestion:
- Explain what to change and why
- Show before and after code
- Explain the benefits
- Note any trade-offs

IMPORTANT: All refactoring must preserve the original functionality."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 5: Explain Code
    # ========================================================================
    elif name == "explain_code":
        code = arguments.get("code")
        audience = arguments.get("audience", "intermediate")
        
        if not code:
            raise ValueError("Missing required argument: code")
        
        audience_guidance = {
            "beginner": "Explain in simple terms, avoiding jargon. Define technical concepts.",
            "intermediate": "Use standard terminology, explain complex concepts clearly.",
            "expert": "Use technical language freely, focus on nuances and implications."
        }
        
        guidance = audience_guidance.get(audience, audience_guidance["intermediate"])
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please explain the following code in clear, understandable terms.

Target audience: {audience} ({guidance})

Code to explain:
```
{code}
```

Structure your explanation:

1. OVERVIEW
   - What does this code do? (high-level purpose)
   - What problem does it solve?

2. STEP-BY-STEP BREAKDOWN
   - Walk through the code line by line or section by section
   - Explain what each part does
   - Explain why each part is necessary

3. KEY CONCEPTS
   - Highlight important programming concepts used
   - Explain any algorithms or patterns
   - Define any technical terms

4. DATA FLOW
   - Describe how data moves through the code
   - Show inputs and outputs
   - Explain transformations

5. NOTABLE ASPECTS
   - Point out clever or interesting parts
   - Mention any gotchas or subtleties
   - Discuss alternatives or trade-offs

Use examples and analogies where helpful. Make it engaging and clear."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 6: Write Documentation
    # ========================================================================
    elif name == "write_documentation":
        code = arguments.get("code")
        doc_type = arguments.get("doc_type")
        style = arguments.get("style", "google")
        
        if not code or not doc_type:
            raise ValueError("Missing required arguments: code and doc_type")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please write {doc_type} documentation for the following code using {style} style.

Code to document:
```
{code}
```

Documentation requirements:

1. CLEAR DESCRIPTION
   - What does this code do?
   - What is its purpose?
   - When should it be used?

2. PARAMETERS/ARGUMENTS
   - List all parameters
   - Describe each parameter's purpose
   - Specify types
   - Note default values
   - Indicate if required or optional

3. RETURN VALUE
   - What does it return?
   - What is the return type?
   - What do different return values mean?

4. EXAMPLES
   - Show basic usage examples
   - Show advanced usage if applicable
   - Include expected output

5. EDGE CASES & ERRORS
   - Note any limitations
   - Describe error conditions
   - Explain exceptions that may be raised

6. ADDITIONAL NOTES
   - Performance considerations
   - Side effects
   - Thread safety (if applicable)
   - Related functions or classes

Follow {style} documentation standards and best practices."""
                }
            )
        ]
    
    # ========================================================================
    # Prompt 7: Optimize Performance
    # ========================================================================
    elif name == "optimize_performance":
        code = arguments.get("code")
        performance_data = arguments.get("performance_data", "")
        
        if not code:
            raise ValueError("Missing required argument: code")
        
        perf_section = f"\n\nPerformance data:\n{performance_data}" if performance_data else ""
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Please analyze the following code for performance bottlenecks and suggest optimizations.

Code to optimize:
```
{code}
```
{perf_section}

Analyze and suggest improvements in these areas:

1. ALGORITHMIC COMPLEXITY
   - What is the current time complexity?
   - What is the current space complexity?
   - Can the algorithm be improved?
   - Are there better data structures to use?

2. BOTTLENECK IDENTIFICATION
   - What are the slowest operations?
   - Which parts run most frequently?
   - Where is time being wasted?

3. OPTIMIZATION OPPORTUNITIES
   - Can we reduce iterations?
   - Can we cache results?
   - Can we avoid redundant calculations?
   - Can we use more efficient operations?

4. RESOURCE USAGE
   - Memory allocation patterns
   - I/O operations
   - Network calls
   - Database queries

5. SPECIFIC RECOMMENDATIONS
   - Provide concrete code improvements
   - Show optimized versions
   - Explain the performance gains
   - Quantify improvements where possible (Big-O notation)

6. TRADE-OFFS
   - Note any trade-offs (e.g., memory vs speed)
   - Discuss when optimizations matter
   - Consider readability vs performance

For each optimization:
- Explain the current inefficiency
- Show the optimized code
- Estimate the performance improvement
- Note any downsides or limitations"""
                }
            )
        ]
    
    # ========================================================================
    # Unknown Prompt
    # ========================================================================
    else:
        raise ValueError(f"Unknown prompt: {name}")


# ============================================================================
# Tools for Prompt Management
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List tools for working with prompts.
    
    These tools help discover and understand available prompts.
    
    Returns:
        List of Tool definitions
    """
    return [
        Tool(
            name="get_prompt_info",
            description="Get detailed information about a specific prompt template",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_name": {
                        "type": "string",
                        "description": "Name of the prompt to get information about"
                    }
                },
                "required": ["prompt_name"]
            }
        ),
        Tool(
            name="suggest_prompt",
            description="Suggest appropriate prompt templates based on a task description",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Description of what you want to accomplish"
                    }
                },
                "required": ["task"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution for prompt discovery.
    
    Args:
        name: Tool name
        arguments: Tool arguments
    
    Returns:
        List of TextContent with results
    """
    
    # ========================================================================
    # Tool 1: Get Prompt Info
    # ========================================================================
    if name == "get_prompt_info":
        prompt_name = arguments["prompt_name"]
        
        # Get all prompts
        prompts = await list_prompts()
        
        # Find the requested prompt
        prompt = next((p for p in prompts if p.name == prompt_name), None)
        
        if not prompt:
            return [TextContent(
                type="text",
                text=f"Error: Prompt '{prompt_name}' not found"
            )]
        
        # Format prompt information
        args_info = []
        for arg in prompt.arguments or []:
            arg_info = f"  - {arg.name}: {arg.description}"
            if arg.required:
                arg_info += " (required)"
            args_info.append(arg_info)
        
        return [TextContent(
            type="text",
            text=f"""Prompt: {prompt.name}

Description: {prompt.description}

Arguments:
{chr(10).join(args_info) if args_info else '  (none)'}

Usage: Use the get_prompt method with this prompt name and appropriate arguments."""
        )]
    
    # ========================================================================
    # Tool 2: Suggest Prompt
    # ========================================================================
    elif name == "suggest_prompt":
        task = arguments["task"].lower()
        
        # Simple keyword-based suggestion
        suggestions = []
        
        if any(word in task for word in ["review", "check", "analyze", "quality"]):
            suggestions.append("code_review")
        
        if any(word in task for word in ["error", "bug", "debug", "fix", "broken"]):
            suggestions.append("debug_error")
        
        if any(word in task for word in ["test", "testing", "unit test", "test case"]):
            suggestions.append("write_tests")
        
        if any(word in task for word in ["refactor", "improve", "clean", "simplify"]):
            suggestions.append("refactor_code")
        
        if any(word in task for word in ["explain", "understand", "what does", "how does"]):
            suggestions.append("explain_code")
        
        if any(word in task for word in ["document", "docstring", "comment", "api doc"]):
            suggestions.append("write_documentation")
        
        if any(word in task for word in ["optimize", "performance", "faster", "slow"]):
            suggestions.append("optimize_performance")
        
        if not suggestions:
            return [TextContent(
                type="text",
                text="I couldn't determine which prompts would be most helpful for your task. "
                     "Try browsing all available prompts with list_prompts()."
            )]
        
        return [TextContent(
            type="text",
            text=f"""Based on your task: "{task}"

I suggest these prompts:
{chr(10).join(f'  - {s}' for s in suggestions)}

Use get_prompt_info to learn more about each prompt."""
        )]
    
    # ========================================================================
    # Unknown Tool
    # ========================================================================
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


# ============================================================================
# Server Lifecycle Management
# ============================================================================

async def main():
    """
    Main entry point for the MCP server.
    
    This function sets up the stdio transport and runs the server.
    """
    print("Starting MCP prompt template server...")
    print("Ready to accept connections via stdio")
    print()
    print("This server provides prompt templates for:")
    print("  - Code review")
    print("  - Error debugging")
    print("  - Test writing")
    print("  - Code refactoring")
    print("  - Code explanation")
    print("  - Documentation writing")
    print("  - Performance optimization")
    print()
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

