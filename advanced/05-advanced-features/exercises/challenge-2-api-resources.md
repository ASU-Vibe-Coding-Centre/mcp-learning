# Challenge 2: Wrap External API as MCP Resources

## Overview

Build an MCP server that wraps an external API and exposes its data as resources. This challenge demonstrates how to integrate third-party services into the MCP ecosystem, making external data accessible to AI models.

**Estimated Time:** 90 minutes

**Difficulty:** Advanced

**Prerequisites:**
- Completed Tutorial 2 (Resources)
- Understanding of REST APIs
- Familiarity with HTTP requests (requests library)
- Experience with JSON data

## Challenge Description

Create an MCP server that:

1. **Wraps a public API** (GitHub, JSONPlaceholder, or similar)
2. **Exposes API endpoints as resources**
3. **Implements resource templates** for dynamic access
4. **Caches API responses** to reduce requests
5. **Handles rate limiting** gracefully
6. **Provides tools** for API discovery and search

## API Choice

Choose ONE of these public APIs (no authentication required):

### Option 1: JSONPlaceholder (Easiest)

**Base URL:** `https://jsonplaceholder.typicode.com`

**Endpoints:**
- `/posts` - Blog posts
- `/comments` - Comments on posts
- `/users` - User information
- `/albums` - Photo albums
- `/photos` - Photos
- `/todos` - Todo items

**Advantages:** Simple, reliable, no rate limits, perfect for learning

### Option 2: GitHub API (Medium)

**Base URL:** `https://api.github.com`

**Endpoints:**
- `/repos/{owner}/{repo}` - Repository information
- `/repos/{owner}/{repo}/readme` - README content
- `/repos/{owner}/{repo}/contents/{path}` - File contents
- `/users/{username}` - User profile
- `/search/repositories` - Search repositories

**Note:** Unauthenticated limit is 60 requests/hour

### Option 3: OpenLibrary (Medium)

**Base URL:** `https://openlibrary.org/api`

**Endpoints:**
- `/books?bibkeys=ISBN:{isbn}` - Book information
- `/search.json?q={query}` - Search books
- `/authors/{author_id}.json` - Author information

## Requirements

### Required Resources

Implement resources for at least 5 API endpoints:

**Resource Requirements:**
- URIs follow consistent pattern (e.g., `api://posts/1`)
- Descriptive names and descriptions
- Correct MIME types (application/json for JSON data)
- Metadata about API source

**Example Resource:**
```python
Resource(
    uri="api://posts/1",
    name="Post #1",
    description="Blog post from JSONPlaceholder API",
    mimeType="application/json"
)
```

### Required Resource Templates

Create templates for dynamic access:

```python
ResourceTemplate(
    uriTemplate="api://posts/{id}",
    name="Posts by ID",
    description="Access any post by its ID",
    mimeType="application/json"
)

ResourceTemplate(
    uriTemplate="api://users/{userId}/posts",
    name="User's Posts",
    description="Access all posts by a specific user",
    mimeType="application/json"
)
```

### Required Tools

Implement these tools:

1. **search_api**
   - Search API resources by keyword
   - Return matching resource URIs
   - Include relevance information

2. **list_endpoints**
   - List all available API endpoints
   - Show endpoint patterns
   - Display rate limit status

3. **refresh_cache**
   - Clear cached API responses
   - Allow selective cache clearing
   - Report cache statistics

4. **get_api_stats**
   - Show request count
   - Display cache hit rate
   - Report rate limit status
   - Show response times

### Caching Requirements

Implement an in-memory cache:

- Cache API responses for 5 minutes
- Include cache timestamp
- Provide cache invalidation
- Report cache hits/misses

### Rate Limiting Requirements

Handle rate limits properly:

- Track request count
- Respect API rate limits
- Provide clear error messages when limited
- Suggest wait time before retry

## Starter Code

