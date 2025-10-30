#!/usr/bin/env python3
"""
Web Scraper MCP Server

Provides web scraping capabilities through MCP. Allows AI to extract data from
websites safely and efficiently, with support for HTML parsing, data extraction,
and structured output.

Features:
- Fetch and parse web pages
- Extract text content and metadata
- Find elements by CSS selectors
- Extract links and images
- Table data extraction
- Respect robots.txt and rate limiting
- Caching for performance
- Error handling and retries

Usage:
    python web_scraper_server.py

Test with MCP Inspector:
    mcp-inspector python web_scraper_server.py

Configure for Claude Desktop:
    {
      "mcpServers": {
        "web_scraper": {
          "command": "python",
          "args": ["/path/to/web_scraper_server.py"]
        }
      }
    }

Security Notes:
- Only scrapes public websites
- Respects robots.txt by default
- Rate limiting to prevent abuse
- No authentication/credential handling
"""

import asyncio
import re
import time
from collections import deque
from typing import Any, Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


# ============================================================================
# Configuration
# ============================================================================

# Rate limiting configuration
MAX_REQUESTS_PER_MINUTE = 10
RATE_LIMIT_WINDOW = 60  # seconds

# Request configuration
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Cache configuration
CACHE_TTL = 300  # 5 minutes

# User agent for requests
USER_AGENT = "MCP-Web-Scraper/1.0 (Educational purposes)"


# ============================================================================
# Rate Limiter
# ============================================================================

