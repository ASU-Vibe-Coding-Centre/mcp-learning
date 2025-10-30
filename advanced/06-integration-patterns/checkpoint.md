# Module 05 Checkpoint: Integration Patterns

This checkpoint validates your understanding of real-world MCP integration. Complete all sections to ensure you're ready to deploy MCP servers in production.

## Purpose

This checkpoint helps you:

1. Verify understanding of integration workflows
2. Confirm ability to connect servers to real AI applications
3. Assess readiness for production deployment
4. Validate debugging and troubleshooting skills

## Estimated Time

45-60 minutes

## Prerequisites

Before starting, you should have:

- Completed Module 03 (Basic MCP Server)
- Completed Module 04 (Advanced Features) recommended
- Access to Cursor IDE or MCP Inspector
- Understanding of the example servers (GitHub, Git)

---

## Part 1: Configuration & Setup

### Question 1: Cursor IDE Config

**Q:** Where is the Cursor IDE configuration file located on your system?

<details>
<summary>Click to reveal answer</summary>

**Location depends on OS:**

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

**Note:** You may need to create this file if it doesn't exist.
</details>

### Question 2: Server Configuration

**Q:** What are the three required fields in an MCP server configuration?

<details>
<summary>Click to reveal answer</summary>

1. **Server ID** (the key): Unique identifier for the server
2. **command**: Executable to run (e.g., `python`, `node`)
3. **args**: Array of arguments (path to server script, etc.)

**Optional but common:**
- **env**: Environment variables (API keys, config)

**Example:**
```json
{
  "my-server": {
    "command": "python",
    "args": ["/path/to/server.py"],
    "env": {
      "API_KEY": "secret"
    }
  }
}
```
</details>

### Question 3: Environment Variables

**Q:** Why use environment variables for API keys instead of hardcoding them?

<details>
<summary>Click to reveal answer</summary>

**Security reasons:**

1. **Not in version control**: Env vars don't get committed to Git
2. **Different per environment**: Dev/staging/prod can have different keys
3. **Easy rotation**: Change keys without changing code
4. **Access control**: OS-level permissions control who sees them
5. **Auditing**: Easier to track who accessed secrets

**Bad:**
```python
GITHUB_TOKEN = "ghp_abc123..."  # Committed to repo!
```

**Good:**
```python
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
```
</details>

---

## Part 2: Debugging & Testing

### Question 4: MCP Inspector

**Q:** What is MCP Inspector and when should you use it?

<details>
<summary>Click to reveal answer</summary>

**What it is:**
- Official debugging tool for MCP servers
- Provides web UI for testing
- Shows raw JSON-RPC messages
- Works like Postman for MCP

**When to use:**
- **During development**: Test new tools before connecting to Claude
- **Debugging**: See exact request/response messages
- **Schema validation**: Verify tool schemas are correct
- **Performance**: Measure response times

**Usage:**
```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector python my_server.py
```

**Opens browser at:** `http://localhost:5173`
</details>

### Question 5: Common Connection Issues

**Q:** Your server starts successfully but doesn't appear in Cursor IDE. What should you check?

<details>
<summary>Click to reveal answer</summary>

**Checklist:**

1. **Configuration file location**: Is it in the right place?
2. **JSON syntax**: Is the config valid JSON? (use jsonlint.com)
3. **File paths**: Are paths absolute? Do they exist?
4. **Command**: Is the command available in PATH?
5. **Permissions**: Can the file be executed?
6. **Restart Claude**: Did you restart after config changes?
7. **Logs**: Check Cursor IDE logs for errors

**Common mistakes:**
```json
{
  "command": "python",
  "args": ["./server.py"]  // BAD: Relative path
}
```

**Better:**
```json
{
  "command": "python",
  "args": ["/absolute/path/to/server.py"]  // GOOD
}
```
</details>

### Question 6: Rate Limiting

**Q:** Your GitHub server works initially but then starts failing. What's likely wrong?

