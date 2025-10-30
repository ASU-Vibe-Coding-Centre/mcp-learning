## Solution: Exercise 1 (Modify the Simple Server)

Add a new tool, e.g., `sum_numbers`, with schema:

```json
{
  "type": "object",
  "properties": {
    "numbers": { "type": "array", "items": { "type": "number" }, "minItems": 1, "maxItems": 100 }
  },
  "required": ["numbers"]
}
```

Implementation notes:
- Validate array length; coerce only numeric inputs
- Return `TextContent` with the numeric sum


