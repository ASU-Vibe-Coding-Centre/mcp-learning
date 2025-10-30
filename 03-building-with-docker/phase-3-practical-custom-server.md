## Phase 3: Build a Practical MCP Server with Persistence

In this phase you will create a practical MCP server (recommended: notes) with persistent storage, multiple tools, and a Dockerized runtime.

### Time Estimate
60–90 minutes

### Prerequisites
- Completed Phase 2
- Docker installed and running
- Basic Python and SQLite/file I/O knowledge

### What You’ll Build
You’ll build a practical "Notes" MCP server with persistent storage and five tools:

- create_note(title: string, content: string) → { id: integer }
  - Creates a note and returns its numeric ID
- get_note(id: integer) → { id: integer, title: string, content: string, created_at: string, updated_at: string }
  - Fetches a single note by ID
- list_notes() → Array<note>
  - Returns all notes sorted by `updated_at` desc
- update_note(id: integer, title?: string, content?: string) → note
  - Updates fields provided and returns the updated note
- delete_note(id: integer) → { success: boolean }
  - Deletes a note by ID and reports success

Data will be persisted to a simple SQLite database (recommended) or file-based JSON store.

### Server Type Decision
Chosen domain: Notes server with SQLite persistence.

### Project Layout
- `examples/practical-server/` (to be implemented)
  - `server.py` – server with CRUD tools and persistence
  - `Dockerfile` – container image for the practical server
  - `requirements.txt` – Python deps (MCP SDK + sqlite helpers if needed)

### Implementation Steps (Overview)
1) Choose persistence: SQLite (recommended) or JSON file store
2) Define JSON Schemas for CRUD tools with clear validation
3) Implement data access layer (DAL) with small functions for DB ops
4) Register tools and wire DAL into tool handlers
5) Add logging and error handling for common scenarios

### Docker Build/Run
Once implemented:

```bash
cd examples/practical-server/
docker build -t practical-mcp-server:latest .
docker run --rm -v "$PWD/data":/app/data \
  --name practical-mcp practical-mcp-server:latest
```

Mounting a volume ensures your notes persist between runs.

#### Building the Docker Image (Step-by-Step)
1) Ensure files exist in `examples/practical-server/`:
   - `server.py`, `Dockerfile`, `requirements.txt`
2) Build the image:
```bash
docker build -t practical-mcp-server:latest .
```
3) Verify the image:
```bash
docker images | grep practical-mcp-server
```
4) Optional: Force a clean rebuild if deps changed:
```bash
docker build --no-cache -t practical-mcp-server:latest .
```

### Running Your Server (with Volume Mounts)
Run the container and mount a host directory so your SQLite DB persists:

```bash
cd examples/practical-server/
mkdir -p data
docker run --rm \
  -v "$PWD/data":/app/data \
  --name practical-mcp \
  practical-mcp-server:latest
```

Notes:
- The bind mount maps `./data` on your host to `/app/data` in the container.
- Ensure the host directory is writable by Docker (check Docker Desktop file sharing on macOS/Windows).

### Testing from Cursor IDE
Add to your MCP config, then try flows like:
- "Create a note titled 'Shopping' with content 'Eggs, Milk'"
- "List my notes"
- "Show note 1"
- "Update note 1 title to 'Groceries'"
- "Delete note 1"

#### Example Prompts and Expected Responses
- Prompt: "Create a note titled 'Shopping' with content 'Eggs, Milk'"
  - Expected: `{ "id": <number> }`
- Prompt: "List my notes"
  - Expected: `[{ id, title, content, created_at, updated_at }, ...]` (JSON-like)
- Prompt: "Show note <id>"
  - Expected: `{ id, title, content, created_at, updated_at }`
- Prompt: "Update note <id> content to 'Eggs, Milk, Bread'"
  - Expected: updated note object with new content and newer `updated_at`
- Prompt: "Delete note <id>"
  - Expected: `{ "success": true }`

### Troubleshooting
- DB locked/file permission errors: ensure volume is writable to the container user
- Schema errors: verify input types/required fields in tool definitions
- Unexpected exceptions: check server logs and validate IDs exist before updates/deletes

### What You’ll Learn
- Designing multi-tool servers with persistence
- Validating and handling CRUD edge cases
- Containerizing stateful MCP servers with bind mounts/volumes

### Understanding the Code (Key Differences from Phase 2)
Open `examples/practical-server/server.py` and compare with the simple server:

1) Persistence layer
- SQLite database at `./data/notes.db` created via `_ensure_db()`
- Context-managed `_db_cursor()` handles open/commit/close; ensures the table exists

2) Data model
- `Note` dataclass represents rows; `_row_to_note()` converts SQLite tuples into typed objects

3) CRUD operations
- Separate pure functions: `create_note`, `get_note`, `list_notes`, `update_note`, `delete_note`
- Each validates inputs and raises `ValueError` for clear client feedback

4) Tool surface and schemas
- `list_tools()` advertises five tools with explicit JSON Schemas and required fields
- Input validation aligns with schema constraints (e.g., positive `id`)

5) Response formatting
- Minimal `_as_json_text()` formats Python objects to JSON-like strings for `TextContent`
- In production, prefer `json.dumps` for robust JSON output

6) Containerization for state
- `Dockerfile` creates `/app/data` and declares a `VOLUME` for persistence
- Run with a bind mount so data survives container restarts

### What You Just Built
- A practical MCP stdio server with five CRUD tools for notes
- SQLite-backed persistence with a simple, testable data access layer
- Containerized runtime with a bind-mounted data directory for durability

Key concepts learned:
- Modeling real-world workflows as MCP tools with clear JSON Schemas
- Validating inputs and returning structured outputs the client can reason about
- Managing persistent state in containers using volumes and predictable paths

### References and Further Reading
- NetworkChuck’s Docker + MCP tutorial repository: [NetworkChuck Docker MCP Tutorial](https://github.com/theNetworkChuck/docker-mcp-tutorial)
- Docker MCP Catalog and Toolkit docs: [Docker MCP Docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- MCP Python SDK: [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### How This Differs/Complements NetworkChuck’s Tutorial
- Scope: NetworkChuck demonstrates a fun dice-roller; this module extends the idea to a CRUD notes server with persistence.
- Depth: We emphasize schemas, validation, and state management patterns suitable for real projects.
- Structure: The module follows a phased learning path (catalog → simple → practical) to build confidence progressively.

### Troubleshooting (Comprehensive)
Build failures
- Symptom: `pip install` errors or image build stops
  - Fix: Check `requirements.txt` versions, ensure internet access, try `--no-cache` rebuild
- Symptom: Permission denied when copying files
  - Fix: Ensure files exist and Dockerfile `COPY` paths match working directory

Container connection issues
- Symptom: Client cannot reach server
  - Fix: For stdio servers, ensure you run via MCP Inspector or client config that supports stdio. If you switch to HTTP later, expose and map ports correctly.
- Symptom: Data not persisting
  - Fix: Verify `-v "$PWD/data":/app/data` bind mount exists and is writable

Common Python/MCP errors
- Symptom: `ValueError: id must be a positive integer`
  - Fix: Provide valid input per JSON Schema; ensure tool prompts include required fields
- Symptom: Unknown tool
  - Fix: Reload client, verify `list_tools()` shows expected names

Testing and debugging tips
- Check container logs: `docker logs practical-mcp`
- Run server locally for faster iteration: `python server.py` with MCP Inspector
- Add print/log statements temporarily to narrow down issues, then remove


