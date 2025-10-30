# Tutorial 2: Building a GitHub Issue Manager

In this tutorial, you'll build a practical MCP server that interacts with the GitHub API to manage issues. This demonstrates real-world API integration, authentication, error handling, and rate limiting - all essential patterns for production MCP servers.

## Learning Objectives

By completing this tutorial, you will:

1. Integrate with external REST APIs in MCP servers
2. Implement authentication using environment variables
3. Handle API rate limits and errors gracefully
4. Build tools for listing, creating, and managing GitHub issues
5. Test API integrations with real services
6. Deploy an API-backed server to Cursor IDE

## Time Estimate

60-75 minutes

## Prerequisites

Before starting, ensure you have:

- Completed Module 03 (Basic MCP Server)
- Completed Tutorial 1 (Cursor IDE Integration) recommended
- GitHub account (free tier is fine)
- Basic understanding of REST APIs
- `requests` library installed: `pip install requests`

## What You'll Build

A GitHub issue management server with tools to:

1. **List issues** - View open/closed issues in a repository
2. **Create issue** - Create new issues with title, description, and labels
3. **Get issue details** - View full information about a specific issue
4. **Search issues** - Find issues matching specific criteria

This is a practical tool you can actually use for managing GitHub projects!

## Overview: GitHub API Basics

Before coding, let's understand what we're working with.

**GitHub REST API:**

- Base URL: `https://api.github.com`
- Authentication: Personal Access Token (PAT)
- Rate Limits: 5000 requests/hour (authenticated), 60/hour (unauthenticated)
- Response Format: JSON

**Common Endpoints:**

```
GET  /repos/{owner}/{repo}/issues          # List issues
POST /repos/{owner}/{repo}/issues          # Create issue
GET  /repos/{owner}/{repo}/issues/{number} # Get issue details
```

**Authentication Header:**

```
Authorization: token ghp_yourTokenHere
```

We'll handle all of this in our server!

## Step 1: Set Up GitHub Authentication

First, you need a GitHub Personal Access Token.

### Create a GitHub Token

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token (Classic)**
   - Click "Generate new token (classic)"
   - Give it a descriptive name: "MCP Server Tutorial"

3. **Select Scopes**
   For this tutorial, select:
   - `repo` - Full control of private repositories (includes issues)
   - Or just `public_repo` if you only need public repos

4. **Generate and Copy**
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Store Your Token Securely

**Important:** Never hardcode tokens in your code!

Create an environment variable:

```bash
# macOS/Linux - Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_token_here"

# Then reload
source ~/.bashrc  # or ~/.zshrc

# Windows PowerShell
$env:GITHUB_TOKEN="ghp_your_token_here"

# Windows CMD
set GITHUB_TOKEN=ghp_your_token_here
```

Verify it's set:

```bash
echo $GITHUB_TOKEN  # macOS/Linux
echo %GITHUB_TOKEN%  # Windows CMD
echo $env:GITHUB_TOKEN  # Windows PowerShell
```

## Step 2: Create the Server Structure

Create a new file: `github_issue_server.py`

```python
#!/usr/bin/env python3
"""
GitHub Issue Manager MCP Server
Manage GitHub issues through MCP.
"""

import asyncio
import os
from typing import Optional

import requests

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# ============================================================================
# Configuration
# ============================================================================

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Check for token on startup
if not GITHUB_TOKEN:
    print("WARNING: GITHUB_TOKEN not set. API calls will fail.")
    print("Set it with: export GITHUB_TOKEN='ghp_your_token'")


# ============================================================================
# GitHub API Client
# ============================================================================

class GitHubClient:
    """Simple GitHub API client."""
    
    def __init__(self, token: Optional[str]):
        """Initialize with authentication token."""
        self.token = token
        self.session = requests.Session()
        
        # Set up authentication headers
        if self.token:
            self.session.headers.update({
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make an authenticated API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., '/repos/owner/repo/issues')
            **kwargs: Additional arguments for requests
        
        Returns:
            Response data as dictionary
        
        Raises:
            Exception: If request fails
        """
        url = f"{GITHUB_API_BASE}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            
            # Return JSON if there's content
            return response.json() if response.content else {}
            
        except requests.HTTPError as e:
            # Provide user-friendly error messages
            if e.response.status_code == 401:
                raise Exception("Authentication failed. Check your GitHub token.")
            elif e.response.status_code == 403:
                raise Exception("Access forbidden. Check token permissions or rate limits.")
            elif e.response.status_code == 404:
                raise Exception(f"Not found: {endpoint}")
            else:
                raise Exception(f"GitHub API error: {e}")
        except requests.Timeout:
            raise Exception("Request timed out. Check your connection.")
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")


# Initialize GitHub client
github = GitHubClient(token=GITHUB_TOKEN)


# ============================================================================
# MCP Server Implementation
# ============================================================================

app = Server("github-issue-manager")
```

