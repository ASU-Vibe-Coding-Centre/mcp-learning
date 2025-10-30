# Tutorial 1: Exploring MCP Concepts

## Overview

This tutorial guides you through exploring Model Context Protocol concepts through guided questions and hands-on investigation. You'll develop a deep understanding of MCP fundamentals without writing code yet.

**Estimated Time**: 30-45 minutes

**Prerequisites**: Read [Module 01 README](../README.md)

## Learning Objectives

By the end of this tutorial, you will:
- Articulate the key problems MCP solves
- Explain the three core MCP concepts (tools, resources, prompts)
- Understand when MCP is appropriate vs alternatives
- Describe the MCP protocol architecture

---

## Part 1: Understanding the Problem Space

### Exercise 1.1: Before MCP

Imagine you're building an AI assistant that needs to:
- Read files from a user's computer
- Query a database
- Send emails
- Search the web

**Questions:**

1. **Without MCP**, list at least 3 challenges you would face in building this assistant to work with:
   - Claude Desktop
   - A custom GPT-4 application
   - An enterprise AI platform

2. **For each challenge**, explain why it's a problem and what complications it causes.

3. **Draw a diagram** (on paper or text) showing how your solution would connect these four capabilities to three different AI platforms. How many integration points are there?

---

**Ask the AI:**

Before moving to the next exercise, deepen your understanding:
- "Can you give me a real-world analogy that explains why having multiple custom integrations becomes a problem?"
- "What architectural pattern does MCP use to solve this integration problem? Don't tell me about MCP yet, just the general pattern."

---

### Exercise 1.2: The MCP Solution

Now consider the same scenario with MCP:

**Questions:**

1. How many MCP servers would you create? What would each one handle?

2. Draw a diagram showing the MCP-based architecture. How many integration points are there now?

3. What are the key differences between your "before" and "after" diagrams?

4. If you wanted to add a fifth capability (like "create calendar events"), what would you need to change in:
   - The non-MCP architecture?
   - The MCP architecture?

---

## Part 2: Core Concepts Deep Dive

### Exercise 2.1: Tools vs Resources

Consider these scenarios and determine whether each should be implemented as a **tool** or a **resource**:

| Scenario | Tool or Resource? | Why? |
|----------|-------------------|------|
| Reading the contents of a log file | | |
| Deleting a file | | |
| Getting current weather for a city | | |
| Calculating the sum of two numbers | | |
| Reading user profile data | | |
| Updating user profile data | | |
| Listing all files in a directory | | |
| Sending a message to Slack | | |

**Hint**: Think about whether the operation has side effects (changes state) or is read-only.

---

**Ask the AI:**

If you're uncertain about the tools vs resources distinction:
- "I think 'reading a log file' should be a [tool/resource] because [your reasoning]. Is this correct?"
- "Can you explain what 'side effects' means in programming without telling me the answers to the table?"

---

### Exercise 2.2: Designing Tools

Design a tool for each scenario. For each, specify:
- Tool name
- Description
- Input parameters (name, type, required?)
- Return value structure

**Scenario A: Temperature Converter**
```
Convert between Fahrenheit, Celsius, and Kelvin

Your design:
Name: 
Description:
Parameters:
  -
  -
Returns:
```

**Scenario B: Database Query**
```
Execute a SELECT query on a SQLite database

Your design:
Name:
Description:
Parameters:
  -
  -
Returns:
```

**Scenario C: File Operations**
```
Copy a file from one location to another

Your design:
Name:
Description:
Parameters:
  -
  -
Returns:
```

### Exercise 2.3: Designing Resources

Design resources for these data access scenarios:

**Scenario A: Configuration Data**
```
Application has multiple configuration files (dev.json, prod.json, test.json)

Your resource design:
URI pattern:
Description:
What varies?:
Example URIs:
  -
  -
```

**Scenario B: User Data**
```
Access user records by user ID

Your resource design:
URI pattern:
Description:
What varies?:
Example URIs:
  -
  -
```

### Exercise 2.4: Prompts

Design a prompt template for this scenario:

**Scenario: Code Review Assistant**

You want to create a reusable prompt for code reviews that:
- Takes the programming language as input
- Takes a code snippet as input
- Provides consistent review structure

```
Your prompt design:
Name:
Description:
Variables:
  -
  -
Template structure (write out the prompt):




```

