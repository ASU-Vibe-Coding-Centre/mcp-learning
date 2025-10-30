#!/usr/bin/env python3
"""
MCP Server with Resources - File System Example

This example demonstrates how to implement resources in an MCP server.
Resources expose data and content that AI models can read for context,
as opposed to tools which perform actions.

Key Concepts Demonstrated:
1. Defining resources with URIs, names, descriptions, and MIME types
2. Implementing resource templates for dynamic discovery
3. Reading resource content by URI
4. Difference between resources (data access) and tools (actions)
5. Security considerations for file system access

Usage:
    python resource_server.py

Test with MCP Inspector:
    mcp-inspector python resource_server.py
"""

import asyncio
import json
import mimetypes
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceTemplate, TextContent, Tool


# ============================================================================
# File System Resource Management
# ============================================================================

# Define the root directory for resources
# In this example, we'll use the parent directory of this script
RESOURCE_ROOT = Path(__file__).parent.parent.parent
EXAMPLES_DIR = Path(__file__).parent


def is_safe_path(base_path: Path, requested_path: Path) -> bool:
    """
    Verify that a requested path is within the allowed base path.
    
    This prevents directory traversal attacks where malicious users
    might try to access files outside the intended directory.
    
    Args:
        base_path: The allowed root directory
        requested_path: The path being requested
    
    Returns:
        True if the path is safe to access, False otherwise
    """
    try:
        # Resolve both paths to absolute paths
        base_abs = base_path.resolve()
        requested_abs = requested_path.resolve()
        
        # Check if requested path is within base path
        return requested_abs.is_relative_to(base_abs)
    except (ValueError, OSError):
        return False


def uri_to_path(uri: str) -> Path:
    """
    Convert a resource URI to a file system path.
    
    Args:
        uri: Resource URI (e.g., "file:///docs/readme.md")
    
    Returns:
        Path object for the file
    
    Raises:
        ValueError: If URI format is invalid
    """
    if not uri.startswith("file://"):
        raise ValueError(f"Invalid URI scheme. Expected 'file://', got '{uri}'")
    
    # Remove 'file://' prefix and convert to path
    # The path after file:// is relative to RESOURCE_ROOT
    relative_path = uri[7:]  # Remove 'file://'
    
    if relative_path.startswith("/"):
        relative_path = relative_path[1:]
    
    return RESOURCE_ROOT / relative_path


def path_to_uri(path: Path) -> str:
    """
    Convert a file system path to a resource URI.
    
    Args:
        path: File system path
    
    Returns:
        Resource URI string
    """
    # Get path relative to RESOURCE_ROOT
    try:
        relative = path.relative_to(RESOURCE_ROOT)
        return f"file:///{relative.as_posix()}"
    except ValueError:
        # Path is not relative to RESOURCE_ROOT
        return f"file:///{path.as_posix()}"


def get_mime_type(path: Path) -> str:
    """
    Determine the MIME type for a file.
    
    Args:
        path: File path
    
    Returns:
        MIME type string (e.g., "text/plain", "application/json")
    """
    # Use mimetypes module for detection
    mime_type, _ = mimetypes.guess_type(str(path))
    
    if mime_type:
        return mime_type
    
    # Fallback for common programming file extensions
    suffix = path.suffix.lower()
    fallbacks = {
        ".py": "text/x-python",
        ".js": "text/javascript",
        ".ts": "text/typescript",
        ".md": "text/markdown",
        ".json": "application/json",
        ".yaml": "text/yaml",
        ".yml": "text/yaml",
        ".toml": "text/toml",
        ".txt": "text/plain",
        ".log": "text/plain",
    }
    
    return fallbacks.get(suffix, "application/octet-stream")


