# Test Prompts for Quick Decision Maker

**Example prompts and expected outputs for testing the MCP server**

## Tool: make_decision

### Prompt 1: Food Decision
**Prompt:**
```
Help me decide what to have for dinner: pizza, sushi, or tacos.
```

**Expected Output:**
The AI should use the `make_decision` tool with options: `["pizza", "sushi", "tacos"]`

**Example Response:**
```
I'll help you decide! Let me randomly choose from your options.

Options: ["pizza", "sushi", "tacos"]
Decision: sushi
```

**What to Verify:**
- Tool is called with correct options list
- Response shows a randomly selected option from the list
- All provided options appear in the response

---

### Prompt 2: Vacation Destination
**Prompt:**
```
I can't decide where to go on vacation. Should I go to Hawaii, Paris, Tokyo, or Bali?
```

**Expected Output:**
AI uses `make_decision` with: `["Hawaii", "Paris", "Tokyo", "Bali"]`

**Example Response:**
```
Let me help you choose a vacation destination!

Options: ["Hawaii", "Paris", "Tokyo", "Bali"]
Decision: Tokyo
```

**What to Verify:**
- Handles 4+ options correctly
- All options are included in the response
- Random selection is made

---

### Prompt 3: Simple Two Options
**Prompt:**
```
Should I work from home or go to the office today?
```

**Expected Output:**
AI uses `make_decision` with: `["work from home", "go to the office"]`

**Example Response:**
```
Decision: work from home
```

**What to Verify:**
- Works with just 2 options (minimum required)
- Response is concise for binary decisions

---

### Prompt 4: Activity Choice
**Prompt:**
```
Help me pick an activity: reading, hiking, cooking, or watching a movie.
```

**Expected Output:**
AI uses `make_decision` with: `["reading", "hiking", "cooking", "watching a movie"]`

**Example Response:**
```
Options: ["reading", "hiking", "cooking", "watching a movie"]
Decision: hiking
```

**What to Verify:**
- Handles various option types
- Response format shows all options and decision

---

## Tool: random_number

### Prompt 5: Default Range (1-100)
**Prompt:**
```
Pick a random number between 1 and 100.
```

**Expected Output:**
AI uses `random_number` with default parameters or `min: 1, max: 100`

**Example Response:**
```
Random number: 42
```

**What to Verify:**
- Number is between 1 and 100 (inclusive)
- Response is clear and concise

---

### Prompt 6: Custom Range
**Prompt:**
```
Generate a random number between 50 and 200.
```

**Expected Output:**
AI uses `random_number` with: `min: 50, max: 200`

**Example Response:**
```
Random number between 50 and 200: 127
```

**What to Verify:**
- Number falls within specified range
- Response shows the range used

---

### Prompt 7: Small Range
**Prompt:**
```
Give me a random number from 1 to 10.
```

**Expected Output:**
AI uses `random_number` with: `min: 1, max: 10`

**Example Response:**
```
Random number between 1 and 10: 7
```

**What to Verify:**
- Works with small ranges
- Result is within 1-10

---

### Prompt 8: Large Range
**Prompt:**
```
Pick a random number between 1000 and 10000.
```

**Expected Output:**
AI uses `random_number` with: `min: 1000, max: 10000`

**Example Response:**
```
Random number between 1000 and 10000: 5832
```

**What to Verify:**
- Handles large ranges correctly
- Number is within specified bounds

---

## Combination Prompts

### Prompt 9: Multiple Decisions
**Prompt:**
```
First, help me decide between breakfast options: pancakes or waffles. Then pick a random number between 1 and 20.
```

**Expected Output:**
AI makes two tool calls:
1. `make_decision` with `["pancakes", "waffles"]`
2. `random_number` with `min: 1, max: 20`

**Example Response:**
```
I'll help with both!

For breakfast:
Decision: pancakes

Random number between 1 and 20: 13
```

**What to Verify:**
- Multiple tools can be called in one request
- Both results are presented clearly

---

## Testing Checklist

After testing these prompts, verify:

- [ ] All prompts successfully invoke the correct tool
- [ ] Tool parameters are correctly extracted from natural language
- [ ] Results are formatted clearly for the user
- [ ] Random selections actually vary (test multiple times)
- [ ] Edge cases work (2 options minimum, various ranges)
- [ ] Error messages are clear if something goes wrong

## Common Issues

**Issue:** Tool not being called
- **Check:** Server is connected in Cursor's MCP panel
- **Solution:** Restart Cursor and verify connection

**Issue:** Wrong parameters
- **Check:** Tool schema matches what's being sent
- **Solution:** Verify server code matches tool definitions

**Issue:** Container stopped
- **Check:** `docker ps` shows running container
- **Solution:** Restart Cursor to reconnect

---

**More examples?** Try creating your own decision prompts!

