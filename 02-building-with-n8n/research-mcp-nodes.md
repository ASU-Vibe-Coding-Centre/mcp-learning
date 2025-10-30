# Research: n8n MCP Nodes (Capabilities & Configuration)

This note summarizes current MCP node options in n8n to inform the Module 02 tutorial.

## Nodes
- MCP Client (tool) node
  - Purpose: Call tools, prompts, and resources exposed by external MCP servers from an n8n workflow.
  - Typical uses: Execute a tool with parameters, fetch a prompt template, read a resource.
- MCP Server Trigger node
  - Purpose: Expose an n8n workflow as an MCP server entry point so external MCP clients can call into it.
  - Typical uses: Provide simple tools (e.g., greeting, calculator, timestamp) backed by n8n nodes.

## Transports supported (varies by implementation)
- STDIO (common for local processes)
- HTTP Streamable (bidirectional over HTTP) - **Recommended**
- Server-Sent Events (SSE) - Legacy, being deprecated

## Common configuration options
- Server connection
  - Base URL / Endpoint
  - Transport selection (STDIO, HTTP streamable, SSE - legacy)
  - Timeouts / retry behavior
- Tools selection
  - Choose which tools to expose (Server) or which to call (Client)
  - Tool parameters schema mapping
- Authentication
  - None (local)
  - Bearer token header
  - Custom header(s)
- Data handling
  - Input mapping from previous nodes
  - Output selection/formatting for downstream nodes
  - Error propagation strategy (fail workflow vs. continue)

## Practical notes for our tutorial
- We will keep to simple, unauthenticated local/HTTP setups to minimize friction.
- For the Server side, expose 2–3 simple tools with clear, typed inputs/outputs.
- For the Client side, demonstrate executing a tool with parameters and handling the response.
- Clearly document where to place credentials if needed and how to switch transports.

## Limitations and caveats
- Community node versions and capabilities can change; pin versions in examples.
- Network/firewall settings may block HTTP transport; provide local-first alternatives.
- Long‑running tool execution may require increased timeouts and retry logic.

## References
- n8n documentation for MCP Client/Server nodes
- Community package pages for MCP nodes
- Example tutorials and videos demonstrating setup and usage
