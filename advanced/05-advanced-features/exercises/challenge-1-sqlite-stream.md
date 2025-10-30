# Challenge 1: Database Server with Streaming

## Overview

Build a complete SQLite database server with streaming query support. This challenge combines database operations with streaming progress notifications to create a production-ready pattern.

**Estimated Time:** 90 minutes

**Difficulty:** Advanced

**Prerequisites:**
- Completed Tutorial 1 (Streaming)
- Understanding of SQL and databases
- Familiarity with Python sqlite3 module

## Challenge Description

Create an MCP server that:

1. **Provides database tools** with streaming progress
2. **Manages a SQLite database** with sample data
3. **Streams query results** for large datasets
4. **Handles errors gracefully** with clear messages
5. **Implements security** to prevent SQL injection

## Requirements

### Required Tools

Implement these tools:

1. **query_database**
   - Execute SELECT queries
   - Stream progress for large result sets
   - Return formatted results
   - Validate queries for security

2. **get_schema**
   - List all tables
   - Show column information
   - Display indexes
   - Return foreign key relationships

3. **get_statistics**
   - Count rows in tables
   - Show database size
   - Calculate storage per table
   - Display index usage

4. **analyze_query**
   - Show query execution plan
   - Estimate result size
   - Suggest optimizations
   - Identify potential issues

### Database Schema

Create a database with these tables:

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_login TEXT
);

-- Posts table
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Comments table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Tags table
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Post-Tag junction table
CREATE TABLE post_tags (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);
```

### Sample Data Requirements

Generate sample data:
- At least 1,000 users
- At least 10,000 posts
- At least 50,000 comments
- At least 50 tags
- Random tag assignments to posts

This volume ensures streaming is necessary and visible.

### Streaming Requirements

Implement streaming progress updates that:

1. **Report progress every**:
   - 100 rows processed, OR
   - 1 second elapsed

2. **Include in progress updates**:
   - Current row count
   - Total expected rows (if known)
   - Percentage complete
   - Estimated time remaining (optional)

3. **Always return complete results** at the end

### Security Requirements

Prevent SQL injection:
- Only allow SELECT queries
- Block dangerous keywords (DROP, DELETE, UPDATE, INSERT, ALTER)
- Use parameterized queries where possible
- Validate query syntax

## Starter Code

```python
#!/usr/bin/env python3
"""
Challenge 1: Database Server with Streaming

Your implementation goes here.
"""

import asyncio
import sqlite3
import time
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Database path
DB_PATH = Path(__file__).parent / "challenge1.db"

# Create server
app = Server("database-streaming-server")

# TODO: Implement database initialization
def initialize_database():
    """Create database schema and populate with sample data."""
    pass

