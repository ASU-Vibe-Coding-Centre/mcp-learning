# Tutorial 1: Implementing Streaming Responses

## Overview

In this tutorial, you'll learn how to implement streaming responses in an MCP server. Streaming allows your server to send progress updates during long-running operations, providing better user experience and feedback.

**Estimated Time:** 60 minutes

**Difficulty:** Intermediate

**Prerequisites:**
- Completed Module 03 (Basic MCP Server)
- Understanding of async/await in Python
- Familiarity with basic MCP server patterns

## Learning Objectives

By the end of this tutorial, you will be able to:

1. Understand when streaming is appropriate
2. Implement progress notifications during long operations
3. Use progress tokens to track operations
4. Balance update frequency for good UX
5. Test streaming servers with MCP Inspector

## Scenario

You'll build a **File Processor Server** that processes multiple files and streams progress updates as each file is processed. This is a common real-world pattern for operations like:

- Batch file processing
- Data migration
- Report generation
- Backup operations

## Step 1: Set Up Your Server File

Create a new file called `file_processor_server.py` in the exercises directory.

Start with the basic server structure:

```python
#!/usr/bin/env python3
"""
File Processor Server with Streaming

Processes multiple files and streams progress updates.
"""

import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server instance
app = Server("file-processor-server")

# We'll add handlers here

async def main():
    """Run the MCP server."""
    print("Starting File Processor Server...")
    print("Supports streaming progress updates")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

Make the file executable:

```bash
chmod +x file_processor_server.py
```

## Step 2: Define Your Tool

Add the tool definition that will support streaming:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="process_files",
            description=(
                "Process multiple files with progress updates. "
                "For demonstration, processes text files and reports statistics."
            ),
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
```

**Key Points:**
- The tool accepts a directory and file pattern
- Description clearly indicates streaming behavior
- Parameters have sensible defaults

## Step 3: Implement File Processing Logic

Before implementing the tool handler, create helper functions:

```python
def find_files(directory: str, pattern: str) -> list[Path]:
    """Find all files matching pattern in directory."""
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return []
    
    if not dir_path.is_dir():
        return []
    
    # Use rglob for recursive search
    return sorted(dir_path.rglob(pattern))


def process_single_file(file_path: Path) -> dict:
    """
    Process a single file and return statistics.
    
    In a real application, this might:
    - Transform file content
    - Extract data
    - Validate format
    - Generate thumbnails
    - etc.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate statistics
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
```

**What This Does:**
- `find_files()`: Discovers files to process
- `process_single_file()`: Simulates file processing with statistics

## Step 4: Implement Streaming Tool Handler

Now implement the tool handler with streaming support:

```python
@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
    request_context: Any
) -> list[TextContent]:
    """
    Handle tool calls with streaming support.
    
    Note: request_context is used to send progress updates.
    """
    
    if name == "process_files":
        directory = arguments.get("directory", ".")
        pattern = arguments.get("pattern", "*.md")
        
        # Find files to process
        files = find_files(directory, pattern)
        total_files = len(files)
        
        if total_files == 0:
            return [TextContent(
                type="text",
                text=f"No files found matching '{pattern}' in '{directory}'"
            )]
        
        # Generate unique progress token
        # This identifies this specific operation
        progress_token = f"process-{id(request_context)}"
        
        # Process files with progress updates
        results = []
        successful = 0
        failed = 0
        
        for i, file_path in enumerate(files):
            # Process the file
            result = process_single_file(file_path)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            # STREAMING: Send progress update
            # In the actual MCP implementation, you would use:
            # await request_context.send_progress(
            #     progress_token=progress_token,
            #     progress=i + 1,
            #     total=total_files
            # )
            
            # For this tutorial, we'll simulate the streaming behavior
            # by adding a small delay and printing progress
            await asyncio.sleep(0.1)  # Simulate processing time
            
            # Send progress every file or every second
            progress_pct = ((i + 1) / total_files) * 100
            print(f"  Progress: {i + 1}/{total_files} ({progress_pct:.1f}%)")
        
        # Return final results
        summary = {
            "total_files": total_files,
            "successful": successful,
            "failed": failed,
            "results": results
        }
        
        return [TextContent(
            type="text",
            text=f"""File Processing Complete

Summary:
- Total files: {total_files}
- Successful: {successful}
- Failed: {failed}

Detailed Results:
{chr(10).join(f"  - {r['file']}: {'✓' if r['success'] else '✗'}" for r in results)}
"""
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]
```

