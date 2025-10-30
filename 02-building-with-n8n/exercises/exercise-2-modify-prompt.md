# Exercise 2 (Optional, Easy): Modify the AI Prompt/Behavior

Goal: Change how the AI node parses natural language into `{ tool, params }`.

## Task
- Update the AI node prompt so it:
  - Accepts phrases like "what time is it?" and maps to `timestamp`
  - Interprets "sum X and Y" as `add` with numeric params
  - Recognizes greetings like "say hi to Ada" as `greet` with `name: "Ada"`
- Ensure the AI output is valid JSON: `{ "tool": string, "params": object }`

## Steps
1) Open Workflow B and locate the AI node (B3)
2) Edit the system prompt to include examples and constraints (JSON-only output)
3) Adjust the user prompt template if needed (e.g., pass `$json.text`)
4) Add a Function/Set node to coerce numeric strings to numbers
5) Validate `tool` is one of `greet`, `add`, `timestamp`; fallback to `timestamp` if unknown

## Example System Prompt
"You extract a tool name and JSON params from a short request. Tools: greet(name), add(a,b), timestamp().
- "what time is it?" -> { \"tool\": \"timestamp\", \"params\": {} }
- "sum 10 and 5" -> { \"tool\": \"add\", \"params\": { \"a\": 10, \"b\": 5 } }
- "say hi to Ada" -> { \"tool\": \"greet\", \"params\": { \"name\": \"Ada\" } }
Respond ONLY with JSON."

## Verify
- Send:
  - `{ "text": "sum 2 and 3" }` → `{ ok: true, tool: "add", result: { sum: 5 } }`
  - `{ "text": "say hi to Grace" }` → `{ ok: true, tool: "greet", result: { message: "Hello, Grace!" } }`
  - `{ "text": "what time is it?" }` → `{ ok: true, tool: "timestamp", result: { iso: "..." } }`

## Hints
- Keep the AI output strict JSON; reject extra commentary
- Use regex in a Function node as a non-AI fallback for "sum X and Y"
- Log the AI output JSON before invoking MCP Client to catch formatting issues
