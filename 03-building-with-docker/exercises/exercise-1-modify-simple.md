## Exercise 1 (Optional, Easy): Modify the Simple Server

Goal: Extend the simple server with one additional tool.

Suggested idea:
- `sum_numbers(numbers: number[]) -> number`

Requirements:
- Add JSON Schema, validation, and type hints
- Return a clear, human-readable `TextContent` response

Hints:
- Start from `examples/simple-server/server.py`
- Mirror the pattern used for `roll_dice`
- Keep bounds reasonable (e.g., max 100 items)

Expected outcome:
- A new tool appears in `list_tools()` and can be called from Cursor


