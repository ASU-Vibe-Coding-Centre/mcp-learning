# Challenge 2: Integrate with External API of Your Choice

Welcome to the ultimate integration challenge! You'll design and build a production-ready MCP server that integrates with a real external API, handling authentication, rate limiting, error recovery, and all the complexities of real-world API integration.

## Challenge Overview

Unlike the tutorials, this challenge gives you creative freedom. Choose an API you're interested in, design the integration, and build a server that brings that API's capabilities to AI assistants through MCP.

This is as close to real-world development as you can get - you'll face the same challenges professional developers encounter when building API integrations.

## Difficulty

Advanced

## Time Estimate

2-3 hours (depending on API complexity and features implemented)

## Learning Objectives

By completing this challenge, you will:

1. Design a comprehensive API integration from scratch
2. Handle authentication and API keys securely
3. Implement robust error handling and retry logic
4. Manage rate limiting and request throttling
5. Cache responses effectively
6. Transform API data into MCP-friendly formats
7. Create intuitive tools for complex API operations
8. Write production-quality integration code
9. Document your integration thoroughly

## Your Mission

**Build a complete MCP server** that integrates with an external API of your choice, implementing tools that make the API's capabilities accessible through natural language interactions with AI.

## Phase 1: API Selection

Choose an API that interests you. Here are suggestions organized by difficulty:

### Beginner-Friendly APIs (Good Starting Point)

**1. OpenWeatherMap**
- **URL**: https://openweathermap.org/api
- **Auth**: API key (free tier available)
- **Rate Limit**: 60 calls/minute (free)
- **Use Cases**: Current weather, forecasts, historical data
- **Why Good**: Simple, well-documented, predictable responses

**2. REST Countries**
- **URL**: https://restcountries.com
- **Auth**: None required
- **Rate Limit**: No strict limits
- **Use Cases**: Country data, currencies, languages
- **Why Good**: No auth needed, stable, educational

**3. JSONPlaceholder**
- **URL**: https://jsonplaceholder.typicode.com
- **Auth**: None required
- **Rate Limit**: No limits
- **Use Cases**: Mock blog data (posts, comments, users)
- **Why Good**: Perfect for learning, no complexity

### Intermediate APIs (More Realistic)

**4. GitHub API**
- **URL**: https://api.github.com
- **Auth**: Personal access token (optional for some endpoints)
- **Rate Limit**: 5000/hour (authenticated), 60/hour (unauthenticated)
- **Use Cases**: Repos, issues, PRs, code search
- **Why Good**: Feature-rich, well-documented, relevant to developers

**5. News API**
- **URL**: https://newsapi.org
- **Auth**: API key (free tier)
- **Rate Limit**: 100 requests/day (free)
- **Use Cases**: News articles, sources, headlines
- **Why Good**: Real-world data, interesting use cases

**6. TMDB (The Movie Database)**
- **URL**: https://www.themoviedb.org/documentation/api
- **Auth**: API key (free)
- **Rate Limit**: 40 requests/10 seconds
- **Use Cases**: Movies, TV shows, actors
- **Why Good**: Rich data, fun to work with

**7. Stripe API (Test Mode)**
- **URL**: https://stripe.com/docs/api
- **Auth**: API key (test mode)
- **Rate Limit**: Generous
- **Use Cases**: Payment data, customers (test mode only)
- **Why Good**: Real payment API, professional quality

### Advanced APIs (Complex Integration)

**8. Slack API**
- **URL**: https://api.slack.com
- **Auth**: OAuth 2.0
- **Rate Limit**: Tier-based
- **Use Cases**: Messages, channels, users, files
- **Why Good**: Complex auth, webhooks, real-time features

**9. Google Calendar API**
- **URL**: https://developers.google.com/calendar/api
- **Auth**: OAuth 2.0
- **Rate Limit**: 1,000,000 queries/day
- **Use Cases**: Events, calendars, scheduling
- **Why Good**: Complex auth flow, useful functionality

**10. Twilio API**
- **URL**: https://www.twilio.com/docs/usage/api
- **Auth**: Account SID + Auth Token
- **Rate Limit**: Varies by endpoint
- **Use Cases**: SMS, calls, verification
- **Why Good**: Real infrastructure API, professional patterns