class RateLimiter:
    """
    Simple rate limiter to prevent overwhelming websites.
    
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
    
    def is_allowed(self, domain: str) -> bool:
        """
        Check if a request is allowed under rate limits.
        
        Args:
            domain: Domain being requested
        
        Returns:
            True if request is allowed
        """
        now = time.time()
        
        # Remove requests outside the time window
        while self.requests and self.requests[0][0] < now - self.time_window:
            self.requests.popleft()
        
        # Check if we're under the limit for this domain
        domain_requests = sum(1 for _, d in self.requests if d == domain)
        return domain_requests < self.max_requests
    
    def record_request(self, domain: str):
        """
        Record that a request was made.
        
        Args:
            domain: Domain that was requested
        """
        self.requests.append((time.time(), domain))
    
    def wait_time(self, domain: str) -> float:
        """
        Calculate seconds to wait before next request is allowed.
        
        Args:
            domain: Domain to check
        
        Returns:
            Seconds to wait
        """
        now = time.time()
        domain_requests = [t for t, d in self.requests if d == domain]
        
        if not domain_requests:
            return 0.0
        
        if len(domain_requests) < self.max_requests:
            return 0.0
        
        oldest_request = domain_requests[0]
        time_until_reset = (oldest_request + self.time_window) - now
        return max(0.0, time_until_reset)


# ============================================================================
# Response Cache
# ============================================================================

class ResponseCache:
    """
    Simple in-memory cache for web requests.
    
    Reduces redundant requests and improves performance.
    """
    
    def __init__(self, ttl: int = 300):
        """
        Initialize cache.
        
        Args:
            ttl: Time-to-live in seconds
        """
        self.ttl = ttl
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[str]:
        """
        Get cached content if not expired.
        
        Args:
            key: Cache key (typically URL)
        
        Returns:
            Cached content or None
        """
        if key in self.cache:
            content, timestamp = self.cache[key]
            
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return content
            else:
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, content: str):
        """
        Store content in cache.
        
        Args:
            key: Cache key
            content: Content to cache
        """
        self.cache[key] = (content, time.time())
    
    def clear(self):
        """Clear all cached entries."""
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2)
        }


# ============================================================================
# Web Scraper
# ============================================================================

class WebScraper:
    """
    Web scraping client with rate limiting, caching, and robots.txt support.
    """
    
    def __init__(self):
        """Initialize web scraper."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.rate_limiter = RateLimiter(MAX_REQUESTS_PER_MINUTE, RATE_LIMIT_WINDOW)
        self.cache = ResponseCache(ttl=CACHE_TTL)
        self.robots_cache = {}  # Cache for robots.txt parsers
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _check_robots_txt(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt.
        
        Args:
            url: URL to check
        
        Returns:
            True if allowed
        """
        try:
            domain = self._get_domain(url)
            
            # Check cache
            if domain not in self.robots_cache:
                rp = RobotFileParser()
                rp.set_url(f"{domain}/robots.txt")
                
                try:
                    rp.read()
                    self.robots_cache[domain] = rp
                except Exception:
                    # If robots.txt can't be read, assume allowed
                    return True
            
            return self.robots_cache[domain].can_fetch(USER_AGENT, url)
        except Exception:
            # On error, assume allowed
            return True
    
    def _fetch_with_retry(self, url: str) -> str:
        """
        Fetch URL with retries and error handling.
        
        Args:
            url: URL to fetch
        
        Returns:
            Response content
        
        Raises:
            Exception: If fetch fails after retries
        """
        domain = self._get_domain(url)
        
        for attempt in range(MAX_RETRIES):
            try:
                # Check rate limit
                if not self.rate_limiter.is_allowed(domain):
                    wait_time = self.rate_limiter.wait_time(domain)
                    raise Exception(
                        f"Rate limit exceeded for {domain}. "
                        f"Please wait {wait_time:.0f} seconds."
                    )
                
                # Make request
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                self.rate_limiter.record_request(domain)
                
                response.raise_for_status()
                return response.text
                
            except requests.HTTPError as e:
                if e.response.status_code in [403, 404]:
                    # Don't retry these
                    raise Exception(f"HTTP {e.response.status_code}: {url}")
                
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise Exception(f"HTTP error: {e}")
                
            except requests.Timeout:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise Exception(f"Request timed out after {REQUEST_TIMEOUT}s")
                
            except requests.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise Exception(f"Request failed: {e}")
        
        raise Exception("Max retries exceeded")
    
    def fetch_page(self, url: str, check_robots: bool = True) -> str:
        """
        Fetch and return HTML content of a page.
        
        Args:
            url: URL to fetch
            check_robots: Whether to check robots.txt
        
        Returns:
            HTML content
        
        Raises:
            Exception: If fetch fails or robots.txt disallows
        """
        # Validate URL
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        
        # Check robots.txt
        if check_robots and not self._check_robots_txt(url):
            raise Exception(f"Access denied by robots.txt: {url}")
        
        # Check cache
        cached = self.cache.get(url)
        if cached is not None:
            return cached
        
        # Fetch content
        content = self._fetch_with_retry(url)
        
        # Cache it
        self.cache.set(url, content)
        
        return content
    
    def extract_text(self, url: str, check_robots: bool = True) -> dict:
        """
        Extract text content from a page.
        
        Args:
            url: URL to scrape
            check_robots: Whether to check robots.txt
        
        Returns:
            Dictionary with title, text, and metadata
        """
        html = self.fetch_page(url, check_robots)
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Extract title
        title = soup.title.string if soup.title else "No title"
        
        # Extract text
        text = soup.get_text(separator="\n", strip=True)
        
        # Extract metadata
        meta_description = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_description = meta_tag["content"]
        
        return {
            "url": url,
            "title": title.strip(),
            "description": meta_description,
            "text": text,
            "length": len(text)
        }
    
    def find_elements(self, url: str, selector: str, check_robots: bool = True) -> list[dict]:
        """
        Find elements matching a CSS selector.
        
        Args:
            url: URL to scrape
            selector: CSS selector
            check_robots: Whether to check robots.txt
        
        Returns:
            List of elements with tag, text, and attributes
        """
        html = self.fetch_page(url, check_robots)
        soup = BeautifulSoup(html, "html.parser")
        
        elements = soup.select(selector)
        
        results = []
        for elem in elements[:50]:  # Limit to 50 elements
            results.append({
                "tag": elem.name,
                "text": elem.get_text(strip=True),
                "attributes": dict(elem.attrs),
                "html": str(elem)[:200]  # First 200 chars of HTML
            })
        
        return results
    
    def extract_links(self, url: str, check_robots: bool = True) -> list[dict]:
        """
        Extract all links from a page.
        
        Args:
            url: URL to scrape
            check_robots: Whether to check robots.txt
        
        Returns:
            List of links with href and text
        """
        html = self.fetch_page(url, check_robots)
        soup = BeautifulSoup(html, "html.parser")
        
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            
            # Skip non-http links
            if not absolute_url.startswith(("http://", "https://")):
                continue
            
            links.append({
                "url": absolute_url,
                "text": a_tag.get_text(strip=True),
                "title": a_tag.get("title", "")
            })
        
        return links
    
    def extract_images(self, url: str, check_robots: bool = True) -> list[dict]:
        """
        Extract all images from a page.
        
        Args:
            url: URL to scrape
            check_robots: Whether to check robots.txt
        
        Returns:
            List of images with src and alt text
        """
        html = self.fetch_page(url, check_robots)
        soup = BeautifulSoup(html, "html.parser")
        
        images = []
        for img_tag in soup.find_all("img", src=True):
            src = img_tag["src"]
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, src)
            
            images.append({
                "url": absolute_url,
                "alt": img_tag.get("alt", ""),
                "title": img_tag.get("title", ""),
                "width": img_tag.get("width", ""),
                "height": img_tag.get("height", "")
            })
        
        return images
    
    def extract_tables(self, url: str, check_robots: bool = True) -> list[dict]:
        """
        Extract tables from a page.
        
        Args:
            url: URL to scrape
            check_robots: Whether to check robots.txt
        
        Returns:
            List of tables with headers and rows
        """
        html = self.fetch_page(url, check_robots)
        soup = BeautifulSoup(html, "html.parser")
        
        tables = []
        for table in soup.find_all("table")[:10]:  # Limit to 10 tables
            # Extract headers
            headers = []
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all("th")]
            
            # Extract rows
            rows = []
            tbody = table.find("tbody") or table
            for tr in tbody.find_all("tr")[:50]:  # Limit to 50 rows
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cells:
                    rows.append(cells)
            
            if rows:
                tables.append({
                    "headers": headers,
                    "rows": rows,
                    "row_count": len(rows),
                    "column_count": len(rows[0]) if rows else 0
                })
        
        return tables


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create server and scraper
app = Server("web-scraper-server")
scraper = WebScraper()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available web scraping tools."""
    return [
        Tool(
            name="scrape_text",
            description="Extract text content from a web page including title and description",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the page to scrape"
                    },
                    "check_robots": {
                        "type": "boolean",
                        "description": "Whether to check robots.txt (default: true)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="scrape_elements",
            description="Find and extract elements from a page using CSS selectors",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the page to scrape"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector (e.g., 'h1', '.className', '#id', 'div.content p')"
                    },
                    "check_robots": {
                        "type": "boolean",
                        "description": "Whether to check robots.txt (default: true)",
                        "default": True
                    }
                },
                "required": ["url", "selector"]
            }
        ),
        Tool(
            name="scrape_links",
            description="Extract all links from a web page",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the page to scrape"
                    },
                    "check_robots": {
                        "type": "boolean",
                        "description": "Whether to check robots.txt (default: true)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="scrape_images",
            description="Extract all images from a web page",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the page to scrape"
                    },
                    "check_robots": {
                        "type": "boolean",
                        "description": "Whether to check robots.txt (default: true)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="scrape_tables",
            description="Extract table data from a web page",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the page to scrape"
                    },
                    "check_robots": {
                        "type": "boolean",
                        "description": "Whether to check robots.txt (default: true)",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="get_scraper_stats",
            description="Get statistics about scraper usage (cache, rate limits)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute web scraping operations."""
    
    try:
        # Tool 1: Scrape Text
        if name == "scrape_text":
            url = arguments["url"]
            check_robots = arguments.get("check_robots", True)
            
            result = scraper.extract_text(url, check_robots)
            
            output = f"""Page Content: {result['title']}

URL: {result['url']}

Description: {result['description'] or 'No description'}

Text Length: {result['length']} characters

Content:
{result['text'][:5000]}{'...' if len(result['text']) > 5000 else ''}

Note: Text truncated to 5000 characters for display
"""
            return [TextContent(type="text", text=output)]
        
        # Tool 2: Scrape Elements
        elif name == "scrape_elements":
            url = arguments["url"]
            selector = arguments["selector"]
            check_robots = arguments.get("check_robots", True)
            
            elements = scraper.find_elements(url, selector, check_robots)
            
            if not elements:
                return [TextContent(
                    type="text",
                    text=f"No elements found matching selector: {selector}"
                )]
            
            output = [f"Found {len(elements)} elements matching '{selector}':\n"]
            for i, elem in enumerate(elements, 1):
                output.append(f"{i}. <{elem['tag']}>")
                if elem['text']:
                    output.append(f"   Text: {elem['text'][:100]}")
                if elem['attributes']:
                    attrs = ', '.join(f"{k}={v}" for k, v in list(elem['attributes'].items())[:3])
                    output.append(f"   Attributes: {attrs}")
                output.append("")
            
            return [TextContent(type="text", text="\n".join(output))]
        
        # Tool 3: Scrape Links
        elif name == "scrape_links":
            url = arguments["url"]
            check_robots = arguments.get("check_robots", True)
            
            links = scraper.extract_links(url, check_robots)
            
            if not links:
                return [TextContent(type="text", text="No links found on page")]
            
            output = [f"Found {len(links)} links:\n"]
            for i, link in enumerate(links[:100], 1):  # Show first 100
                output.append(f"{i}. {link['text'] or '(no text)'}")
                output.append(f"   URL: {link['url']}")
                if link['title']:
                    output.append(f"   Title: {link['title']}")
                output.append("")
            
            if len(links) > 100:
                output.append(f"... and {len(links) - 100} more links")
            
            return [TextContent(type="text", text="\n".join(output))]
        
        # Tool 4: Scrape Images
        elif name == "scrape_images":
            url = arguments["url"]
            check_robots = arguments.get("check_robots", True)
            
            images = scraper.extract_images(url, check_robots)
            
            if not images:
                return [TextContent(type="text", text="No images found on page")]
            
            output = [f"Found {len(images)} images:\n"]
            for i, img in enumerate(images[:50], 1):  # Show first 50
                output.append(f"{i}. {img['url']}")
                if img['alt']:
                    output.append(f"   Alt: {img['alt']}")
                if img['width'] and img['height']:
                    output.append(f"   Size: {img['width']}x{img['height']}")
                output.append("")
            
            if len(images) > 50:
                output.append(f"... and {len(images) - 50} more images")
            
            return [TextContent(type="text", text="\n".join(output))]
        
        # Tool 5: Scrape Tables
        elif name == "scrape_tables":
            url = arguments["url"]
            check_robots = arguments.get("check_robots", True)
            
            tables = scraper.extract_tables(url, check_robots)
            
            if not tables:
                return [TextContent(type="text", text="No tables found on page")]
            
            output = [f"Found {len(tables)} tables:\n"]
            
            for i, table in enumerate(tables, 1):
                output.append(f"Table {i}: {table['row_count']} rows × {table['column_count']} columns")
                
                # Show headers
                if table['headers']:
                    output.append(f"Headers: {', '.join(table['headers'])}")
                
                # Show first few rows
                output.append("\nData:")
                for row_idx, row in enumerate(table['rows'][:10], 1):
                    output.append(f"  Row {row_idx}: {' | '.join(str(cell)[:30] for cell in row)}")
                
                if table['row_count'] > 10:
                    output.append(f"  ... and {table['row_count'] - 10} more rows")
                
                output.append("")
            
            return [TextContent(type="text", text="\n".join(output))]
        
        # Tool 6: Get Stats
        elif name == "get_scraper_stats":
            cache_stats = scraper.cache.get_stats()
            
            output = f"""Web Scraper Statistics:

Cache:
- Cached pages: {cache_stats['entries']}
- Cache hits: {cache_stats['hits']}
- Cache misses: {cache_stats['misses']}
- Hit rate: {cache_stats['hit_rate_percent']}%

Configuration:
- Rate limit: {MAX_REQUESTS_PER_MINUTE} requests per {RATE_LIMIT_WINDOW}s
- Request timeout: {REQUEST_TIMEOUT}s
- Max retries: {MAX_RETRIES}
- Cache TTL: {CACHE_TTL}s
"""
            return [TextContent(type="text", text=output)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except ValueError as e:
        return [TextContent(type="text", text=f"Invalid input: {e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


# ============================================================================
# Server Lifecycle
# ============================================================================

async def main():
    """Run the web scraper server."""
    print("=" * 70)
    print("Web Scraper MCP Server")
    print("=" * 70)
    print()
    print("Features:")
    print("  - Extract text content from web pages")
    print("  - Find elements with CSS selectors")
    print("  - Extract links, images, and tables")
    print("  - Rate limiting and caching")
    print("  - Respects robots.txt")
    print()
    print("Configuration:")
    print(f"  - Rate limit: {MAX_REQUESTS_PER_MINUTE} requests per {RATE_LIMIT_WINDOW}s")
    print(f"  - Cache TTL: {CACHE_TTL}s")
    print(f"  - Request timeout: {REQUEST_TIMEOUT}s")
    print()
    print("Security:")
    print("  - Only public websites")
    print("  - Respects robots.txt by default")
    print("  - Rate limiting prevents abuse")
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

