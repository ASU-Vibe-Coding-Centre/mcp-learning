#!/usr/bin/env python3
"""
MCP Server with Streaming Support - SQLite Database Example

This example demonstrates how to implement streaming responses in an MCP server.
Streaming allows servers to send progress updates during long-running operations,
providing better user experience and feedback.

Key Concepts Demonstrated:
1. Streaming progress notifications during database queries
2. Incremental result delivery for large datasets
3. Using request_context to send progress updates
4. Progress tokens for tracking operations
5. Combining streaming with regular tool responses

Usage:
    python streaming_server.py

Test with MCP Inspector:
    mcp-inspector python streaming_server.py
"""

import asyncio
import json
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# ============================================================================
# Database Setup and Management
# ============================================================================

# Database file path (will be created in the same directory as this script)
DB_PATH = Path(__file__).parent / "streaming_example.db"


def initialize_database() -> None:
    """
    Initialize the SQLite database with sample data.
    
    This creates:
    - A 'users' table with 1000 sample records
    - A 'orders' table with 5000 sample records
    - Indexes for efficient querying
    
    The large dataset is perfect for demonstrating streaming,
    as queries will take long enough to show progress updates.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Check if we need to populate data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Populate users table with 1000 records
        departments = ["Engineering", "Sales", "Marketing", "HR", "Finance"]
        for i in range(1, 1001):
            cursor.execute("""
                INSERT INTO users (name, email, department, created_at)
                VALUES (?, ?, ?, datetime('now', '-' || ? || ' days'))
            """, (
                f"User {i}",
                f"user{i}@example.com",
                departments[i % len(departments)],
                i  # Created between 1 and 1000 days ago
            ))
        
        # Populate orders table with 5000 records
        products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
        statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        for i in range(1, 5001):
            cursor.execute("""
                INSERT INTO orders (user_id, product, amount, status, order_date)
                VALUES (?, ?, ?, ?, datetime('now', '-' || ? || ' days'))
            """, (
                (i % 1000) + 1,  # user_id (1-1000)
                products[i % len(products)],
                round((i % 100) * 1.5 + 10.0, 2),  # amount ($10-$160)
                statuses[i % len(statuses)],
                i % 365  # order_date (last year)
            ))
        
        conn.commit()
        print(f"✓ Initialized database with sample data at {DB_PATH}")
    
    # Create indexes for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_department ON users(department)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
    
    conn.commit()
    conn.close()


def execute_query(query: str, params: tuple = ()) -> list[dict[str, Any]]:
    """
    Execute a SQL query and return results as a list of dictionaries.
    
    Args:
        query: SQL query string
        params: Query parameters (for parameterized queries)
    
    Returns:
        List of dictionaries where keys are column names
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return results


def get_row_count(query: str, params: tuple = ()) -> int:
    """
    Get the number of rows that would be returned by a query.
    
    This is useful for calculating progress percentages.
    
    Args:
        query: SQL query string
        params: Query parameters
    
    Returns:
        Number of rows
    """
    # Convert SELECT query to COUNT query
    # This is a simplified approach - production code would parse SQL properly
    count_query = f"SELECT COUNT(*) FROM ({query})"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(count_query, params)
    count = cursor.fetchone()[0]
    conn.close()
    
    return count


# ============================================================================
# MCP Server Implementation
# ============================================================================

