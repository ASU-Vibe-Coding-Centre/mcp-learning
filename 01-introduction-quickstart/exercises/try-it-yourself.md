## Try It Yourself — Mini Exercises (≈10–15 minutes)

Use your connected MCP server to complete a few quick tasks. Keep it simple and focus on seeing structured requests and responses end‑to‑end.

### Prompts to Try
1) "List all available tools from the connected server."
2) "Use the weather tool to get the current temperature for London."
3) "List available resources and read `server_info` (if available)."

### Expected Behavior
- For listing tools: You see tool names with brief descriptions and input schemas.
- For the weather tool: You receive structured output (e.g., temperature, units, summary).
- For resources and `server_info`: You see available resource IDs and a small JSON/text payload when reading `server_info`.

### What You Learned
- How to discover server capabilities (tools/resources) in your IDE
- How to invoke a tool with structured inputs and read structured outputs
- How to list and read resources exposed by an MCP server
- How to troubleshoot common connection and command issues

### What’s Next?
Proceed to Module 02 — Building with n8n. You’ll:
- Create a tiny MCP server workflow
- Call it from a client workflow
- See the bidirectional pattern in action


