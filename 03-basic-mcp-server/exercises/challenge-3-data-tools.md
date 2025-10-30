# Challenge 3: Data Processing Tools

Build an MCP server for working with structured data in JSON and CSV formats. This challenge focuses on data transformation, querying, and validation - essential skills for real-world integrations.

## Challenge Overview

Create a "Data Toolkit" server with tools for reading, transforming, filtering, and validating JSON and CSV data. You'll handle common data processing tasks that come up frequently when building integrations and automation.

## Difficulty

Intermediate to Advanced

## Time Estimate

90-120 minutes

## Learning Objectives

By completing this challenge, you will:

1. Work with structured data formats (JSON, CSV)
2. Implement data transformation and filtering logic
3. Handle malformed and invalid data gracefully
4. Design tools for common data processing tasks
5. Validate complex data structures
6. Build tools that work together in workflows

## Required Tools

Implement ALL of the following tools:

### 1. parse_json

Parse and validate JSON strings.

**Parameters**:

- `json_string` (string, required): JSON data as a string
- `validate_schema` (boolean, optional): Whether to validate structure (default: false)

**Returns**:

- Success: "Valid JSON" with summary (number of keys, type of root element)
- Error: Specific parsing error with line/position

**Example**:

```
Input: json_string='{"name": "Alice", "age": 30}'
Output: "Valid JSON object with 2 keys: name, age"

Input: json_string='{"name": "Alice", "age": }'
Output: "Error: Invalid JSON at position 27: Expecting value"
```

### 2. json_query

Extract values from JSON using paths.

**Parameters**:

- `json_string` (string, required): JSON data as a string
- `path` (string, required): Dot-notation path to value (e.g., "user.address.city")

**Returns**:

- The value at the specified path
- Error if path doesn't exist

**Example**:

```
Input: json_string='{"user": {"name": "Alice", "address": {"city": "NYC"}}}', 
       path="user.address.city"
Output: "NYC"

Input: path="user.phone"
Output: "Error: Path 'user.phone' not found"
```

**Bonus**: Support array indexing (e.g., "users[0].name")

### 3. json_transform

Transform JSON data.

**Parameters**:

- `json_string` (string, required): Source JSON
- `operation` (string, required): One of "flatten", "pretty", "minify", "keys_only"

**Operations**:

- **flatten**: Convert nested JSON to flat structure with dot notation keys
- **pretty**: Format with indentation for readability
- **minify**: Remove all whitespace
- **keys_only**: Return only the keys at top level

**Example**:

```
Input: json_string='{"user":{"name":"Alice"}}', operation="flatten"
Output: {"user.name": "Alice"}

Input: json_string='{"a":1,"b":2}', operation="pretty"
Output:
{
  "a": 1,
  "b": 2
}
```

### 4. parse_csv

Parse and analyze CSV data.

**Parameters**:

- `csv_string` (string, required): CSV data as a string
- `has_header` (boolean, optional): Whether first row is a header (default: true)
- `delimiter` (string, optional): Field delimiter (default: ",")

**Returns**:

- Row count
- Column count
- Column names (if has_header=true)
- First 3 rows as preview

**Example**:

```
Input: csv_string="name,age\nAlice,30\nBob,25", has_header=true
Output:
  Rows: 2 (plus 1 header row)
  Columns: 2 (name, age)
  Preview:
    Alice, 30
    Bob, 25
```

### 5. csv_filter

Filter CSV rows based on conditions.

**Parameters**:

- `csv_string` (string, required): CSV data as a string
- `column` (string, required): Column name to filter on
- `operator` (string, required): One of "equals", "contains", "greater_than", "less_than"
- `value` (string, required): Value to compare against
- `has_header` (boolean, optional): Whether first row is a header (default: true)

**Returns**:

- Filtered CSV data
- Count of matching rows

**Example**:

```
Input: csv_string="name,age\nAlice,30\nBob,25\nCharlie,30", 
       column="age", operator="equals", value="30"
Output:
  name,age
  Alice,30
  Charlie,30
  
  (2 rows matched)
```

### 6. csv_to_json

Convert CSV to JSON.

**Parameters**:

- `csv_string` (string, required): CSV data as a string
- `has_header` (boolean, optional): Whether first row is a header (default: true)
- `format` (string, optional): One of "array_of_objects", "array_of_arrays" (default: "array_of_objects")

**Returns**:

- JSON representation of the CSV data

**Example**:

```
Input: csv_string="name,age\nAlice,30\nBob,25", format="array_of_objects"
Output: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

Input: format="array_of_arrays"
Output: [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
```

## Optional Bonus Tools

For extra challenge:

### 7. json_to_csv

Convert JSON to CSV.

**Parameters**:

- `json_string` (string, required): JSON array of objects
- `columns` (string, optional): Comma-separated list of columns to include (default: all)

### 8. validate_data

Validate data against common patterns.

**Parameters**:

