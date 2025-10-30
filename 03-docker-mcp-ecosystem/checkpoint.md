# Module 03 Checkpoint: Docker MCP Ecosystem

Complete this checkpoint to validate your understanding of Docker's MCP infrastructure before moving to the next module.

---

## Knowledge Check

Answer these questions to test your conceptual understanding:

### 1. Docker MCP Components

**Question:** What are the four main components of the Docker MCP ecosystem?

<details>
<summary>Show Answer</summary>

1. **Docker MCP Catalog** - Centralized registry of 200+ pre-built MCP servers
2. **Docker MCP Toolkit** - GUI in Docker Desktop for managing MCP servers
3. **Docker MCP Gateway** - Orchestration layer that aggregates servers into single endpoint
4. **Docker Hub MCP Integration** - Distribution platform for publishing MCP servers

</details>

### 2. Local vs Remote Servers

**Question:** Explain the difference between local and remote MCP servers. Give an example of each.

<details>
<summary>Show Answer</summary>

**Local MCP Servers:**
- Run as containers on your machine
- Work offline once downloaded
- Complete data privacy
- Predictable performance
- Example: `mcp/filesystem`, `mcp/sqlite`, `mcp/git`

**Remote MCP Servers:**
- Hosted services accessed over internet
- Maintained by service providers
- Always up-to-date with live data
- Require internet connectivity
- Example: `mcp/github` (calls GitHub API), `mcp/stripe`, `mcp/weather`

</details>

### 3. Gateway Architecture

**Question:** Why use the MCP Gateway instead of connecting clients directly to each server?

<details>
<summary>Show Answer</summary>

**Benefits of Gateway:**
1. **Simplified Configuration** - Client connects to one endpoint, not many
2. **Centralized Management** - Single place to manage all servers
3. **Unified Security** - Authentication and authorization in one place
4. **Better Observability** - Single point for logging and monitoring
5. **Easier Scaling** - Gateway handles load balancing and routing

**Without Gateway:** Each client must configure and manage connections to every server individually.

</details>

### 4. Security Features

**Question:** What security features are built into Docker MCP Toolkit?

<details>
<summary>Show Answer</summary>

1. **Image Signing** - All official servers are digitally signed by Docker
2. **Resource Limits** - Default 1 CPU, 2GB memory per container
3. **Filesystem Isolation** - No host access by default
4. **Network Restrictions** - Limited to necessary endpoints only
5. **Secret Management** - Encrypted storage for API keys and credentials
6. **Attestation** - Verification of image source and integrity

</details>

### 5. Use Cases

**Question:** When should you use catalog servers vs building custom servers?

<details>
<summary>Show Answer</summary>

**Use Catalog Servers When:**
- Standard integration exists (GitHub, databases, filesystems)
- Want immediate availability without coding
- Need production-ready, tested tools
- Don't require customization

**Build Custom Servers When:**
- Unique business logic required
- Internal/proprietary integrations needed
- Specific customization beyond configuration
- Learning MCP fundamentals deeply

**Best Practice:** Start with catalog servers for standard needs, build custom for specialized requirements.

</details>

---

## Hands-On Validation

Complete these practical exercises to prove your skills:

### Exercise 1: Catalog Server Setup

**Task:** Install and configure a catalog server of your choice (not filesystem if you did Tutorial 1)

**Requirements:**
- [ ] Server installed from Docker MCP Catalog
- [ ] Required environment variables configured
- [ ] Server status shows "Running"
- [ ] Connected to an AI client (Claude Desktop, Cursor, etc.)
- [ ] Successfully tested at least 2 tools provided by the server

**Validation Questions:**
1. Which server did you install?
2. What environment variables were required?
3. What tools does it provide?
4. Show a screenshot or describe a successful tool call

---

### Exercise 2: Multiple Servers

**Task:** Set up 2-3 different MCP servers running simultaneously

**Requirements:**
- [ ] At least 2 servers installed and running
- [ ] Each server properly configured
- [ ] All connected through single Gateway endpoint
- [ ] Can use tools from different servers in same conversation

**Validation Questions:**
1. Which servers are you running?
2. Can you use tools from different servers in a single AI conversation?
3. How much memory are all servers using combined?
4. What's the Gateway endpoint URL?

---

### Exercise 3: Configuration Management

