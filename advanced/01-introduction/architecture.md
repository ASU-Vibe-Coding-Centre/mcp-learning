# MCP Architecture Deep Dive

This document provides a detailed technical exploration of the Model Context Protocol architecture, including protocol layers, message flow, and implementation details.

## Table of Contents

1. [Protocol Stack Overview](#protocol-stack-overview)
2. [Transport Layer](#transport-layer)
3. [Message Layer (JSON-RPC 2.0)](#message-layer-json-rpc-20)
4. [Protocol Layer](#protocol-layer)
5. [Application Layer](#application-layer)
6. [Message Flow Patterns](#message-flow-patterns)
7. [Connection Lifecycle](#connection-lifecycle)
8. [Error Handling](#error-handling)

---

## Protocol Stack Overview

MCP is built as a layered protocol, with each layer handling specific concerns:

```
┌─────────────────────────────────────────┐
│     Application Layer                   │  Your business logic
│  (Tools, Resources, Prompts)            │  (what the server does)
├─────────────────────────────────────────┤
│     Protocol Layer                      │  MCP-specific operations
│  (Capability negotiation, discovery)    │  (tools/list, resources/read, etc.)
├─────────────────────────────────────────┤
│     Message Layer                       │  Request/response structure
│  (JSON-RPC 2.0)                         │  (id, method, params, result)
├─────────────────────────────────────────┤
│     Transport Layer                     │  How messages are delivered
│  (stdio, HTTP+SSE, WebSockets)          │  (bytes on the wire)
└─────────────────────────────────────────┘
```

### Layer Responsibilities

- **Transport Layer**: Handles the physical delivery of messages between client and server
- **Message Layer**: Structures requests and responses in a standard format
- **Protocol Layer**: Defines MCP-specific methods and workflows
- **Application Layer**: Implements the actual capabilities (your code)

---

## Transport Layer

The transport layer defines how messages are physically transmitted between client and server.

### stdio (Standard Input/Output)

**How it works**:
- Server runs as a subprocess of the client
- Client writes requests to server's stdin
- Server writes responses to stdout
- Stderr is used for logging and diagnostics

**Message Format**:
Each message is a single line of JSON followed by a newline:
```
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}\n
```

**Advantages**:
- Simple to implement
- Works on all platforms
- No network configuration needed
- Easy to debug (just watch stdin/stdout)

**Disadvantages**:
- Server must run on same machine as client
- Cannot share one server across multiple clients
- Process management overhead

**Use Cases**:
- Local development tools
- IDE integrations
- Desktop applications like Cursor IDE

**Example Implementation**:
```python
import sys
import json

# Reading from stdin
line = sys.stdin.readline()
request = json.loads(line)

# Writing to stdout
response = {"jsonrpc": "2.0", "id": request["id"], "result": {...}}
sys.stdout.write(json.dumps(response) + "\n")
sys.stdout.flush()  # Important: flush to ensure delivery
```

### HTTP with Server-Sent Events (SSE)

**How it works**:
- Client connects to HTTP server
- Client sends requests via HTTP POST
- Server sends responses and notifications via SSE stream
- Bidirectional communication over HTTP

**Message Format**:
- Requests: Standard HTTP POST with JSON body
- Responses: SSE events with JSON data

**SSE Event Format**:
```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}

event: message
data: {"jsonrpc":"2.0","method":"notification","params":{...}}
```

**Advantages**:
- Server can be remote
- Multiple clients can connect to one server
- Works through firewalls and proxies
- Standard HTTP infrastructure

**Disadvantages**:
- More complex to implement
- Requires network configuration
- Higher latency than stdio

**Use Cases**:
- Shared services across teams
- Cloud-hosted MCP servers
- Web-based AI applications

### HTTP with WebSockets

**How it works**:
- Client establishes WebSocket connection
- Both client and server can send messages at any time
- Full-duplex bidirectional communication

**Advantages**:
- True bidirectional streaming
- Lower latency than SSE
- Efficient for real-time updates

**Disadvantages**:
- More complex than SSE
- Some proxies don't support WebSockets well
- Requires connection state management

**Use Cases**:
- Real-time collaborative applications
- Streaming data scenarios
- Low-latency requirements

---

## Message Layer (JSON-RPC 2.0)

MCP uses JSON-RPC 2.0 as its message format. This provides a standardized way to structure requests, responses, and errors.

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculator",
    "arguments": {
      "operation": "add",
      "a": 5,
      "b": 3
    }
  }
}
```

**Fields**:
- `jsonrpc`: Always "2.0" (required)
- `id`: Unique identifier for the request (required for requests that expect a response)
- `method`: The RPC method to call (required)
- `params`: Method parameters (optional)

### Response Format

**Success Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "8"
      }
    ]
  }
}
```

**Error Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "Parameter 'a' must be a number"
    }
  }
}
```

**Fields**:
- `jsonrpc`: Always "2.0" (required)
- `id`: Must match the request id (required)
- `result`: The result of the method call (for success)
- `error`: Error information (for failures)

### Notifications

Notifications are one-way messages that don't expect a response:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "abc123",
    "progress": 50,
    "total": 100
  }
}
```

**Key difference**: No `id` field, so no response is expected.

### Error Codes

JSON-RPC 2.0 defines standard error codes:

| Code | Message | Meaning |
|------|---------|---------|
| -32700 | Parse error | Invalid JSON received |
| -32600 | Invalid Request | JSON is valid but request structure is wrong |
| -32601 | Method not found | The method doesn't exist |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Server internal error |

MCP can define additional application-specific error codes (outside the -32768 to -32000 range).

---

## Protocol Layer

The protocol layer defines MCP-specific methods and workflows.

### Initialization Sequence

Before any other operations, client and server must negotiate capabilities:

```
Client                                    Server
  │                                         │
  ├──────── initialize ──────────────────>  │
  │  { capabilities: {...} }                │
  │                                         │
  │  <─────── result ─────────────────────  │
  │  { capabilities: {...}, serverInfo: {...} }
  │                                         │
  ├──────── initialized ─────────────────>  │
  │  (notification)                         │
  │                                         │
  │  <<<  Normal operations begin >>>       │
```

**initialize request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "ExampleClient",
      "version": "1.0.0"
    }
  }
}
```

**initialize response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {
        "subscribe": true
      },
      "prompts": {}
    },
    "serverInfo": {
      "name": "ExampleServer",
      "version": "1.0.0"
    }
  }
}
```

