# Solution: Exercise 2 — Modify the AI Prompt/Behavior

## System prompt (example)
"You extract a tool name and JSON params from a short request. Tools: greet(name), add(a,b), timestamp().
- 'what time is it?' -> { \"tool\": \"timestamp\", \"params\": {} }
- 'sum 10 and 5' -> { \"tool\": \"add\", \"params\": { \"a\": 10, \"b\": 5 } }
- 'say hi to Ada' -> { \"tool\": \"greet\", \"params\": { \"name\": \"Ada\" } }
Respond ONLY with JSON."

## User prompt template
"Request: {{$json.text}}"

## Output post-processing
- Parse model output as JSON
- Coerce numeric strings to numbers
- Ensure `tool` ∈ { `greet`, `add`, `timestamp` }, else fallback to `timestamp` with `{}`

## Test cases
- `{ "text": "sum 2 and 3" }` → `{ tool: "add", params: { a: 2, b: 3 } }`
- `{ "text": "say hi to Grace" }` → `{ tool: "greet", params: { name: "Grace" } }`
- `{ "text": "what time is it?" }` → `{ tool: "timestamp", params: {} }`
