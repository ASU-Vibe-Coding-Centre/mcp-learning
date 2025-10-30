# Module 01 Checkpoint: Introduction to MCP

This checkpoint validates your understanding of MCP fundamentals before proceeding to hands-on implementation.

**Estimated Time**: 30-45 minutes

---

## Purpose

This checkpoint ensures you can:
- Explain MCP concepts clearly
- Make informed architecture decisions
- Understand when MCP is appropriate
- Distinguish between MCP and alternatives

**Passing Criteria**: You should feel confident in your answers to at least 80% of the questions.

---

## Part 1: Core Concepts (Essential)

### Question 1: What is MCP?

In 2-3 sentences, explain what the Model Context Protocol is and why it exists.

```
Your answer:




```

**Self-Check**: Did you mention:
- [ ] It's a protocol (not a framework)
- [ ] For AI-to-external-system communication
- [ ] Standardization benefit

---

### Question 2: Tools, Resources, and Prompts

For each scenario, identify whether it should be a **Tool**, **Resource**, or **Prompt**:

| Scenario | Type | Justification |
|----------|------|---------------|
| Send an email to a customer | | |
| Read the contents of a configuration file | | |
| Delete all files in a directory | | |
| Provide a template for code review | | |
| Fetch user data from database | | |
| Calculate the factorial of a number | | |
| Template for translating text | | |

**Self-Check**: 
- Resources are read-only data access
- Tools perform actions or have side effects
- Prompts are reusable templates

---

### Question 3: Protocol Architecture

Draw or describe the MCP protocol stack (all 4 layers) and what each layer does:

```
Layer 4 (Top):

Layer 3:

Layer 2:

Layer 1 (Bottom):
```

**Self-Check**: Layers should be:
- [ ] Application Layer (tools, resources, prompts)
- [ ] Protocol Layer (MCP-specific methods)
- [ ] Message Layer (JSON-RPC 2.0)
- [ ] Transport Layer (stdio, HTTP, WebSockets)

---

### Question 4: Client-Server Model

True or False (and explain why):

1. **T/F**: In MCP, the AI model is the client.
   - **Your answer**: 
   - **Why**: 

2. **T/F**: You typically build the MCP client.
   - **Your answer**: 
   - **Why**: 

3. **T/F**: One MCP server can only connect to one client at a time.
   - **Your answer**: 
   - **Why**: 

4. **T/F**: MCP servers must run on the same machine as the client.
   - **Your answer**: 
   - **Why**: 

**Self-Check Answers**:
1. True - The client runs alongside/within the AI model
2. False - Clients are provided by platforms (Claude Desktop, etc.)
3. False - Depends on transport; HTTP can support multiple clients
4. False - Depends on transport; HTTP allows remote servers

---

## Part 2: Protocol Details (Important)

### Question 5: JSON-RPC Messages

Given this tool call, write the JSON-RPC request and response:

**Tool**: `search_database`
**Parameters**: `{ "query": "users with age > 30", "limit": 10 }`
**Result**: Found 3 users

```json
// Request:
{



}

// Response:
{



}
```

**Self-Check**: Did you include:
- [ ] `jsonrpc: "2.0"`
- [ ] `id` field (matching in response)
- [ ] `method: "tools/call"`
- [ ] Correct params structure
- [ ] Result wrapped in content array

---

### Question 6: Transport Selection

For each scenario, choose the best transport (stdio, HTTP+SSE, or WebSockets):

**Scenario A**: Claude Desktop extension
- **Your choice**: 
- **Why**: 

**Scenario B**: Company-wide shared database access server
- **Your choice**: 
- **Why**: 

**Scenario C**: Real-time collaborative coding tool
- **Your choice**: 
- **Why**: 

**Self-Check**:
- stdio: Local, simple, subprocess model
- HTTP+SSE: Remote, multiple clients, web-compatible
- WebSockets: Real-time bidirectional, low latency

---

### Question 7: Capability Negotiation

What happens during the initialization sequence? List the steps in order:

```
1.

2.

3.

4.
```

**Self-Check**: Should include:
1. Client sends `initialize` request with client capabilities
2. Server responds with server capabilities
3. Client sends `initialized` notification
4. Normal operations begin

---

## Part 3: Comparison & Decision Making (Critical)

### Question 8: MCP vs LangChain

Complete this comparison:

| Aspect | MCP | LangChain |
|--------|-----|-----------|
| **Type** | | |
| **Primary purpose** | | |
| **Best for** | | |
| **Not ideal for** | | |

**Self-Check**:
- MCP: Protocol for standardization
- LangChain: Framework for AI applications
- They solve different (but related) problems

---

### Question 9: When to Use MCP

For each requirement, indicate if it suggests using MCP (Yes/No) and why:

1. **Need tools to work across Claude and GPT-4**
   - MCP appropriate? 
   - Why: 

2. **Building internal tool, only using Python with LangChain**
   - MCP appropriate? 
   - Why: 

3. **Complex workflow with branching logic and non-technical users**
   - MCP appropriate? 
   - Why: 

4. **Building IDE extensions for multiple editors**
   - MCP appropriate? 
   - Why: 

5. **Need to share expensive resources across multiple AI apps**
   - MCP appropriate? 
   - Why: 

**Self-Check**:
- Cross-platform → MCP strength
- Single deployment, using framework → LangChain ok
- Workflow complexity + non-tech users → n8n
- Multi-IDE → MCP strength
- Shared resources → MCP strength

---

### Question 10: Architecture Design