```python
#!/usr/bin/env python3
"""
Challenge 2: API Resource Server

Wraps external API as MCP resources.
"""

import asyncio
import time
from typing import Any, Optional
from datetime import datetime, timedelta

import requests

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceTemplate, TextContent, Tool

# API Configuration
API_BASE_URL = "https://jsonplaceholder.typicode.com"  # Change based on your choice

# Create server
app = Server("api-resource-server")

# Cache implementation
class APICache:
    """Simple in-memory cache for API responses."""
    
    def __init__(self, ttl_seconds=300):  # 5 minute default TTL
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[dict]:
        """Get cached value if not expired."""
        # TODO: Implement cache retrieval with expiration check
        pass
    
    def set(self, key: str, value: dict):
        """Store value in cache with timestamp."""
        # TODO: Implement cache storage
        pass
    
    def clear(self, pattern: Optional[str] = None):
        """Clear cache entries matching pattern."""
        # TODO: Implement cache clearing
        pass
    
    def stats(self) -> dict:
        """Get cache statistics."""
        # TODO: Return cache stats
        pass

# Rate limiter implementation
class RateLimiter:
    """Track API request rate."""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def can_make_request(self) -> bool:
        """Check if request is allowed."""
        # TODO: Implement rate limit check
        pass
    
    def record_request(self):
        """Record a request."""
        # TODO: Add request to history
        pass
    
    def wait_time(self) -> float:
        """Time to wait before next request allowed."""
        # TODO: Calculate wait time
        pass

# Global instances
cache = APICache()
rate_limiter = RateLimiter(max_requests=60, time_window=3600)  # Adjust based on API

# TODO: Implement API fetching
def fetch_from_api(endpoint: str) -> dict:
    """
    Fetch data from API with caching and rate limiting.
    
    Args:
        endpoint: API endpoint path
    
    Returns:
        JSON response as dictionary
    """
    pass

# TODO: Implement resource listing
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available API resources."""
    pass

# TODO: Implement resource templates
@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List resource templates for dynamic access."""
    pass

# TODO: Implement resource reading
@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read API resource content."""
    pass

# TODO: Implement tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    pass

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tools."""
    pass

async def main():
    """Run the server."""
    print(f"Starting API Resource Server")
    print(f"API Base URL: {API_BASE_URL}")
    print("Ready to accept connections")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Implementation Steps

### Step 1: Implement Cache

Create a working cache system:

```python
class APICache:
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[dict]:
        if key in self.cache:
            entry = self.cache[key]
            # Check if expired
            if time.time() - entry['timestamp'] < self.ttl:
                self.hits += 1
                return entry['data']
            else:
                # Expired, remove it
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: dict):
        self.cache[key] = {
            'data': value,
            'timestamp': time.time()
        }
```

### Step 2: Implement Rate Limiter

Track and enforce rate limits:

```python
class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def can_make_request(self) -> bool:
        # Remove old requests outside time window
        cutoff = time.time() - self.time_window
        self.requests = [r for r in self.requests if r > cutoff]
        
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        self.requests.append(time.time())
```

### Step 3: Implement API Fetching

Fetch with cache and rate limiting:

```python
def fetch_from_api(endpoint: str) -> dict:
    # Check cache first
    cached = cache.get(endpoint)
    if cached is not None:
        return cached
    
    # Check rate limit
    if not rate_limiter.can_make_request():
        wait_time = rate_limiter.wait_time()
        raise Exception(f"Rate limit exceeded. Wait {wait_time:.0f} seconds")
    
    # Make API request
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    # Cache and record
    cache.set(endpoint, data)
    rate_limiter.record_request()
    
    return data