---

**Ask the AI:**

As you design these tools, resources, and prompts:
- "For my temperature converter tool, I'm thinking of parameters [list yours]. What am I missing?"
- "What's the difference between a resource URI pattern like 'db://users/{id}' versus 'db://users/123'?"
- "How does a prompt template differ from just writing a good prompt manually each time?"

---

## Part 3: Protocol Understanding

### Exercise 3.1: Message Flow

Given this sequence of events, write out the JSON-RPC messages that would be exchanged:

**Sequence:**
1. Client connects and initializes
2. Client requests list of available tools
3. Client calls a tool named "calculate" with parameters: operation="add", a=5, b=3
4. Server returns result: 8

**Your messages:**

```json
// Message 1: Initialize request
{


}

// Message 2: Initialize response
{


}

// Message 3: List tools request
{


}

// Message 4: List tools response
{


}

// Message 5: Call tool request
{


}

// Message 6: Call tool response
{


}
```

**Hint**: Refer to [architecture.md](../architecture.md) for message format examples.

---

**Ask the AI:**

If you're stuck on JSON-RPC message structure:
- "Can you explain what JSON-RPC 'id' field is used for without writing the messages for me?"
- "I'm confused about the initialize handshake. What information does the client need to send?"
- "What's the structure of a successful tool call response versus an error response?"

---

### Exercise 3.2: Transport Selection

For each scenario, choose the most appropriate transport (stdio, HTTP+SSE, or WebSockets) and explain why:

**Scenario A: IDE Extension**
- Your choice:
- Reasoning:

**Scenario B: Shared Database Server**
- Your choice:
- Reasoning:

**Scenario C: Real-time Collaboration Tool**
- Your choice:
- Reasoning:

**Scenario D: Desktop AI Application**
- Your choice:
- Reasoning:

---

**Ask the AI:**

To understand transport options better:
- "What are the pros and cons of stdio transport versus HTTP? When would I choose each?"
- "Why would WebSockets be better than HTTP+SSE for real-time collaboration?"
- "Can you explain what 'stdio' means and how it enables processes to communicate?"

---

## Part 4: Architectural Thinking

### Exercise 4.1: System Design

Design an MCP-based architecture for this system:

**Requirements:**
- AI-powered customer support system
- Needs to access: customer database, order history, knowledge base articles
- Needs to perform: send emails, create support tickets, escalate to human
- Used by: web chat interface, mobile app, Slack bot

**Your design:**

1. **How many MCP servers would you create?**

2. **For each server, list:**
   - Server name and purpose
   - What tools it provides
   - What resources it provides
   - What systems it integrates with

3. **Draw a diagram** showing:
   - MCP servers
   - Clients (web, mobile, Slack)
   - External systems (database, email, etc.)
   - How they connect

4. **Explain:**
   - Why did you organize it this way?
   - What are the benefits of your design?
   - What are potential challenges?

### Exercise 4.2: Comparison Analysis

You're advising a team choosing between MCP and LangChain. Given these requirements, which would you recommend and why?

**Scenario A:**
- Building a research assistant for internal use
- Needs conversation memory
- Complex multi-step reasoning required
- Python-based project
- Single deployment target

**Your recommendation:**
**Reasoning:**

**Scenario B:**
- Building developer tools for IDE integration
- Need to support VS Code, JetBrains, and Cursor
- Tools should work with Claude, GPT-4, and local models
- Focus on code analysis and generation

**Your recommendation:**
**Reasoning:**

**Scenario C:**
- Customer service automation
- Non-technical support managers need to modify workflows
- Complex routing logic
- Needs scheduling and triggers

**Your recommendation:**
**Reasoning (could include multiple tools):**

---

**Ask the AI:**

For architecture and comparison decisions:
- "I designed [X servers] for the customer support system. Does this separation make sense, or am I over-complicating it?"
- "For Scenario A, I'm torn between MCP and LangChain because [reason]. How should I weigh these factors?"
- "What questions should I ask to determine if a project needs MCP's multi-platform support?"

---

## Part 5: Reflection Questions

### Exercise 5.1: Key Insights

Answer these reflection questions:

1. **What was the most surprising thing you learned about MCP?**

2. **What is the primary benefit of MCP in your own words?**

3. **What type of project are you most likely to use MCP for?**

4. **What questions do you still have about MCP?**

