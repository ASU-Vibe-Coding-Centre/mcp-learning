# Tutorial: Simple Bidirectional Workflow with n8n and MCP

This tutorial guides you through building two n8n workflows:
- Workflow A: MCP Server (exposes simple tools)
- Workflow B: MCP Client (calls those tools and returns a response)

Estimated time: 30–45 minutes

## What is n8n?
n8n is a workflow automation platform for connecting apps, APIs, and custom logic into repeatable flows. It provides a visual editor with nodes for triggers (e.g., HTTP) and actions (e.g., HTTP Request, AI, MCP), so you can orchestrate data between systems without writing full applications. You can run it in the cloud or self‑host it and extend it with community nodes when you need new capabilities.

## Why Combine n8n with MCP?
- Unify AI and automation: call MCP tools/resources inside orchestrated n8n flows
- Reuse standard tools: connect to any MCP server without custom adapters
- Close the loop: expose n8n workflows as MCP tools that AI agents can invoke
- Scale safely: add retries, timeouts, and monitoring around AI tool calls

## Prerequisites
- n8n account (Cloud or self‑hosted, latest version)
- Cursor IDE configured for MCP from Module 01
- One accessible MCP server to call (e.g., free catalog option or local)
- Optional: AI node credentials (if you include an AI step)
- Optional: curl/Postman for testing HTTP endpoints

## What You’ll Build
- Workflow A: MCP Server — exposes 2–3 tools (greeting, calculator, timestamp) via an MCP Server Trigger so external clients can call them.
- Workflow B: MCP Client — receives an HTTP request, optionally parses intent with an AI node, then calls a selected tool on Workflow A via the MCP Client node and returns a JSON response.

At the end, you’ll have a working bidirectional pattern: n8n can both provide tools to AI agents and act as an AI‑powered client that calls tools.

---

## Workflow A: MCP Server

### A1. Create a new workflow
- In n8n, click "+" → Create Workflow → name it "MCP Server".
- Keep it disabled until configuration is complete.

### A2. Add MCP Server Trigger node
- Add node: search for "MCP Server Trigger" and place it as the first node.
- Transport: use the default recommended transport for your n8n version (SSE or HTTP Streamable).
- Tools: start with three tools: `greet`, `add`, `timestamp`.

### A2.1 MCP Server Trigger configuration details
- Transport
  - Start with the default recommended (often SSE or HTTP Streamable).
  - If running behind proxies/firewalls, HTTP Streamable is often more reliable than SSE.
- Tools
  - Define tool names (`greet`, `add`, `timestamp`) and attach input schemas.
  - Map each tool to the correct downstream node/branch.
- Inputs/Outputs
  - Validate required fields; provide sensible defaults where possible.
  - Ensure outputs are plain JSON objects (no binary) and small enough for logs.
- Authentication (optional)
  - Local/demo: none.
  - Protected: add a bearer token or custom headers as required by your environment.
- Timeouts & retries
  - Increase timeout if tools may take longer (e.g., external API calls).
  - Prefer at-most-once execution; log and surface errors clearly.
- Testing tips
  - Enable the workflow and try each tool from an MCP client.
  - Inspect execution logs to verify input mapping and output shape.

### A3. Define simple tools (inputs/outputs)
- greet
  - inputs: `name` (string)
  - output: `{ message: string }`
- add
  - inputs: `a` (number), `b` (number)
  - output: `{ sum: number }`
- timestamp
  - inputs: none
  - output: `{ iso: string }`

### A3.1 Tool schemas and examples

- greet
  - JSON Schema (inputs):
    ```json
    {
      "type": "object",
      "properties": {
        "name": { "type": "string", "minLength": 1 }
      },
      "required": ["name"],
      "additionalProperties": false
    }
    ```
  - Output shape:
    ```json
    { "message": "Hello, <name>!" }
    ```
  - Example input:
    ```json
    { "name": "Ada" }
    ```

- add
  - JSON Schema (inputs):
    ```json
    {
      "type": "object",
      "properties": {
        "a": { "type": "number" },
        "b": { "type": "number" }
      },
      "required": ["a", "b"],
      "additionalProperties": false
    }
    ```
  - Output shape:
    ```json
    { "sum": 5 }
    ```
  - Example input:
    ```json
    { "a": 2, "b": 3 }
    ```