**Key Points:**

- We load `GITHUB_TOKEN` from environment (secure!)
- Simple `GitHubClient` handles authentication and requests
- Error handling converts API errors to user-friendly messages

## Step 3: Implement List Issues Tool

Add the tool registration and handler for listing issues:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register GitHub issue tools."""
    return [
        Tool(
            name="list_issues",
            description="List issues from a GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner (username or organization)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    },
                    "state": {
                        "type": "string",
                        "description": "Issue state: open, closed, or all",
                        "enum": ["open", "closed", "all"],
                        "default": "open"
                    }
                },
                "required": ["owner", "repo"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "list_issues":
            owner = arguments["owner"]
            repo = arguments["repo"]
            state = arguments.get("state", "open")
            
            # Make API request
            params = {"state": state, "per_page": 20}
            issues = github._make_request(
                "GET",
                f"/repos/{owner}/{repo}/issues",
                params=params
            )
            
            # Format response
            if not issues:
                return [TextContent(
                    type="text",
                    text=f"No {state} issues found in {owner}/{repo}"
                )]
            
            # Build formatted list
            lines = [f"Found {len(issues)} {state} issues in {owner}/{repo}:\n"]
            
            for issue in issues:
                # Skip pull requests (they appear in issues API)
                if "pull_request" in issue:
                    continue
                
                lines.append(f"#{issue['number']}: {issue['title']}")
                lines.append(f"  State: {issue['state']} | Comments: {issue['comments']}")
                lines.append(f"  URL: {issue['html_url']}")
                lines.append("")
            
            return [TextContent(type="text", text="\n".join(lines))]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

**What This Does:**

1. Accepts repository owner, name, and optional state
2. Calls GitHub API to list issues
3. Formats the response nicely
4. Handles errors gracefully

## Step 4: Test List Issues

Before adding more tools, let's test what we have:

```bash
# Set your token if not already set
export GITHUB_TOKEN="ghp_your_token"

# Test with MCP Inspector
mcp-inspector python github_issue_server.py
```

In the Inspector:

1. You should see the `list_issues` tool
2. Try calling it with:
   ```json
   {
     "owner": "microsoft",
     "repo": "vscode",
     "state": "open"
   }
   ```
3. You should get a list of VS Code issues!

**Troubleshooting:**

- "Authentication failed" → Check `GITHUB_TOKEN` is set correctly
- "Not found" → Verify owner/repo spelling
- "Rate limit" → Wait a bit, or use authenticated requests

## Step 5: Add Create Issue Tool

Now add the ability to create issues. Update your `list_tools()` function to include this new tool:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register GitHub issue tools."""
    return [
        Tool(
            name="list_issues",
            description="List issues from a GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner (username or organization)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    },
                    "state": {
                        "type": "string",
                        "description": "Issue state: open, closed, or all",
                        "enum": ["open", "closed", "all"],
                        "default": "open"
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        # NEW TOOL:
        Tool(
            name="create_issue",
            description="Create a new issue in a GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    },
                    "title": {
                        "type": "string",
                        "description": "Issue title"
                    },
                    "body": {
                        "type": "string",
                        "description": "Issue description/body (optional)"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Labels to add (optional)"
                    }
                },
                "required": ["owner", "repo", "title"]
            }
        )
    ]
```

Now add the handler in your `call_tool()` function:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "list_issues":
            # ... existing code ...
            pass  # (keep your existing implementation)
        
        # NEW HANDLER:
        elif name == "create_issue":
            # Check authentication
            if not GITHUB_TOKEN:
                return [TextContent(
                    type="text",
                    text="Error: GITHUB_TOKEN required to create issues. "
                         "Set it with: export GITHUB_TOKEN='ghp_your_token'"
                )]
            
            owner = arguments["owner"]
            repo = arguments["repo"]
            title = arguments["title"]
            body = arguments.get("body", "")
            labels = arguments.get("labels", [])
            
            # Prepare issue data
            issue_data = {
                "title": title,
                "body": body
            }
            if labels:
                issue_data["labels"] = labels
            
            # Create the issue
            issue = github._make_request(
                "POST",
                f"/repos/{owner}/{repo}/issues",
                json=issue_data
            )
            
            # Format success response
            response = f"""Issue created successfully!

#{issue['number']}: {issue['title']}
State: {issue['state']}
URL: {issue['html_url']}

Created by: {issue['user']['login']}
"""
            return [TextContent(type="text", text=response)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

## Step 6: Test Create Issue

**Important:** Only test this on repositories you own or have permission to modify!

Create a test repository on GitHub for practice, then:

```bash
mcp-inspector python github_issue_server.py
```

Try creating an issue:

```json
{
  "owner": "your-username",
  "repo": "test-repo",
  "title": "Test issue from MCP",
  "body": "This issue was created via the MCP server!",
  "labels": ["test", "mcp"]
}
```

Check your repository - the issue should appear!

## Step 7: Add Get Issue Details Tool

Add another tool to get detailed information about a specific issue:

```python
# Add to list_tools():
Tool(
    name="get_issue",
    description="Get detailed information about a specific issue",
    inputSchema={
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "Repository owner"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            },
            "issue_number": {
                "type": "integer",
                "description": "Issue number"
            }
        },
        "required": ["owner", "repo", "issue_number"]
    }
)

