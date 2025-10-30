"""
Practical MCP Server: Notes with SQLite Persistence (HTTP Version)

Tools:
- create_note(title: str, content: str) -> id
- get_note(id: int) -> note
- list_notes() -> list[note]
- update_note(id: int, title?: str, content?: str) -> note
- delete_note(id: int) -> success

Notes are stored in SQLite at ./data/notes.db (relative to working directory).

This server uses Streamable HTTP transport via FastAPI. Compare with server.py to see the
difference between stdio and HTTP transports.

FastAPI provides a cleaner, simpler implementation compared to manual ASGI code.
"""

import asyncio
import os
import sqlite3
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator, Optional

from fastapi import FastAPI
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool, TextContent
import uvicorn


DATA_DIR = os.path.join(os.getcwd(), "data")
DB_PATH = os.path.join(DATA_DIR, "notes.db")


@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str


def _utc_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _ensure_db() -> None:
    """Create the data directory and notes table if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def _db_cursor() -> Iterator[sqlite3.Cursor]:
    """Yield a SQLite cursor with auto-commit and ensure DB is initialized."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()


def _row_to_note(row: tuple[Any, ...]) -> Note:
    """Convert a SQLite row into a Note dataclass instance."""
    return Note(
        id=row[0],
        title=row[1],
        content=row[2],
        created_at=row[3],
        updated_at=row[4],
    )


def create_note(title: str, content: str) -> int:
    """Insert a new note and return its id."""
    if not title or not isinstance(title, str):
        raise ValueError("title must be a non-empty string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")

    now = _utc_iso()
    with _db_cursor() as cur:
        cur.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now),
        )
        return int(cur.lastrowid)


def get_note(note_id: int) -> Note:
    """Fetch a single note by id or raise if not found."""
    with _db_cursor() as cur:
        cur.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Note {note_id} not found")
        return _row_to_note(row)


def list_notes() -> list[Note]:
    """Return all notes sorted by most recently updated first."""
    with _db_cursor() as cur:
        cur.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY datetime(updated_at) DESC, id DESC"
        )
        rows = cur.fetchall()
        return [_row_to_note(row) for row in rows]


def update_note(note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Note:
    """Update a note's title and/or content and return the updated record."""
    if title is None and content is None:
        raise ValueError("At least one of title or content must be provided")

    with _db_cursor() as cur:
        # Ensure the note exists first
        cur.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
        if cur.fetchone() is None:
            raise ValueError(f"Note {note_id} not found")

        fields = []
        params: list[Any] = []
        if title is not None:
            if not isinstance(title, str) or title == "":
                raise ValueError("title must be a non-empty string if provided")
            fields.append("title = ?")
            params.append(title)
        if content is not None:
            if not isinstance(content, str):
                raise ValueError("content must be a string if provided")
            fields.append("content = ?")
            params.append(content)
        fields.append("updated_at = ?")
        params.append(_utc_iso())
        params.append(note_id)

        cur.execute(f"UPDATE notes SET {', '.join(fields)} WHERE id = ?", params)

        # Return the updated note
        cur.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cur.fetchone()
        assert row is not None
        return _row_to_note(row)


def delete_note(note_id: int) -> bool:
    """Delete a note; return True if a row was removed."""
    with _db_cursor() as cur:
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        return cur.rowcount > 0


# Create the MCP server instance for the practical notes server
app = Server("notes-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Advertise CRUD tools with JSON Schemas for client discovery."""
    return [
        Tool(
            name="create_note",
            description="Create a note with a title and content; returns the new id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Note title"},
                    "content": {"type": "string", "description": "Note content"},
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="get_note",
            description="Get a single note by id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1, "description": "Note id"}
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="list_notes",
            description="List all notes (most recent first).",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="update_note",
            description="Update a note's title and/or content and return the updated note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="delete_note",
            description="Delete a note by id; returns success true/false.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1, "description": "Note id"}
                },
                "required": ["id"],
            },
        ),
    ]


