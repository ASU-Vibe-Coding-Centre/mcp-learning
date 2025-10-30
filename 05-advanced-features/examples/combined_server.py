#!/usr/bin/env python3
"""
MCP Server with All Advanced Features Combined

This example demonstrates a complete MCP server that integrates all three
advanced primitives: streaming, resources, and prompts. This represents
a production-ready pattern for building comprehensive MCP integrations.

Key Concepts Demonstrated:
1. Tools with streaming progress notifications
2. Resources for exposing project data
3. Prompt templates for guided workflows
4. How all three primitives work together cohesively
5. Real-world integration patterns

The server provides a "Project Analysis" system that can:
- Analyze code files with streaming progress (Tools + Streaming)
- Expose project files as resources (Resources)
- Provide analysis templates and workflows (Prompts)

Usage:
    python combined_server.py

Test with MCP Inspector:
    mcp-inspector python combined_server.py
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    ResourceTemplate,
    TextContent,
    Tool,
)


# ============================================================================
# Configuration
# ============================================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Sample project directory for analysis (use current module)
SAMPLE_PROJECT = Path(__file__).parent.parent


# ============================================================================
# Utility Functions
# ============================================================================

def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except (UnicodeDecodeError, PermissionError):
        return 0


def is_safe_path(base: Path, target: Path) -> bool:
    """Check if target path is within base path."""
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def get_python_files(directory: Path) -> list[Path]:
    """Get all Python files in a directory."""
    if not directory.exists():
        return []
    return sorted([f for f in directory.rglob("*.py") if f.is_file()])


# ============================================================================
# MCP Server Implementation
# ============================================================================

app = Server("combined-advanced-server")


# ============================================================================
# TOOLS: Actions with Streaming Support
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools.
    
    This server provides tools for project analysis with streaming support.
    """
    return [
        Tool(
            name="analyze_project",
            description=(
                "Analyze a project directory for code statistics, structure, "
                "and potential issues. Streams progress updates as files are processed."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to analyze (relative to project root)",
                        "default": "04-advanced-features"
                    }
                }
            }
        ),
        Tool(
            name="analyze_file",
            description="Analyze a single Python file for complexity, style, and potential issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to Python file (relative to project root)"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="search_code",
            description="Search for code patterns across the project",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Text pattern to search for"
                    },
                    "directory": {
                        "type": "string",
                        "description": "Directory to search in (optional)",
                        "default": "."
                    }
                },
                "required": ["pattern"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict, request_context: Any) -> list[TextContent]:
    """
    Execute tools with streaming support.
    
    Demonstrates how streaming integrates with tool execution.
    """
    
    # ========================================================================
    # Tool 1: Analyze Project (with Streaming)
    # ========================================================================
    if name == "analyze_project":
        directory = arguments.get("directory", "04-advanced-features")
        target_dir = PROJECT_ROOT / directory
        
        if not is_safe_path(PROJECT_ROOT, target_dir):
            return [TextContent(
                type="text",
                text=f"Error: Directory '{directory}' is outside project root"
            )]
        
        if not target_dir.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory '{directory}' not found"
            )]
        
        # Find all Python files
        py_files = get_python_files(target_dir)
        total_files = len(py_files)
        
        if total_files == 0:
            return [TextContent(
                type="text",
                text=f"No Python files found in {directory}"
            )]
        
        # Analyze files with streaming progress
        analysis_results = {
            "directory": directory,
            "total_files": total_files,
            "total_lines": 0,
            "files": []
        }
        
        for i, py_file in enumerate(py_files):
            # Count lines
            line_count = count_lines(py_file)
            analysis_results["total_lines"] += line_count
            
            # Add file info
            relative_path = py_file.relative_to(PROJECT_ROOT)
            analysis_results["files"].append({
                "path": str(relative_path),
                "lines": line_count
            })
            
            # Send progress update (in real implementation)
            # This simulates streaming progress
            if i % 5 == 0:  # Every 5 files
                await asyncio.sleep(0)  # Yield control
                progress_pct = (i + 1) / total_files * 100
                print(f"  Progress: {i + 1}/{total_files} files ({progress_pct:.1f}%)")
        
        # Return complete analysis
        return [TextContent(
            type="text",
            text=f"""Project Analysis Complete

Directory: {directory}
Total Files: {total_files}
Total Lines: {analysis_results['total_lines']}

Files:
{json.dumps(analysis_results['files'], indent=2)}

Summary:
- Average lines per file: {analysis_results['total_lines'] // total_files}
- Largest file: {max(analysis_results['files'], key=lambda x: x['lines'])['path']} ({max(f['lines'] for f in analysis_results['files'])} lines)

Use the 'analyze_file' tool to get detailed analysis of specific files.
Use resources to read file contents.
Use prompts for guided code review workflows.
"""
        )]
    
    # ========================================================================
    # Tool 2: Analyze File
    # ========================================================================
    elif name == "analyze_file":
        file_path = arguments["file_path"]
        target_file = PROJECT_ROOT / file_path
        
        if not is_safe_path(PROJECT_ROOT, target_file):
            return [TextContent(
                type="text",
                text=f"Error: File is outside project root"
            )]
        
        if not target_file.exists():
            return [TextContent(
                type="text",
                text=f"Error: File not found"
            )]
        
        # Analyze file
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            lines = content.split("\n")
            analysis = {
                "file": file_path,
                "total_lines": len(lines),
                "blank_lines": sum(1 for line in lines if not line.strip()),
                "comment_lines": sum(1 for line in lines if line.strip().startswith("#")),
                "code_lines": 0,
                "has_docstring": '"""' in content or "'''" in content,
                "imports": [],
                "functions": [],
                "classes": []
            }
            
            # Count code lines
            analysis["code_lines"] = (
                analysis["total_lines"]
                - analysis["blank_lines"]
                - analysis["comment_lines"]
            )
            
            # Find imports
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("import ") or stripped.startswith("from "):
                    analysis["imports"].append(stripped)
            
            # Find functions and classes (simple detection)
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("def "):
                    func_name = stripped.split("(")[0].replace("def ", "")
                    analysis["functions"].append(func_name)
                elif stripped.startswith("class "):
                    class_name = stripped.split("(")[0].split(":")[0].replace("class ", "")
                    analysis["classes"].append(class_name)
            
            return [TextContent(
                type="text",
                text=f"""File Analysis: {file_path}

Lines:
  - Total: {analysis['total_lines']}
  - Code: {analysis['code_lines']}
  - Comments: {analysis['comment_lines']}
  - Blank: {analysis['blank_lines']}

Structure:
  - Classes: {len(analysis['classes'])}
  - Functions: {len(analysis['functions'])}
  - Imports: {len(analysis['imports'])}
  - Has docstring: {'Yes' if analysis['has_docstring'] else 'No'}

Classes:
{json.dumps(analysis['classes'], indent=2)}

Functions:
{json.dumps(analysis['functions'], indent=2)}

Top Imports:
{json.dumps(analysis['imports'][:10], indent=2)}

TIP: Use the 'code_review' prompt to get detailed code quality analysis.
TIP: Read the file as a resource using URI: file:///{file_path}
"""
            )]
        
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error analyzing file: {str(e)}"
            )]
    
    # ========================================================================
    # Tool 3: Search Code
    # ========================================================================
    elif name == "search_code":
        pattern = arguments["pattern"]
        directory = arguments.get("directory", ".")
        search_dir = PROJECT_ROOT / directory
        
        if not is_safe_path(PROJECT_ROOT, search_dir):
            return [TextContent(
                type="text",
                text=f"Error: Directory is outside project root"
            )]
        
        if not search_dir.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory not found"
            )]
        
        # Search for pattern
        results = []
        py_files = get_python_files(search_dir)
        
        for py_file in py_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if pattern in line:
                            results.append({
                                "file": str(py_file.relative_to(PROJECT_ROOT)),
                                "line": line_num,
                                "content": line.strip()
                            })
            except (UnicodeDecodeError, PermissionError):
                continue
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No matches found for pattern: {pattern}"
            )]
        
        # Limit results to 50
        if len(results) > 50:
            results = results[:50]
            truncated_msg = f"\n\n(Showing first 50 of {len(results)} results)"
        else:
            truncated_msg = ""
        
        return [TextContent(
            type="text",
            text=f"""Search Results for "{pattern}":

Found {len(results)} matches

{json.dumps(results, indent=2)}
{truncated_msg}
"""
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


# ============================================================================
# RESOURCES: Data Access
# ============================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List available resources.
    
    Exposes project files as resources that can be read for context.
    """
    resources = []
    
    # Add example Python files from current module
    example_files = [
        ("streaming_server.py", "Streaming example server"),
        ("resource_server.py", "Resource example server"),
        ("prompt_server.py", "Prompt example server"),
        ("combined_server.py", "Combined features server (this file)"),
    ]
    
    for filename, description in example_files:
        file_path = SAMPLE_PROJECT / "examples" / filename
        if file_path.exists():
            relative = file_path.relative_to(PROJECT_ROOT)
            resources.append(Resource(
                uri=f"file:///{relative.as_posix()}",
                name=f"Example: {filename}",
                description=description,
                mimeType="text/x-python"
            ))
    
    # Add README files
    readme_path = SAMPLE_PROJECT / "README.md"
    if readme_path.exists():
        relative = readme_path.relative_to(PROJECT_ROOT)
        resources.append(Resource(
            uri=f"file:///{relative.as_posix()}",
            name="Module 04 README",
            description="Advanced features module documentation",
            mimeType="text/markdown"
        ))
    
    return resources


@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """
    List resource templates for dynamic access.
    
    Templates allow clients to construct URIs for any project file.
    """
    return [
        ResourceTemplate(
            uriTemplate="file:///{path}",
            name="Project Files",
            description="Access any file in the project by path",
            mimeType="text/plain"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read resource content.
    
    Provides file content for AI context.
    """
    if not uri.startswith("file:///"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    # Extract path from URI
    path_str = uri[8:]  # Remove "file:///"
    file_path = PROJECT_ROOT / path_str
    
    # Security check
    if not is_safe_path(PROJECT_ROOT, file_path):
        raise PermissionError(f"Access denied: {uri}")
    
    if not file_path.exists():
        raise ValueError(f"Resource not found: {uri}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file: {uri}")
    
    # Read file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError(f"Binary file cannot be read as text: {uri}")


# ============================================================================
# PROMPTS: Guided Workflows
# ============================================================================

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """
    List available prompt templates.
    
    Provides guided workflows for code analysis and review.
    """
    return [
        Prompt(
            name="analyze_project_workflow",
            description=(
                "Comprehensive project analysis workflow. Guides through "
                "analyzing project structure, code quality, and potential improvements."
            ),
            arguments=[
                PromptArgument(
                    name="directory",
                    description="Project directory to analyze",
                    required=True
                )
            ]
        ),
        Prompt(
            name="code_review_file",
            description=(
                "Detailed code review for a specific file. Uses resources "
                "to read file content and applies systematic review criteria."
            ),
            arguments=[
                PromptArgument(
                    name="file_path",
                    description="Path to file to review",
                    required=True
                )
            ]
        ),
        Prompt(
            name="refactoring_plan",
            description=(
                "Create a refactoring plan for a project or file. "
                "Identifies areas for improvement and suggests systematic approach."
            ),
            arguments=[
                PromptArgument(
                    name="target",
                    description="What to refactor (file path or directory)",
                    required=True
                )
            ]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    """
    Get prompt with arguments filled in.
    
    These prompts guide AI through systematic analysis workflows.
    """
    
    if name == "analyze_project_workflow":
        directory = arguments.get("directory")
        if not directory:
            raise ValueError("Missing required argument: directory")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Let's analyze the project in directory: {directory}

Follow this systematic workflow:

STEP 1: INITIAL SCAN
- Use the 'analyze_project' tool to get an overview
- Note the number of files, total lines, and structure

STEP 2: IDENTIFY KEY FILES
- Look for the largest files (likely most complex)
- Look for files with many imports (likely central to architecture)
- Identify configuration and entry point files

STEP 3: DETAILED ANALYSIS
- Use 'analyze_file' tool on key files
- Read file contents as resources for detailed review
- Note patterns, architecture decisions, and code quality

STEP 4: PATTERN SEARCH
- Use 'search_code' to find:
  - TODO comments (incomplete work)
  - Error handling patterns
  - Common imports (dependencies)
  - Test coverage indicators

STEP 5: ASSESSMENT
Summarize findings:
- Overall code quality (1-10)
- Architectural strengths
- Areas for improvement
- Specific recommendations

STEP 6: ACTION ITEMS
Prioritize:
- Critical issues (security, bugs)
- High-impact improvements (performance, maintainability)
- Nice-to-have enhancements

Begin the analysis now."""
                }
            )
        ]
    
    elif name == "code_review_file":
        file_path = arguments.get("file_path")
        if not file_path:
            raise ValueError("Missing required argument: file_path")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Conduct a comprehensive code review of: {file_path}

STEP 1: READ THE CODE
- Read the file as a resource: file:///{file_path}
- Get file statistics with 'analyze_file' tool

STEP 2: STRUCTURAL REVIEW
Analyze:
- Organization (is code well-structured?)
- Functions and classes (clear responsibilities?)
- Imports (appropriate dependencies?)
- Documentation (docstrings, comments)

STEP 3: CODE QUALITY
Check for:
- Correctness (does it work as intended?)
- Readability (clear variable names, logical flow?)
- Maintainability (easy to modify and extend?)
- Best practices (follows language conventions?)

STEP 4: POTENTIAL ISSUES
Look for:
- Security vulnerabilities
- Performance bottlenecks
- Error handling gaps
- Edge cases not handled

STEP 5: SPECIFIC RECOMMENDATIONS
For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Specific location
- Clear explanation
- Concrete fix suggestion

STEP 6: POSITIVE ASPECTS
Highlight what the code does well.

Provide your review now."""
                }
            )
        ]
    
    elif name == "refactoring_plan":
        target = arguments.get("target")
        if not target:
            raise ValueError("Missing required argument: target")
        
        return [
            PromptMessage(
                role="user",
                content={
                    "type": "text",
                    "text": f"""Create a refactoring plan for: {target}

STEP 1: ANALYZE CURRENT STATE
- Use appropriate tools to understand current code
- Identify complexity hotspots
- Note code smells and anti-patterns

STEP 2: DEFINE GOALS
What should refactoring achieve?
- Improve readability?
- Reduce complexity?
- Better separation of concerns?
- Enhanced testability?
- Performance improvements?

STEP 3: IDENTIFY REFACTORING OPPORTUNITIES
Look for:
- Long functions (break down)
- Repeated code (extract to functions)
- Complex conditionals (simplify)
- Poor naming (clarify)
- Missing abstractions (introduce patterns)

STEP 4: PRIORITIZE CHANGES
Order by:
1. High impact, low risk
2. High impact, medium risk
3. Medium impact, low risk
4. Other improvements

STEP 5: CREATE PLAN
For each refactoring:
- What to change
- Why it improves the code
- How to do it safely (with tests)
- Estimated effort

STEP 6: RISK ASSESSMENT
Note:
- Potential breaking changes
- Testing requirements
- Dependencies affected

Provide the refactoring plan now."""
                }
            )
        ]
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


# ============================================================================
# Server Lifecycle
# ============================================================================

async def main():
    """
    Main entry point.
    
    This server combines all advanced MCP features:
    - Tools with streaming
    - Resources for file access
    - Prompts for guided workflows
    """
    print("=" * 70)
    print("MCP Combined Advanced Features Server")
    print("=" * 70)
    print()
    print("This server demonstrates all advanced MCP primitives:")
    print()
    print("TOOLS (with Streaming):")
    print("  - analyze_project: Project-wide code analysis with progress updates")
    print("  - analyze_file: Detailed single-file analysis")
    print("  - search_code: Search for patterns across project")
    print()
    print("RESOURCES:")
    print("  - Access to example Python files")
    print("  - Module documentation")
    print("  - Dynamic file access via templates")
    print()
    print("PROMPTS:")
    print("  - analyze_project_workflow: Guided project analysis")
    print("  - code_review_file: Systematic file review")
    print("  - refactoring_plan: Create refactoring strategy")
    print()
    print("HOW THEY WORK TOGETHER:")
    print("  1. Use TOOLS to analyze and discover")
    print("  2. Read RESOURCES for detailed content")
    print("  3. Apply PROMPTS for systematic workflows")
    print()
    print("=" * 70)
    print("Server ready on stdio")
    print("=" * 70)
    print()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