# Add to call_tool():
elif name == "get_issue":
    owner = arguments["owner"]
    repo = arguments["repo"]
    issue_number = arguments["issue_number"]
    
    # Get issue details
    issue = github._make_request(
        "GET",
        f"/repos/{owner}/{repo}/issues/{issue_number}"
    )
    
    # Format detailed response
    response = f"""Issue #{issue['number']}: {issue['title']}

Repository: {owner}/{repo}
State: {issue['state']}
Created: {issue['created_at']}
Updated: {issue['updated_at']}

Author: {issue['user']['login']}
Comments: {issue['comments']}

Labels: {', '.join(label['name'] for label in issue['labels']) or 'None'}

Description:
{issue['body'] or '(no description)'}

URL: {issue['html_url']}
"""
    return [TextContent(type="text", text=response)]
```

## Step 8: Add Search Issues Tool

Finally, add a tool to search issues by keywords:

```python
# Add to list_tools():
Tool(
    name="search_issues",
    description="Search for issues in a repository by keyword",
    inputSchema={
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "Repository owner"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            },
            "query": {
                "type": "string",
                "description": "Search query (keywords to search for)"
            },
            "state": {
                "type": "string",
                "description": "Issue state filter",
                "enum": ["open", "closed", "all"],
                "default": "open"
            }
        },
        "required": ["owner", "repo", "query"]
    }
)

# Add to call_tool():
elif name == "search_issues":
    owner = arguments["owner"]
    repo = arguments["repo"]
    query = arguments["query"]
    state = arguments.get("state", "open")
    
    # Build search query
    search_query = f"{query} repo:{owner}/{repo} type:issue state:{state}"
    
    # Search issues
    result = github._make_request(
        "GET",
        "/search/issues",
        params={"q": search_query, "per_page": 10}
    )
    
    items = result.get("items", [])
    
    if not items:
        return [TextContent(
            type="text",
            text=f"No issues found matching: {query}"
        )]
    
    # Format results
    lines = [f"Found {len(items)} issues matching '{query}':\n"]
    
    for issue in items:
        lines.append(f"#{issue['number']}: {issue['title']}")
        lines.append(f"  State: {issue['state']} | Comments: {issue['comments']}")
        lines.append(f"  URL: {issue['html_url']}")
        lines.append("")
    
    return [TextContent(type="text", text="\n".join(lines))]
```

## Step 9: Add Server Lifecycle

Complete your server with the main function:

```python
async def main():
    """Run the GitHub issue manager server."""
    print("=" * 70)
    print("GitHub Issue Manager MCP Server")
    print("=" * 70)
    print()
    
    if GITHUB_TOKEN:
        print("✓ GitHub token configured")
    else:
        print("⚠ WARNING: No GitHub token configured")
        print("  Set GITHUB_TOKEN environment variable to use this server")
        print("  export GITHUB_TOKEN='ghp_your_token'")
    
    print()
    print("Available tools:")
    print("  - list_issues: List issues in a repository")
    print("  - create_issue: Create a new issue")
    print("  - get_issue: Get detailed issue information")
    print("  - search_issues: Search for issues by keyword")
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
```

## Step 10: Test Your Complete Server

Test all tools with MCP Inspector:

```bash
export GITHUB_TOKEN="ghp_your_token"
mcp-inspector python github_issue_server.py
```

Try each tool:

1. **List Issues**: `{"owner": "microsoft", "repo": "vscode", "state": "open"}`
2. **Search Issues**: `{"owner": "microsoft", "repo": "vscode", "query": "bug", "state": "open"}`
3. **Get Issue**: `{"owner": "microsoft", "repo": "vscode", "issue_number": 1}`
4. **Create Issue**: Only on your own test repo!

## Step 11: Deploy to Cursor IDE

Now integrate your server with Cursor IDE!

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github-issues": {
      "command": "python",
      "args": ["/full/path/to/github_issue_server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Security Note:** The token will be in your config file. Make sure this file has proper permissions:

```bash
# macOS/Linux - Restrict access
chmod 600 ~/Library/Application\ Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

Restart Cursor IDE and try:

- "Can you list the open issues in microsoft/vscode?"
- "Search for bugs in the vscode repository"
- "Show me details about issue #12345 in owner/repo"