<details>
<summary>Click to reveal answer</summary>

**Most likely: Rate limit exceeded**

**GitHub API Limits:**
- **Without auth**: 60 requests/hour
- **With auth token**: 5,000 requests/hour

**Solutions:**

1. **Add authentication**:
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_your_token"
  }
}
```

2. **Implement caching**:
```python
cache = APICache(ttl=300)  # Cache for 5 minutes
```

3. **Check rate limit status**:
```python
# Include rate_limit_status tool in your server
```

4. **Graceful handling**:
```python
if not rate_limiter.is_allowed():
    return error_message_with_retry_time()
```
</details>

---

## Part 3: Real-World Patterns

### Question 7: Multi-Server Architecture

**Q:** When should you use multiple MCP servers instead of one?

<details>
<summary>Click to reveal answer</summary>

**Use multiple servers when:**

1. **Different Domains**
   - Git server for version control
   - Database server for data
   - API server for external integrations
   - Each handles distinct functionality

2. **Security Boundaries**
   - Read-only vs write operations
   - Different permission levels
   - Separate sensitive operations

3. **Different Technologies**
   - Python server for ML tasks
   - Node.js server for web APIs
   - Each uses best tool for the job

4. **Team Ownership**
   - Frontend team owns UI server
   - Backend team owns API server
   - Clear ownership boundaries

5. **Performance**
   - Distribute load across servers
   - Prevent one slow operation blocking others

**Example configuration:**
```json
{
  "mcpServers": {
    "git": { "command": "python", "args": ["git_server.py"] },
    "github": { "command": "python", "args": ["github_server.py"] },
    "database": { "command": "python", "args": ["db_server.py"] }
  }
}
```
</details>

### Question 8: Error Handling

**Q:** What makes a good error message in an MCP server?

<details>
<summary>Click to reveal answer</summary>

**Good error messages are:**

1. **Clear**: Explain what went wrong
2. **Actionable**: Tell user how to fix it
3. **Safe**: Don't leak sensitive information
4. **Contextual**: Include relevant details

**Examples:**

**Bad:**
```python
return [TextContent(type="text", text="Error")]
```

**Good:**
```python
return [TextContent(
    type="text",
    text="GitHub API rate limit exceeded. Your limit resets at 14:30 UTC (in 15 minutes). Try again after that time."
)]
```

**Bad (leaks info):**
```python
text=f"Error: Could not access /Users/admin/.ssh/id_rsa"
```

**Good (safe):**
```python
text="Authentication failed. Please check your credentials."
```

**Pattern:**
```python
try:
    result = dangerous_operation()
except SpecificError as e:
    # User-friendly message with solution
    return [TextContent(type="text", text=f"Error: {explain_and_suggest_fix(e)}")]
except Exception as e:
    # Log detailed error server-side
    logger.error(f"Unexpected error: {e}", exc_info=True)
    # Generic message to user
    return [TextContent(type="text", text="An unexpected error occurred. Please try again.")]
```
</details>

### Question 9: Caching Strategy

**Q:** You're building an API integration server. Where should you implement caching?

<details>
<summary>Click to reveal answer</summary>

**Cache at these levels:**

**1. API Response Level** (Recommended)
```python
class APICache:
    def get(self, endpoint: str):
        # Check if cached and not expired
        if cached and not_expired:
            return cached_data
        return None
    
    def set(self, endpoint: str, data):
        # Store with timestamp
        cache[endpoint] = (data, time.time())
```

**When to cache:**
- **Frequently accessed data**: User profiles, repo info
- **Slow operations**: Complex API queries
- **Rate-limited APIs**: Reduce request count
- **Relatively static data**: Documentation, schemas

**When NOT to cache:**
- **Real-time data**: Stock prices, live scores
- **User-specific actions**: Creating issues, posting comments
- **Security-sensitive**: Auth tokens, private data

**TTL Guidelines:**
- **Stable data** (docs, schemas): 1 hour+
- **Semi-stable** (repo info): 5-15 minutes
- **Frequently changing** (issue lists): 1-5 minutes

**Example:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_repo_info":
        cache_key = f"repo:{arguments['owner']}/{arguments['repo']}"
        
        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Fetch from API
        data = api.get_repo(...)
        
        # Cache for 5 minutes
        cache.set(cache_key, data, ttl=300)
        return data
```
</details>

