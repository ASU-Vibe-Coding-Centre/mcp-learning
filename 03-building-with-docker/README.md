## Module 03: Building MCP Servers with Docker

Welcome to Module 03. In this module you will learn how to run existing containerized MCP servers from a catalog and then build, containerize, and test your own MCP servers using Docker.

This module is hands-on and split into three phases. You can complete Phase 1 independently if you only need to run existing servers, or proceed through Phases 2 and 3 to build your own.

### What You'll Learn
- Understand the Docker MCP toolkit and how containerized MCP servers are structured
- Run catalog servers locally and connect them to your MCP client (Cursor IDE)
- Build a simple MCP server from scratch and package it with Docker
- Build a practical MCP server with data persistence and multiple tools
- Test and troubleshoot containerized MCP servers across platforms

### Time Estimate
- Total: 3–4 hours
  - Phase 1: 20–30 minutes
  - Phase 2: 45–60 minutes
  - Phase 3: 60–90 minutes

### Prerequisites
- Docker Desktop installed and running (macOS, Windows) or Docker Engine (Linux)
- Completion of Module 01 (Cursor IDE MCP quickstart)
- Basic familiarity with Python if you plan to complete Phases 2–3

If you do not have Docker installed, see the Docker setup guide in `docker/README.md` from this repository before proceeding.

### Module Structure
1. Phase 1: Running Catalog Servers
   - Use pre-built container images from the Docker MCP catalog
   - Pull and run a server locally
   - Connect from Cursor IDE and test
2. Phase 2: Simple Custom Server
   - Build a minimal MCP server (e.g., dice roller, coin flip, or random quote)
   - Containerize with a small `Dockerfile`
   - Test locally via Cursor IDE
3. Phase 3: Practical Custom Server
   - Build a real utility server (e.g., notes or todos) with persistence
   - Add 3–5 tools and robust schemas
   - Containerize, run, and verify data persistence

### How to Use This Module
Work through each phase in order. Each phase has a dedicated guide:
- Phase 1: `phase-1-running-catalog-servers.md`
- Phase 2: `phase-2-simple-custom-server.md`
- Phase 3: `phase-3-practical-custom-server.md`

Examples for Phases 2 and 3 are provided under `examples/` with complete, runnable code and Dockerfiles. Follow the instructions in each phase to build and test the images locally.

### Outcomes
By the end of this module you will be able to:
- Confidently run containerized MCP servers from a catalog
- Build and package your own MCP servers using Docker
- Connect those servers to an MCP client (Cursor IDE) and validate behavior
- Troubleshoot common issues across build, run, and connection steps

### Next Steps
Ready? Start with Phase 1: `phase-1-running-catalog-servers.md`.

### Where to Go Next?
- Explore advanced topics in the `advanced/` directory:
  - `advanced/04-basic-mcp-server/` – deeper dive into server patterns
  - `advanced/05-advanced-features/` – resources, prompts, streaming
  - `advanced/06-integration-patterns/` – multi-server, API integrations, gateways

### Suggestions for Your Own Servers
- Personal knowledge tools (bookmarks, snippets, templates)
- Team utilities (lightweight ticket triage, changelog generator)
- Data tools (CSV/SQLite explorers, log filters)
- DevOps helpers (status checks, release notes)

### Community and Registry
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Docker MCP Catalog/Toolkit: https://docs.docker.com/ai/mcp-catalog-and-toolkit/
- MCP Registry (community servers): https://github.com/docker/mcp-registry

### Real-World Ideas to Try
- Bookmark manager with tags and search
- Todo/notes hybrid with due dates and priorities
- Simple passwordless contact directory for a small team