- `data` (string, required): Data to validate
- `type` (string, required): One of "email", "url", "phone", "date", "credit_card"

### 9. csv_aggregate

Perform aggregations on CSV data.

**Parameters**:

- `csv_string` (string, required): CSV data
- `column` (string, required): Column to aggregate
- `operation` (string, required): One of "sum", "average", "min", "max", "count"

## Requirements

### Data Handling

1. Handle malformed JSON/CSV gracefully
2. Provide specific error messages (line numbers, positions)
3. Support various CSV delimiters (comma, tab, pipe)
4. Handle quoted fields in CSV (e.g., "Smith, John")
5. Handle empty rows and missing values

### Validation

1. Validate that JSON is well-formed before parsing
2. Validate that CSV has consistent column counts
3. Validate parameter types and values
4. Check for empty inputs

### Output Format

1. Return data in requested format
2. Include metadata (row counts, column names)
3. Provide previews for large datasets
4. Format errors clearly

## Implementation Strategy

### Phase 1: Setup

```python
#!/usr/bin/env python3
"""Data Processing MCP Server"""

import asyncio
import json
import csv
import io
from typing import Any, List, Dict
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("data-tools")
```

### Phase 2: Helper Functions

Create helper functions for:

- JSON parsing with error handling
- CSV parsing with different delimiters
- Path navigation in nested JSON
- Data transformation operations
- Validation utilities

### Phase 3: Implement Tools

Start with simpler tools:

1. `parse_json` - foundation for other JSON tools
2. `parse_csv` - foundation for other CSV tools
3. `json_query` - build on parse_json
4. `csv_to_json` - combine both formats

Then tackle complex tools:

5. `json_transform` - requires transformation logic
6. `csv_filter` - requires filtering logic

### Phase 4: Testing

Test with:

- Valid, well-formed data
- Malformed data (syntax errors)
- Edge cases (empty, very large)
- Real-world data samples

## Helpful Code Snippets

### JSON Parsing with Error Details

```python
import json

def parse_json_safe(json_string: str) -> tuple[Any, str]:
    """
    Parse JSON and return (result, error_message).
    
    Returns:
        (parsed_data, None) on success
        (None, error_message) on failure
    """
    try:
        data = json.loads(json_string)
        return data, None
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
        return None, error_msg
    except Exception as e:
        return None, f"Error parsing JSON: {str(e)}"
```

### JSON Path Navigation

```python
def get_nested_value(data: dict, path: str) -> Any:
    """
    Get value from nested dict using dot notation path.
    
    Example: get_nested_value({"a": {"b": 1}}, "a.b") returns 1
    
    Raises:
        KeyError: If path doesn't exist
    """
    keys = path.split('.')
    value = data
    
    for key in keys:
        if isinstance(value, dict):
            value = value[key]  # Raises KeyError if not found
        else:
            raise KeyError(f"Cannot navigate to '{key}' in non-dict value")
    
    return value
```

### CSV Parsing

```python
import csv
import io

def parse_csv_string(csv_string: str, has_header: bool = True, 
                     delimiter: str = ',') -> tuple[List[str], List[List[str]]]:
    """
    Parse CSV string into headers and rows.
    
    Returns:
        (headers, rows) where headers is list of column names (or None)
        and rows is list of row data
    """
    reader = csv.reader(io.StringIO(csv_string), delimiter=delimiter)
    rows = list(reader)
    
    if not rows:
        return None, []
    
    if has_header:
        headers = rows[0]
        data_rows = rows[1:]
        return headers, data_rows
    else:
        return None, rows
```

### JSON Flattening

```python
def flatten_json(data: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flatten nested JSON dict.
    
    Example: {"a": {"b": 1}} becomes {"a.b": 1}
    """
    items = []
    
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)
```

### CSV Filtering

```python
def filter_csv_rows(headers: List[str], rows: List[List[str]], 
                    column: str, operator: str, value: str) -> List[List[str]]:
    """
    Filter CSV rows based on condition.
    
    Returns list of rows that match the condition.
    """
    if column not in headers:
        raise ValueError(f"Column '{column}' not found")
    
    col_index = headers.index(column)
    filtered = []
    
    for row in rows:
        if len(row) <= col_index:
            continue
        
        cell_value = row[col_index]
        
        if operator == "equals":
            if cell_value == value:
                filtered.append(row)
        elif operator == "contains":
            if value in cell_value:
                filtered.append(row)
        elif operator == "greater_than":
            try:
                if float(cell_value) > float(value):
                    filtered.append(row)
            except ValueError:
                pass
        elif operator == "less_than":
            try:
                if float(cell_value) < float(value):
                    filtered.append(row)
            except ValueError:
                pass
    
    return filtered
```

## Edge Cases to Handle

### JSON Edge Cases

- Empty string: `""`
- Just whitespace: `"   "`
- Not JSON at all: `"hello"`
- Incomplete JSON: `'{"a": }'`
- Very large JSON (MB+)
- Deeply nested JSON (100+ levels)

