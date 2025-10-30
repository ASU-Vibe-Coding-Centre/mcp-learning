#!/usr/bin/env python3
"""
Git Operations MCP Server

Provides access to local Git operations through MCP. Allows AI to interact
with Git repositories for version control tasks.

Features:
- Repository status and info
- Commit history and logs
- Diff viewing
- Branch management
- File operations
- Safe, read-only by default with explicit write operations

Usage:
    python git_server.py

Test with MCP Inspector:
    mcp-inspector python git_server.py

Configure for Claude Desktop:
    {
      "mcpServers": {
        "git": {
          "command": "python",
          "args": ["/path/to/git_server.py"],
          "env": {
            "GIT_REPO_PATH": "/path/to/your/repo"
          }
        }
      }
    }
"""

import asyncio
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool


# ============================================================================
# Configuration
# ============================================================================

# Default repository path (can be overridden with GIT_REPO_PATH env var)
DEFAULT_REPO_PATH = Path.cwd()
REPO_PATH = Path(os.environ.get("GIT_REPO_PATH", DEFAULT_REPO_PATH))


# ============================================================================
# Git Operations
# ============================================================================

class GitRepo:
    """
    Git repository operations wrapper.
    
    Provides safe, controlled access to Git operations.
    """
    
    def __init__(self, repo_path: Path):
        """
        Initialize Git repository wrapper.
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = repo_path
        self._verify_git_repo()
    
    def _verify_git_repo(self):
        """Verify that the path is a valid Git repository."""
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise ValueError(f"Not a Git repository: {self.repo_path}")
    
    def _run_git_command(self, args: list[str], capture_output: bool = True) -> str:
        """
        Run a Git command safely.
        
        Args:
            args: Git command arguments (e.g., ['status', '--short'])
            capture_output: Whether to capture and return output
        
        Returns:
            Command output as string
        
        Raises:
            Exception: If command fails
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                timeout=30,
                check=True
            )
            return result.stdout if capture_output else ""
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git command failed: {e.stderr or str(e)}")
        except subprocess.TimeoutExpired:
            raise Exception("Git command timed out")
        except FileNotFoundError:
            raise Exception("Git executable not found. Please ensure Git is installed.")
    
    def status(self, short: bool = False) -> str:
        """
        Get repository status.
        
        Args:
            short: Use short format
        
        Returns:
            Status output
        """
        args = ["status"]
        if short:
            args.append("--short")
        return self._run_git_command(args)
    
    def log(self, max_count: int = 10, oneline: bool = False, branch: Optional[str] = None) -> str:
        """
        Get commit history.
        
        Args:
            max_count: Maximum number of commits
            oneline: Use one line per commit
            branch: Specific branch (None for current)
        
        Returns:
            Log output
        """
        args = ["log", f"--max-count={max_count}"]
        
        if oneline:
            args.append("--oneline")
        else:
            args.extend(["--pretty=format:%H%n%an <%ae>%n%ad%n%s%n%b%n---"])
        
        if branch:
            args.append(branch)
        
        return self._run_git_command(args)
    
    def diff(self, path: Optional[str] = None, cached: bool = False) -> str:
        """
        Show changes.
        
        Args:
            path: Specific file/directory (None for all)
            cached: Show staged changes
        
        Returns:
            Diff output
        """
        args = ["diff"]
        
        if cached:
            args.append("--cached")
        
        if path:
            args.append("--")
            args.append(path)
        
        output = self._run_git_command(args)
        
        if not output:
            return "No changes" + (" (staged)" if cached else "")
        
        return output
    
    def show(self, commit: str = "HEAD") -> str:
        """
        Show commit details.
        
        Args:
            commit: Commit reference (default: HEAD)
        
        Returns:
            Commit details and diff
        """
        return self._run_git_command(["show", commit])
    
    def branch_list(self, all_branches: bool = False) -> str:
        """
        List branches.
        
        Args:
            all_branches: Include remote branches
        
        Returns:
            Branch list
        """
        args = ["branch"]
        if all_branches:
            args.append("--all")
        
        return self._run_git_command(args)
    
    def current_branch(self) -> str:
        """Get current branch name."""
        return self._run_git_command(["branch", "--show-current"]).strip()
    
    def remote_list(self) -> str:
        """List configured remotes."""
        return self._run_git_command(["remote", "-v"])
    
    def file_history(self, file_path: str, max_count: int = 10) -> str:
        """
        Get commit history for a specific file.
        
        Args:
            file_path: Path to file
            max_count: Maximum commits
        
        Returns:
            File history
        """
        return self._run_git_command([
            "log",
            f"--max-count={max_count}",
            "--oneline",
            "--",
            file_path
        ])
    
    def blame(self, file_path: str) -> str:
        """
        Show what revision and author last modified each line.
        
        Args:
            file_path: Path to file
        
        Returns:
            Blame output
        """
        return self._run_git_command(["blame", file_path])
    
    def list_files(self, tree: str = "HEAD") -> list[str]:
        """
        List files in repository.
        
        Args:
            tree: Tree reference (default: HEAD)
        
        Returns:
            List of file paths
        """
        output = self._run_git_command(["ls-tree", "-r", "--name-only", tree])
        return [line for line in output.split("\n") if line.strip()]
    
    def get_commit_info(self, commit: str = "HEAD") -> dict:
        """
        Get detailed commit information.
        
        Args:
            commit: Commit reference
        
        Returns:
            Dictionary with commit details
        """
        # Get commit hash
        commit_hash = self._run_git_command(["rev-parse", commit]).strip()
        
        # Get commit details
        format_str = "%H%n%an%n%ae%n%ad%n%s%n%b"
        output = self._run_git_command([
            "show",
            "-s",
            f"--format={format_str}",
            commit
        ])
        
        lines = output.strip().split("\n")
        
        return {
            "hash": lines[0] if len(lines) > 0 else "",
            "author_name": lines[1] if len(lines) > 1 else "",
            "author_email": lines[2] if len(lines) > 2 else "",
            "date": lines[3] if len(lines) > 3 else "",
            "subject": lines[4] if len(lines) > 4 else "",
            "body": "\n".join(lines[5:]) if len(lines) > 5 else ""
        }


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create server and Git repository wrapper
app = Server("git-operations-server")
git_repo = GitRepo(REPO_PATH)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Git operations."""
    return [
        Tool(
            name="git_status",
            description="Get the current status of the Git repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "short": {
                        "type": "boolean",
                        "description": "Use short format",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="git_log",
            description="View commit history",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_count": {
                        "type": "integer",
                        "description": "Maximum number of commits to show",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "oneline": {
                        "type": "boolean",
                        "description": "Show one line per commit",
                        "default": False
                    },
                    "branch": {
                        "type": "string",
                        "description": "Specific branch to view (optional)"
                    }
                }
            }
        ),
        Tool(
            name="git_diff",
            description="Show changes in the working directory or staged changes",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Specific file or directory path (optional)"
                    },
                    "cached": {
                        "type": "boolean",
                        "description": "Show staged changes instead of working directory",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="git_show_commit",
            description="Show details of a specific commit",
            inputSchema={
                "type": "object",
                "properties": {
                    "commit": {
                        "type": "string",
                        "description": "Commit reference (hash, branch, HEAD, etc.)",
                        "default": "HEAD"
                    }
                }
            }
        ),
        Tool(
            name="git_branch_list",
            description="List all branches",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {
                        "type": "boolean",
                        "description": "Include remote branches",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="git_current_branch",
            description="Get the name of the current branch",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="git_remote_list",
            description="List configured remote repositories",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="git_file_history",
            description="View commit history for a specific file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file"
                    },
                    "max_count": {
                        "type": "integer",
                        "description": "Maximum number of commits",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="git_blame",
            description="Show what revision and author last modified each line of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="git_list_files",
            description="List all files tracked by Git",
            inputSchema={
                "type": "object",
                "properties": {
                    "tree": {
                        "type": "string",
                        "description": "Tree reference (branch, commit, etc.)",
                        "default": "HEAD"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Git operations."""
    
    try:
        if name == "git_status":
            short = arguments.get("short", False)
            output = git_repo.status(short=short)
            
            if not output.strip():
                output = "Working tree clean"
            
            return [TextContent(type="text", text=f"Repository Status:\n\n{output}")]
        
        elif name == "git_log":
            max_count = arguments.get("max_count", 10)
            oneline = arguments.get("oneline", False)
            branch = arguments.get("branch")
            
            output = git_repo.log(max_count=max_count, oneline=oneline, branch=branch)
            
            title = f"Last {max_count} commits"
            if branch:
                title += f" on {branch}"
            
            return [TextContent(type="text", text=f"{title}:\n\n{output}")]
        
        elif name == "git_diff":
            path = arguments.get("path")
            cached = arguments.get("cached", False)
            
            output = git_repo.diff(path=path, cached=cached)
            
            location = f" in {path}" if path else ""
            stage = " (staged)" if cached else " (working directory)"
            
            return [TextContent(type="text", text=f"Changes{location}{stage}:\n\n{output}")]
        
        elif name == "git_show_commit":
            commit = arguments.get("commit", "HEAD")
            output = git_repo.show(commit=commit)
            
            return [TextContent(type="text", text=f"Commit {commit}:\n\n{output}")]
        
        elif name == "git_branch_list":
            all_branches = arguments.get("all", False)
            output = git_repo.branch_list(all_branches=all_branches)
            
            title = "All branches:" if all_branches else "Local branches:"
            return [TextContent(type="text", text=f"{title}\n\n{output}")]
        
        elif name == "git_current_branch":
            branch = git_repo.current_branch()
            
            if not branch:
                return [TextContent(type="text", text="Not on any branch (detached HEAD)")]
            
            return [TextContent(type="text", text=f"Current branch: {branch}")]
        
        elif name == "git_remote_list":
            output = git_repo.remote_list()
            
            if not output.strip():
                return [TextContent(type="text", text="No remotes configured")]
            
            return [TextContent(type="text", text=f"Configured remotes:\n\n{output}")]
        
        elif name == "git_file_history":
            file_path = arguments["file_path"]
            max_count = arguments.get("max_count", 10)
            
            output = git_repo.file_history(file_path, max_count=max_count)
            
            if not output.strip():
                return [TextContent(type="text", text=f"No history found for: {file_path}")]
            
            return [TextContent(type="text", text=f"History for {file_path}:\n\n{output}")]
        
        elif name == "git_blame":
            file_path = arguments["file_path"]
            output = git_repo.blame(file_path)
            
            return [TextContent(type="text", text=f"Blame for {file_path}:\n\n{output}")]
        
        elif name == "git_list_files":
            tree = arguments.get("tree", "HEAD")
            files = git_repo.list_files(tree=tree)
            
            if not files:
                return [TextContent(type="text", text=f"No files found in {tree}")]
            
            output = "\n".join(files)
            return [TextContent(type="text", text=f"Files in {tree} ({len(files)} total):\n\n{output}")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    Expose Git repository files as resources.
    
    This allows AI to read file contents from the repository.
    """
    try:
        files = git_repo.list_files()
        resources = []
        
        # Limit to reasonable number for listing
        for file_path in files[:100]:
            resources.append(Resource(
                uri=f"git://{file_path}",
                name=file_path,
                description=f"File from Git repository: {file_path}",
                mimeType="text/plain"  # Simplified, could detect based on extension
            ))
        
        return resources
    except Exception:
        # If listing fails, return empty list
        return []


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read file content from Git repository.
    
    Args:
        uri: Resource URI (e.g., "git://src/main.py")
    
    Returns:
        File content
    """
    if not uri.startswith("git://"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    # Extract file path
    file_path = uri[6:]  # Remove "git://"
    
    try:
        # Use git show to get file content at HEAD
        output = git_repo._run_git_command(["show", f"HEAD:{file_path}"])
        return output
    except Exception as e:
        raise ValueError(f"Failed to read file: {e}")


# ============================================================================
# Server Lifecycle
# ============================================================================

async def main():
    """Run the Git operations server."""
    print("=" * 70)
    print("Git Operations MCP Server")
    print("=" * 70)
    print()
    print(f"Repository: {REPO_PATH}")
    
    try:
        current_branch = git_repo.current_branch()
        print(f"Current branch: {current_branch or '(detached HEAD)'}")
    except Exception as e:
        print(f"Warning: Could not determine branch: {e}")
    
    print()
    print("Available operations:")
    print("  - Repository status")
    print("  - Commit history and logs")
    print("  - View diffs")
    print("  - Branch management")
    print("  - File history and blame")
    print("  - File content access (resources)")
    print()
    print("Note: All operations are read-only by default")
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
    try:
        asyncio.run(main())
    except ValueError as e:
        print(f"Error: {e}")
        print()
        print("Please run this server from within a Git repository,")
        print("or set GIT_REPO_PATH environment variable to a valid Git repository.")