def list_files_in_directory(directory: Path, pattern: str = "*") -> list[Path]:
    """
    List all files in a directory matching a pattern.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern for matching files
    
    Returns:
        List of file paths
    """
    if not directory.exists():
        return []
    
    if not directory.is_dir():
        return []
    
    try:
        # Use rglob for recursive search
        files = [f for f in directory.rglob(pattern) if f.is_file()]
        return sorted(files)
    except PermissionError:
        return []


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create the MCP server instance
app = Server("resource-file-system-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    List all available resources.
    
    Resources in this server include:
    1. Example Python files from the examples/ directory
    2. Key project files (README.md, requirements.txt, etc.)
    
    Returns:
        List of Resource definitions
    """
    resources = []
    
    # ========================================================================
    # Example Code Resources
    # ========================================================================
    
    if EXAMPLES_DIR.exists():
        # Find all Python files in examples/
        py_files = [f for f in EXAMPLES_DIR.glob("*.py") if f.is_file()]
        for py_file in py_files:
            if is_safe_path(RESOURCE_ROOT, py_file):
                relative_path = py_file.relative_to(RESOURCE_ROOT)
                resources.append(Resource(
                    uri=f"file:///{relative_path.as_posix()}",
                    name=f"Example: {py_file.stem}",
                    description=f"Example MCP server: {relative_path}",
                    mimeType="text/x-python"
                ))
    
    # ========================================================================
    # Key Project Files
    # ========================================================================
    
    key_files = [
        ("README.md", "Main project README", "text/markdown"),
        ("requirements.txt", "Python dependencies", "text/plain"),
        ("pyproject.toml", "Project configuration", "text/toml"),
        ("QUICK_START.md", "Quick start guide", "text/markdown"),
        ("LEARNING_PATH.md", "Learning path guide", "text/markdown"),
    ]
    
    for filename, description, mime_type in key_files:
        file_path = RESOURCE_ROOT / filename
        if file_path.exists() and is_safe_path(RESOURCE_ROOT, file_path):
            resources.append(Resource(
                uri=f"file:///{filename}",
                name=filename,
                description=description,
                mimeType=mime_type
            ))
    
    return resources


@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """
    List resource templates for dynamic resource discovery.
    
    Templates allow clients to construct URIs for resources that
    aren't explicitly listed. This is useful for large file systems
    where listing all resources would be impractical.
    
    Returns:
        List of ResourceTemplate definitions
    """
    return [
        ResourceTemplate(
            uriTemplate="file:///{path}",
            name="File System Access",
            description=(
                "Access any file in the project by path. "
                "Path should be relative to project root. "
                "Example: file:///03-basic-mcp-server/README.md"
            ),
            mimeType="application/octet-stream"  # Generic, actual type determined at read time
        ),
        ResourceTemplate(
            uriTemplate="file:///{module}/README.md",
            name="Module Documentation",
            description=(
                "Access README for any module. "
                "Modules: 01-introduction, 02-environment-setup, 03-basic-mcp-server, etc. "
                "Example: file:///03-basic-mcp-server/README.md"
            ),
            mimeType="text/markdown"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read the content of a specific resource.
    
    This handler:
    1. Converts URI to file system path
    2. Validates the path is safe (no directory traversal)
    3. Reads and returns the file content
    
    Args:
        uri: Resource URI to read
    
    Returns:
        Resource content as string
    
    Raises:
        ValueError: If URI is invalid or file doesn't exist
        PermissionError: If file is outside allowed directory
    """
    try:
        # Convert URI to path
        file_path = uri_to_path(uri)
        
        # Security check: ensure path is within RESOURCE_ROOT
        if not is_safe_path(RESOURCE_ROOT, file_path):
            raise PermissionError(
                f"Access denied: {uri} is outside the allowed directory"
            )
        
        # Check if file exists
        if not file_path.exists():
            raise ValueError(f"Resource not found: {uri}")
        
        if not file_path.is_file():
            raise ValueError(f"Resource is not a file: {uri}")
        
        # Read file content
        try:
            # Try reading as text first
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            # If binary file, return error (MCP text resources should be text)
            raise ValueError(
                f"Resource is binary and cannot be read as text: {uri}"
            )
    
    except Exception as e:
        # Re-raise with more context
        raise ValueError(f"Error reading resource {uri}: {str(e)}")


# ============================================================================
# Tools for Resource Management
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List tools for working with resources.
    
    While resources are primarily for reading, tools can help
    discover and search for resources.
    
    Returns:
        List of Tool definitions
    """
    return [
        Tool(
            name="search_files",
            description=(
                "Search for files in the project by pattern. "
                "Returns a list of matching file URIs that can be read as resources."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match files (e.g., '*.py', '**/*.md')"
                    },
                    "directory": {
                        "type": "string",
                        "description": "Directory to search in (relative to project root, optional)",
                        "default": "."
                    }
                },
                "required": ["pattern"]
            }
        ),
        Tool(
            name="get_file_info",
            description="Get metadata about a file (size, modification time, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "uri": {
                        "type": "string",
                        "description": "File URI (e.g., 'file:///README.md')"
                    }
                },
                "required": ["uri"]
            }
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path relative to project root"
                    }
                },
                "required": ["path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution for resource discovery.
    
    Args:
        name: Tool name
        arguments: Tool arguments
    
    Returns:
        List of TextContent with results
    """
    
    # ========================================================================
    # Tool 1: Search Files
    # ========================================================================
    if name == "search_files":
        pattern = arguments["pattern"]
        directory = arguments.get("directory", ".")
        
        search_path = RESOURCE_ROOT / directory
        
        if not is_safe_path(RESOURCE_ROOT, search_path):
            return [TextContent(
                type="text",
                text=f"Error: Directory '{directory}' is outside allowed path"
            )]
        
        if not search_path.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory '{directory}' does not exist"
            )]
        
        # Search for matching files
        matching_files = list_files_in_directory(search_path, pattern)
        
        # Convert to URIs
        results = []
        for file_path in matching_files:
            if is_safe_path(RESOURCE_ROOT, file_path):
                uri = path_to_uri(file_path)
                relative = file_path.relative_to(RESOURCE_ROOT)
                results.append({
                    "uri": uri,
                    "path": str(relative),
                    "name": file_path.name,
                    "mime_type": get_mime_type(file_path)
                })
        
        return [TextContent(
            type="text",
            text=f"""Found {len(results)} matching files:

{json.dumps(results, indent=2)}

These files can be read as resources using their URIs.
"""
        )]
    
    # ========================================================================
    # Tool 2: Get File Info
    # ========================================================================
    elif name == "get_file_info":
        uri = arguments["uri"]
        
        try:
            file_path = uri_to_path(uri)
            
            if not is_safe_path(RESOURCE_ROOT, file_path):
                return [TextContent(
                    type="text",
                    text=f"Error: File is outside allowed path"
                )]
            
            if not file_path.exists():
                return [TextContent(
                    type="text",
                    text=f"Error: File not found"
                )]
            
            # Gather file information
            stat = file_path.stat()
            info = {
                "uri": uri,
                "path": str(file_path.relative_to(RESOURCE_ROOT)),
                "name": file_path.name,
                "size_bytes": stat.st_size,
                "size_human": f"{stat.st_size / 1024:.2f} KB" if stat.st_size > 1024 else f"{stat.st_size} bytes",
                "modified": stat.st_mtime,
                "mime_type": get_mime_type(file_path),
                "is_text": get_mime_type(file_path).startswith("text/")
            }
            
            return [TextContent(
                type="text",
                text=f"""File Information:

{json.dumps(info, indent=2)}
"""
            )]
        
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
    
    # ========================================================================
    # Tool 3: List Directory
    # ========================================================================
    elif name == "list_directory":
        path = arguments["path"]
        dir_path = RESOURCE_ROOT / path
        
        if not is_safe_path(RESOURCE_ROOT, dir_path):
            return [TextContent(
                type="text",
                text=f"Error: Directory is outside allowed path"
            )]
        
        if not dir_path.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory not found"
            )]
        
        if not dir_path.is_dir():
            return [TextContent(
                type="text",
                text=f"Error: Path is not a directory"
            )]
        
        # List directory contents
        try:
            items = []
            for item in sorted(dir_path.iterdir()):
                if item.name.startswith("."):
                    continue  # Skip hidden files
                
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                }
                
                if item.is_file():
                    item_info["uri"] = path_to_uri(item)
                    item_info["mime_type"] = get_mime_type(item)
                
                items.append(item_info)
            
            return [TextContent(
                type="text",
                text=f"""Directory contents for '{path}':

{json.dumps(items, indent=2)}
"""
            )]
        
        except PermissionError:
            return [TextContent(
                type="text",
                text=f"Error: Permission denied reading directory"
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
    print("Starting MCP resource file system server...")
    print(f"Resource root: {RESOURCE_ROOT}")
    print("Ready to accept connections via stdio")
    print()
    print("This server exposes:")
    print("  - Resources: Files that can be read for context")
    print("  - Resource Templates: Dynamic file access patterns")
    print("  - Tools: File search and discovery")
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