**initialized notification**:
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### Capability Negotiation

Capabilities determine what features are available:

**Client Capabilities**:
- `roots.listChanged`: Client can notify server of root directory changes
- `sampling`: Client supports sampling (asking the LLM for responses)

**Server Capabilities**:
- `tools`: Server provides tools that can be called
- `resources.subscribe`: Server supports resource subscriptions for updates
- `prompts`: Server provides prompt templates
- `logging`: Server can send log messages to client

### Core Methods

#### Tools

**tools/list** - List available tools:
```json
Request:
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}

Response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "calculator",
        "description": "Performs basic arithmetic operations",
        "inputSchema": {
          "type": "object",
          "properties": {
            "operation": {
              "type": "string",
              "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": { "type": "number" },
            "b": { "type": "number" }
          },
          "required": ["operation", "a", "b"]
        }
      }
    ]
  }
}
```

**tools/call** - Execute a tool:
```json
Request:
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "calculator",
    "arguments": {
      "operation": "add",
      "a": 5,
      "b": 3
    }
  }
}

Response:
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Result: 8"
      }
    ]
  }
}
```

#### Resources

**resources/list** - List available resources:
```json
Response:
{
  "resources": [
    {
      "uri": "file:///logs/app.log",
      "name": "Application Log",
      "description": "Current application log file",
      "mimeType": "text/plain"
    }
  ]
}
```

**resources/read** - Read a resource:
```json
Request:
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/read",
  "params": {
    "uri": "file:///logs/app.log"
  }
}

Response:
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "contents": [
      {
        "uri": "file:///logs/app.log",
        "mimeType": "text/plain",
        "text": "2024-10-30 10:00:00 INFO Server started\n..."
      }
    ]
  }
}
```

#### Prompts