### CSV Edge Cases

- Empty string
- Header only (no data rows)
- Inconsistent column counts
- Quoted fields with commas: `"Smith, John",30`
- Quoted fields with quotes: `"He said ""hello""",test`
- Empty fields: `name,,age`
- Different line endings (`\n` vs `\r\n`)

### Path Navigation Edge Cases

- Empty path: `""`
- Non-existent path: `"user.email"` when email doesn't exist
- Path through array: `"users[0].name"`
- Path through non-dict: `"name.first"` when name is a string

## Testing Checklist

### parse_json

- [ ] Valid JSON object
- [ ] Valid JSON array
- [ ] Invalid JSON (syntax error)
- [ ] Empty string
- [ ] Very large JSON

### json_query

- [ ] Simple path (one level)
- [ ] Nested path (multiple levels)
- [ ] Non-existent path
- [ ] Path through array (bonus)

### json_transform

- [ ] Flatten nested object
- [ ] Pretty print
- [ ] Minify with whitespace
- [ ] Keys only

### parse_csv

- [ ] CSV with header
- [ ] CSV without header
- [ ] Different delimiters
- [ ] Quoted fields
- [ ] Empty rows

### csv_filter

- [ ] Filter with equals
- [ ] Filter with contains
- [ ] Filter with greater_than
- [ ] No matches found
- [ ] Invalid column name

### csv_to_json

- [ ] Array of objects format
- [ ] Array of arrays format
- [ ] Empty CSV
- [ ] Single row

## Example Test Data

### Sample JSON

```json
{
  "user": {
    "id": 123,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "address": {
      "street": "123 Main St",
      "city": "NYC",
      "zip": "10001"
    },
    "tags": ["admin", "verified"]
  }
}
```

### Sample CSV

```csv
id,name,email,age,city
1,Alice Smith,alice@example.com,30,NYC
2,Bob Jones,bob@example.com,25,LA
3,Charlie Brown,charlie@example.com,35,NYC
4,Diana Prince,diana@example.com,28,Chicago
```

### Sample Malformed Data

```json
// Invalid JSON examples
{"name": "Alice", "age": }  // Missing value
{'name': 'Alice'}  // Single quotes
{name: "Alice"}  // Unquoted key
```

```csv
# Invalid CSV examples
name,age
Alice,30,extra  # Too many columns
Bob  # Too few columns
```

## Common Pitfalls

### Pitfall 1: Not Handling Quotes in CSV

```python
# Wrong - doesn't handle quoted fields
rows = csv_string.split('\n')
cells = row.split(',')

# Right - use csv module
import csv
reader = csv.reader(io.StringIO(csv_string))
```

### Pitfall 2: Assuming JSON is Always Valid

```python
# Wrong - no error handling
data = json.loads(json_string)

# Right - catch errors
try:
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    # Handle error
```

### Pitfall 3: Not Validating Column Names

```python
# Wrong - might raise IndexError
col_index = headers.index(column)

# Right - check first
if column not in headers:
    return error_response(f"Column '{column}' not found")
col_index = headers.index(column)
```

## Success Criteria

Your implementation is complete when:

- [ ] All 6 required tools implemented
- [ ] Handles malformed data gracefully
- [ ] Provides specific error messages
- [ ] Tested with sample data
- [ ] Tested edge cases
- [ ] Code is organized with helper functions
- [ ] Documentation explains complex logic

## Real-World Applications

These tools enable workflows like:

1. **API Integration**: Parse API responses, extract values, transform formats
2. **Data Migration**: Convert between JSON and CSV for database imports
3. **Data Validation**: Check data quality before processing
4. **Report Generation**: Filter and aggregate data for reports
5. **Configuration Management**: Query and validate config files

## Ask the AI

Questions you might ask:

- "How do I parse CSV with quoted fields containing commas?"
- "What's the best way to navigate nested JSON?"
- "How do I flatten a deeply nested JSON structure?"
- "How can I validate JSON against a schema?"
- "What's the best error message for malformed JSON?"

## Going Further

After completing the required tools:

1. **Add json_to_csv** tool
2. **Add data validation** tool
3. **Add csv_aggregate** for calculations
4. **Support JSON Schema** validation
5. **Add JSON diff** tool to compare two JSON objects
6. **Optimize for large files** (streaming, chunking)

## Solution Availability

A complete reference implementation is available in `solutions/challenge-3-solution.md`. Try to solve it yourself first!

## What You're Learning

This challenge teaches:

- **Data parsing**: Working with structured formats
- **Error handling**: Gracefully handling malformed data
- **Data transformation**: Converting between formats
- **Querying**: Navigating and extracting data
- **Validation**: Checking data integrity
- **Real-world skills**: Practical data processing tasks

These are essential skills for building integrations, APIs, and automation tools.

## Ready to Build?

Start with `parse_json` and `parse_csv` as your foundation, then build the other tools on top. Take your time with error handling - it's the most important part!

Happy data processing!

