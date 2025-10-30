## Solution: Exercise 2 (Enhance the Practical Server)

Option A: `search_notes(query: string)`
- Add schema with required `query`
- SQL: `SELECT ... FROM notes WHERE title LIKE ? OR content LIKE ?`
- Params: `f"%{query}%"`

Option B: `archive_note(id: number)`
- Add `archived INTEGER DEFAULT 0` column
- `UPDATE notes SET archived = 1, updated_at = ? WHERE id = ?`
- `list_notes` can filter archived by default or add a flag