**Task:** Configure a server with custom settings and secrets

**Requirements:**
- [ ] Server installed (e.g., mcp/github requires GitHub token)
- [ ] At least one secret configured securely
- [ ] Custom environment variables beyond defaults
- [ ] Server works with configured settings

**Validation Questions:**
1. What secret did you configure?
2. How did you verify the secret was stored securely?
3. What happens if you provide an invalid secret?

---

## Conceptual Challenges

Test your deeper understanding:

### Challenge 1: Architecture Design

**Scenario:** You're building an AI assistant for developers that needs:
- Git operations
- GitHub API access
- File system operations
- PostgreSQL database access
- Slack notifications

**Questions:**
1. Which catalog servers would you use?
2. Would you use Gateway or direct connections? Why?
3. What security considerations matter?
4. Draw or describe the architecture

<details>
<summary>Show Answer</summary>

**Recommended Servers:**
1. `mcp/git` - Local git operations
2. `mcp/github` - GitHub API (requires token)
3. `mcp/filesystem` - File operations
4. `mcp/postgres` - Database access
5. `mcp/slack` - Slack notifications

**Architecture:**
```
Claude Desktop
     │
     └─→ MCP Gateway (localhost:3000)
            ├─→ mcp/git (local)
            ├─→ mcp/github (remote API)
            ├─→ mcp/filesystem (local)
            ├─→ mcp/postgres (local/remote DB)
            └─→ mcp/slack (remote API)
```

**Use Gateway because:**
- Single configuration in Claude Desktop
- Centralized secret management (GitHub token, Slack token, DB credentials)
- Unified logging of all tool calls
- Easy to add/remove servers

**Security Considerations:**
- Store all API keys/tokens as secrets in Gateway
- Limit filesystem ROOT_PATH to project directory only
- Use read-only database user if possible
- Configure resource limits per server
- Review Slack permissions carefully

</details>

---

### Challenge 2: Publishing Decision

**Scenario:** You built a custom MCP server for internal company use that connects to your proprietary CRM system.

**Questions:**
1. Should you publish this to the Docker MCP Catalog? Why or why not?
2. If yes, what would you need to do?
3. If no, how would you distribute it internally?

<details>
<summary>Show Answer</summary>

**Should NOT publish to public Docker MCP Catalog because:**
- Proprietary/internal system (not useful to public)
- May contain company-specific logic
- Security: Don't expose internal API details
- Maintenance burden for public consumption

**Internal Distribution Options:**

**Option 1: Private Docker Registry**
```bash
# Build and tag
docker build -t company-registry.com/mcp/crm-server:1.0.0 .

# Push to private registry
docker push company-registry.com/mcp/crm-server:1.0.0

# Team members pull
docker pull company-registry.com/mcp/crm-server:1.0.0
```

**Option 2: Internal Documentation**
- Provide Dockerfile in company Git repo
- Document build and configuration steps
- Team builds locally as needed

**Option 3: Shared Docker Image File**
- Export: `docker save mcp/crm-server > crm-server.tar`
- Share via internal file system
- Import: `docker load < crm-server.tar`

**If It Were Public-Appropriate:**
1. Remove company-specific code/config
2. Generalize for multiple CRM systems
3. Add comprehensive documentation
4. Create example configurations
5. Submit to docker/mcp-registry on GitHub
6. Follow contribution guidelines
7. Wait for Docker team review and approval

</details>

---

### Challenge 3: Troubleshooting

**Scenario:** A colleague says: "I installed mcp/github from the catalog but Claude says it can't access my repositories."

**Questions:**
1. What are 5 things you would check?
2. How would you diagnose the issue step-by-step?
3. What's the most likely problem?

<details>
<summary>Show Answer</summary>

**5 Things to Check:**

1. **Server Status**
   - Is server showing "Running" in MCP Toolkit?
   - Check server logs for errors

2. **GitHub Token**
   - Is GITHUB_TOKEN environment variable set?
   - Is the token valid and not expired?
   - Does token have correct permissions (repo, read:org)?

3. **Client Connection**
   - Is Claude Desktop connected to Gateway?
   - Did they restart Claude after setup?
   - Can they see other MCP servers?

4. **Network Access**
   - Can the server reach api.github.com?
   - Is there a firewall blocking?
   - Try: `docker exec <container> curl https://api.github.com`