- timestamp
  - JSON Schema (inputs):
    ```json
    {
      "type": "object",
      "properties": {},
      "additionalProperties": false
    }
    ```
  - Output shape:
    ```json
    { "iso": "2025-01-15T12:34:56.789Z" }
    ```
  - Example input:
    ```json
    {}
    ```

### A4. Connect supporting nodes
- For `greet`: add a Function node after the trigger that returns `{ message: `Hello, ${$json.name}!` }`.
- For `add`: add a Function node that parses `a` and `b` as numbers and returns `{ sum: a + b }`.
- For `timestamp`: add a Function node that returns `{ iso: new Date().toISOString() }`.
- Map tool selection to the corresponding Function node (use Switch/IF or separate branches as supported by your MCP Server Trigger node’s configuration UI).

### A5. Activate and test locally
- Activate the workflow.
- From an MCP client (e.g., another n8n workflow or a tool-using IDE/agent), call tool `greet` with `{ name: "Ada" }` → expect `{ message: "Hello, Ada!" }`.
- Call `add` with `{ a: 2, b: 3 }` → expect `{ sum: 5 }`.
- Call `timestamp` with no inputs → expect `{ iso: "<ISO-8601>" }`.

### A6. Export Workflow A
- Menu → Export → Download JSON.
- Save as `02-building-with-n8n/examples/workflow-a-server.json` in this repo.

---

## Workflow B: MCP Client

### B1. Create a new workflow
- In n8n, click "+" → Create Workflow → name it "MCP Client".

### B2. Add HTTP Trigger
- Add node: HTTP Trigger.
- Method: POST.
- Path: `/mcp-client` (or your choice).
- Example request body:
  ```json
  { "tool": "add", "params": { "a": 2, "b": 3 } }
  ```

### B2.1 HTTP Trigger configuration details
- Method: POST (use GET only for simple health checks)
- Path: choose a unique path, e.g. `/mcp-client`
- Response: add a terminal HTTP Response node later in the flow
- Test payload:
  ```json
  { "tool": "add", "params": { "a": 2, "b": 3 } }
  ```
- Headers:
  - Content-Type: application/json
  - Optional auth header if exposing publicly (e.g., `x-api-key`)
- Security tips:
  - Keep this workflow disabled until finished
  - Use an env var or credential for any secret keys
  - If self‑hosting, restrict exposure to your network or add a reverse proxy with auth

### B3. (Optional) Add AI node to parse intent
- If you want natural language input, insert an AI node after the trigger to parse a sentence into `{ tool, params }`.
- Keep it simple for the first run; you can add this later.

### B3.1 AI node configuration (optional)
- Goal: turn natural language like "add 2 and 3" into `{ tool: "add", params: { a: 2, b: 3 } }`.
- Model/Provider: choose any supported provider you have credentials for.
- System prompt (concise):
  "You extract a tool name and JSON params from a short request. Tools: greet(name), add(a,b), timestamp(). Respond ONLY with JSON: { \"tool\": string, \"params\": object }."
- User prompt template:
  "Request: {{$json.text}}"
- Output mapping:
  - Parse the model output as JSON.
  - Ensure `tool` is one of: `greet`, `add`, `timestamp`.
  - Coerce numeric strings to numbers when needed (e.g., `"2"` → `2`).
- Fallbacks:
  - If parsing fails, default to `timestamp` with `{}` and include a warning field downstream.

### B4. Add MCP Client node
- Add node: MCP Client.
- Connection: point to your Workflow A (MCP Server) endpoint/transport per your setup.
- Tool name: from incoming body (`$json.tool`).
- Tool params: pass through (`$json.params`).

### B4.1 MCP Client configuration details
- Connection
  - Point to Workflow A’s MCP Server Trigger (same host/transport you enabled there).
  - Transport: match Server’s transport (SSE or HTTP Streamable). If unsure, use the same one you tested in A5.
- Authentication (if required)
  - Local/demo: none
  - Protected: bearer token or custom headers; store in n8n credentials/env vars
