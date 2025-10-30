# Solution: Exercise 3 — Error Handling

## Validation
- Function node after HTTP Trigger:
  - Check `tool` in { greet, add, timestamp, reverse? }
  - Validate required params per tool schema
  - If invalid → set `{ ok: false, error: "invalid input" }` and return HTTP 400

## MCP Client error path
- On error branch from MCP Client:
  - Body: `{ ok: false, error: $json.message }`
  - HTTP status: 502/500

## Timeouts & retries
- MCP Client timeout: 30s
- Retries: 1 (transient errors only)

## Logging
- Add `traceId` via Set → include in logs and responses

## Tests
- Missing `b` in add → 400
- Unknown tool → 400
- Forced error in Workflow A → 502/500