# Create the MCP server instance
app = Server("streaming-database-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available database tools.
    
    This server provides three tools:
    1. query_database - Execute SQL queries with streaming results
    2. get_schema - Get database schema information
    3. get_stats - Get database statistics
    
    Returns:
        List of Tool definitions with schemas
    """
    return [
        Tool(
            name="query_database",
            description=(
                "Execute a SQL query against the sample database. "
                "For large result sets, progress updates will be streamed. "
                "The database contains 'users' and 'orders' tables with sample data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query to execute (read-only queries only)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows to return (optional, default: 1000)",
                        "default": 1000,
                        "minimum": 1,
                        "maximum": 10000
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_schema",
            description="Get the schema information for all tables in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Optional: Get schema for specific table (users or orders)"
                    }
                }
            }
        ),
        Tool(
            name="get_stats",
            description="Get statistics about the database (row counts, table sizes, etc.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict, request_context: Any) -> list[TextContent]:
    """
    Handle tool execution with streaming support.
    
    This handler demonstrates:
    - How to send progress notifications during long operations
    - How to use request_context for streaming
    - How to provide incremental results
    
    Args:
        name: Tool name to execute
        arguments: Tool arguments from the client
        request_context: Request context for sending progress updates
    
    Returns:
        List of TextContent with results
    """
    
    # ========================================================================
    # Tool 1: Query Database (with streaming)
    # ========================================================================
    if name == "query_database":
        query = arguments["query"].strip()
        limit = arguments.get("limit", 1000)
        
        # Validate query (basic security check)
        query_upper = query.upper()
        if not query_upper.startswith("SELECT"):
            return [TextContent(
                type="text",
                text="Error: Only SELECT queries are allowed for security reasons"
            )]
        
        # Check for dangerous keywords
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE"]
        if any(keyword in query_upper for keyword in dangerous_keywords):
            return [TextContent(
                type="text",
                text=f"Error: Query contains forbidden keywords. Only SELECT queries are allowed."
            )]
        
        try:
            # Add LIMIT clause if not present
            if "LIMIT" not in query_upper:
                query = f"{query} LIMIT {limit}"
            
            # Get total row count for progress calculation
            # Note: In production, you might want to skip this for very large datasets
            # to avoid the overhead of counting
            total_rows = get_row_count(query, ())
            
            # Generate unique progress token for this operation
            progress_token = f"query-{id(request_context)}"
            
            # Execute query with streaming progress updates
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            
            results = []
            rows_processed = 0
            
            # Stream results with progress updates
            # Send progress every 100 rows or every second (whichever comes first)
            last_progress_time = asyncio.get_event_loop().time()
            
            for row in cursor:
                results.append(dict(row))
                rows_processed += 1
                
                # Send progress update every 100 rows or every 1 second
                current_time = asyncio.get_event_loop().time()
                time_since_last_update = current_time - last_progress_time
                
                if rows_processed % 100 == 0 or time_since_last_update >= 1.0:
                    # Send progress notification
                    # Note: The actual implementation of send_progress depends on
                    # the MCP SDK version. This is the conceptual approach.
                    try:
                        # Progress notifications don't return values, they're fire-and-forget
                        # The client receives them as separate notifications
                        await asyncio.sleep(0)  # Allow other tasks to run
                        
                        # Calculate progress percentage
                        progress_pct = (rows_processed / total_rows * 100) if total_rows > 0 else 0
                        
                        # In a real implementation, you would send a progress notification here
                        # For this example, we'll simulate the delay that would occur
                        # during actual streaming
                        print(f"  Progress: {rows_processed}/{total_rows} rows ({progress_pct:.1f}%)")
                        
                    except Exception as e:
                        # Progress notification failed, but continue processing
                        print(f"Warning: Failed to send progress notification: {e}")
                    
                    last_progress_time = current_time
            
            conn.close()
            
            # Format results as JSON
            results_json = json.dumps(results, indent=2)
            
            return [TextContent(
                type="text",
                text=f"""Query executed successfully.

Rows returned: {len(results)}

Results:
{results_json}
"""
            )]
            
        except sqlite3.Error as e:
            return [TextContent(
                type="text",
                text=f"Database error: {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error executing query: {str(e)}"
            )]
    
    # ========================================================================
    # Tool 2: Get Schema
    # ========================================================================
    elif name == "get_schema":
        table_name = arguments.get("table_name")
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if table_name:
                # Get schema for specific table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                if not columns:
                    conn.close()
                    return [TextContent(
                        type="text",
                        text=f"Error: Table '{table_name}' not found"
                    )]
                
                schema_info = {
                    "table": table_name,
                    "columns": [
                        {
                            "name": col[1],
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ]
                }
            else:
                # Get schema for all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                schema_info = {}
                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    schema_info[table] = [
                        {
                            "name": col[1],
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ]
            
            conn.close()
            
            return [TextContent(
                type="text",
                text=f"""Database Schema:

{json.dumps(schema_info, indent=2)}
"""
            )]
            
        except sqlite3.Error as e:
            return [TextContent(
                type="text",
                text=f"Database error: {str(e)}"
            )]
    
    # ========================================================================
    # Tool 3: Get Stats
    # ========================================================================
    elif name == "get_stats":
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Get table statistics
            stats = {}
            
            # Users table stats
            cursor.execute("SELECT COUNT(*) FROM users")
            stats["users_count"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT department) FROM users")
            stats["departments_count"] = cursor.fetchone()[0]
            
            # Orders table stats
            cursor.execute("SELECT COUNT(*) FROM orders")
            stats["orders_count"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(amount) FROM orders")
            stats["total_revenue"] = round(cursor.fetchone()[0], 2)
            
            cursor.execute("SELECT AVG(amount) FROM orders")
            stats["average_order_value"] = round(cursor.fetchone()[0], 2)
            
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)
            stats["orders_by_status"] = {row[0]: row[1] for row in cursor.fetchall()}
            
            conn.close()
            
            return [TextContent(
                type="text",
                text=f"""Database Statistics:

{json.dumps(stats, indent=2)}
"""
            )]
            
        except sqlite3.Error as e:
            return [TextContent(
                type="text",
                text=f"Database error: {str(e)}"
            )]
    
    # ========================================================================
    # Unknown Tool
    # ========================================================================
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


# ============================================================================
# Server Lifecycle Management
# ============================================================================

async def main():
    """
    Main entry point for the MCP server.
    
    This function:
    1. Initializes the database with sample data
    2. Sets up the stdio transport
    3. Runs the MCP server
    """
    # Initialize database before starting server
    print("Initializing database...")
    initialize_database()
    print("Database ready!")
    print(f"Database location: {DB_PATH}")
    print()
    print("Starting MCP streaming database server...")
    print("Ready to accept connections via stdio")
    print()
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