- Tool selection
  - Tool name: `$json.tool` from the HTTP Trigger (or AI output)
  - Params: `$json.params`
  - Validate tool name is one of: `greet`, `add`, `timestamp`
- Timeouts & retries
  - Set a reasonable timeout (e.g., 30–60s) if tools may call external APIs
  - Enable limited retries for transient network failures
- Error handling
  - On tool failure, return `{ ok: false, error: $json.message }` with HTTP 400/500
  - Log the full error for debugging; avoid exposing secrets in responses
- Testing
  - Send the sample POST body from B2 to verify each tool end-to-end
  - Check that outputs match the schemas defined in A3.1

### B5.1 Formatting and returning the response
- Use a Set or Function node to produce a stable shape:
  ```json
  { "ok": true, "tool": $json.tool, "result": $json }
  ```
- Add an HTTP Response node:
  - Status: 200 when success; 400/500 on error
  - Body: previous node’s output
- Error path:
  - If MCP call fails, format as `{ "ok": false, "error": $json.message }` and set HTTP status accordingly

### B6. Add HTTP Response
- Add node: Respond to Webhook/HTTP Response.
- Status: 200.
- Body: output from previous node.

### B7. Activate and export Workflow B
- Activate and test with curl/Postman:
  ```bash
  curl -X POST http://localhost:5678/webhook/mcp-client \
    -H 'Content-Type: application/json' \
    -d '{"tool":"add","params":{"a":2,"b":3}}'
  ```
- Menu → Export → Download JSON.
- Save as `02-building-with-n8n/examples/workflow-b-client.json` in this repo.

---

## Testing Your Workflows

With both workflows active, send HTTP requests to Workflow B’s trigger (adjust host/port/path as needed).

- greet
  - Request:
    ```bash
    curl -s -X POST http://localhost:5678/webhook/mcp-client \
      -H 'Content-Type: application/json' \
      -d '{"tool":"greet","params":{"name":"Ada"}}'
    ```
  - Expected response (shape):
    ```json
    { "ok": true, "tool": "greet", "result": { "message": "Hello, Ada!" } }
    ```

- add
  - Request:
    ```bash
    curl -s -X POST http://localhost:5678/webhook/mcp-client \
      -H 'Content-Type: application/json' \
      -d '{"tool":"add","params":{"a":2,"b":3}}'
    ```
  - Expected response (shape):
    ```json
    { "ok": true, "tool": "add", "result": { "sum": 5 } }
    ```

- timestamp
  - Request:
    ```bash
    curl -s -X POST http://localhost:5678/webhook/mcp-client \
      -H 'Content-Type: application/json' \
      -d '{"tool":"timestamp","params":{}}'
    ```
  - Expected response (shape):
    ```json
    { "ok": true, "tool": "timestamp", "result": { "iso": "<ISO-8601>" } }
    ```

If you receive errors, check execution logs in both workflows and confirm transport/auth match.

## Understanding the Bidirectional Pattern

You built two halves that work both ways:
- Server side (Workflow A): n8n exposes MCP tools that external AI agents/clients can call.
- Client side (Workflow B): n8n acts as an MCP client, calling those tools when an HTTP request arrives.

Simple flow:
1) HTTP request hits Workflow B →
2) (Optional) AI node turns text into `{ tool, params }` →
3) MCP Client calls Workflow A’s tool →
4) Workflow A runs logic and returns JSON →
5) Workflow B formats and responds to the caller.

This pattern lets you insert n8n into both ends of AI‑powered automation: providing tools to models and orchestrating tool calls from external inputs.

## Troubleshooting
- Connection issues between workflows
- Node configuration mistakes
- Testing and debugging tips

## What You Just Built

- An MCP Server in n8n (Workflow A) that exposes three simple tools with schemas
- An MCP Client in n8n (Workflow B) that receives HTTP, optionally uses AI to parse intent, calls a tool, and responds
- A bidirectional pattern you can reuse: n8n can both provide tools to AI agents and orchestrate tool usage from external requests

You now know how to:
- Configure MCP Server Trigger and MCP Client nodes (transport, auth, mapping)
- Define JSON schemas for tools and validate inputs/outputs
- Test end‑to‑end with curl and format API responses consistently

