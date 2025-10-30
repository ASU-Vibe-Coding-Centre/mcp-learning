# Module 02: Building with n8n

Build a simple bidirectional MCP setup in n8n: one workflow exposes MCP tools (server), another calls those tools (client). This module is hands-on and follows the concepts from Module 01.

## Objectives
- Understand what n8n is and how it orchestrates workflows
- Create an MCP Server workflow that exposes simple tools
- Create an MCP Client workflow that calls your server via MCP
- Test both ends and see the bidirectional pattern in action

## Time Estimate
30–45 minutes

## Prerequisites
- n8n account (Cloud or self‑hosted)
- Completed Module 01: Introduction & QuickStart (Cursor configured for MCP)
- Basic comfort with HTTP requests and JSON

## What You’ll Build
- Workflow A (MCP Server): Exposes simple tools (e.g., greeting, calculator, timestamp)
- Workflow B (MCP Client): Receives input, uses AI to parse intent, then calls Workflow A via MCP

## Sections
1. What is n8n?
2. Why Combine n8n with MCP?
3. Tutorial: Workflow A – MCP Server
4. Tutorial: Workflow B – MCP Client
5. Testing Your Workflows
6. Understanding the Bidirectional Pattern
7. Troubleshooting
8. What You Just Built
9. Exercises (Optional)

## Navigation
- Tutorial: see `tutorial-simple-workflow.md`
- Examples: exported JSON files in `examples/`
- Exercises: step‑by‑step challenges in `exercises/`

## Expected Outcomes
By the end, you will be able to:
- Configure n8n nodes to host MCP tools and to call MCP tools
- Move data between workflows using HTTP triggers and MCP nodes
- Validate end‑to‑end behavior with example requests and responses

---

Ready? Start with the tutorial in `tutorial-simple-workflow.md`.