**Key Streaming Concepts:**

1. **Progress Token**: Unique identifier for this operation
   ```python
   progress_token = f"process-{id(request_context)}"
   ```

2. **Progress Updates**: Sent during processing
   ```python
   # In production, use:
   await request_context.send_progress(
       progress_token=progress_token,
       progress=current,
       total=total
   )
   ```

3. **Update Frequency**: Balance between too many and too few updates
   - Update every N items (e.g., every 10 files)
   - Update every N seconds (e.g., every 1-2 seconds)
   - Always update at significant milestones

4. **Final Result**: Always return complete result at the end

## Step 5: Test Your Server

Save your file and test it:

```bash
# Test with Python directly
python file_processor_server.py
```

The server should start without errors.

### Test with MCP Inspector

```bash
# Install MCP Inspector if not already installed
npm install -g @modelcontextprotocol/inspector

# Run with Inspector
mcp-inspector python file_processor_server.py
```

In the Inspector:

1. **List Tools**: Verify `process_files` appears
2. **Call Tool**: Try processing files:
   ```json
   {
     "directory": "../../resources",
     "pattern": "*.md"
   }
   ```
3. **Watch Console**: You should see progress updates in the terminal
4. **Check Response**: Verify complete results are returned

## Step 6: Enhance with Better Progress Updates

Improve the progress update logic to handle different scenarios:

```python
# Add after your imports
import time

# Update the tool handler with better progress tracking
@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
    request_context: Any
) -> list[TextContent]:
    """Handle tool calls with improved streaming."""
    
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
        
        progress_token = f"process-{id(request_context)}"
        
        results = []
        successful = 0
        failed = 0
        
        # Track timing for better progress updates
        last_update_time = time.time()
        update_interval = 1.0  # Update at least every 1 second
        
        for i, file_path in enumerate(files):
            result = process_single_file(file_path)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # SMART UPDATE LOGIC:
            # Update if:
            # - At least 1 second has passed, OR
            # - Every 10 files, OR
            # - This is the last file
            current_time = time.time()
            should_update = (
                (current_time - last_update_time) >= update_interval or
                (i + 1) % 10 == 0 or
                (i + 1) == total_files
            )
            
            if should_update:
                progress_pct = ((i + 1) / total_files) * 100
                print(f"  Progress: {i + 1}/{total_files} ({progress_pct:.1f}%) - {successful} successful, {failed} failed")
                last_update_time = current_time
        
        # Return results...
        # (same as before)
```

**What Changed:**
- Added time-based update threshold
- Update at least every second
- Update every 10 files
- Always update on last file
- Include success/failure counts in progress

## Step 7: Add Error Handling

Make your streaming robust with error handling:

