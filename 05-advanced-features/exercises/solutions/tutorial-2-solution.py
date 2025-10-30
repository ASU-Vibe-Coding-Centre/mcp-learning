#!/usr/bin/env python3
"""
Tutorial 2 Solution: Documentation Resource Server

This is a complete solution for Tutorial 2, demonstrating resource
implementation with templates and security.
"""

import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceTemplate, TextContent, Tool

app = Server("documentation-resource-server")

# Define project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "resources"


def is_safe_path(base: Path, target: Path) -> bool:
    """Check if target path is within base path."""
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources."""
    resources = []
    
    # Find markdown files in docs directory
    if DOCS_DIR.exists() and DOCS_DIR.is_dir():
        md_files = sorted(DOCS_DIR.rglob("*.md"))
        
        for md_file in md_files:
            try:
                relative_path = md_file.relative_to(PROJECT_ROOT)
                
                resources.append(Resource(
                    uri=f"file:///{relative_path.as_posix()}",
                    name=f"Documentation: {md_file.stem}",
                    description=f"Project documentation: {relative_path}",
                    mimeType="text/markdown"
                ))
            except ValueError:
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


@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List resource templates for dynamic discovery."""
    return [
        ResourceTemplate(
            uriTemplate="file:///{path}",
            name="Project Files",
            description="Access any file in the project by path",
            mimeType="text/plain"
        ),
        ResourceTemplate(
            uriTemplate="file:///resources/{category}/{filename}",
            name="Resource Files by Category",
            description="Access resource files by category",
            mimeType="text/markdown"
        ),
        ResourceTemplate(
            uriTemplate="file:///{module}/README.md",
            name="Module README Files",
            description="Access README for any module",
            mimeType="text/markdown"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read the content of a resource."""
    if not uri.startswith("file:///"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    # Extract path from URI
    path_str = uri[8:]  # Remove "file:///"
    file_path = PROJECT_ROOT / path_str
    
    # Security: ensure path is within PROJECT_ROOT
    if not is_safe_path(PROJECT_ROOT, file_path):
        raise PermissionError(f"Access denied: {uri}")
    
    # Check file exists
    if not file_path.exists():
        raise ValueError(f"Resource not found: {uri}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file: {uri}")
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError(f"Binary file cannot be read as text: {uri}")


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
                        "description": "Text to search for"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for resource discovery."""
    
    if name == "search_documentation":
        query = arguments["query"].lower()
        results = []
        
        if DOCS_DIR.exists():
            for md_file in DOCS_DIR.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        if query in f.read().lower():
                            relative_path = md_file.relative_to(PROJECT_ROOT)
                            results.append({
                                "file": str(relative_path),
                                "uri": f"file:///{relative_path.as_posix()}"
                            })
                except:
                    continue
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No documentation found containing '{query}'"
            )]
        
        return [TextContent(
            type="text",
            text=f"""Found {len(results)} files containing '{query}':

{chr(10).join(f"  - {r['file']}" for r in results)}

Use read_resource() to read any file by its URI.
"""
        )]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


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

