# Challenge 1: Design and Implement a Custom Tool

Congratulations on completing the tutorials! Now it's time to apply what you've learned by designing and implementing your own custom MCP tool from scratch.

## Challenge Overview

Unlike the tutorials, this challenge is less structured. You'll make design decisions, handle edge cases, and create something unique. This mirrors real-world development where requirements are high-level and implementation details are up to you.

## Difficulty

Intermediate

## Time Estimate

45-75 minutes (depending on chosen use case)

## Learning Objectives

By completing this challenge, you will:

1. Analyze a use case and design an appropriate tool
2. Define a clear tool contract (parameters and return values)
3. Implement comprehensive input validation
4. Handle edge cases and errors gracefully
5. Write tests to verify your tool works correctly
6. Document your tool for other users

## Your Mission

Choose ONE of the following use cases and implement a complete MCP server with the required tool(s):

### Option A: URL Information Tool

**Use Case**: Extract information from URLs

**Tool Name**: `analyze_url`

**What it should do**:

- Accept a URL string
- Parse and extract components (protocol, domain, path, query parameters)
- Return structured information about the URL

**Example**:

```
Input: "https://example.com/path/to/page?id=123&sort=date"
Output:
  Protocol: https
  Domain: example.com
  Path: /path/to/page
  Query Parameters:
    - id: 123
    - sort: date
```

**Requirements**:

- Validate that input is a valid URL
- Handle URLs with and without query parameters
- Handle URLs with and without ports
- Return clear error messages for invalid URLs
- Support both HTTP and HTTPS protocols

**Bonus Points**:

- Detect common URL schemes (mailto:, ftp:, etc.)
- Extract anchor fragments (#section)
- Validate domain format

### Option B: Password Strength Checker

**Use Case**: Evaluate password security

**Tool Name**: `check_password_strength`

**What it should do**:

- Accept a password string
- Analyze strength based on multiple criteria
- Return a strength rating and recommendations

**Criteria to check**:

- Length (minimum 8 characters recommended)
- Contains uppercase letters
- Contains lowercase letters
- Contains numbers
- Contains special characters (!@#$%^&*, etc.)
- Not a common password (check against a small list)

**Output should include**:

- Strength rating (Weak/Moderate/Strong/Very Strong)
- Which criteria passed/failed
- Specific recommendations for improvement

**Requirements**:

- Accept any string input
- Never expose the actual password in responses
- Provide actionable feedback
- Handle empty strings
- Don't recommend specific characters (security best practice)

**Bonus Points**:

- Check for sequential characters (abc, 123)
- Check for repeated characters (aaa, 111)
- Estimate time to crack

### Option C: Temperature Converter

**Use Case**: Convert between temperature scales

**Tool Name**: `convert_temperature`

**What it should do**:

- Accept a temperature value and source scale
- Convert to a target scale
- Return the converted value

**Supported scales**:

- Celsius (C)
- Fahrenheit (F)
- Kelvin (K)

**Parameters**:

- `value`: number (temperature value)
- `from_scale`: string (source scale: "C", "F", or "K")
- `to_scale`: string (target scale: "C", "F", or "K")

**Requirements**:

- Validate that scales are valid
- Validate that Kelvin temperatures aren't below absolute zero
- Round results to 2 decimal places
- Handle the case where from_scale == to_scale
- Return clear error messages

**Bonus Points**:

- Support full scale names ("Celsius" not just "C")
- Add Rankine scale support
- Include interesting facts (e.g., "That's below absolute zero!")

### Option D: Text Statistics Tool

**Use Case**: Analyze text and provide statistics

**Tool Name**: `analyze_text`

**What it should do**:

- Accept a text string
- Calculate various statistics
- Return a comprehensive analysis

**Statistics to calculate**:

- Character count (total and excluding spaces)
- Word count
- Sentence count
- Average word length
- Longest word
- Most common word
- Reading time estimate (assume 200 words per minute)

**Requirements**:

- Handle empty strings
- Handle text with multiple spaces/newlines
- Define what constitutes a "word" and "sentence"
- Return results in a clear, formatted way
- Handle special characters appropriately

**Bonus Points**:

- Readability score (Flesch Reading Ease)
- Paragraph count
- Vocabulary richness (unique words / total words)
- Sentiment analysis (positive/negative/neutral)

### Option E: Create Your Own!

Have an idea for a different tool? Great! Design and implement your own.

**Your tool should**:

- Solve a clear, specific problem
- Have well-defined inputs and outputs
- Include proper validation
- Handle edge cases
- Be testable

**Get approval** by writing a brief design document (see template below).

## Design Document Template

Before coding, write a design document. This helps clarify your thoughts and catches issues early.

```markdown
# Tool Design: [Tool Name]

## Purpose
[One sentence describing what the tool does]

## Use Case
[Who would use this tool and why?]

## Input Parameters
- parameter_name (type): description
  - Validation rules
  - Default value (if optional)

## Output Format
[Describe what the tool returns]

Example:
```
[Show example output]
```

## Edge Cases to Handle
1. [Edge case and how you'll handle it]
2. [Edge case and how you'll handle it]
3. ...

## Error Scenarios
- [What errors might occur and what messages to return]

## Testing Plan
- [How you'll verify it works]
```

## Implementation Steps

### Step 1: Design First

Write your design document (see template above). Think through:

- What parameters do you need?
- What types should they be?
- What values are valid?
- What should the output look like?
- What can go wrong?

### Step 2: Set Up the Server Structure

Create your server file with the basic structure:

```python
#!/usr/bin/env python3
"""[Your tool description]"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("[your-server-name]")

# Your code here

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 3: Define the Tool Schema

Implement `list_tools()` with your tool definition:

- Clear, descriptive name
- Comprehensive description
- Detailed parameter schema with descriptions
- Specify required vs. optional parameters

### Step 4: Implement Helper Functions

Before writing the handler, create helper functions:

- Input validation functions
- Core logic functions
- Response formatting functions

This keeps your handler clean and makes testing easier.

### Step 5: Implement the Handler

Write `call_tool()` to:

1. Extract parameters
2. Validate inputs (use your helper functions)
3. Perform the operation
4. Format and return the result
5. Handle all error cases

### Step 6: Test Thoroughly

Use the MCP Inspector to test:

**Happy Path Tests**:

- Normal, valid inputs
- Verify correct output

**Edge Case Tests**:

- Boundary values (empty strings, zero, max values)
- Optional parameters missing
- Unusual but valid inputs

**Error Tests**:

- Invalid types
- Invalid values
- Missing required parameters
- Out-of-range values

Create a test checklist as you go.

### Step 7: Document

Add comments explaining:

- Why you made certain design decisions
- How complex algorithms work
- What edge cases you're handling

## Success Criteria

Your implementation is complete when:

- Tool works correctly for all valid inputs
- All edge cases are handled gracefully
- Errors return helpful messages
- Code is well-commented
- You've tested with the Inspector
- Someone else could use your tool based on the description

## Example: Complete URL Analyzer Snippet

Here's a small example to illustrate the quality expected:

```python
from urllib.parse import urlparse, parse_qs

def analyze_url_string(url: str) -> dict:
    """
    Parse a URL and extract components.
    
    Args:
        url: URL string to analyze
        
    Returns:
        Dictionary with URL components
        
    Raises:
        ValueError: If URL is invalid
    """
    # Validate input
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Parse the URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid URL format: {str(e)}")
    
    # Ensure we have at least a scheme and netloc
    if not parsed.scheme:
        raise ValueError("URL must include a protocol (e.g., https://)")
    
    if not parsed.netloc:
        raise ValueError("URL must include a domain")
    
    # Extract query parameters
    query_params = {}
    if parsed.query:
        query_params = {k: v[0] if len(v) == 1 else v 
                       for k, v in parse_qs(parsed.query).items()}
    
    return {
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path or "/",
        "query_parameters": query_params,
        "fragment": parsed.fragment or None
    }
```

Notice:

- Clear docstring
- Type hints
- Input validation
- Helpful error messages
- Handles edge cases (missing path, no query params)
- Returns structured data

## Getting Unstuck

If you're stuck, try:

### Design Phase

- **"I don't know what to validate"**: Think about what could break your code. Try passing weird values.
- **"I don't know what to return"**: What would be most useful to the user? Look at the examples.
- **"Too many edge cases"**: Start simple. Handle the basics first, add edge case handling later.

### Implementation Phase

- **"My handler is too long"**: Extract helper functions for validation, processing, and formatting.
- **"I keep getting errors"**: Add print statements (to stderr) to see what's happening.
- **"I don't know how to validate X"**: Ask the AI assistant! It can suggest validation approaches.

### Testing Phase

- **"Not sure what to test"**: Test: normal inputs, edge cases, errors, missing parameters, wrong types.
- **"It works in my tests but fails in Inspector"**: Check JSON format and type conversions.

## Ask the AI

The AI assistant can help with:

- "How do I validate that a string is a valid URL?"
- "What's a good way to structure my tool's output?"
- "How do I handle optional parameters in the schema?"
- "Can you review my design and suggest improvements?"
- "What edge cases am I missing?"

Remember: Ask for guidance, not complete solutions. You learn more by solving problems yourself!

## Submission Checklist

Before considering this challenge complete, verify:

- [ ] Design document written
- [ ] Tool schema defined with clear descriptions
- [ ] Helper functions implemented
- [ ] Tool handler implemented
- [ ] Input validation for all parameters
- [ ] Error handling for edge cases
- [ ] Tested with MCP Inspector
- [ ] Tested happy path scenarios
- [ ] Tested edge cases
- [ ] Tested error scenarios
- [ ] Code has comments explaining complex parts
- [ ] Error messages are helpful and specific

## Going Further

After completing your tool:

1. **Add a second related tool** - What complementary functionality makes sense?
2. **Write unit tests** - Create Python unit tests for your helper functions
3. **Optimize** - Can you make it faster or more efficient?
4. **Review** - Have someone else try your tool and give feedback

## Solution Availability

A reference solution for each option is available in `solutions/challenge-1-solution.md`. However, try to complete the challenge on your own first! There are many correct ways to implement each tool.

The solution shows one approach, but yours might be different - and that's great! Compare your implementation to learn alternative approaches.

## What You're Learning

This challenge develops skills beyond just coding:

- **Design thinking**: Analyzing requirements and making design decisions
- **User perspective**: Thinking about how others will use your tool
- **Robustness**: Handling edge cases and errors
- **Communication**: Writing clear descriptions and error messages
- **Testing mindset**: Thinking about what could go wrong

These skills are essential for building production-quality MCP servers.

## Ready to Start?

Pick your option, write your design document, and start building! Good luck, and remember: it's okay to iterate. Your first design doesn't have to be perfect - you can refine as you implement and test.

Happy coding!

