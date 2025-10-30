#!/usr/bin/env python3
"""
File Operations MCP Server

A practical MCP server demonstrating file system operations:
- read_file: Read and return the contents of a file
- write_file: Write or overwrite a file with new content
- list_directory: List files and directories in a given path

This server demonstrates:
- Working with the file system
- Path validation and security considerations
- Different parameter types (strings, optional parameters)
- Handling real-world errors (file not found, permission denied, etc.)

SECURITY NOTE: This is a learning example. In production, you should:
- Restrict file operations to specific directories (sandboxing)
- Validate and sanitize all paths
- Implement proper authentication and authorization
- Log all file operations for auditing
"""

import asyncio
import os
from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the server
app = Server("file-operations-server")


# ============================================================================
# CONFIGURATION
# ============================================================================
# In a production server, you'd want to configure allowed directories

# For this example, we'll use a workspace directory
# You should change this to an appropriate location for testing
WORKSPACE_DIR = Path.home() / "mcp_workspace"

# Create the workspace directory if it doesn't exist
WORKSPACE_DIR.mkdir(exist_ok=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def resolve_path(relative_path: str) -> Path:
    """
    Resolve a relative path to an absolute path within the workspace.
    
    This provides basic path traversal protection by ensuring all
    operations stay within the workspace directory.
    
    Args:
        relative_path: Path relative to workspace
        
    Returns:
        Absolute Path object
        
    Raises:
        ValueError: If path tries to escape workspace
    """
    # Convert to Path object and resolve to absolute path
    requested_path = (WORKSPACE_DIR / relative_path).resolve()
    
    # Ensure the path is within our workspace (security check)
    try:
        requested_path.relative_to(WORKSPACE_DIR)
    except ValueError:
        raise ValueError(
            f"Access denied: Path '{relative_path}' is outside the workspace"
        )
    
    return requested_path


def format_file_list(path: Path) -> str:
    """
    Format a directory listing as a human-readable string.
    
    Args:
        path: Directory path to list
        
    Returns:
        Formatted string listing files and directories
    """
    try:
        items = sorted(path.iterdir())
        
        if not items:
            return "Directory is empty"
        
        lines = [f"Contents of {path}:\n"]
        
        for item in items:
            # Add indicator for directories
            if item.is_dir():
                lines.append(f"  [DIR]  {item.name}/")
            else:
                # Show file size
                size = item.stat().st_size
                lines.append(f"  [FILE] {item.name} ({size} bytes)")
        
        return "\n".join(lines)
    
    except PermissionError:
        raise PermissionError(f"Permission denied to list directory: {path}")


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Return all available file operation tools.
    
    Each tool has different parameter requirements based on its operation.
    """
    return [
        Tool(
            name="read_file",
            description=(
                f"Read the contents of a file from the workspace directory "
                f"({WORKSPACE_DIR}). Provide a relative path to the file you want to read. "
                f"Returns the file contents as text."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file, relative to workspace directory"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description=(
                f"Write content to a file in the workspace directory ({WORKSPACE_DIR}). "
                f"Creates the file if it doesn't exist, overwrites if it does. "
                f"Parent directories will be created automatically."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file, relative to workspace directory"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description=(
                f"List the contents of a directory in the workspace ({WORKSPACE_DIR}). "
                f"Shows files and subdirectories with their sizes. "
                f"If no path is provided, lists the root workspace directory."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the directory, relative to workspace. Leave empty for workspace root."
                    }
                },
                # Note: 'path' is optional for this tool
                "required": []
            }
        )
    ]


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

async def handle_read_file(arguments: dict) -> list[TextContent]:
    """
    Handle the read_file tool invocation.
    
    Args:
        arguments: Dictionary containing 'path' parameter
        
    Returns:
        File contents or error message
    """
    path_str = arguments.get("path")
    
    if not path_str:
        return [TextContent(
            type="text",
            text="Error: 'path' parameter is required"
        )]
    
    try:
        # Resolve and validate the path
        file_path = resolve_path(path_str)
        
        # Check if file exists
        if not file_path.exists():
            return [TextContent(
                type="text",
                text=f"Error: File not found: {path_str}"
            )]
        
        # Check if it's actually a file (not a directory)
        if not file_path.is_file():
            return [TextContent(
                type="text",
                text=f"Error: {path_str} is not a file"
            )]
        
        # Read the file contents
        content = file_path.read_text(encoding="utf-8")
        
        return [TextContent(
            type="text",
            text=f"Contents of {path_str}:\n\n{content}"
        )]
    
    except ValueError as e:
        # Path validation error (e.g., trying to escape workspace)
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    except PermissionError:
        return [TextContent(
            type="text",
            text=f"Error: Permission denied to read: {path_str}"
        )]
    
    except UnicodeDecodeError:
        return [TextContent(
            type="text",
            text=f"Error: File {path_str} is not a text file (binary file detected)"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error reading file: {str(e)}"
        )]


async def handle_write_file(arguments: dict) -> list[TextContent]:
    """
    Handle the write_file tool invocation.
    
    Args:
        arguments: Dictionary containing 'path' and 'content' parameters
        
    Returns:
        Success confirmation or error message
    """
    path_str = arguments.get("path")
    content = arguments.get("content")
    
    if not path_str:
        return [TextContent(
            type="text",
            text="Error: 'path' parameter is required"
        )]
    
    if content is None:  # Allow empty string but not None
        return [TextContent(
            type="text",
            text="Error: 'content' parameter is required"
        )]
    
    try:
        # Resolve and validate the path
        file_path = resolve_path(path_str)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the content
        file_path.write_text(content, encoding="utf-8")
        
        # Get file size for confirmation
        size = file_path.stat().st_size
        
        return [TextContent(
            type="text",
            text=f"Successfully wrote {size} bytes to {path_str}"
        )]
    
    except ValueError as e:
        # Path validation error
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    except PermissionError:
        return [TextContent(
            type="text",
            text=f"Error: Permission denied to write: {path_str}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error writing file: {str(e)}"
        )]


async def handle_list_directory(arguments: dict) -> list[TextContent]:
    """
    Handle the list_directory tool invocation.
    
    Args:
        arguments: Dictionary optionally containing 'path' parameter
        
    Returns:
        Directory listing or error message
    """
    # Path is optional; default to workspace root
    path_str = arguments.get("path", "")
    
    try:
        # Resolve the path (empty string resolves to workspace root)
        dir_path = resolve_path(path_str) if path_str else WORKSPACE_DIR
        
        # Check if directory exists
        if not dir_path.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory not found: {path_str or '(workspace root)'}"
            )]
        
        # Check if it's actually a directory
        if not dir_path.is_dir():
            return [TextContent(
                type="text",
                text=f"Error: {path_str} is not a directory"
            )]
        
        # Format and return the listing
        listing = format_file_list(dir_path)
        
        return [TextContent(type="text", text=listing)]
    
    except ValueError as e:
        # Path validation error
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    except PermissionError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error listing directory: {str(e)}"
        )]


# ============================================================================
# TOOL CALL HANDLER
# ============================================================================

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Route tool calls to appropriate handlers.
    
    Args:
        name: Tool name
        arguments: Tool parameters
        
    Returns:
        Tool response
    """
    if name == "read_file":
        return await handle_read_file(arguments)
    
    elif name == "write_file":
        return await handle_write_file(arguments)
    
    elif name == "list_directory":
        return await handle_list_directory(arguments)
    
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


# ============================================================================
# SERVER LIFECYCLE
# ============================================================================

async def main():
    """
    Run the file operations MCP server.
    
    Prints the workspace directory on startup for reference.
    """
    print(f"File Operations Server starting...", file=os.sys.stderr)
    print(f"Workspace directory: {WORKSPACE_DIR}", file=os.sys.stderr)
    print(f"Server ready.", file=os.sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# USAGE EXAMPLES
# ============================================================================
#
# Test with MCP Inspector:
#   npx @modelcontextprotocol/inspector python file_server.py
#
# Example interactions:
#
# 1. List workspace (initially empty):
#    Tool: list_directory
#    Arguments: {}
#    Response: "Directory is empty"
#
# 2. Create a file:
#    Tool: write_file
#    Arguments: {"path": "notes.txt", "content": "Hello, MCP!"}
#    Response: "Successfully wrote 11 bytes to notes.txt"
#
# 3. Read the file:
#    Tool: read_file
#    Arguments: {"path": "notes.txt"}
#    Response: "Contents of notes.txt:\n\nHello, MCP!"
#
# 4. List workspace (now contains file):
#    Tool: list_directory
#    Arguments: {}
#    Response: "Contents of /path/to/workspace:\n  [FILE] notes.txt (11 bytes)"
#
# 5. Create file in subdirectory:
#    Tool: write_file
#    Arguments: {"path": "subdir/data.txt", "content": "More data"}
#    Response: "Successfully wrote 9 bytes to subdir/data.txt"
#
# 6. List subdirectory:
#    Tool: list_directory
#    Arguments: {"path": "subdir"}
#    Response: "Contents of /path/to/workspace/subdir:\n  [FILE] data.txt (9 bytes)"
#
# ============================================================================
# SECURITY CONSIDERATIONS
# ============================================================================
#
# This example includes basic security measures:
#
# 1. WORKSPACE SANDBOXING
#    - All operations restricted to WORKSPACE_DIR
#    - Path traversal attacks (../) are prevented
#    - resolve_path() validates all paths
#
# 2. ERROR HANDLING
#    - File not found errors
#    - Permission denied errors
#    - Binary file detection
#
# 3. PATH VALIDATION
#    - Paths must be relative to workspace
#    - Absolute paths are rejected
#    - Symlink resolution is handled
#
# For production use, you should add:
#
# 1. AUTHENTICATION
#    - Verify caller identity
#    - Implement access control lists
#
# 2. RATE LIMITING
#    - Limit operations per time period
#    - Prevent resource exhaustion
#
# 3. FILE SIZE LIMITS
#    - Reject very large files
#    - Prevent disk space exhaustion
#
# 4. AUDIT LOGGING
#    - Log all file operations
#    - Track who accessed what and when
#
# 5. VIRUS SCANNING
#    - Scan uploaded files
#    - Block suspicious content
#
# ============================================================================
# PATTERNS DEMONSTRATED
# ============================================================================
#
# 1. CONFIGURATION
#    - Workspace directory constant
#    - Initialization on startup
#
# 2. PATH HANDLING
#    - Using pathlib.Path for cross-platform compatibility
#    - Path resolution and validation
#    - Directory creation
#
# 3. OPTIONAL PARAMETERS
#    - list_directory has optional 'path' parameter
#    - Default values in function arguments
#    - Empty required list in schema
#
# 4. SEPARATE HANDLER FUNCTIONS
#    - Each tool has its own handler
#    - Cleaner code organization
#    - Easier to test individually
#
# 5. COMPREHENSIVE ERROR HANDLING
#    - Specific error types (FileNotFound, PermissionError, etc.)
#    - User-friendly error messages
#    - Graceful degradation
#
# 6. INFORMATIVE OUTPUT
#    - File sizes in responses
#    - Directory structure visualization
#    - Clear success/error messages
#
# ============================================================================

