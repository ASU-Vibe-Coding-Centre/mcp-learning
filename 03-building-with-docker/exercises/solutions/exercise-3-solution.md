## Solution: Exercise 3 (Run Multiple Servers)

Run simple server (stdio inside container runs python):
```bash
docker run --rm --name simple-mcp simple-mcp-server:latest
```

Run practical server with volume:
```bash
cd examples/practical-server && mkdir -p data
docker run --rm -v "$PWD/data":/app/data --name practical-mcp practical-mcp-server:latest
```

Configure Cursor to talk to both servers per your MCP config.


