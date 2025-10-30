#!/usr/bin/env python3
"""
Tutorial 1 Solution: File Processor with Streaming

This is a complete solution for Tutorial 1, demonstrating streaming
progress updates during file processing.
"""

import asyncio
import time
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("file-processor-server")


def find_files(directory: str, pattern: str) -> list[Path]:
    """Find all files matching pattern in directory."""
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    
    return sorted(dir_path.rglob(pattern))


def process_single_file(file_path: Path) -> dict:
    """Process a single file and return statistics."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        words = content.split()
        
        return {
            "file": str(file_path),
            "success": True,
            "lines": len(lines),
            "words": len(words),
            "characters": len(content),
            "size_bytes": file_path.stat().st_size
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "success": False,
            "error": str(e)
        }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="process_files",
            description="Process multiple files with progress updates",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory containing files to process",
                        "default": "."
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern (e.g., '*.txt', '*.md')",
                        "default": "*.md"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
    request_context: Any = None
) -> list[TextContent]:
    """Handle tool calls with streaming support."""
    
    if name == "process_files":
        directory = arguments.get("directory", ".")
        pattern = arguments.get("pattern", "*.md")
        
        files = find_files(directory, pattern)
        total_files = len(files)
        
        if total_files == 0:
            return [TextContent(
                type="text",
                text=f"No files found matching '{pattern}' in '{directory}'"
            )]
        
        results = []
        successful = 0
        failed = 0
        last_update_time = time.time()
        
        for i, file_path in enumerate(files):
            result = process_single_file(file_path)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # Send progress update every second or every 10 files
            current_time = time.time()
            should_update = (
                (current_time - last_update_time) >= 1.0 or
                (i + 1) % 10 == 0 or
                (i + 1) == total_files
            )
            
            if should_update:
                progress_pct = ((i + 1) / total_files) * 100
                print(f"  Progress: {i + 1}/{total_files} ({progress_pct:.1f}%)", flush=True)
                last_update_time = current_time
        
        return [TextContent(
            type="text",
            text=f"""File Processing Complete

Summary:
- Total files: {total_files}
- Successful: {successful}
- Failed: {failed}

Details:
{chr(10).join(f"  - {r['file']}: {'✓' if r['success'] else '✗'}" for r in results)}
"""
        )]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    print("Starting File Processor Server with Streaming...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