# TODO: Implement tool listing
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available database tools."""
    pass

# TODO: Implement tool handler with streaming
@app.call_tool()
async def call_tool(name: str, arguments: dict, request_context: Any) -> list[TextContent]:
    """Execute tools with streaming support."""
    pass

# TODO: Implement main function
async def main():
    """Run the server."""
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## Implementation Steps

### Step 1: Database Initialization

Implement `initialize_database()`:

- Create tables if they don't exist
- Check if data already exists
- Generate sample data if needed
- Create indexes for performance
- Print progress during data generation

**Hints:**
- Use `executemany()` for batch inserts
- Generate data in batches to manage memory
- Use `random` module for realistic data
- Add `datetime('now')` for timestamps

### Step 2: Tool Definitions

Define comprehensive tool schemas:

- Clear descriptions
- Proper parameter types
- Required vs optional parameters
- Default values where appropriate
- Examples in descriptions

### Step 3: Query Execution with Streaming

Implement streaming query execution:

```python
# Pseudocode structure
async def execute_streaming_query(query, request_context):
    # 1. Validate query
    # 2. Count expected rows
    # 3. Execute query with cursor
    # 4. Iterate results with progress updates
    # 5. Return formatted results
```

**Key Considerations:**
- How to count rows without executing twice?
- When to send progress updates?
- How to format large result sets?
- How to handle query errors?

### Step 4: Schema Information

Implement get_schema tool:

```python
# Get table information
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Get column information for each table
cursor.execute(f"PRAGMA table_info({table_name})")

# Get index information
cursor.execute(f"PRAGMA index_list({table_name})")

# Get foreign keys
cursor.execute(f"PRAGMA foreign_key_list({table_name})")
```

### Step 5: Statistics and Analysis

Implement analytics tools:

```python
# Row counts
cursor.execute(f"SELECT COUNT(*) FROM {table}")

# Database size
cursor.execute("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()")

# Table sizes
cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name='{table}'")
```

### Step 6: Query Analysis

Implement query analysis:

```python
# Execution plan
cursor.execute(f"EXPLAIN QUERY PLAN {query}")

# Estimated rows
# Use EXPLAIN to get query plan
# Parse plan for row estimates
```

## Testing Scenarios

Test your implementation with these queries:

### Test 1: Small Query
```sql
SELECT * FROM users LIMIT 10
```
Expected: Quick results, no streaming needed

### Test 2: Medium Query
```sql
SELECT * FROM posts WHERE views > 100
```
Expected: Some streaming, clear progress

### Test 3: Large Query
```sql
SELECT u.username, p.title, c.content
FROM comments c
JOIN posts p ON c.post_id = p.id
JOIN users u ON c.user_id = u.id
```
Expected: Significant streaming, multiple progress updates

### Test 4: Complex Aggregation
```sql
SELECT u.username, COUNT(p.id) as post_count, AVG(p.views) as avg_views
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id
ORDER BY post_count DESC
```
Expected: Streaming with formatted results

### Test 5: Security Tests
```sql
SELECT * FROM users; DROP TABLE users;
```
Expected: Rejected with security error

```sql
DELETE FROM users WHERE id=1
```
Expected: Rejected (not a SELECT query)

## Success Criteria

Your implementation should:

- [ ] Create and populate database successfully
- [ ] Execute SELECT queries correctly
- [ ] Stream progress for large queries
- [ ] Show accurate progress percentages
- [ ] Format results readably
- [ ] Provide schema information
- [ ] Calculate database statistics
- [ ] Analyze query execution plans
- [ ] Reject dangerous queries
- [ ] Handle SQL errors gracefully
- [ ] Work with MCP Inspector
- [ ] Include comprehensive comments

## Extension Challenges

If you finish early, try these enhancements:

### Extension 1: Query Caching

Cache query results for repeated queries:

```python
# Simple cache implementation
query_cache = {}

def get_cached_or_execute(query):
    if query in query_cache:
        return query_cache[query]
    
    result = execute_query(query)
    query_cache[query] = result
    return result
```

### Extension 2: Parameterized Queries

Support safe parameterization:

```json
{
  "query": "SELECT * FROM users WHERE username = ?",
  "parameters": ["john"]
}
```

### Extension 3: Export Results

Add tool to export results to CSV/JSON:

```python
Tool(
    name="export_query",
    description="Execute query and export results to file",
    inputSchema={...}
)
```

### Extension 4: Query History

Track executed queries:

```python
query_history = []

def log_query(query, rows_returned, execution_time):
    query_history.append({
        "query": query,
        "rows": rows_returned,
        "time": execution_time,
        "timestamp": datetime.now()
    })
```

## Evaluation Rubric

Your solution will be evaluated on:

### Functionality (40%)
- All required tools work correctly
- Database schema matches specification
- Sample data is generated properly
- Queries execute successfully

### Streaming Implementation (25%)
- Progress updates are sent appropriately
- Progress information is accurate
- Update frequency is reasonable
- Final results are complete

### Security (20%)
- SQL injection prevention works
- Query validation is comprehensive
- Error messages don't leak sensitive info
- Path validation prevents file access issues

### Code Quality (15%)
- Clear, well-commented code
- Proper error handling
- Type hints used appropriately
- Code follows Python conventions

## Common Pitfalls

### Pitfall 1: Not Counting Rows First

**Problem:** Can't show accurate progress without knowing total

**Solution:**
```python
# Get count first
count = cursor.execute(f"SELECT COUNT(*) FROM ({query})").fetchone()[0]

# Then execute for results
cursor.execute(query)
```

### Pitfall 2: Blocking on Large Results

**Problem:** Fetching all rows at once consumes memory

**Solution:**
```python
# Iterate cursor, don't use fetchall()
for row in cursor:
    # Process row
    pass
```

### Pitfall 3: SQL Injection via String Formatting

**Problem:** Using f-strings or % formatting with user input

**Solution:**
```python
# WRONG:
cursor.execute(f"SELECT * FROM {table}")

# RIGHT:
allowed_tables = ['users', 'posts', 'comments']
if table not in allowed_tables:
    raise ValueError("Invalid table")
cursor.execute(f"SELECT * FROM {table}")  # Now safe
```

### Pitfall 4: Progress Updates Too Frequent

**Problem:** Sending updates every row kills performance

**Solution:**
```python
# Update every N rows OR every N seconds
if (row_count % 100 == 0) or (time.time() - last_update > 1.0):
    send_progress_update()
```

## Debugging Tips

### Tip 1: Print SQL Queries

```python
print(f"Executing: {query}")
cursor.execute(query)
```

### Tip 2: Validate Data Generation

```python
def verify_data():
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM posts")
    print(f"Posts: {cursor.fetchone()[0]}")
```

### Tip 3: Test Queries in SQLite CLI

```bash
sqlite3 challenge1.db
sqlite> SELECT COUNT(*) FROM users;
sqlite> .schema users
sqlite> .quit
```

### Tip 4: Time Operations

```python
start = time.time()
# ... operation ...
elapsed = time.time() - start
print(f"Took {elapsed:.2f}s")
```

## Solution Reference

A complete solution is available in `solutions/challenge-1-solution.py`.

Try to complete the challenge on your own first. The solution shows one possible implementation, but there are many valid approaches.

## Next Steps

After completing this challenge:

1. Try Challenge 2 (API Resources)
2. Review the streaming_server.py example
3. Consider how this pattern applies to your projects
4. Think about combining this with resources and prompts

## Key Learnings

This challenge reinforces:

- Streaming for long-running database operations
- Security considerations in data access
- Progress tracking and user feedback
- Database schema design
- Query optimization
- Error handling in async operations

Great work tackling this advanced challenge!