### Custom API

**Have your own API?** Use one from your workplace or personal projects!

**Requirements**:
- Must be accessible via HTTP/HTTPS
- Must have some form of documentation
- Should have at least 3-4 meaningful endpoints
- Bonus points for production APIs you actually use

## Phase 2: Design Your Integration

Before coding, complete this design document:

### API Analysis

**API Name**: [Your chosen API]

**Base URL**: [API base URL]

**Authentication Method**: 
- [ ] None
- [ ] API Key (header)
- [ ] API Key (query parameter)
- [ ] Basic Auth
- [ ] Bearer Token
- [ ] OAuth 2.0
- [ ] Other: ___________

**Rate Limits**: [Describe rate limits]

**Key Endpoints** (list 5-10 you'll integrate):

1. **Endpoint**: `/path/to/endpoint`
   - **Method**: GET/POST/etc.
   - **Purpose**: What does it do?
   - **Parameters**: What parameters does it accept?
   - **Response**: What data does it return?

2. [Repeat for each endpoint]

### Tool Design

For each endpoint, design one or more MCP tools:

**Tool 1: [Tool Name]**

```python
Tool(
    name="tool_name",
    description="Clear description of what this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description"
            }
        },
        "required": ["param1"]
    }
)
```

**Justification**: Why is this tool needed? What use case does it enable?

**Tool 2-N**: [Repeat for each tool]

### Integration Patterns

**Caching Strategy**:
- [ ] No caching needed
- [ ] Cache all responses for _____ minutes
- [ ] Selective caching (which endpoints?)
- [ ] Time-based invalidation
- [ ] Manual cache refresh

**Rate Limiting Strategy**:
- [ ] No rate limiting needed
- [ ] Track requests per minute/hour
- [ ] Queue requests when approaching limit
- [ ] Return clear error when limited
- [ ] Implement exponential backoff

**Error Handling Strategy**:
- [ ] Retry on network errors (how many times?)
- [ ] Retry on 5xx errors (with backoff?)
- [ ] Handle 4xx errors gracefully
- [ ] Validate responses before returning
- [ ] Log errors for debugging

**Data Transformation**:
- How will you format API responses for AI consumption?
- Will you filter or summarize large responses?
- How will you handle pagination?

## Phase 3: Implementation

### Required Components

Your server must include:

#### 1. Configuration Management

```python
import os
from typing import Optional

class APIConfig:
    """Configuration for API integration."""
    
    def __init__(self):
        self.base_url = "https://api.example.com"
        self.api_key = os.environ.get("API_KEY")
        self.timeout = 30  # seconds
        self.max_retries = 3
        
    def validate(self) -> bool:
        """Validate configuration is complete."""
        if not self.api_key and self._requires_auth():
            raise ValueError("API_KEY environment variable required")
        return True
```

#### 2. API Client

```python
import requests
from typing import Dict, Any, Optional
import time

class APIClient:
    """Client for making API requests."""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Configure session with headers, auth, etc."""
        # Add authentication headers
        # Set user agent
        # Configure timeouts
        pass
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request with error handling."""
        # Implement with:
        # - Retry logic
        # - Error handling
        # - Rate limit checking
        # - Response validation
        pass
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request with error handling."""
        pass
```

#### 3. Cache Implementation

```python
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class ResponseCache:
    """Cache for API responses."""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        if datetime.now() - timestamp > self.ttl:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any):
        """Store value in cache."""
        self.cache[key] = (value, datetime.now())
    
    def clear(self, pattern: Optional[str] = None):
        """Clear cache entries."""
        if pattern is None:
            self.cache.clear()
        else:
            # Implement pattern-based clearing
            pass
    
    def stats(self) -> Dict[str, int]:
        """Return cache statistics."""
        return {
            "entries": len(self.cache),
            "size_bytes": self._estimate_size()
        }
```

#### 4. Rate Limiter

```python
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    """Track and enforce rate limits."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = deque()
    
    def can_make_request(self) -> bool:
        """Check if request is allowed under rate limit."""
        self._clean_old_requests()
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        """Record that a request was made."""
        self.requests.append(datetime.now())
    
    def time_until_available(self) -> float:
        """Return seconds until next request is allowed."""
        if self.can_make_request():
            return 0.0
        
        self._clean_old_requests()
        if len(self.requests) == 0:
            return 0.0
        
        oldest_request = self.requests[0]
        wait_until = oldest_request + self.window
        return (wait_until - datetime.now()).total_seconds()
    
    def _clean_old_requests(self):
        """Remove requests outside the window."""
        cutoff = datetime.now() - self.window
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()
```

#### 5. MCP Server Implementation

```python
#!/usr/bin/env python3
"""
[API Name] MCP Server

Complete integration with [API Name] API.
"""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import your components
from api_config import APIConfig
from api_client import APIClient
from cache import ResponseCache
from rate_limiter import RateLimiter

# Initialize components
config = APIConfig()
client = APIClient(config)
cache = ResponseCache(ttl_seconds=300)
rate_limiter = RateLimiter(max_requests=60, window_seconds=60)

# Create server
app = Server("api-integration-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        # Define your tools here
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    # Check rate limit
    if not rate_limiter.can_make_request():
        wait_time = rate_limiter.time_until_available()
        return [TextContent(
            type="text",
            text=f"Rate limit exceeded. Please wait {wait_time:.1f} seconds."
        )]
    
    # Check cache
    cache_key = f"{name}:{str(arguments)}"
    cached = cache.get(cache_key)
    if cached:
        return [TextContent(type="text", text=f"[Cached] {cached}")]
    
    try:
        # Route to appropriate handler
        if name == "tool1":
            result = await handle_tool1(arguments)
        elif name == "tool2":
            result = await handle_tool2(arguments)
        # ... more tools
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        # Record request and cache result
        rate_limiter.record_request()
        cache.set(cache_key, result)
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def handle_tool1(arguments: dict) -> str:
    """Handle specific tool logic."""
    # Validate arguments
    # Call API
    # Transform response
    # Return formatted result
    pass

async def main():
    """Run the server."""
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Start server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### Required Features Checklist

Your implementation must include:

**Core Functionality**:
- [ ] At least 5 tools covering different API endpoints
- [ ] All tools have clear descriptions and parameter schemas
- [ ] Tools return well-formatted, human-readable results
- [ ] Error messages are clear and actionable

**Authentication**:
- [ ] API credentials loaded from environment variables
- [ ] Clear error if credentials are missing
- [ ] Credentials never logged or exposed
- [ ] Session/client properly configured with auth

**Rate Limiting**:
- [ ] Request tracking implemented
- [ ] Rate limits respected
- [ ] Clear error messages when limited
- [ ] Wait time estimates provided

**Caching**:
- [ ] Response caching implemented
- [ ] TTL (time-to-live) configurable
- [ ] Cache hits/misses tracked
- [ ] Manual cache clearing available
- [ ] Cache status reportable

**Error Handling**:
- [ ] Network errors caught and retried
- [ ] API errors handled gracefully
- [ ] Validation errors reported clearly
- [ ] Unexpected errors don't crash server
- [ ] All errors logged appropriately

**Data Transformation**:
- [ ] API responses formatted for readability
- [ ] Large responses summarized appropriately
- [ ] Pagination handled where needed
- [ ] Data types properly converted

**Observability**:
- [ ] Request logging to stderr
- [ ] Performance metrics tracked
- [ ] Cache statistics available
- [ ] Rate limit status reportable

## Phase 4: Testing

### Manual Testing with MCP Inspector

```bash
# Start your server with Inspector
mcp-inspector python your_api_server.py

# Set environment variables if needed
export API_KEY="your-key-here"
mcp-inspector python your_api_server.py
```

Test each tool:
1. Call with valid parameters
2. Call with invalid parameters
3. Call repeatedly to test caching
4. Call rapidly to test rate limiting
5. Call with missing required parameters

### Test Scenarios

Create test cases for:

**Happy Path**:
- [ ] Each tool works with valid inputs
- [ ] Results are formatted correctly
- [ ] Cache works after repeated calls
- [ ] Performance is acceptable

**Error Handling**:
- [ ] Invalid parameters rejected
- [ ] Missing parameters detected
- [ ] API errors handled gracefully
- [ ] Network errors recovered from
- [ ] Rate limits respected

**Edge Cases**:
- [ ] Empty responses handled
- [ ] Very large responses handled
- [ ] Special characters in input handled
- [ ] Concurrent requests handled
- [ ] Cache expiration works correctly

### Integration Testing with Cursor IDE

Configure your server in Cursor IDE:

```json
{
  "mcpServers": {
    "my-api": {
      "command": "python",
      "args": ["/path/to/your_api_server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

Test with real queries:
- "Use [your API] to find..."
- "Get information about..."
- "Search for..."

## Phase 5: Documentation

Create comprehensive documentation:

### README.md

```markdown
# [API Name] MCP Server

Complete MCP integration with [API Name] API.

## Features

- [List key features]
- [Highlight what makes it useful]

## Prerequisites

- Python 3.9+
- MCP SDK
- [API Name] API key (get from [URL])

## Installation

```bash
pip install mcp requests
```

## Configuration

Set your API key as an environment variable:

```bash
export API_KEY="your-key-here"
```

## Usage

### With MCP Inspector

```bash
mcp-inspector python api_server.py
```

### With Cursor IDE

Add to your configuration:

```json
{
  "mcpServers": {
    "my-api": {
      "command": "python",
      "args": ["/absolute/path/to/api_server.py"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Available Tools

### tool_name

Description of what it does.

**Parameters**:
- `param1` (string): Description
- `param2` (number, optional): Description

**Example**:
```
Input: {"param1": "value", "param2": 123}
Output: [Formatted result]
```

[Repeat for each tool]

## Rate Limits

- [Describe rate limits]
- Cached responses used when available (5 minute TTL)
- Clear messages when rate limited

## Error Handling

- Network errors: Retried up to 3 times
- API errors: Clear error messages returned
- Rate limits: Wait time displayed
- Validation errors: Specific feedback provided

## Architecture

[Brief description of how your integration works]

## Development

[How to contribute or modify]

## License

[License information]
```

### API_GUIDE.md

Document your API integration decisions:

```markdown
# API Integration Guide

## API Overview

[Brief description of the API]

## Endpoints Integrated

[List and describe each endpoint you integrated]

## Design Decisions

### Why These Tools?

[Explain your tool choices]

### Caching Strategy

[Explain what you cache and why]

### Rate Limiting Approach

[Explain how you handle rate limits]

### Error Handling Philosophy

[Explain your error handling approach]

## Known Limitations

[Be honest about what doesn't work or could be better]

## Future Enhancements

[What you'd add with more time]
```

## Success Criteria

Your integration will be evaluated on:

### Functionality (40%)

- [ ] All tools work correctly
- [ ] Error handling is comprehensive
- [ ] Rate limiting works
- [ ] Caching improves performance
- [ ] Authentication is secure

### Code Quality (30%)

- [ ] Code is well-organized and modular
- [ ] Functions have clear purposes
- [ ] Type hints used throughout
- [ ] Comments explain complex logic
- [ ] No security vulnerabilities

### User Experience (20%)

- [ ] Tool descriptions are clear
- [ ] Error messages are helpful
- [ ] Results are well-formatted
- [ ] Performance is good
- [ ] Configuration is straightforward

### Documentation (10%)

- [ ] README is complete
- [ ] Setup instructions work
- [ ] Examples are helpful
- [ ] Design decisions explained
- [ ] Limitations acknowledged

## Common Pitfalls

### 1. Hardcoded Credentials

**Bad**:
```python
api_key = "sk_live_1234567890"  # Never do this!
```

**Good**:
```python
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable required")
```

### 2. No Error Handling

**Bad**:
```python
response = requests.get(url)
return response.json()  # What if this fails?
```

**Good**:
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.Timeout:
    return {"error": "Request timed out"}
except requests.RequestException as e:
    return {"error": f"API request failed: {str(e)}"}
```

### 3. Ignoring Rate Limits

**Bad**:
```python
# Just make requests without tracking
response = api_call()
```

**Good**:
```python
if not rate_limiter.can_make_request():
    wait = rate_limiter.time_until_available()
    raise RateLimitError(f"Please wait {wait:.1f} seconds")

response = api_call()
rate_limiter.record_request()
```

### 4. Poor Response Formatting

**Bad**:
```python
return str(api_response)  # Returns ugly JSON string
```

**Good**:
```python
# Format nicely for human reading
result = f"""
Movie: {data['title']}
Year: {data['year']}
Rating: {data['rating']}/10
Plot: {data['overview']}
"""
return result
```

### 5. No Caching

**Bad**:
```python
# Hit API every time even for identical requests
data = api_call(endpoint)
```

**Good**:
```python
cache_key = f"{endpoint}:{params}"
cached = cache.get(cache_key)
if cached:
    return cached

data = api_call(endpoint, params)
cache.set(cache_key, data)
return data
```

## Advanced Extensions

If you finish early, enhance your integration:

### 1. Pagination Support

Handle paginated API responses:

```python
async def fetch_all_pages(endpoint: str) -> list:
    """Fetch all pages of a paginated endpoint."""
    results = []
    page = 1
    
    while True:
        response = api_call(endpoint, {"page": page})
        results.extend(response["items"])
        
        if not response["has_next"]:
            break
        
        page += 1
    
    return results
```

### 2. Webhook Support

If API supports webhooks, implement handlers:

```python
@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="register_webhook",
            description="Register for real-time updates"
        )
    ]
```

### 3. Batch Operations

Support batch requests for efficiency:

```python
Tool(
    name="batch_lookup",
    description="Look up multiple items in one request",
    inputSchema={
        "type": "object",
        "properties": {
            "ids": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
)
```

### 4. Smart Caching

Implement cache warming or predictive caching:

```python
async def warm_cache(popular_queries: list):
    """Pre-fetch commonly requested data."""
    for query in popular_queries:
        cache.set(query, await api_call(query))
```

### 5. Monitoring Dashboard

Create a tool that reports detailed stats:

```python
Tool(
    name="get_detailed_stats",
    description="Get comprehensive integration statistics"
)

# Returns:
# - Request count per endpoint
# - Average response times
# - Cache hit rates
# - Error rates
# - Rate limit status
```

## Example Project Structure

```
api-integration-challenge/
├── api_server.py           # Main MCP server
├── api_client.py           # API client implementation
├── api_config.py           # Configuration management
├── cache.py                # Caching implementation
├── rate_limiter.py         # Rate limiting
├── response_formatter.py   # Format API responses
├── tests/
│   ├── test_client.py
│   ├── test_cache.py
│   └── test_integration.py
├── docs/
│   ├── README.md
│   └── API_GUIDE.md
├── requirements.txt
└── .env.example
```

## Submission Checklist

Before considering this complete:

- [ ] All required components implemented
- [ ] All features from checklist working
- [ ] Manual testing completed successfully
- [ ] Integration tested in Cursor IDE
- [ ] README.md written and complete
- [ ] API_GUIDE.md written with design decisions
- [ ] Code is clean and well-commented
- [ ] No hardcoded secrets
- [ ] Error handling is comprehensive
- [ ] Performance is acceptable

## What You've Learned

By completing this challenge, you now understand:

1. **Real-world API integration** - Handling auth, rate limits, errors
2. **Production patterns** - Caching, retry logic, observability
3. **MCP tool design** - Creating intuitive interfaces for complex APIs
4. **Error handling** - Graceful degradation and clear messaging
5. **Configuration management** - Secure credential handling
6. **Performance optimization** - Caching and request management
7. **Documentation** - Writing clear guides for users

These skills translate directly to professional API integration work!

## Showcase Your Work

Share your integration:

1. Push to GitHub with good documentation
2. Share in MCP community
3. Add to your portfolio
4. Use as a reference for future projects

## Next Steps

- Complete **Module 07** (Security Best Practices) to harden your integration
- Try **Module 08** (Debugging & Troubleshooting) to improve error handling
- Build a multi-server system combining your API with others
- Integrate with a production API at your workplace

You're now capable of building production-grade MCP integrations for any API. Congratulations!

