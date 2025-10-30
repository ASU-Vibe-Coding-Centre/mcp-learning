# Tutorial 1: Using Docker MCP Catalog Servers

**Time:** 30-40 minutes  
**Difficulty:** Beginner  
**Prerequisites:** Docker Desktop installed (Module 02)

---

## Learning Objectives

By the end of this tutorial, you will:
- Browse the Docker MCP Catalog
- Install a pre-built MCP server
- Configure environment variables and secrets
- Connect a catalog server to Cursor IDE
- Test tools provided by the server

---

## Introduction

The Docker MCP Catalog provides 200+ pre-built, verified MCP servers that you can use immediately without writing any code. This tutorial walks you through using your first catalog server.

We'll use the `mcp/filesystem` server as an example - it provides tools for reading, writing, and listing files.

---

## Step 1: Open Docker Desktop MCP Toolkit

1. **Launch Docker Desktop**
   - On macOS: Click Docker icon in menu bar
   - On Windows: Click Docker icon in system tray
   - On Linux: Launch from applications menu

2. **Navigate to MCP Section**
   - Look for "MCP" or "MCP Toolkit" in the left sidebar
   - Click to open the MCP Toolkit interface

3. **Verify You See the Catalog**
   - You should see a "Browse Catalog" or similar option
   - The catalog should show available servers

**Expected Result:** MCP Toolkit interface is open showing the catalog browser.

**Troubleshooting:**
- **Don't see MCP section?** 
  - Ensure Docker Desktop version is 4.25+ (check: Docker Desktop → About)
  - Update Docker Desktop if needed
- **Catalog empty?**
  - Check internet connection
  - Try clicking "Refresh Catalog"

---

## Step 2: Browse and Select a Server

1. **Search for Filesystem Server**
   - In the catalog browser, search for "filesystem"
   - Or browse under category: "Development & DevOps"

2. **Review Server Details**
   - **Name:** `mcp/filesystem`
   - **Publisher:** Docker (verified)
   - **Type:** Local (runs on your machine)
   - **Description:** File system operations (read, write, list)

3. **Check Available Tools**
   The filesystem server provides:
   - `read_file` - Read file contents
   - `write_file` - Write content to file
   - `list_directory` - List directory contents
   - `create_directory` - Create new directory
   - `delete_file` - Delete a file

4. **Check Configuration Requirements**
   - **Required:** `ROOT_PATH` - Base directory for file operations
   - **Optional:** `ALLOWED_EXTENSIONS` - File type restrictions

**Expected Result:** You understand what the filesystem server does and what it needs.

---

## Step 3: Install the Server

1. **Click "Install" or "Enable"**
   - This pulls the Docker image `mcp/filesystem:latest`
   - Wait for download to complete (usually 30-60 seconds)

2. **Monitor Installation Progress**
   - You'll see download progress in the toolkit
   - Image layers will download and extract

3. **Verify Installation**
   - Server should appear in "My Servers" or "Installed Servers"
   - Status might show "Stopped" or "Not Configured" - this is normal

**Expected Result:** `mcp/filesystem` appears in your installed servers list.

**Troubleshooting:**
- **Installation fails?**
  - Check Docker has enough disk space (need ~100MB)
  - Check internet connection
  - Try manually: `docker pull mcp/filesystem:latest`

---

## Step 4: Configure the Server

1. **Open Server Settings**
   - Click on `mcp/filesystem` in your servers list
   - Click "Settings" or "Configure"

2. **Set Required Environment Variable**
   ```
   Variable Name: ROOT_PATH
   Value: /Users/YOUR_USERNAME/Documents
   
   (Replace YOUR_USERNAME with your actual username)
   
   macOS/Linux examples:
   - /Users/john/Documents
   - /home/john/projects
   
   Windows example:
   - C:\Users\john\Documents
   ```

3. **Optional: Set Allowed Extensions**
   ```
   Variable Name: ALLOWED_EXTENSIONS
   Value: .txt,.md,.json,.py
   
   (This restricts operations to these file types only)
   ```

4. **Save Configuration**
   - Click "Save" or "Apply"
   - Server should now show "Configured" status