### Question 10: Security

**Q:** What security checks should every resource implementation include?

<details>
<summary>Click to reveal answer</summary>

**Essential security checks:**

**1. Path Traversal Prevention**
```python
def is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False  # target is outside base

if not is_safe_path(PROJECT_ROOT, file_path):
    raise PermissionError("Access denied")
```

**2. URI Scheme Validation**
```python
if not uri.startswith("file:///"):
    raise ValueError("Invalid URI scheme")
```

**3. File Type Restrictions**
```python
ALLOWED_EXTENSIONS = {'.md', '.txt', '.json', '.py'}
if file_path.suffix not in ALLOWED_EXTENSIONS:
    raise ValueError("File type not allowed")
```

**4. Existence Checks**
```python
if not file_path.exists():
    raise ValueError("Resource not found")

if not file_path.is_file():
    raise ValueError("Not a file")
```

**5. Permission Checks**
```python
try:
    with open(file_path, 'r') as f:
        content = f.read()
except PermissionError:
    raise PermissionError("Access denied")
```

**6. Safe Error Messages**
```python
# DON'T leak paths
# Bad: f"Error: /Users/admin/secrets/api_key.txt not found"

# DO provide generic messages
# Good: "Resource not found"
```

**Complete example:**
```python
@app.read_resource()
async def read_resource(uri: str) -> str:
    # 1. Validate scheme
    if not uri.startswith("file:///"):
        raise ValueError("Invalid URI")
    
    # 2. Parse path
    file_path = uri_to_path(uri)
    
    # 3. Check bounds
    if not is_safe_path(BASE_DIR, file_path):
        raise PermissionError("Access denied")
    
    # 4. Check existence
    if not file_path.exists():
        raise ValueError("Not found")
    
    # 5. Check type
    if not file_path.is_file():
        raise ValueError("Not a file")
    
    # 6. Read safely
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError("Binary file")
    except PermissionError:
        raise PermissionError("Access denied")
```
</details>

---

## Part 4: Practical Exercise

Create a complete integration that demonstrates all concepts learned.

### Exercise: Multi-Server Setup

**Objective:** Configure and test a multi-server setup with Cursor IDE.

**Requirements:**

1. **Configure Three Servers:**
   - Basic calculator (from Module 03)
   - Git operations (from Module 05)
   - One custom server of your choice

2. **Create Configuration File:**
   - Valid JSON syntax
   - Absolute paths
   - Environment variables where appropriate
   - Clear server IDs

3. **Test Each Server:**
   - Verify each server starts independently with Inspector
   - Test key tools from each server
   - Confirm all servers work together in Cursor IDE

4. **Document:**
   - Configuration file location
   - How to set environment variables
   - Common issues and solutions
   - Example queries for each server

**Success Criteria:**

- [ ] Configuration file is valid JSON
- [ ] All three servers appear in Cursor IDE
- [ ] Can successfully call tools from each server
- [ ] Servers don't interfere with each other
- [ ] Error messages are clear and helpful
- [ ] Documentation is complete

**Time Limit:** 30 minutes

---

## Part 5: Troubleshooting Scenarios

Debug these common issues:

### Scenario 1: Server Not Appearing