```

### Step 4: Implement URI Parsing

Convert between URIs and API endpoints:

```python
def uri_to_endpoint(uri: str) -> str:
    """Convert resource URI to API endpoint."""
    if not uri.startswith("api://"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    # Remove 'api://' prefix
    endpoint = uri[6:]
    return endpoint

def endpoint_to_uri(endpoint: str) -> str:
    """Convert API endpoint to resource URI."""
    return f"api://{endpoint}"
```

### Step 5: List Resources

Discover and list API resources:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    resources = []
    
    # For JSONPlaceholder example
    # List some posts
    posts_data = fetch_from_api("posts")
    for post in posts_data[:10]:  # First 10
        resources.append(Resource(
            uri=f"api://posts/{post['id']}",
            name=f"Post: {post['title'][:50]}",
            description=f"Blog post #{post['id']}",
            mimeType="application/json"
        ))
    
    # List some users
    users_data = fetch_from_api("users")
    for user in users_data:
        resources.append(Resource(
            uri=f"api://users/{user['id']}",
            name=f"User: {user['name']}",
            description=f"User profile for {user['username']}",
            mimeType="application/json"
        ))
    
    return resources
```

### Step 6: Implement Resource Reading

Read resource content:

```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    endpoint = uri_to_endpoint(uri)
    
    try:
        data = fetch_from_api(endpoint)
        # Return as formatted JSON
        import json
        return json.dumps(data, indent=2)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Resource not found: {uri}")
        else:
            raise ValueError(f"API error: {e}")
    except Exception as e:
        raise ValueError(f"Error fetching resource: {e}")
```

## Testing Scenarios

### Test 1: Basic Resource Reading

```
1. List resources
2. Pick a resource URI
3. Read the resource
4. Verify JSON is returned
```

### Test 2: Cache Effectiveness

```
1. Read a resource (cache miss)
2. Read same resource again (cache hit)
3. Check cache stats - should show 1 hit
4. Wait 6 minutes
5. Read again (cache expired, new fetch)
```

### Test 3: Rate Limiting

```
1. Make many requests rapidly
2. Verify rate limiter triggers
3. Check wait time is calculated
4. Verify clear error message
```

### Test 4: Resource Templates

```
1. List resource templates
2. Construct URI from template
3. Read resource with constructed URI
4. Verify it works correctly
```

### Test 5: Error Handling

```
1. Request non-existent resource
2. Verify 404 is handled gracefully
3. Request malformed URI
4. Verify clear error message
```

## Success Criteria

Your implementation should:

- [ ] Fetch data from chosen API successfully
- [ ] Expose at least 5 types of resources
- [ ] Implement at least 3 resource templates
- [ ] Cache API responses
- [ ] Respect rate limits
- [ ] Provide all required tools
- [ ] Handle errors gracefully
- [ ] Format JSON readably
- [ ] Include comprehensive comments
- [ ] Work with MCP Inspector

## Extension Challenges

### Extension 1: Authentication Support

Add API key/token support:

```python
headers = {
    "Authorization": f"Bearer {api_token}"
}
response = requests.get(url, headers=headers)
```

### Extension 2: Pagination Support

Handle paginated API responses:

```python
def fetch_all_pages(endpoint: str) -> list:
    all_data = []
    page = 1
    
    while True:
        data = fetch_from_api(f"{endpoint}?page={page}")
        if not data:
            break
        all_data.extend(data)
        page += 1
    
    return all_data
```

### Extension 3: Webhooks

Cache invalidation via webhooks:

```python
@app.post("/webhook")
def handle_webhook(request):
    # Clear relevant cache entries
    cache.clear(pattern=request.json['resource'])
```

### Extension 4: Response Transformation

Transform API responses for better readability:

```python
def transform_response(data: dict, resource_type: str) -> dict:
    """Simplify or enhance API response."""
    if resource_type == "user":
        return {
            "name": data["name"],
            "email": data["email"],
            # ... simplified structure
        }
    return data
```

## Evaluation Rubric

### Functionality (35%)
- All required resources work
- Resource templates function correctly
- Tools provide useful functionality
- API integration is complete

### Caching & Performance (25%)
- Cache implementation is correct
- Cache TTL works properly
- Cache improves performance
- Cache stats are accurate

### Rate Limiting (20%)
- Rate limiter works correctly
- Clear error messages
- Proper wait time calculation
- Respects API limits

### Code Quality (20%)
- Well-structured code
- Comprehensive error handling
- Good comments
- Type hints used

## Common Pitfalls

### Pitfall 1: No Error Handling

**Problem:** Network errors crash the server

**Solution:**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    raise ValueError("API request timed out")
except requests.HTTPError as e:
    raise ValueError(f"API error: {e}")
```

### Pitfall 2: Cache Never Expires

**Problem:** Stale data served forever

**Solution:** Always check timestamp on cache retrieval

### Pitfall 3: JSON Serialization Errors

**Problem:** Some API responses aren't JSON-serializable

**Solution:**
```python
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

### Pitfall 4: Ignoring Rate Limits

**Problem:** API blocks your requests

**Solution:** Track requests and enforce limits before making calls

## Debugging Tips

### Tip 1: Log API Calls

```python
print(f"Fetching: {url}")
print(f"Cache: {'HIT' if cached else 'MISS'}")
print(f"Rate limit: {len(rate_limiter.requests)}/{rate_limiter.max_requests}")
```

### Tip 2: Test API Separately

```python
# Test API directly first
import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.json())
```

### Tip 3: Verify Resource URIs

```python
# Print URIs as you create them
print(f"Created resource: {uri}")
```

### Tip 4: Monitor Cache Size

```python
print(f"Cache entries: {len(cache.cache)}")
print(f"Cache hit rate: {cache.hits / (cache.hits + cache.misses) * 100:.1f}%")
```

## Solution Reference

A complete solution is available in `solutions/challenge-2-solution.py`.

Try to complete the challenge independently first. The solution demonstrates one approach, but many implementations are valid.

## Key Learnings

This challenge teaches:

- Integrating external APIs with MCP
- Caching strategies for performance
- Rate limiting implementation
- Resource template design
- Error handling for network operations
- URI scheme design
- API response transformation

## Next Steps

After completing this challenge:

1. Review all Module 04 examples
2. Complete the module checkpoint
3. Consider combining API resources with tools and prompts
4. Think about production considerations (authentication, monitoring)

Excellent work on this advanced challenge!

