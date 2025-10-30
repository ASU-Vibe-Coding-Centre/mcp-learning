#!/usr/bin/env python3
"""
GitHub Integration MCP Server

Integrates with GitHub API to provide repository operations, issue management,
and file access. Demonstrates real-world API integration with authentication,
rate limiting, error handling, and caching.

Features:
- Repository operations (list, get info, search)
- Issue management (list, create, update)
- File access (read files, get README)
- Pull request operations
- Authentication with personal access tokens
- Rate limiting and quota management
- Response caching for performance

Usage:
    # Set GitHub token
    export GITHUB_TOKEN="ghp_your_token_here"
    
    # Run server
    python github_server.py

Test with MCP Inspector:
    mcp-inspector python github_server.py

Configure for Claude Desktop:
    Add to claude_desktop_config.json:
    {
      "mcpServers": {
        "github": {
          "command": "python",
          "args": ["/path/to/github_server.py"],
          "env": {
            "GITHUB_TOKEN": "ghp_your_token_here"
          }
        }
      }
    }
"""

import asyncio
import json
import os
import time
from collections import deque
from typing import Any, Optional

import requests

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool


# ============================================================================
# Configuration
# ============================================================================

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Rate limiting configuration (GitHub allows 5000 requests/hour with auth)
MAX_REQUESTS_PER_HOUR = 5000 if GITHUB_TOKEN else 60
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds

# Cache configuration
CACHE_TTL = 300  # 5 minutes


# ============================================================================
# Rate Limiter Implementation
# ============================================================================

class RateLimiter:
    """
    Token bucket rate limiter for API requests.
    
    Tracks requests over a time window and enforces limits.
    """
    
    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def is_allowed(self) -> bool:
        """Check if a request is allowed under rate limits."""
        now = time.time()
        
        # Remove requests outside the time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # Check if we're under the limit
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        """Record that a request was made."""
        self.requests.append(time.time())
    
    def wait_time(self) -> float:
        """Calculate seconds to wait before next request is allowed."""
        if not self.requests:
            return 0.0
        
        oldest_request = self.requests[0]
        time_until_reset = (oldest_request + self.time_window) - time.time()
        return max(0.0, time_until_reset)
    
    def get_stats(self) -> dict:
        """Get current rate limit statistics."""
        now = time.time()
        
        # Count recent requests
        recent = sum(1 for t in self.requests if t > now - self.time_window)
        
        return {
            "requests_made": recent,
            "requests_available": self.max_requests - recent,
            "limit": self.max_requests,
            "window_seconds": self.time_window,
            "reset_in_seconds": self.wait_time() if recent >= self.max_requests else 0
        }


# ============================================================================
# Cache Implementation
# ============================================================================

class APICache:
    """
    Simple in-memory cache for API responses.
    
    Caches responses with time-to-live (TTL) to reduce API calls.
    """
    
    def __init__(self, ttl: int = 300):
        """
        Initialize cache.
        
        Args:
            ttl: Time-to-live in seconds (default: 5 minutes)
        """
        self.ttl = ttl
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value if not expired.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return value
            else:
                # Remove expired entry
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any):
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = (value, time.time())
    
    def clear(self, pattern: Optional[str] = None):
        """
        Clear cache entries.
        
        Args:
            pattern: If provided, only clear keys containing this pattern
        """
        if pattern is None:
            self.cache.clear()
        else:
            keys_to_delete = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.cache[key]
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2),
            "ttl_seconds": self.ttl
        }


# ============================================================================
# GitHub API Client
# ============================================================================