## Enhancements & Extensions

### Rate Limiting

Add rate limit tracking:

```python
class GitHubClient:
    def __init__(self, token):
        # ... existing code ...
        self.requests_made = 0
        self.requests_remaining = 5000
    
    def _make_request(self, method, endpoint, **kwargs):
        # ... existing code ...
        
        # Track rate limits from response headers
        if 'X-RateLimit-Remaining' in response.headers:
            self.requests_remaining = int(response.headers['X-RateLimit-Remaining'])
            
            if self.requests_remaining < 100:
                print(f"WARNING: Only {self.requests_remaining} API requests remaining")
        
        return response.json() if response.content else {}
```

### Caching

Add simple caching to reduce API calls:

```python
from datetime import datetime, timedelta

class GitHubClient:
    def __init__(self, token):
        # ... existing code ...
        self.cache = {}
        self.cache_ttl = timedelta(minutes=5)
    
    def _make_request(self, method, endpoint, **kwargs):
        # Check cache for GET requests
        if method == "GET":
            cache_key = f"{endpoint}:{kwargs.get('params', {})}"
            
            if cache_key in self.cache:
                data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_ttl:
                    return data
        
        # Make request...
        data = # ... existing request code ...
        
        # Cache successful GET requests
        if method == "GET":
            self.cache[cache_key] = (data, datetime.now())
        
        return data
```

### Add More Tools

Extend with additional GitHub operations:

- **Update Issue**: Modify title, description, labels
- **Close Issue**: Close an issue with a comment
- **Add Comment**: Comment on existing issues
- **List Labels**: Get available labels for a repo
- **Get Repo Info**: Repository statistics and metadata

### Error Recovery

Add retry logic for transient failures:

```python
import time

def _make_request_with_retry(self, method, endpoint, max_retries=3, **kwargs):
    """Make request with automatic retry on failure."""
    for attempt in range(max_retries):
        try:
            return self._make_request(method, endpoint, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

## Best Practices You've Learned

1. **Secure Credentials**: Use environment variables, never hardcode
2. **Error Handling**: Convert API errors to user-friendly messages
3. **Rate Limiting**: Track and respect API limits
4. **Input Validation**: Use JSON schemas to validate parameters
5. **Helpful Descriptions**: Write clear tool descriptions for AI
6. **User Feedback**: Provide informative success/error messages
7. **Testing**: Use Inspector before deploying to Claude

## Common Issues & Solutions

### Issue: "Authentication Failed"

**Cause:** Token not set or invalid.

**Solution:**
```bash
# Verify token is set
echo $GITHUB_TOKEN

# Check token hasn't expired
# Go to: https://github.com/settings/tokens

# Regenerate if needed
```

### Issue: "Rate Limit Exceeded"

**Cause:** Too many API requests.

**Solution:**
- Wait for rate limit to reset (1 hour)
- Implement caching
- Use conditional requests (ETags)

### Issue: "Not Found"

**Cause:** Repository doesn't exist or token lacks access.

**Solution:**
- Verify owner/repo spelling
- Check repository is public or token has access
- Ensure token has correct scopes

## Verification Checklist

- [ ] Server runs without errors
- [ ] All four tools are registered
- [ ] `list_issues` works with public repos
- [ ] `create_issue` works on test repo (with auth)
- [ ] `get_issue` retrieves issue details
- [ ] `search_issues` finds relevant issues
- [ ] Errors are handled gracefully
- [ ] Server integrates with Cursor IDE
- [ ] Token is stored securely (not in code)

## What You've Learned

Congratulations! You've built a production-ready API integration. You now understand:

1. **API Integration**: Connecting MCP to external REST APIs
2. **Authentication**: Secure token management and headers
3. **Error Handling**: Converting API errors to user-friendly messages
4. **Rate Limiting**: Respecting API constraints
5. **Real-World Deployment**: Using your server with Cursor IDE
6. **Best Practices**: Security, testing, and user experience

## Next Steps

1. **Add more GitHub tools** (pull requests, branches, commits)
2. **Try Challenge 2** - Integrate a different API (weather, news, etc.)
3. **Explore the full GitHub server** in examples/
4. **Build your own integration** with an API you use

## Additional Resources

- **GitHub API Docs**: https://docs.github.com/rest
- **GitHub API Explorer**: https://docs.github.com/rest/overview/explorer
- **Rate Limiting**: https://docs.github.com/rest/overview/rate-limits
- **MCP Examples**: Check `05-integration-patterns/examples/github_server.py`

## Summary

You've created a practical MCP server that bridges AI assistants with GitHub's powerful API. This pattern applies to any REST API - weather services, databases, internal tools, and more. The key skills (authentication, error handling, rate limiting) are universal for API integrations.

Now Claude can manage your GitHub issues through natural conversation. That's the power of MCP!