**prompts/list** - List available prompt templates:
```json
Response:
{
  "prompts": [
    {
      "name": "code_review",
      "description": "Review code for quality and best practices",
      "arguments": [
        {
          "name": "language",
          "description": "Programming language",
          "required": true
        }
      ]
    }
  ]
}
```

**prompts/get** - Get a prompt template:
```json
Request:
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "language": "python"
    }
  }
}

Response:
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code for..."
        }
      }
    ]
  }
}
```

---

## Application Layer

The application layer is where your business logic lives. This is the code you write to implement tools, resources, and prompts.

### Tool Implementation Pattern

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("example")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculator",
            description="Performs arithmetic",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "calculator":
        a = arguments["a"]
        b = arguments["b"]
        op = arguments["operation"]
        
        if op == "add":
            result = a + b
        # ... other operations
        
        return [TextContent(type="text", text=f"Result: {result}")]
```

---

## Message Flow Patterns

### Simple Request-Response

```
Client                                    Server
  │                                         │
  ├──────── tools/call ──────────────────>  │
  │                                         │
  │                         [Server processes request]
  │                                         │
  │  <─────── result ─────────────────────  │
  │                                         │
```

### Streaming Response

For long-running operations, servers can stream results:

```
Client                                    Server
  │                                         │
  ├──────── tools/call ──────────────────>  │
  │                                         │
  │  <────── progress notification ────────│
  │  <────── progress notification ────────│
  │  <────── progress notification ────────│
  │                                         │
  │  <─────── final result ────────────────│
  │                                         │
```

### Resource Subscription

Clients can subscribe to resource changes:

```
Client                                    Server
  │                                         │
  ├──────── resources/subscribe ─────────>  │
  │  { uri: "file:///logs/app.log" }        │
  │                                         │
  │  <─────── success ────────────────────  │
  │                                         │
  │         [Resource changes]              │
  │                                         │
  │  <────── resource updated notification ─│
  │                                         │
```

---

## Connection Lifecycle

### Full Connection Lifecycle

```
1. CONNECTING
   ├─> Client launches server process (stdio)
   │   OR connects to HTTP endpoint
   │
2. INITIALIZING
   ├─> Client sends "initialize"
   ├─> Server responds with capabilities
   ├─> Client sends "initialized" notification
   │
3. OPERATING
   ├─> Normal request/response operations
   ├─> Tools called, resources read, prompts fetched
   │
4. CLOSING
   ├─> Client sends "shutdown" request (optional)
   ├─> Server responds to acknowledge
   ├─> Client closes connection
   │
5. CLOSED
   └─> Connection terminated
```

### Graceful Shutdown

```
Client                                    Server
  │                                         │
  ├──────── shutdown ────────────────────>  │
  │                                         │
  │  <─────── result ─────────────────────  │
  │                                         │
  ├──── close connection ─────────────────> │
  │                                         │
```

---

## Error Handling

### Error Handling Strategies

**At Transport Layer**:
- Connection failures
- Timeout handling
- Message corruption

**At Message Layer**:
- JSON parsing errors
- Invalid JSON-RPC structure
- Protocol violations

**At Protocol Layer**:
- Unknown methods
- Invalid parameters
- Capability mismatches

**At Application Layer**:
- Business logic errors
- Resource not found
- Permission denied

### Error Response Pattern

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "parameter": "operation",
      "expected": "string",
      "received": "number",
      "suggestion": "Use 'add', 'subtract', 'multiply', or 'divide'"
    }
  }
}
```

**Best Practices**:
1. Use appropriate error codes
2. Provide clear error messages
3. Include actionable details in `data` field
4. Don't leak sensitive information in errors
5. Log detailed errors server-side for debugging

---

## Key Takeaways

1. **Layered Architecture**: MCP separates concerns across transport, message, protocol, and application layers
2. **JSON-RPC 2.0**: Standard message format ensures interoperability
3. **Capability Negotiation**: Clients and servers declare their features during initialization
4. **Multiple Transports**: Choose stdio for local, HTTP/SSE for remote deployments
5. **Structured Error Handling**: Each layer handles errors appropriately

---

## Further Reading

- [Official MCP Specification](https://spec.modelcontextprotocol.io)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

**Next**: [comparison.md](./comparison.md) - Compare MCP with alternative approaches