5. **Repository Access**
   - Does the token have access to the specific repos?
   - Are repos private or public?
   - Test token manually with GitHub API

**Diagnosis Steps:**

```bash
# Step 1: Check server is running
# In MCP Toolkit, verify status is "Running"

# Step 2: Check logs
# Click "View Logs" in toolkit
# Look for authentication errors

# Step 3: Test GitHub token manually
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/user

# Step 4: Verify in Claude
# Ask: "What MCP tools do you have access to?"
# Should list github tools

# Step 5: Test simple operation
# Ask: "List my GitHub repositories"
# Check if specific error message appears
```

**Most Likely Problem:**
Missing or invalid GITHUB_TOKEN. The server requires a personal access token with appropriate permissions, and this is a common setup oversight.

**Solution:**
1. Generate GitHub personal access token
2. Add as secret in MCP Toolkit
3. Restart mcp/github server
4. Restart Claude Desktop

</details>

---

## Self-Assessment

Rate your understanding (be honest!):

### Docker MCP Catalog
- [ ] I can browse and search the catalog
- [ ] I understand local vs remote server types
- [ ] I can read and interpret server metadata
- [ ] I know how to check server requirements
- [ ] I can identify which catalog server fits a use case

### Docker MCP Toolkit
- [ ] I can install servers via GUI
- [ ] I can configure environment variables
- [ ] I can manage secrets securely
- [ ] I can start/stop/monitor servers
- [ ] I understand resource limits
- [ ] I can connect clients through Gateway

### Docker MCP Gateway
- [ ] I understand Gateway's role as aggregator
- [ ] I know why Gateway simplifies client configuration
- [ ] I can explain Gateway vs direct connection trade-offs
- [ ] I understand security benefits of Gateway
- [ ] I could set up standalone Gateway if needed

### Publishing & Distribution
- [ ] I understand contribution process to catalog
- [ ] I know requirements for published servers
- [ ] I can build Docker images for MCP servers
- [ ] I understand image signing and verification
- [ ] I know when to publish vs keep private

---

## Minimum Passing Criteria

To consider this module complete, you should:

**Knowledge:**
- ✅ Correctly answer at least 4 of 5 knowledge check questions
- ✅ Complete at least 2 of 3 hands-on validation exercises
- ✅ Attempt at least 2 of 3 conceptual challenges

**Practical Skills:**
- ✅ Successfully installed and ran at least 1 catalog server
- ✅ Connected server to an AI client
- ✅ Configured environment variables or secrets
- ✅ Used tools from server in AI conversation

**Self-Assessment:**
- ✅ Rated yourself competent in at least 3 areas per section
- ✅ Can explain Docker MCP ecosystem to a colleague
- ✅ Feel confident exploring catalog independently

---

## What's Next?

### If You Passed

**Next Module Options:**

1. **Module 04: Basic MCP Server** - Learn to build servers from scratch
   - Understand what catalog servers do internally
   - Implement custom business logic
   - Deep dive into MCP protocol

2. **Module 06: Integration Patterns** - Skip ahead to integrations
   - Advanced Gateway configurations
   - Multi-server architectures
   - Production deployment patterns

### If You Need More Practice

**Additional Exercises:**
1. Install 5 different catalog servers
2. Create a multi-server workflow (e.g., read from filesystem, process, write to database)
3. Experiment with resource limits and monitoring
4. Try standalone Gateway setup
5. Build a simple Docker image for custom server

**Resources:**
- Re-read [Module 03 README](../README.md)
- Review [Docker MCP official docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- Try different catalog servers
- Join Docker community forums for help

---

## Checkpoint Completion

**Date Completed:** _______________

**Servers Mastered:** _______________

**Tools Used Successfully:** _______________

**Most Challenging Concept:** _______________

**Most Useful Discovery:** _______________

**Ready for Next Module:** ☐ Yes  ☐ Need more practice

---

**Congratulations on completing Module 03!**

You now understand Docker's MCP ecosystem and can leverage pre-built servers for immediate productivity. You're ready to either build your own servers (Module 04) or jump to advanced integrations (Module 06).

**Next:** [Module 04: Basic MCP Server](../04-basic-mcp-server/README.md) OR [Module 06: Integration Patterns](../06-integration-patterns/README.md)

