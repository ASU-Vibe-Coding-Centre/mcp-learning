## Phase 1: Running Catalog MCP Servers with Docker

In this phase you will run pre-built containerized MCP servers from the Docker MCP catalog and connect them to your MCP client (Cursor IDE). This is the fastest way to get productive with MCP servers without writing any code.

### Prerequisites
- Docker Desktop (macOS/Windows) or Docker Engine (Linux) installed and running
- Cursor IDE configured from Module 01

If you need Docker setup instructions, see `docker/README.md` in this repository.

### What You’ll Do
1. Browse the Docker MCP catalog to find a server
2. Pull the image locally
3. Run the container
4. Connect from Cursor IDE and test a few prompts

### 1) Browsing the Docker MCP Catalog
The catalog contains official and community MCP servers packaged as Docker images. Look for simple, stateless servers to start (e.g., filesystem viewer, time utilities, or calculator).

- Recommended first picks: a read-only filesystem server or a time utilities server
- Note the image name and any environment variables or volumes required

### 2) Pulling a Catalog Server Image
Use `docker pull` with the image name from the catalog. Example:

```bash
docker pull example/mcp-filesystem:latest
```

Tip: If you’re on a slower connection, pulls may take a few minutes the first time.

### 3) Running the Server
Start the container with `docker run`. Most MCP servers expose a local HTTP port. Replace paths/ports as needed for your chosen image.

Example (filesystem server with a read-only mount):

```bash
docker run --rm \
  -p 3333:3333 \
  -v "$HOME/Documents":/data:ro \
  --name mcp-filesystem \
  example/mcp-filesystem:latest
```

Notes:
- `-p 3333:3333` publishes the server’s port to your host
- `-v …:/data:ro` mounts a host directory inside the container (read-only)
- `--rm` cleans up the container when it exits

Keep this terminal running while you test from Cursor.

### 4) Connecting from Cursor IDE
Add an MCP server entry in your Cursor MCP configuration, pointing to the container’s host/port. If following Module 01, you’ll edit your Cursor MCP config to include something like:

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "http",
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

Restart Cursor (or reload MCP) so it picks up the new server. You should now see the server available under MCP tools/resources in Cursor.

### 5) Testing in Cursor
Try a few prompts depending on the server’s capabilities:
- List directory contents (resources)
- Read a file
- Call a simple tool (e.g., get current time)

You should see successful responses coming from the containerized MCP server.

### Troubleshooting
If something doesn’t work, check the following common issues:

- Port already in use
  - Symptom: `Error starting userland proxy: listen tcp 0.0.0.0:3333: bind: address already in use`
  - Fix: Use a different host port (e.g., `-p 3334:3333`) and update Cursor config

- Container can’t access files
  - Symptom: Permission denied or missing files
  - Fix: Use absolute paths for volume mounts; on macOS/Windows ensure Docker Desktop has file sharing permission for the folder

- Cursor can’t connect to server
  - Symptom: Timeouts or connection refused
  - Fix: Verify container logs, confirm port mapping, ensure `url` in Cursor config is correct (`http://localhost:<hostPort>/mcp` for Streamable HTTP transport)

- Image not found
  - Symptom: `pull access denied` or `manifest unknown`
  - Fix: Double-check image name/tag; ensure you’re pulling from the correct registry and that the image is public

- Server crashes on start
  - Symptom: Container exits immediately
  - Fix: Run with `--name` then inspect logs via `docker logs <name>`; check required environment variables or version compatibility

### Next: Phase 2
When you’re comfortable running a catalog server and connecting from Cursor, continue to Phase 2 to build a simple custom server: `phase-2-simple-custom-server.md`.