def _as_json_text(obj: Any) -> str:
    """Very small JSON text formatter for human-readable TextContent.

    For production code, prefer `json.dumps` with `ensure_ascii=False`.
    """
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return f'"{obj.replace("\\", "\\\\").replace("\"", "\\\"")}"'
    if isinstance(obj, dict):
        return "{" + ", ".join(f"{_as_json_text(k)}: {_as_json_text(v)}" for k, v in obj.items()) + "}"
    if isinstance(obj, list):
        return "[" + ", ".join(_as_json_text(v) for v in obj) + "]"
    if isinstance(obj, Note):
        return _as_json_text(
            {
                "id": obj.id,
                "title": obj.title,
                "content": obj.content,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at,
            }
        )
    raise TypeError("Unsupported type for JSON text conversion")


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch CRUD tool calls and return TextContent payloads as JSON strings."""
    if name == "create_note":
        new_id = create_note(arguments.get("title"), arguments.get("content"))
        return [TextContent(type="text", text=_as_json_text({"id": new_id}))]

    if name == "get_note":
        note_id = arguments.get("id")
        if not isinstance(note_id, int) or note_id < 1:
            raise ValueError("id must be a positive integer")
        note = get_note(note_id)
        return [TextContent(type="text", text=_as_json_text(note))]

    if name == "list_notes":
        notes = list_notes()
        return [TextContent(type="text", text=_as_json_text(notes))]

    if name == "update_note":
        note_id = arguments.get("id")
        if not isinstance(note_id, int) or note_id < 1:
            raise ValueError("id must be a positive integer")
        updated = update_note(note_id, arguments.get("title"), arguments.get("content"))
        return [TextContent(type="text", text=_as_json_text(updated))]

    if name == "delete_note":
        note_id = arguments.get("id")
        if not isinstance(note_id, int) or note_id < 1:
            raise ValueError("id must be a positive integer")
        ok = delete_note(note_id)
        return [TextContent(type="text", text=_as_json_text({"success": ok}))]

    raise ValueError(f"Unknown tool: {name}")


# Create the Streamable HTTP session manager
session_manager = StreamableHTTPSessionManager(app)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manage MCP session manager lifecycle with FastAPI.
    
    This lifespan context manager handles startup and shutdown of the MCP session manager.
    FastAPI calls this automatically when the application starts and stops.
    
    Startup: Starts the session manager background tasks
    Shutdown: Automatically cleans up when the app stops
    """
    # Startup: start the session manager
    async with session_manager.run():
        yield  # App runs here
    # Shutdown: cleanup happens automatically


# Create FastAPI app with lifespan events
# FastAPI handles HTTP routing, error handling, and lifespan management automatically
fastapi_app = FastAPI(lifespan=lifespan)


# Create ASGI app wrapper for MCP session manager
# This wrapper allows us to mount the MCP session manager at /mcp
class MCPASGIApp:
    """ASGI application wrapper for the MCP session manager.
    
    This class wraps the session manager's handle_request method as an ASGI application
    so it can be mounted in FastAPI. It delegates all HTTP requests to the session manager.
    """
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    async def __call__(self, scope, receive, send):
        """Handle ASGI requests by delegating to the session manager."""
        if scope["type"] == "http":
            await self.session_manager.handle_request(scope, receive, send)


# Mount the MCP ASGI app at /mcp
# FastAPI can mount other ASGI applications as sub-applications
# This routes all requests to /mcp/* to the MCP session manager
fastapi_app.mount("/mcp", MCPASGIApp(session_manager))


async def main() -> None:
    """Run the MCP server using FastAPI and uvicorn.
    
    This server uses FastAPI with Streamable HTTP transport, which provides a simpler,
    more efficient bidirectional communication over HTTP compared to the legacy SSE transport.
    
    Advantages of FastAPI over manual ASGI:
    - Cleaner code (~30 lines vs ~60 lines)
    - Built-in lifespan management
    - Automatic routing and error handling
    - Easy to extend with additional routes or middleware
    """
    port = int(os.getenv("PORT", "3333"))
    host = os.getenv("HOST", "0.0.0.0")
    
    # FastAPI is already an ASGI app, so we can use it directly with uvicorn
    config = uvicorn.Config(
        app=fastapi_app,
        host=host,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