```python
@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
    request_context: Any
) -> list[TextContent]:
    """Handle tool calls with error-safe streaming."""
    
    if name == "process_files":
        directory = arguments.get("directory", ".")
        pattern = arguments.get("pattern", "*.md")
        
        # Validate directory
        dir_path = Path(directory)
        if not dir_path.exists():
            return [TextContent(
                type="text",
                text=f"Error: Directory '{directory}' does not exist"
            )]
        
        if not dir_path.is_dir():
            return [TextContent(
                type="text",
                text=f"Error: '{directory}' is not a directory"
            )]
        
        files = find_files(directory, pattern)
        total_files = len(files)
        
        if total_files == 0:
            return [TextContent(
                type="text",
                text=f"No files found matching '{pattern}' in '{directory}'"
            )]
        
        progress_token = f"process-{id(request_context)}"
        
        results = []
        successful = 0
        failed = 0
        last_update_time = time.time()
        
        for i, file_path in enumerate(files):
            try:
                # Process file
                result = process_single_file(file_path)
                results.append(result)
                
                if result["success"]:
                    successful += 1
                else:
                    failed += 1
                
                # Simulate processing
                await asyncio.sleep(0.1)
                
                # Send progress update
                current_time = time.time()
                if ((current_time - last_update_time) >= 1.0 or
                    (i + 1) % 10 == 0 or
                    (i + 1) == total_files):
                    
                    progress_pct = ((i + 1) / total_files) * 100
                    print(f"  Progress: {i + 1}/{total_files} ({progress_pct:.1f}%)")
                    last_update_time = current_time
            
            except Exception as e:
                # Handle unexpected errors gracefully
                print(f"  Error processing {file_path}: {e}")
                results.append({
                    "file": str(file_path),
                    "success": False,
                    "error": str(e)
                })
                failed += 1
        
        # Return final results
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
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]
```

## Challenge Extensions

Try these enhancements to deepen your understanding:

### Challenge 1: Detailed Progress Messages

Instead of just numbers, send descriptive progress messages:

```python
print(f"  Processing: {file_path.name} ({i+1}/{total_files})")
```

### Challenge 2: Estimated Time Remaining

Calculate and display estimated time to completion:

```python
elapsed = time.time() - start_time
rate = (i + 1) / elapsed  # files per second
remaining_files = total_files - (i + 1)
eta_seconds = remaining_files / rate if rate > 0 else 0
print(f"  ETA: {eta_seconds:.1f}s")
```

### Challenge 3: Cancellation Support

Allow operations to be cancelled (advanced):

```python
# Check if operation should be cancelled
if should_cancel():
    return [TextContent(
        type="text",
        text="Operation cancelled by user"
    )]
```

### Challenge 4: Different Update Strategies

Implement configurable update frequency:

```python
{
    "update_strategy": "time",  # or "count" or "percent"
    "update_interval": 2.0,  # seconds, or 10 files, or 5%
}
```

## Testing Checklist

Verify your implementation handles these scenarios:

- [ ] Processes multiple files successfully
- [ ] Shows progress updates during processing
- [ ] Handles empty directories gracefully
- [ ] Handles non-existent directories with clear error
- [ ] Handles files that can't be read (permission errors)
- [ ] Returns complete results at the end
- [ ] Progress percentages are accurate
- [ ] Works with different file patterns

## Common Issues and Solutions

### Issue: No Progress Updates Appear

**Problem:** You don't see progress updates in the console.

**Solution:** Check that you're:
- Using `await asyncio.sleep(0)` or similar to yield control
- Printing to stdout, not stderr
- Flushing output if needed: `print(..., flush=True)`

### Issue: Updates Too Frequent

**Problem:** Console is flooded with progress updates.

**Solution:** Adjust update frequency:
- Increase time threshold (e.g., 2 seconds instead of 1)
- Update less frequently (e.g., every 20 files instead of 10)
- Use exponential backoff for very long operations

### Issue: Final Result Missing

**Problem:** Progress updates work but no final result.

**Solution:** Always return a `TextContent` list at the end of your handler.

## Key Takeaways

1. **Streaming Improves UX**: Long operations feel faster with progress feedback
2. **Balance is Important**: Not too many updates, not too few
3. **Always Return Results**: Progress is supplementary to final results
4. **Progress Tokens Matter**: They identify specific operations
5. **Error Handling**: Stream progress even when errors occur

## Next Steps

- Complete Tutorial 2 (Resources)
- Try Challenge 1 (SQLite with Streaming)
- Review the streaming_server.py example for more patterns
- Experiment with different progress update strategies

## Solution

A complete solution is available in `solutions/tutorial-1-solution.py`.

Compare your implementation with the solution to see different approaches and optimizations.

Great work! You now understand how to implement streaming in MCP servers.

