# Exercise 1 (Optional, Easy): Add Another MCP Tool

Goal: Add a new tool to Workflow A (MCP Server) and call it from Workflow B.

## Task
- Create a tool named `reverse`
  - Input schema: `{ text: string }`
  - Output: `{ reversed: string }`
- Wire it in Workflow A and expose it via the MCP Server Trigger
- Call it from Workflow B by sending `{ "tool": "reverse", "params": { "text": "hello" } }`

## Steps
1) In Workflow A
   - Define tool `reverse` (schema and mapping)
   - Add a Function node:
     - Input: `$json.text`
     - Output: `{ reversed: $json.text.split('').reverse().join('') }`
   - Map tool name `reverse` to this Function node
2) In Workflow B
   - Send a POST to your HTTP Trigger with the new tool and params
   - Confirm MCP Client routes to the new tool
3) Test
   - Expect `{ ok: true, tool: "reverse", result: { reversed: "olleh" } }`

## Hints
- Copy the pattern from `greet`/`timestamp` for tools without complex validation
- If strings arrive with extra whitespace, trim before reversing
- If you get a 4xx, check the tool name and schema keys

## Stretch Ideas
- Add an optional `uppercase` boolean to transform the output
- Add basic validation for max input length
