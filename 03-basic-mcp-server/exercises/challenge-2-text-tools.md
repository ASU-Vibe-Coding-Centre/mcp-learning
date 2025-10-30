# Challenge 2: Text Manipulation Tools

Build a comprehensive text processing MCP server with multiple tools for common string operations. This challenge focuses on building a cohesive set of related tools and handling various string manipulation edge cases.

## Challenge Overview

You'll create a "Text Toolbox" server with 6-8 tools for text manipulation. These tools should work together logically and handle Unicode, special characters, and edge cases properly.

## Difficulty

Intermediate

## Time Estimate

60-90 minutes

## Learning Objectives

By completing this challenge, you will:

1. Build a multi-tool server with consistent patterns
2. Handle string encoding and Unicode properly
3. Work with regular expressions and string methods
4. Design tools that complement each other
5. Handle edge cases in text processing
6. Create a cohesive tool API

## Required Tools

Implement ALL of the following tools:

### 1. text_transform

Transform text case.

**Parameters**:

- `text` (string, required): The text to transform
- `operation` (string, required): One of "upper", "lower", "title", "capitalize", "swap"

**Operations**:

- **upper**: ALL UPPERCASE
- **lower**: all lowercase
- **title**: Title Case (capitalize first letter of each word)
- **capitalize**: Sentence case (only first letter capitalized)
- **swap**: sWAP cASE (uppercase becomes lowercase and vice versa)

**Example**:

```
Input: text="hello world", operation="title"
Output: "Hello World"
```

### 2. count_words

Count words in text with options.

**Parameters**:

- `text` (string, required): The text to analyze
- `count_unique` (boolean, optional): Count only unique words (default: false)

**Returns**:

- Total word count (or unique word count if requested)
- Should handle multiple spaces, newlines, punctuation

**Example**:

```
Input: text="Hello world hello", count_unique=true
Output: "Unique word count: 2 (hello, world)"
```

### 3. reverse_text

Reverse text at different levels.

**Parameters**:

- `text` (string, required): The text to reverse
- `level` (string, required): One of "characters", "words", "sentences"

**Levels**:

- **characters**: Reverse the entire string character by character
- **words**: Reverse the order of words
- **sentences**: Reverse the order of sentences

**Example**:

```
Input: text="Hello world", level="characters"
Output: "dlrow olleH"

Input: text="Hello world", level="words"
Output: "world Hello"
```

### 4. find_replace

Find and replace text with options.

**Parameters**:

- `text` (string, required): The text to process
- `find` (string, required): Text to find
- `replace` (string, required): Text to replace with
- `case_sensitive` (boolean, optional): Whether search is case-sensitive (default: true)
- `all_occurrences` (boolean, optional): Replace all or just first (default: true)

**Returns**:

- Modified text
- Count of replacements made

**Example**:

```
Input: text="Hello hello HELLO", find="hello", replace="hi", case_sensitive=false
Output: "hi hi hi (3 replacements made)"
```

### 5. extract_pattern

Extract text matching a pattern.

**Parameters**:

- `text` (string, required): The text to search
- `pattern_type` (string, required): One of "emails", "urls", "phone_numbers", "numbers"

**Pattern types**:

- **emails**: Extract email addresses
- **urls**: Extract URLs (http, https)
- **phone_numbers**: Extract US phone numbers (various formats)
- **numbers**: Extract all numbers (integers and decimals)

**Returns**:

- List of found matches
- Count of matches

**Example**:

```
Input: text="Contact me at user@example.com or visit https://example.com"
       pattern_type="emails"
Output: "Found 1 email: user@example.com"
```

### 6. text_summary

Provide statistics about text.

**Parameters**:

- `text` (string, required): The text to analyze

**Returns**:

- Character count (total and without spaces)
- Word count
- Sentence count
- Line count
- Longest word
- Average word length
- Most common word (and its count)

**Example**:

```
Input: text="Hello world. This is a test. Hello there."
Output:
  Characters: 41 (35 without spaces)
  Words: 8
  Sentences: 3
  Lines: 1
  Longest word: "Hello" (5 letters)
  Average word length: 4.4 letters
  Most common: "Hello" (appears 2 times)
```

## Optional Bonus Tools