### Exercise 5.2: Real-World Application

Think about a project you're working on or want to build:

1. **Briefly describe the project:**

2. **Would MCP be appropriate? Why or why not?**

3. **If yes, what MCP servers would you build?**

4. **If no, what would you use instead?**

---

## Completion Checklist

Before moving to the next tutorial, ensure you can:

- [ ] Explain the problems MCP solves in your own words
- [ ] Distinguish between tools, resources, and prompts
- [ ] Design a basic tool with appropriate parameters
- [ ] Choose the right transport for different scenarios
- [ ] Understand the JSON-RPC message structure
- [ ] Compare MCP with alternatives and make informed choices
- [ ] Design a multi-server MCP architecture

---

## Next Steps

1. **Review your answers** with the [solution guide](./solutions/tutorial-1-answers.md)
2. **Discuss with a colleague** or in the community
3. **Move to Challenge 1** for more advanced analysis: [challenge-1-analysis.md](./challenge-1-analysis.md)
4. **Proceed to Module 02** once comfortable with concepts

---

## Additional Resources

- [MCP README](../README.md) - Fundamentals overview
- [Architecture Guide](../architecture.md) - Protocol deep dive
- [Comparison Guide](../comparison.md) - MCP vs alternatives
- [Official MCP Docs](https://modelcontextprotocol.io)

---

## Tips for Success

1. **Don't rush** - Take time to think through each question
2. **Draw diagrams** - Visual representations help understanding
3. **Discuss with others** - Explaining concepts reinforces learning
4. **Refer back to docs** - It's okay to look things up
5. **Ask questions** - Use the community or AI assistance

---

## How to Use AI Assistance

This tutorial is designed to be completed with the help of AI assistants. Here's how to use them effectively:

### Getting Started Help

If you're unsure how to begin:

```
I'm working on understanding MCP concepts. Can you help me think through 
Exercise 1.1 without giving me the answer? What should I consider when 
thinking about integration challenges?
```

### Understanding Concepts

For conceptual questions:

```
I'm trying to understand the difference between MCP tools and resources. 
Can you explain this with an analogy without directly answering Exercise 2.1?
```

```
I'm confused about JSON-RPC message flow. Can you walk me through what 
happens when a client calls a tool, step by step?
```

### Getting Unstuck

If you're stuck on a specific exercise:

```
I'm stuck on Exercise 3.1 (message flow). I understand the client connects, 
but I'm not sure what fields go in the initialize request. Can you give me 
a hint about what to look for in the architecture docs?
```

```
For Exercise 4.1, I'm not sure how to decide how many MCP servers to create. 
What factors should I consider? Don't tell me the answer, just guide my thinking.
```

### Checking Your Thinking

To validate your reasoning:

```
I think [scenario X] should use a Tool rather than a Resource because 
[your reasoning]. Is my thinking on the right track?
```

```
I designed my architecture with 3 servers: one for data access, one for 
actions, and one for knowledge base. Can you point out any issues with 
this approach without redesigning it for me?
```

### Progressive Hints

Ask for hints in stages:

```
I'm working on Exercise 4.2 comparing MCP and LangChain. 
Can you give me just the first consideration I should think about? 
Don't give me the full answer.
```

Then if you need more:

```
OK, I've considered [X]. What's another factor I should evaluate?
```

### What NOT to Ask

Avoid these approaches as they skip the learning:

- "Give me the complete answer to Exercise 1.1"
- "Write out all the JSON messages for Exercise 3.1"
- "Tell me which tool to pick for each scenario in 2.1"

### Example Conversation

**Good approach:**
1. "What should I consider when choosing between tools and resources?"
2. Read the response, think about it
3. "OK, so side effects matter. Does 'reading a log file' have side effects?"
4. Work through the reasoning
5. "I think it's a resource because... Is this correct?"

**Less effective:**
1. "Is reading a log file a tool or resource?"
2. Get answer without understanding why

---

## Need Help?

If you're stuck:

1. Review the relevant sections in the [Module 01 README](../README.md)
2. Check the [architecture.md](../architecture.md) for technical details
3. Use the AI assistance guide above to get targeted help
4. Look at the [solution guide](./solutions/tutorial-1-answers.md) for hints
5. Ask in the community discussions

Remember: Understanding concepts before coding leads to better implementations!

