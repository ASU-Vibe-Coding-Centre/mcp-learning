# Exercise 3 (Optional, Medium): Add Error Handling

Goal: Improve resilience by handling invalid inputs, timeouts, and downstream failures.

## Tasks
- In Workflow B, handle MCP Client errors and return `{ ok: false, error }` with proper HTTP status
- Validate inputs before calling tools; reject bad schemas with a clear message
- Add retries/timeouts where appropriate

## Steps
1) Input validation
   - Add a Function node after HTTP Trigger to validate `tool` and `params`
   - If invalid, branch to HTTP Response with 400 and `{ ok: false, error: "invalid input" }`
2) MCP Client error path
   - On error output, format `{ ok: false, error: $json.message }` and return 502/500
3) Timeouts & retries
   - Set MCP Client timeout (e.g., 30s) and 1–2 retries for transient errors
4) Logging
   - Add a Set node to include a short `traceId` in responses and logs

## Verify
- Missing field
  - Request: `{ "tool": "add", "params": { "a": 2 } }`
  - Expect: HTTP 400 with `{ ok: false, error: "invalid input" }`
- Bad tool name
  - Request: `{ "tool": "sumz", "params": { "a": 1, "b": 2 } }`
  - Expect: HTTP 400 with `{ ok: false, error: "unknown tool" }`
- Simulated failure
  - Temporarily throw an error in a Function node inside Workflow A
  - Expect: HTTP 502/500 with `{ ok: false, error: "..." }`

## Hints
- Use IF/Switch nodes or a Function node to route success vs error paths
- Never leak secrets in error messages; prefer generic text for clients
- Keep error shapes consistent for easy client handling