Want an extra challenge? Add these:

### 7. truncate_text

Intelligently truncate text.

**Parameters**:

- `text` (string, required): Text to truncate
- `max_length` (integer, required): Maximum length
- `strategy` (string, optional): "words" or "characters" (default: "characters")
- `ellipsis` (boolean, optional): Add "..." (default: true)

**Strategies**:

- **characters**: Cut at exact character count
- **words**: Cut at word boundary before max_length

### 8. slugify

Convert text to URL-friendly slug.

**Parameters**:

- `text` (string, required): Text to slugify
- `separator` (string, optional): Separator character (default: "-")

**Example**:

```
Input: text="Hello World! This is a Test"
Output: "hello-world-this-is-a-test"
```

Should:

- Convert to lowercase
- Replace spaces with separator
- Remove special characters
- Handle multiple consecutive spaces/separators

## Requirements

### Functionality

1. All required tools must work correctly
2. Handle empty strings appropriately
3. Handle Unicode characters (emojis, accents, etc.)
4. Validate all parameters
5. Return helpful error messages

### Code Quality

1. Use helper functions to avoid duplication
2. Add docstrings to all functions
3. Use type hints
4. Handle edge cases explicitly
5. Write clear, self-documenting code

### Tool Design

1. Consistent parameter naming across tools
2. Consistent output format
3. Comprehensive tool descriptions
4. Clear parameter descriptions in schemas

## Implementation Strategy

### Phase 1: Setup and Structure

1. Create server file: `text_tools_server.py`
2. Set up basic server structure
3. Plan your helper functions

### Phase 2: Implement Core Tools

Start with simpler tools:

1. `text_transform` - good starting point
2. `reverse_text` - practice with string manipulation
3. `count_words` - introduce counting logic

### Phase 3: Implement Advanced Tools

Move to more complex tools:

4. `find_replace` - multiple options, counting
5. `extract_pattern` - regular expressions
6. `text_summary` - comprehensive analysis

### Phase 4: Testing and Refinement

- Test each tool individually
- Test edge cases
- Refine error messages
- Add comments

## Helpful Code Snippets

### Regular Expressions for Patterns

```python
import re

# Email pattern (simple version)
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# URL pattern
URL_PATTERN = r'https?://[^\s]+'

# US Phone pattern (simple)
PHONE_PATTERN = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'

# Numbers pattern
NUMBER_PATTERN = r'\b\d+\.?\d*\b'

# Usage
emails = re.findall(EMAIL_PATTERN, text)
```

### Case-Insensitive Replace

```python
import re

def case_insensitive_replace(text: str, find: str, replace: str) -> str:
    """Replace text case-insensitively."""
    pattern = re.compile(re.escape(find), re.IGNORECASE)
    return pattern.sub(replace, text)
```

### Counting Replacements

```python
import re

def replace_and_count(text: str, find: str, replace: str) -> tuple[str, int]:
    """Replace and return count of replacements."""
    pattern = re.compile(re.escape(find))
    count = len(pattern.findall(text))
    new_text = pattern.sub(replace, text)
    return new_text, count
```

### Word Extraction

```python
import re

def extract_words(text: str) -> list[str]:
    """Extract words from text, handling punctuation."""
    # Extract sequences of word characters
    words = re.findall(r'\b\w+\b', text.lower())
    return words
```

### Finding Most Common Word

```python
from collections import Counter

def find_most_common_word(text: str) -> tuple[str, int]:
    """Find the most common word and its count."""
    words = extract_words(text)
    if not words:
        return None, 0
    
    counter = Counter(words)
    most_common = counter.most_common(1)[0]
    return most_common  # Returns (word, count)
```

## Edge Cases to Handle

### Empty and Whitespace

- Empty string: `""`
- Only whitespace: `"   "`
- Only newlines: `"\n\n\n"`

### Unicode and Special Characters

- Emojis: `"Hello 👋 World"`
- Accents: `"café résumé"`
- Mixed scripts: `"Hello мир 世界"`

### Word Boundaries

- Multiple spaces: `"hello    world"`
- Punctuation: `"Hello, world! How are you?"`
- Hyphenated words: `"well-known"`

### Numbers and Patterns