**Important:** Choose a directory you're comfortable letting the AI access. Start with a test directory if unsure.

**Expected Result:** Server is configured with `ROOT_PATH` set.

---

## Step 5: Start the Server

1. **Enable/Start the Server**
   - Toggle "Enabled" switch to ON
   - Or click "Start" button

2. **Verify Server is Running**
   - Status should change to "Running"
   - You should see a green indicator or checkmark

3. **Check Logs (Optional)**
   - Click "View Logs" if available
   - Should see initialization messages
   - No errors should appear

**Expected Result:** Server status shows "Running" with green indicator.

**Troubleshooting:**
- **Won't start?**
  - Check ROOT_PATH exists and is accessible
  - Check Docker has permission to access that directory
  - View logs for specific error messages

---

## Step 6: Connect to Cursor IDE

Now let's connect this server to Cursor IDE so the AI can use it.

1. **In Docker MCP Toolkit, Go to Client Configuration**
   - Look for "Clients" or "Client Configuration" section
   - Select "Cursor IDE"

2. **Enable Connection**
   - Toggle "Enable" for Cursor IDE
   - The toolkit will show the connection endpoint
   - Usually: `http://localhost:3000/mcp`

3. **Verify Configuration Was Created**
   - Toolkit should indicate "Cursor IDE: Connected"
   - Configuration file is automatically created at:
     - macOS: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
     - Windows: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

**Expected Result:** Cursor IDE is connected to the MCP Gateway.

**Alternative Manual Configuration:**

If automatic configuration doesn't work, create/edit the file manually:

```json
{
  "mcpServers": {
    "docker-mcp-gateway": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

---

## Step 7: Test in Cursor IDE

1. **Launch Cursor IDE**
   - Start or restart Cursor IDE application
   - Wait for it to fully load

2. **Verify Server is Connected**
   - Look for a tools or MCP indicator
   - You might see "MCP: 1 server connected" or similar

3. **Test the Filesystem Tools**

Try these prompts:

**Test 1: List Directory**
```
Can you list the files in my documents directory?
```

Claude should use the `list_directory` tool and show your files.

**Test 2: Create a Test File**
```
Create a new file called test-mcp.txt with the content "Hello from MCP!"
```

Claude should:
- Use the `write_file` tool
- Create the file in your ROOT_PATH
- Confirm the file was created

**Test 3: Read the File Back**
```
Read the contents of test-mcp.txt
```

Claude should:
- Use the `read_file` tool
- Show you the content "Hello from MCP!"

**Test 4: Verify Manually**
- Open your file explorer
- Navigate to ROOT_PATH directory
- Confirm `test-mcp.txt` exists
- Open it to verify contents

**Expected Result:** Claude successfully uses filesystem tools to manipulate files.

---

## Step 8: Explore Server Capabilities

Now that it's working, explore what else you can do:

1. **Try Different Operations**
   ```
   Create a subdirectory called "mcp-test"
   Write three different files in that subdirectory
   List all files recursively
   ```

2. **Test Error Handling**
   ```
   Try to read a file that doesn't exist
   Try to write to a file with forbidden extension (if you set ALLOWED_EXTENSIONS)
   ```

   Claude should gracefully handle these errors.

3. **Check Resource Limits**
   - In Docker MCP Toolkit, view server resource usage
   - Should stay under 1 CPU, 2GB memory (default limits)

---

## Step 9: Stop and Manage Server

When you're done testing:

1. **Stop the Server (Optional)**
   - In MCP Toolkit, toggle server to "Disabled"
   - Or click "Stop"
   - Server container stops but configuration is saved

2. **View Server Logs**
   - Click "View Logs" in toolkit
   - See all tool calls that were made
   - Useful for debugging

3. **Restart Server**
   - Toggle back to "Enabled"
   - Server starts with saved configuration
   - Cursor IDE reconnects automatically

---

## What You Learned

- **Catalog Navigation:** How to find and review MCP servers
- **Installation:** Pulling Docker images for MCP servers
- **Configuration:** Setting environment variables and secrets
- **Client Integration:** Connecting servers to Cursor IDE via Gateway
- **Testing:** Verifying tools work correctly
- **Management:** Starting, stopping, and monitoring servers

---

## Next Steps

### Try More Catalog Servers

**Easy Next Servers:**
1. **`mcp/git`** - Git operations (status, commit, push)
2. **`mcp/sqlite`** - SQLite database operations
3. **`mcp/weather`** - Weather data (if available)

**More Advanced:**
4. **`mcp/github`** - GitHub API (requires GitHub token)
5. **`mcp/postgres`** - PostgreSQL database (requires database)
6. **`mcp/slack`** - Slack integration (requires API key)

### Install Multiple Servers

Try installing 2-3 servers simultaneously:
- They all connect through the same Gateway
- Claude can use tools from all servers
- Each runs in its own isolated container

### Experiment with Configuration

- Change ROOT_PATH to different directories
- Set ALLOWED_EXTENSIONS restrictions
- Try different resource limits

---

## Checkpoint Questions

Answer these to verify your understanding:

1. **What's the difference between local and remote MCP servers?**
   <details>
   <summary>Answer</summary>
   Local servers run as containers on your machine and work offline. Remote servers are hosted services accessed over the internet and require connectivity.
   </details>

2. **Why do we need to configure ROOT_PATH for the filesystem server?**
   <details>
   <summary>Answer</summary>
   ROOT_PATH defines the base directory the server can access. This provides security by restricting the server to a specific directory, preventing it from accessing your entire filesystem.
   </details>

3. **What's the role of the MCP Gateway in this setup?**
   <details>
   <summary>Answer</summary>
   The Gateway aggregates all MCP servers into a single endpoint. Cursor IDE connects to the Gateway, which routes tool calls to the appropriate servers. This means you only configure one connection in Claude, not one per server.
   </details>

4. **If a server won't start, where should you look first?**
   <details>
   <summary>Answer</summary>
   Check the server logs in Docker MCP Toolkit. Common issues are missing/invalid configuration (like ROOT_PATH not existing) or permission problems.
   </details>

---

## Troubleshooting Guide

### Server Won't Start

**Symptom:** Server status stuck on "Starting" or immediately goes to "Stopped"

**Solutions:**
1. Check server logs for errors
2. Verify required environment variables are set correctly
3. Ensure paths exist and are accessible
4. Restart Docker Desktop
5. Try pulling image again: `docker pull mcp/filesystem:latest`

### Claude Doesn't See Tools

**Symptom:** Claude responds but doesn't use any MCP tools

**Solutions:**
1. Verify server status is "Running" in toolkit
2. Check Client Configuration shows Claude as "Connected"
3. Restart Cursor IDE application
4. Check Cursor IDE config file exists and has correct endpoint
5. Try asking explicitly: "What MCP tools do you have access to?"

### Permission Errors

**Symptom:** Server starts but tools fail with permission errors

**Solutions:**
1. Check ROOT_PATH permissions (should be readable/writable)
2. On macOS: Grant Docker Desktop permission in System Settings → Privacy & Security
3. On Linux: Ensure Docker has permission to mount the directory
4. Try a directory in your home folder

### Tools Work But Files Not Created

**Symptom:** Claude says file was created but you can't find it

**Solutions:**
1. Double-check ROOT_PATH configuration
2. Files are created relative to ROOT_PATH
3. Refresh file explorer
4. Check if ALLOWED_EXTENSIONS is blocking the file type

---

## Summary

You've successfully:
- ✅ Browsed the Docker MCP Catalog
- ✅ Installed your first MCP server
- ✅ Configured environment variables
- ✅ Connected to Cursor IDE via Gateway
- ✅ Tested tools in a real AI application

**Time Invested:** ~30-40 minutes  
**Servers Mastered:** 1 (filesystem)  
**Tools Used:** 3-5 filesystem operations  
**Difficulty Level:** Beginner ✓

---

**Next Tutorial:** [Tutorial 2: Docker MCP Toolkit Deep Dive](tutorial-2-toolkit-setup.md)

**Next Challenge:** [Challenge 1: Multi-Server Setup](challenge-1-multi-server.md)