class GitHubClient:
    """
    GitHub API client with authentication, rate limiting, and caching.
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.rate_limiter = RateLimiter(MAX_REQUESTS_PER_HOUR, RATE_LIMIT_WINDOW)
        self.cache = APICache(ttl=CACHE_TTL)
        self.session = requests.Session()
        
        # Set up authentication headers
        if self.token:
            self.session.headers.update({
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            })
        else:
            print("WARNING: No GitHub token provided. API rate limits will be strict (60/hour).")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make authenticated API request with rate limiting and caching.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., '/repos/owner/repo')
            **kwargs: Additional arguments for requests
        
        Returns:
            API response as dictionary
        
        Raises:
            Exception: If rate limited or API error occurs
        """
        # Check cache for GET requests
        if method.upper() == "GET":
            cache_key = f"{endpoint}:{json.dumps(kwargs.get('params', {}))}"
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        # Check rate limit
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.wait_time()
            raise Exception(
                f"GitHub API rate limit exceeded. "
                f"Please wait {wait_time:.0f} seconds before retrying."
            )
        
        # Make request
        url = f"{GITHUB_API_BASE}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            self.rate_limiter.record_request()
            
            # Handle rate limit headers
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                if remaining < 10:
                    print(f"WARNING: Only {remaining} API requests remaining")
            
            response.raise_for_status()
            data = response.json() if response.content else {}
            
            # Cache successful GET requests
            if method.upper() == "GET":
                self.cache.set(cache_key, data)
            
            return data
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif e.response.status_code == 401:
                raise Exception("Authentication failed. Please check your GitHub token.")
            elif e.response.status_code == 403:
                raise Exception("Access forbidden. Check token permissions or rate limits.")
            else:
                raise Exception(f"GitHub API error: {e}")
        except requests.Timeout:
            raise Exception("GitHub API request timed out. Please try again.")
        except requests.RequestException as e:
            raise Exception(f"Network error: {e}")
    
    def get_repo(self, owner: str, repo: str) -> dict:
        """Get repository information."""
        return self._make_request("GET", f"/repos/{owner}/{repo}")
    
    def list_repos(self, username: str) -> list:
        """List user's repositories."""
        return self._make_request("GET", f"/users/{username}/repos")
    
    def search_repos(self, query: str, sort: str = "stars", max_results: int = 10) -> list:
        """Search repositories."""
        params = {
            "q": query,
            "sort": sort,
            "per_page": min(max_results, 100)
        }
        result = self._make_request("GET", "/search/repositories", params=params)
        return result.get("items", [])
    
    def get_readme(self, owner: str, repo: str) -> str:
        """Get repository README content."""
        try:
            data = self._make_request("GET", f"/repos/{owner}/{repo}/readme")
            # README content is base64 encoded
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        except Exception as e:
            raise Exception(f"Failed to fetch README: {e}")
    
    def list_issues(self, owner: str, repo: str, state: str = "open") -> list:
        """List repository issues."""
        params = {"state": state, "per_page": 30}
        return self._make_request("GET", f"/repos/{owner}/{repo}/issues", params=params)
    
    def create_issue(self, owner: str, repo: str, title: str, body: str = "", labels: list = None) -> dict:
        """Create a new issue."""
        data = {
            "title": title,
            "body": body
        }
        if labels:
            data["labels"] = labels
        
        return self._make_request("POST", f"/repos/{owner}/{repo}/issues", json=data)
    
    def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """Get file content from repository."""
        try:
            data = self._make_request("GET", f"/repos/{owner}/{repo}/contents/{path}")
            
            if data.get("type") != "file":
                raise Exception(f"'{path}' is not a file")
            
            # File content is base64 encoded
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        except Exception as e:
            raise Exception(f"Failed to fetch file: {e}")


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create server and GitHub client
app = Server("github-integration-server")
github = GitHubClient(token=GITHUB_TOKEN)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available GitHub operations."""
    return [
        Tool(
            name="github_get_repo",
            description="Get information about a GitHub repository",
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
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        Tool(
            name="github_search_repos",
            description="Search for repositories on GitHub",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'machine learning python')"
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort by: stars, forks, or updated",
                        "enum": ["stars", "forks", "updated"],
                        "default": "stars"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return (1-100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="github_get_readme",
            description="Get the README content from a repository",
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
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        Tool(
            name="github_list_issues",
            description="List issues for a repository",
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
        Tool(
            name="github_create_issue",
            description="Create a new issue in a repository (requires authentication)",
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
                        "description": "Issue body/description"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Issue labels"
                    }
                },
                "required": ["owner", "repo", "title"]
            }
        ),
        Tool(
            name="github_get_file",
            description="Get content of a file from a repository",
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
                    "path": {
                        "type": "string",
                        "description": "File path in repository"
                    }
                },
                "required": ["owner", "repo", "path"]
            }
        ),
        Tool(
            name="github_get_rate_limit",
            description="Get current GitHub API rate limit status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute GitHub operations."""
    
    try:
        # Tool 1: Get Repository
        if name == "github_get_repo":
            owner = arguments["owner"]
            repo = arguments["repo"]
            
            data = github.get_repo(owner, repo)
            
            result = f"""Repository: {data['full_name']}

Description: {data.get('description', 'No description')}
Stars: {data['stargazers_count']}
Forks: {data['forks_count']}
Open Issues: {data['open_issues_count']}
Language: {data.get('language', 'N/A')}
License: {data.get('license', {}).get('name', 'None')}

Homepage: {data.get('homepage', 'N/A')}
URL: {data['html_url']}

Created: {data['created_at']}
Last Updated: {data['updated_at']}
"""
            return [TextContent(type="text", text=result)]
        
        # Tool 2: Search Repositories
        elif name == "github_search_repos":
            query = arguments["query"]
            sort = arguments.get("sort", "stars")
            max_results = arguments.get("max_results", 10)
            
            repos = github.search_repos(query, sort, max_results)
            
            if not repos:
                return [TextContent(type="text", text=f"No repositories found for: {query}")]
            
            results = [f"Found {len(repos)} repositories:\n"]
            for i, repo in enumerate(repos, 1):
                results.append(f"{i}. {repo['full_name']}")
                results.append(f"   ⭐ {repo['stargazers_count']} stars | "
                             f"🔱 {repo['forks_count']} forks")
                if repo.get('description'):
                    results.append(f"   {repo['description']}")
                results.append(f"   {repo['html_url']}\n")
            
            return [TextContent(type="text", text="\n".join(results))]
        
        # Tool 3: Get README
        elif name == "github_get_readme":
            owner = arguments["owner"]
            repo = arguments["repo"]
            
            content = github.get_readme(owner, repo)
            
            return [TextContent(
                type="text",
                text=f"README for {owner}/{repo}:\n\n{content}"
            )]
        
        # Tool 4: List Issues
        elif name == "github_list_issues":
            owner = arguments["owner"]
            repo = arguments["repo"]
            state = arguments.get("state", "open")
            
            issues = github.list_issues(owner, repo, state)
            
            if not issues:
                return [TextContent(
                    type="text",
                    text=f"No {state} issues found for {owner}/{repo}"
                )]
            
            results = [f"{len(issues)} {state} issues for {owner}/{repo}:\n"]
            for issue in issues[:20]:  # Limit to 20
                # Skip pull requests (they appear in issues API)
                if 'pull_request' in issue:
                    continue
                
                results.append(f"#{issue['number']}: {issue['title']}")
                results.append(f"  State: {issue['state']} | "
                             f"Comments: {issue['comments']}")
                if issue.get('labels'):
                    labels = ', '.join(l['name'] for l in issue['labels'])
                    results.append(f"  Labels: {labels}")
                results.append(f"  {issue['html_url']}\n")
            
            return [TextContent(type="text", text="\n".join(results))]
        
        # Tool 5: Create Issue
        elif name == "github_create_issue":
            if not GITHUB_TOKEN:
                return [TextContent(
                    type="text",
                    text="Error: GitHub token required to create issues. "
                         "Set GITHUB_TOKEN environment variable."
                )]
            
            owner = arguments["owner"]
            repo = arguments["repo"]
            title = arguments["title"]
            body = arguments.get("body", "")
            labels = arguments.get("labels", [])
            
            issue = github.create_issue(owner, repo, title, body, labels)
            
            return [TextContent(
                type="text",
                text=f"""Issue created successfully!

#{issue['number']}: {issue['title']}
State: {issue['state']}
URL: {issue['html_url']}
"""
            )]
        
        # Tool 6: Get File
        elif name == "github_get_file":
            owner = arguments["owner"]
            repo = arguments["repo"]
            path = arguments["path"]
            
            content = github.get_file_content(owner, repo, path)
            
            return [TextContent(
                type="text",
                text=f"Content of {path} in {owner}/{repo}:\n\n{content}"
            )]
        
        # Tool 7: Get Rate Limit
        elif name == "github_get_rate_limit":
            rate_stats = github.rate_limiter.get_stats()
            cache_stats = github.cache.get_stats()
            
            result = f"""GitHub API Status:

Rate Limiting:
- Requests made: {rate_stats['requests_made']} / {rate_stats['limit']}
- Requests available: {rate_stats['requests_available']}
- Window: {rate_stats['window_seconds']} seconds
- Reset in: {rate_stats['reset_in_seconds']:.0f} seconds

Cache:
- Cached entries: {cache_stats['entries']}
- Cache hits: {cache_stats['hits']}
- Cache misses: {cache_stats['misses']}
- Hit rate: {cache_stats['hit_rate_percent']}%
- TTL: {cache_stats['ttl_seconds']} seconds

Authentication: {'✓ Token configured' if GITHUB_TOKEN else '✗ No token (limited to 60 req/hour)'}
"""
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        # Return user-friendly error message
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


# ============================================================================
# Server Lifecycle
# ============================================================================

async def main():
    """Run the GitHub integration server."""
    print("=" * 70)
    print("GitHub Integration MCP Server")
    print("=" * 70)
    print()
    
    if GITHUB_TOKEN:
        print("✓ GitHub token configured")
        print(f"✓ Rate limit: {MAX_REQUESTS_PER_HOUR} requests/hour")
    else:
        print("⚠ No GitHub token configured")
        print("⚠ Rate limit: 60 requests/hour (unauthenticated)")
        print()
        print("To increase rate limits, set GITHUB_TOKEN environment variable:")
        print("  export GITHUB_TOKEN='ghp_your_token_here'")
    
    print()
    print("Available operations:")
    print("  - Get repository information")
    print("  - Search repositories")
    print("  - Read README files")
    print("  - List and create issues")
    print("  - Get file contents")
    print("  - Check rate limit status")
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