- Decimals: `"3.14"`
- Negative numbers: `"-42"`
- Phone with various formats: `"123-456-7890"`, `"(123) 456-7890"`, `"1234567890"`

## Testing Checklist

For each tool, test:

### Basic Functionality

- [ ] Normal, expected inputs work correctly
- [ ] Output format matches specification
- [ ] Required parameters are enforced

### Edge Cases

- [ ] Empty string input
- [ ] Very long input (1000+ characters)
- [ ] Unicode characters (emojis, accents)
- [ ] Special characters and punctuation
- [ ] Multiple spaces and newlines

### Error Handling

- [ ] Missing required parameters
- [ ] Invalid parameter types
- [ ] Invalid parameter values
- [ ] Out-of-range values

### Tool-Specific Tests

For `find_replace`:

- [ ] Case-sensitive vs. case-insensitive
- [ ] Replace all vs. replace first
- [ ] Find text not present (0 replacements)

For `extract_pattern`:

- [ ] No matches found
- [ ] Multiple matches
- [ ] Edge-case patterns

For `text_summary`:

- [ ] Text with no words
- [ ] Text with one word
- [ ] Text with repeated words

## Success Criteria

Your implementation is complete when:

- [ ] All 6 required tools implemented and working
- [ ] All edge cases handled gracefully
- [ ] Tested with MCP Inspector
- [ ] Code is well-organized with helper functions
- [ ] Error messages are clear and helpful
- [ ] Documentation explains design decisions
- [ ] You can explain how each tool works

## Example Test Session

Here's an example testing flow:

```
1. text_transform:
   Input: text="hello WORLD", operation="title"
   Expected: "Hello World"

2. count_words:
   Input: text="hello world hello", count_unique=true
   Expected: "Unique word count: 2"

3. reverse_text:
   Input: text="hello world", level="words"
   Expected: "world hello"

4. find_replace:
   Input: text="Hello hello", find="hello", replace="hi", case_sensitive=false
   Expected: "hi hi (2 replacements made)"

5. extract_pattern:
   Input: text="Email me at test@example.com", pattern_type="emails"
   Expected: "Found 1 email: test@example.com"

6. text_summary:
   Input: text="Hello world"
   Expected: Shows all statistics correctly
```

## Common Pitfalls

### Pitfall 1: Not Handling Unicode

```python
# Wrong - may break with Unicode
text.upper()  # Might not work correctly for all languages

# Better
text.upper()  # Actually this is fine in Python 3!
# But be aware of edge cases like Turkish i
```

### Pitfall 2: Word Extraction Issues

```python
# Wrong - splits on spaces only
words = text.split(' ')  # Doesn't handle punctuation

# Better - use regex
import re
words = re.findall(r'\b\w+\b', text)
```

### Pitfall 3: Not Counting Correctly

```python
# Wrong - doesn't count replacements
new_text = text.replace(find, replace)

# Better
count = text.count(find)
new_text = text.replace(find, replace)
```

## Ask the AI

Questions you might ask:

- "How do I write a regex pattern for email addresses?"
- "What's the best way to count unique words?"
- "How do I handle case-insensitive replacement?"
- "How can I split text into sentences?"
- "What's the difference between str.split() and re.findall()?"

## Going Further

After completing the required tools:

1. **Add the bonus tools** (truncate_text, slugify)
2. **Add a tool** that combines multiple operations
3. **Optimize** for very long text (10,000+ words)
4. **Add caching** for expensive operations
5. **Write unit tests** for helper functions

## Solution Availability

A complete reference implementation is available in `solutions/challenge-2-solution.md`. Try to complete the challenge first, then compare approaches!

## What You're Learning

This challenge teaches:

- **String manipulation**: Core Python string operations
- **Regular expressions**: Pattern matching and extraction
- **Edge case handling**: Unicode, empty strings, special characters
- **API design**: Creating cohesive, related tools
- **Code organization**: Structuring a multi-tool server
- **Validation patterns**: Checking inputs thoroughly

These skills are essential for building robust text-processing tools that handle real-world data.

## Ready to Build?

Start with your server structure, implement the tools one by one, and test thoroughly. Take breaks between tools to test and refine before moving on.

Good luck, and enjoy building your text toolbox!

