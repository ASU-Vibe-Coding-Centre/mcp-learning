## Exercise 2 (Optional, Medium): Enhance the Practical Server

Goal: Add one or two more tools to the notes server.

Suggested ideas:
- `search_notes(query: string) -> note[]` (match title/content)
- `archive_note(id: number) -> note` (add archived flag)

Requirements:
- Update JSON Schemas for new tools
- Add DB changes (e.g., `archived` column) via `ALTER TABLE` if needed
- Preserve existing behavior and tests

Hints:
- Add columns lazily: check if column exists by attempting `ALTER TABLE` and ignoring errors
- Reuse `_row_to_note` or extend it for new fields

Expected outcome:
- Tools appear in `list_tools()` and return results for realistic prompts