## What’s Next?
Ready to containerize your own MCP server? Continue to Module 03: Building with Docker. You’ll start with catalog images, then build a simple custom server, and finally a practical server with persistence. This is where you’ll package and ship what you built so others (and your future self) can use it anywhere.

## Using Cursor IDE with Workflow A (n8n MCP Server)

You can have Cursor act as an MCP client to your n8n server.

1) In n8n
- Ensure Workflow A (MCP Server Trigger) is enabled
- Note the server endpoint/transport (SSE or HTTP Streamable)
- If protected, prepare a bearer token or custom header

2) In Cursor MCP settings (JSON)
Add an entry pointing to your n8n endpoint. Example (SSE):
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "transport": "sse",
      "url": "https://your-n8n.example.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_IF_USED"
      }
    }
  }
}
```
Notes:
- If SSE is blocked by a proxy/firewall, try HTTP streamable if your Cursor build supports it
- Keep secrets in env/secure storage; avoid hardcoding in shared configs

3) Test from Cursor
- Restart Cursor to reload MCP servers
- Open the MCP tool list and find: `greet`, `add`, `timestamp`
- Run a tool, e.g. `add` with `{ "a": 2, "b": 3 }`, and verify the result

## Troubleshooting: Connection issues between workflows
- Tools not visible in client
  - Cause: Workflow A not enabled or transport mismatch
  - Fix: Enable Workflow A; ensure both sides use the same transport (SSE or HTTP streamable)
- 4xx/5xx from MCP Client node
  - Cause: wrong URL/headers or auth missing
  - Fix: verify endpoint, add bearer/custom headers, and test locally first
- Timeouts when calling tools
  - Cause: long-running steps or network latency
  - Fix: increase timeout/retries in MCP Client; optimize tool logic
- CORS/proxy interference
  - Cause: proxy drops SSE or modifies headers
  - Fix: prefer HTTP streamable or adjust proxy to allow SSE and required headers
- Inconsistent payloads
  - Cause: schema mismatch (e.g., numbers as strings)
  - Fix: coerce types in Set/Function nodes; validate against schemas in A3.1

## Troubleshooting: Common n8n configuration mistakes
- Workflow not executing
  - Mistake: workflow left disabled
  - Fix: enable the workflow and re-test
- Wrong node order
  - Mistake: HTTP Response before MCP Client/formatting nodes
  - Fix: ensure HTTP Response is the final node on each path
- Mixed transports
  - Mistake: Server Trigger uses SSE but Client expects HTTP streamable (or vice versa)
  - Fix: align transports; test the same URL manually
- Credentials not loaded
  - Mistake: missing env/credential reference in headers
  - Fix: store tokens in Credentials and reference them in node config
- JSON shape mismatches
  - Mistake: expecting `{ a, b }` but sending strings or different keys
  - Fix: validate with schemas from A3.1 and coerce types
- Exported JSON not updated
  - Mistake: examples directory contains old placeholder exports
  - Fix: re-export each workflow after changes and replace the files in `examples/`

## Troubleshooting: Testing and debugging tips
- Test nodes individually
  - Use "Execute Node" to verify inputs/outputs at each step
- Add temporary Set/Function nodes
  - Log `$json` at key points to confirm shapes
- Check Execution List
  - Re-run past executions and inspect data; compare success vs failure runs
- Use curl/Postman collections
  - Save requests for greet/add/timestamp; vary edge cases (missing fields, strings vs numbers)
- Timeouts and retries
  - Start with longer timeouts during development; reduce later
- Version drift
  - If something breaks unexpectedly, re-export/import workflows to ensure local JSON matches
- Network isolation
  - If remote URLs fail, replicate locally (same machine) to isolate network/proxy issues

## Testing in n8n Cloud
- Import both workflows
  - In n8n Cloud, create two workflows and import the JSON exports from `examples/`
- Configure credentials
  - Set any AI/API credentials used by nodes; add headers/tokens for MCP if required
- Enable and run
  - Enable Workflow A (Server) first, then Workflow B (Client)
  - Send the curl requests from the Testing section and verify responses
- Monitor
  - Use the Execution List to confirm successful runs and inspect any failures
- Adjust
  - If SSE is blocked, switch to HTTP streamable (if available) or test from local n8n
