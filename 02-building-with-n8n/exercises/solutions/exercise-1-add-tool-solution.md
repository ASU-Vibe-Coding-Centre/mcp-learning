# Solution: Exercise 1 — Add Another MCP Tool (reverse)

## Workflow A changes
- Tool name: `reverse`
- Input schema: `{ text: string }`
- Function node code (pseudo):
  - Input: `$json.text`
  - Output: `{ reversed: $json.text.split('').reverse().join('') }`
- Map MCP Server Trigger tool `reverse` → this Function node

## Workflow B test
- Request:
```json
{ "tool": "reverse", "params": { "text": "hello" } }
```
- Expected response shape:
```json
{ "ok": true, "tool": "reverse", "result": { "reversed": "olleh" } }
```

Notes
- Trim input if needed: `$json.text.trim()`
- Keep schema strict: `required: ["text"], additionalProperties: false`