```json
{
  "mcpServers": {
    "myserver": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

**Q:** Server configured but not appearing in Cursor IDE. Why?

<details>
<summary>Click to reveal answer</summary>

**Problem:** Relative path in args

**Fix:** Use absolute path
```json
{
  "args": ["/Users/yourname/path/to/server.py"]
}
```

**Also check:**
- Did you restart Cursor IDE?
- Does the file exist at that path?
- Is python in PATH?
- Are there syntax errors in the config JSON?
</details>

### Scenario 2: Permission Denied

```
Error: Permission denied reading: file:///../../etc/passwd
```

**Q:** What security issue does this reveal?

<details>
<summary>Click to reveal answer</summary>

**Issue:** Path traversal attack attempt

**What happened:**
User tried to access `/etc/passwd` using `../../` to escape the allowed directory.

**Fix:** Implement path validation
```python
def is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False

if not is_safe_path(BASE_DIR, file_path):
    raise PermissionError("Access denied")
```

**Key lesson:** Always validate paths before file access.
</details>

### Scenario 3: Intermittent Failures

Server works sometimes but fails randomly with "rate limit exceeded" errors.

**Q:** How do you diagnose and fix this?

<details>
<summary>Click to reveal answer</summary>

**Diagnosis steps:**

1. **Add rate limit monitoring:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Rate limit: {limiter.requests_remaining()}/{limiter.max_requests}")
    # ... rest of code
```

2. **Check logs** for patterns:
   - Time between failures
   - Which operations trigger it
   - External API responses

3. **Test rate limiter**:
```python
# Does limiter correctly track requests?
# Is time window correct?
```

**Fixes:**

1. **Increase cache TTL:**
```python
cache = APICache(ttl=600)  # 10 minutes instead of 5
```

2. **Add authentication:**
```python
# GitHub: 60/hr → 5000/hr with token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
```

3. **Implement backoff:**
```python
if not limiter.is_allowed():
    wait = limiter.wait_time()
    return [TextContent(
        type="text",
        text=f"Rate limit exceeded. Please wait {wait:.0f} seconds."
    )]
```
</details>

---

## Part 6: Self-Assessment

Rate your confidence (1-5, where 5 is very confident):

### Configuration
- [ ] I can configure Cursor IDE for MCP servers
- [ ] I understand environment variable usage
- [ ] I can debug configuration issues
- [ ] I know where to find logs and errors

### Testing
- [ ] I can use MCP Inspector effectively
- [ ] I can interpret JSON-RPC messages
- [ ] I can debug protocol-level issues
- [ ] I can profile server performance

### Integration Patterns
- [ ] I understand when to use multiple servers
- [ ] I can implement proper error handling
- [ ] I know how to implement caching
- [ ] I can secure resource access

### Production Readiness
- [ ] I can implement rate limiting
- [ ] I understand security best practices
- [ ] I can handle API authentication
- [ ] I'm ready to deploy servers for real use

**If any rating is < 3:** Review that section of Module 05 before proceeding.

---

## Part 7: Next Steps

### Before Moving to Module 06

Ensure you can:

1. **Configure servers** in Cursor IDE successfully
2. **Debug issues** using Inspector and logs
3. **Implement integrations** with external APIs
4. **Design** multi-server architectures
5. **Apply** production best practices (caching, rate limiting, security)

### Recommended Practice

Build a complete integration:

1. Choose an API or service you use
2. Build an MCP server for it
3. Add authentication, caching, rate limiting
4. Test with Inspector
5. Deploy to Cursor IDE
6. Use it for real tasks

### Module 06 Preview

Next, you'll learn:

- Authentication and authorization patterns
- Input validation and sanitization
- Comprehensive security auditing
- Production deployment strategies
- Monitoring and observability

---

## Completion Certificate

Once you've successfully:

- ✓ Answered all concept questions correctly
- ✓ Completed the practical exercise
- ✓ Debugged all scenarios
- ✓ Rated yourself 3+ on all self-assessment items
- ✓ Tested servers with Cursor IDE or Inspector

**You're ready for Module 06: Security & Best Practices!**

---

**Congratulations on completing the integration patterns module!**

You now have the skills to deploy MCP servers that work seamlessly with real AI applications in production environments.

