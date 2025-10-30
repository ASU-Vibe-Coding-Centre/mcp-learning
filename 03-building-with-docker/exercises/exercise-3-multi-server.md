## Exercise 3 (Optional, Medium): Run Multiple Servers

Goal: Run both the simple and practical servers side-by-side and connect from Cursor.

Requirements:
- Start simple server container (`simple-mcp-server`)
- Start practical server container (`practical-mcp-server`) with volume
- Configure Cursor to talk to both servers

Hints:
- Use distinct container names
- Keep stdio vs HTTP transport considerations in mind; for stdio, run locally via MCP Inspector
- For two HTTP servers, map different host ports (if you later add HTTP transport)

Expected outcome:
- You can call tools from each server in the same Cursor session


