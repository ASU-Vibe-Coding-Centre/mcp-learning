# MCP Server Learning Repository

Learn to build AI tools with Model Context Protocol - from beginner to builder in 4-6 hours.

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that lets AI assistants like Claude and Cursor connect to external tools and data. Think of it as a universal plug that allows AI to interact with your databases, APIs, file systems, and services.

Instead of building custom integrations for every AI application, you build one MCP server that works everywhere. It's like creating an API, but specifically designed for AI assistants to discover and use your tools automatically.

## Why MCP Matters

- **Build Once, Use Everywhere**: Your MCP server works with Claude, Cursor IDE, and any MCP-compatible AI application
- **AI-Native Design**: Tools are described in a way AI models understand and can use automatically
- **Growing Ecosystem**: Connect to 200+ pre-built servers or build custom tools for your needs
- **Simple to Start**: Get your first server running in 10 minutes, build custom servers in a few hours

## When to Use MCP

**Use MCP when:**
- You want AI assistants to access your tools, databases, or services
- You're building tools that multiple AI applications should use
- You need a standard way for AI to interact with your systems

**Consider alternatives when:**
- You're building quick prototypes (start simple, add MCP later)
- Everything runs in a single application with no need for external AI access

## What You'll Learn

This repository teaches you to build MCP servers through three hands-on modules:

### Module 01: Introduction & QuickStart
**Time:** 30-45 minutes

Understand MCP concepts and connect your first server to Cursor IDE in 10 minutes. No coding required - just configuration and testing.

**You'll Learn:**
- What MCP is and why it exists
- How AI assistants discover and use tools
- Connecting a free MCP server from mcp.so

### Module 02: Building with n8n
**Time:** 30-45 minutes

Build a simple workflow automation that works as an MCP server. Perfect for creating tools without writing much code.

**You'll Learn:**
- Creating MCP server workflows in n8n
- Calling MCP tools from other workflows
- The bidirectional server/client pattern

### Module 03: Building with Docker
**Time:** 3-4 hours

Build two custom MCP servers from scratch - one simple (dice roller/quotes) and one practical (notes/todos). Complete with Docker packaging.

**You'll Learn:**
- Running pre-built servers from Docker's MCP Catalog
- Building a simple fun server (dice, coins, quotes)
- Building a practical utility server (notes, todos, bookmarks)
- Packaging servers with Docker for easy distribution

**Total Learning Time:** 4-6 hours from start to finish

## Prerequisites

**You'll Need:**
- Basic Python knowledge (functions, variables)
- Comfort with command-line basics
- Docker installed (for Module 03)
- Cursor IDE or Claude Desktop (for testing)

**No Prior Experience Needed:**
- No AI/ML knowledge required
- No MCP experience needed
- No advanced Python skills required

## Get Started

**Quick Start** (10 minutes):
```bash
# 1. Visit https://mcp.so to find free MCP servers
# 2. Follow Module 01's quickstart guide
# 3. Connect a server to Cursor IDE
# 4. Test it with example prompts
```

**Ready to Learn?**

Start with **[Module 01: Introduction & QuickStart](01-introduction-quickstart/)** →

## Learning Paths

### Fast Track (2 hours)
Perfect for getting hands-on quickly:
1. Module 01: QuickStart guide only (10 min)
2. Module 03: Phase 1 - Run a catalog server (20 min)
3. Module 03: Phase 2 - Build simple server (60 min)

### Complete Path (4-6 hours)
Full learning experience:
1. Module 01: Introduction & QuickStart (45 min)
2. Module 02: Building with n8n (45 min)
3. Module 03: Building with Docker (3-4 hours)
4. Optional exercises throughout

### Implementation-Focused (3-4 hours)
Jump straight to building:
1. Module 01: Concepts only (15 min)
2. Module 03: All three phases (3-4 hours)

## Repository Structure

```
mcp-server/
├── 01-introduction-quickstart/    # Concepts + 10-min quickstart
├── 02-building-with-n8n/           # Workflow automation approach
├── 03-building-with-docker/        # Build custom servers
├── advanced/                       # Deep-dive content (16-23 hours)
│   ├── 01-introduction/            # Protocol details
│   ├── 02-environment-setup/       # Advanced setup
│   ├── 03-docker-mcp-ecosystem/    # Docker deep dive
│   ├── 04-basic-mcp-server/        # Server fundamentals
│   ├── 05-advanced-features/       # Streaming, resources, prompts
│   ├── 06-integration-patterns/    # Production patterns
│   ├── 07-security-best-practices/ # Security hardening
│   └── 08-debugging-troubleshooting/ # Debug strategies
└── docker/                         # Docker configurations
```

## Time Investment

| Module | Time | What You'll Build |
|--------|------|-------------------|
| **01: Intro & QuickStart** | 30-45 min | Connected MCP server (using existing) |
| **02: n8n** | 30-45 min | Workflow-based MCP server |
| **03: Docker** | 3-4 hours | Two custom servers + Docker packaging |
| **Total** | **4-6 hours** | **Three working implementations** |

## Resources

- **[Official MCP Documentation](https://modelcontextprotocol.io/)** - Protocol specification
- **[mcp.so](https://mcp.so)** - Discover free MCP servers
- **[Docker MCP Catalog](https://hub.docker.com/u/mcp)** - 200+ pre-built servers
- **[NetworkChuck's Docker MCP Tutorial](https://github.com/theNetworkChuck/docker-mcp-tutorial)** - Additional Docker examples

## Ready for More?

After completing the main modules, explore the **[advanced/ directory](advanced/)** for:
- In-depth protocol details
- Production deployment patterns
- Security and debugging strategies
- Advanced integration techniques

Total advanced content: 16-23 hours

## Support

- **Questions**: Open an issue on GitHub
- **Bugs**: Report in GitHub issues
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE) file

---

**Start Learning:** [Module 01: Introduction & QuickStart](01-introduction-quickstart/) →

Built by [ASU Vibe Coding Centre](https://github.com/ASU-Vibe-Coding-Centre)