**Scenario**: Build an AI assistant for a development team that needs to:
- Query Jira for tickets
- Search codebase (GitHub)
- Access team documentation (Confluence)
- Run code linters

**Your Task**: Design the MCP architecture

```
Number of MCP servers:

Server 1:
  Name:
  Purpose:
  Tools:
  Resources:

Server 2:
  Name:
  Purpose:
  Tools:
  Resources:

(Add more if needed)

Why this design?:


```

**Self-Check**: 
- Logical grouping of related capabilities
- Clear separation of concerns
- Appropriate use of tools vs resources

---

## Part 4: Practical Understanding (Essential)

### Question 11: Tool Design

Design a tool for this requirement:

**Requirement**: "Search GitHub repositories for code matching a pattern"

```
Tool name:

Description:

Input parameters:
  - 
  - 
  - 

Output structure:
{

}

Error cases to handle:
  1.
  2.
```

**Self-Check**:
- Clear, descriptive name
- All necessary parameters
- Structured output
- Error handling considered

---

### Question 12: Resource Design

Design resources for accessing weather data:

**Requirement**: "Provide weather data for cities, with current conditions and forecasts"

```
Resource URI pattern:


Description:


Example URIs:
  1.
  2.
  3.

What data does each resource return?:


```

**Self-Check**:
- URI pattern uses variables
- Clear examples
- Read-only access (resources don't modify)

---

### Question 13: Security Considerations

For a healthcare MCP server handling patient data, list 5 security considerations:

```
1.

2.

3.

4.

5.
```

**Self-Check**: Should consider:
- Authentication/authorization
- Encryption (in transit and at rest)
- Audit logging
- Input validation
- Data minimization

---

## Part 5: Critical Thinking (Advanced)

### Question 14: Trade-offs

Explain the trade-offs for each decision:

**Decision 1**: Use multiple specialized MCP servers vs one server with all capabilities

```
Multiple servers:
  Pros:


  Cons:


One server:
  Pros:


  Cons:


```

**Decision 2**: Use stdio vs HTTP transport

```
stdio:
  Pros:


  Cons:


HTTP:
  Pros:


  Cons:


```

---

### Question 15: Problem Solving

**Problem**: Your MCP server handles 1000 requests/second and response time is degrading.

```
What could be causing this?
1.

2.

3.

How would you investigate?
1.

2.

What optimizations might help?
1.

2.

3.
```

---

## Part 6: Readiness Assessment

### Self-Evaluation

Rate your confidence (1-5, 5 = very confident):

**Core Concepts:**
- Understanding what MCP is: ___/5
- Tools, resources, and prompts: ___/5
- Protocol architecture: ___/5
- Client-server model: ___/5

**Technical Details:**
- JSON-RPC message format: ___/5
- Transport options: ___/5
- Capability negotiation: ___/5

**Decision Making:**
- When to use MCP vs alternatives: ___/5
- Designing MCP architectures: ___/5
- Security considerations: ___/5

**Overall Confidence**: ___/5

### Knowledge Gaps

What topics do you still feel unclear about?

```
1.

2.

3.
```

### Action Plan

For each knowledge gap, what will you do?

```
Gap 1 → Action:

Gap 2 → Action:

Gap 3 → Action:
```

---

## Validation

### Minimum Requirements to Proceed

You should be able to:

- [ ] Explain MCP in your own words
- [ ] Distinguish tools, resources, and prompts
- [ ] Describe the protocol architecture
- [ ] Write basic JSON-RPC messages
- [ ] Choose appropriate transports
- [ ] Compare MCP with alternatives
- [ ] Design a simple MCP architecture
- [ ] Identify security considerations
- [ ] Make informed trade-off decisions

### Recommended Actions

**If you checked 9-10 boxes above:**
- You're ready for Module 02: Environment Setup
- Proceed with confidence

**If you checked 7-8 boxes:**
- Review specific unclear topics
- Re-read relevant sections of the README or architecture guide
- Retry the checkpoint
- Then proceed to Module 02

**If you checked fewer than 7 boxes:**
- Review the entire module carefully
- Complete the exercises again
- Discuss concepts with peers or mentors
- Retry the checkpoint before proceeding

---

## Next Steps

1. **Review Your Answers**: 
   - Compare with solution guides for exercises
   - Identify areas needing more study

2. **Fill Knowledge Gaps**:
   - Re-read specific sections
   - Complete additional exercises
   - Ask questions in community

3. **Proceed to Module 02**:
   - [Environment Setup](../02-environment-setup/README.md)
   - Set up your development environment
   - Install MCP SDK and tools

---

## Additional Resources

**If You Need More Practice:**
- Re-read [README.md](./README.md) for fundamentals
- Deep dive into [architecture.md](./architecture.md)
- Study [comparison.md](./comparison.md) for decision-making
- Redo [Tutorial 1](./exercises/tutorial-1-exploration.md)
- Attempt [Challenge 1](./exercises/challenge-1-analysis.md) again

**If You're Confused:**
- Ask in community discussions
- Use AI assistance with lesson prompts
- Discuss with colleagues
- Take a break and come back fresh

---

## Remember

- **Understanding > Memorization**: Focus on grasping concepts, not memorizing details
- **It's OK to review**: Architecture takes time to internalize
- **Practice helps**: The more you engage with these concepts, the clearer they become
- **Ask questions**: No question is too basic

**You're building a foundation for practical MCP development. Take the time to understand these concepts deeply.**

---

**Ready to proceed?** Head to [Module 02: Environment Setup](../02-environment-setup/README.md)!

