# Challenge 1: Docker Customization

## Overview

This challenge pushes you to customize the Docker development environment for specific needs. You'll modify the Dockerfile, add custom tools, optimize the image, and create specialized development containers.

**Estimated Time**: 60-90 minutes

**Prerequisites**: 
- Complete both tutorials
- Docker installed and working
- Basic understanding of Dockerfile syntax

**Difficulty**: Intermediate

---

## The Challenges

You have four independent challenges. Complete at least two to pass, or attempt all for mastery.

---

## Challenge A: Add Database Tools

### Scenario

Your MCP servers will need to interact with PostgreSQL and SQLite databases. Add database tools to the Docker image.

### Requirements

1. Add PostgreSQL client tools (`psql`)
2. Add SQLite tools
3. Add Python database libraries (psycopg2, aiosqlite)
4. Test database connectivity from within container

### Your Task

**Step 1: Modify Dockerfile**

Create `docker/Dockerfile.db`:

```dockerfile
FROM python:3.11-slim

# Your modifications here:
# - Install PostgreSQL client
# - Install SQLite
# - Install Python database libraries

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install database libraries
RUN pip install --no-cache-dir \
    # Add database libraries here

WORKDIR /workspace

CMD ["bash"]
```

**Step 2: Build and Test**

```bash
# Build the image
docker build -t mcp-db:dev -f docker/Dockerfile.db .

# Test PostgreSQL client
docker run --rm mcp-db:dev psql --version

# Test SQLite
docker run --rm mcp-db:dev sqlite3 --version

# Test Python imports
docker run --rm mcp-db:dev python -c "import psycopg2, aiosqlite; print('DB libraries work!')"
```

### Success Criteria

- [ ] PostgreSQL client available in container
- [ ] SQLite available in container  
- [ ] Python can import psycopg2 and aiosqlite
- [ ] Image builds without errors

### Bonus

- Add pgcli (better PostgreSQL client)
- Add database migration tool (Alembic)
- Create Docker Compose service with actual PostgreSQL database

---

**Ask the AI:**

For Challenge A:
- "What's the difference between installing PostgreSQL server versus just the client? Which do I need?"
- "I'm getting an error installing psycopg2. What are common causes and how do I diagnose?"

---

## Challenge B: Multi-Stage Build Optimization

### Scenario

The development Docker image is large. Use multi-stage builds to create a smaller production image.

### Requirements

1. Create a builder stage for dependencies
2. Create a runtime stage with only what's needed
3. Reduce final image size by at least 30%
4. Maintain all MCP functionality

### Your Task

**Step 1: Check Current Size**

```bash
docker images mcp-learning:dev
# Note the SIZE column
```

**Step 2: Create Optimized Dockerfile**

Create `docker/Dockerfile.optimized`:

```dockerfile
# Stage 1: Builder
FROM python:3.11 as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Copy only Python packages from builder
COPY --from=builder /root/.local /root/.local

# Update PATH
ENV PATH=/root/.local/bin:$PATH

WORKDIR /workspace

CMD ["bash"]
```

**Step 3: Build and Compare**

```bash
# Build optimized image
docker build -t mcp-learning:optimized -f docker/Dockerfile.optimized .

# Compare sizes
docker images | grep mcp-learning

# Test functionality
docker run --rm mcp-learning:optimized python -c "import mcp; print('MCP works!')"
```

### Success Criteria

- [ ] Multi-stage build working
- [ ] Final image smaller than original
- [ ] All MCP functionality works
- [ ] No unnecessary build tools in final image

### Bonus

- Use alpine base image (even smaller)
- Add health check
- Implement distroless final stage

---

**Ask the AI:**

For Challenge B:
- "In multi-stage builds, what gets copied to the final stage? How do I know what to include?"
- "Why use COPY --from=builder instead of just installing packages in the final stage?"

---

## Challenge C: Development vs Production Images

### Scenario

Create separate images for development (with debugging tools) and production (minimal and secure).

### Requirements

1. Development image: Full tools, debuggers, editors
2. Production image: Minimal, no debug tools, runs as non-root
3. Shared base to avoid duplication
4. Both work with the same codebase

### Your Task

**Step 1: Create Base Dockerfile**

Create `docker/Dockerfile.base`:

```dockerfile
FROM python:3.11-slim as base

# Common setup
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /workspace
```

**Step 2: Create Development Dockerfile**

Create `docker/Dockerfile.dev`:

```dockerfile
FROM docker/Dockerfile.base as base

# Development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    git \
    curl \
    ipython3 \
    && rm -rf /var/lib/apt/lists/*

# Development Python packages
RUN pip install --no-cache-dir \
    ipdb \
    pytest-cov \
    pytest-watch

USER mcpuser

CMD ["bash"]
```

**Step 3: Create Production Dockerfile**

Create `docker/Dockerfile.prod`:

```dockerfile
FROM docker/Dockerfile.base as base

# Minimal additions only
# No development tools

USER mcpuser

# Run server by default
CMD ["python", "server.py"]
```

**Step 4: Build and Test**

```bash
# Build both
docker build -t mcp:dev -f docker/Dockerfile.dev .
docker build -t mcp:prod -f docker/Dockerfile.prod .

# Compare sizes
docker images | grep mcp

# Test dev has tools
docker run --rm mcp:dev which vim
docker run --rm mcp:dev which ipdb

# Test prod doesn't have tools
docker run --rm mcp:prod which vim  # Should fail
```

### Success Criteria

- [ ] Base image built successfully
- [ ] Dev image has development tools
- [ ] Prod image is minimal
- [ ] Both images work with MCP
- [ ] Prod runs as non-root user

### Bonus

- Add docker-compose.yml with both services
- Implement security scanning
- Add HEALTHCHECK to production image

---

**Ask the AI:**

For Challenge C:
- "Why is running containers as non-root important? What vulnerabilities does it prevent?"
- "How do I share a base image between two Dockerfiles? What's the best practice?"

---

## Challenge D: Custom Tool Integration

### Scenario

Add specialized tools your MCP servers will need: HTTP client, JSON processor, and code quality tools.

### Requirements

1. Add httpie or curl for API testing
2. Add jq for JSON processing
3. Add additional code quality tools
4. Create helper scripts

### Your Task

**Step 1: Extend Dockerfile**

Create `docker/Dockerfile.tools`:

```dockerfile
FROM python:3.11-slim

# Install system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Add httpie, jq, etc.
    && rm -rf /var/lib/apt/lists/*

# Install Python tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Additional Python tools
RUN pip install --no-cache-dir \
    httpx \
    rich \
    # Add more

# Add helper scripts
COPY docker/scripts/ /usr/local/bin/

WORKDIR /workspace

CMD ["bash"]
```

**Step 2: Create Helper Scripts**

Create `docker/scripts/test-api.sh`:

```bash
#!/bin/bash
# Helper script to test MCP servers

set -e

SERVER_FILE=$1

if [ -z "$SERVER_FILE" ]; then
    echo "Usage: test-api.sh <server_file>"
    exit 1
fi

echo "Starting MCP server..."
python "$SERVER_FILE" &
SERVER_PID=$!

sleep 2

echo "Testing server..."
# Add test logic

kill $SERVER_PID
echo "Tests complete!"
```

**Step 3: Create JSON Helper**

Create `docker/scripts/format-json.sh`:

```bash
#!/bin/bash
# Format MCP JSON responses

if [ -t 0 ]; then
    # From file
    cat "$1" | jq '.'
else
    # From pipe
    jq '.'
fi
```

**Step 4: Build and Test**

```bash
# Build
docker build -t mcp-tools:dev -f docker/Dockerfile.tools .

# Test httpie/curl
docker run --rm mcp-tools:dev curl --version

# Test jq
docker run --rm mcp-tools:dev jq --version

# Test helper scripts
docker run --rm mcp-tools:dev test-api.sh
```

### Success Criteria

- [ ] HTTP client available
- [ ] jq installed and working
- [ ] Helper scripts executable
- [ ] Scripts work from within container

### Bonus

- Add interactive debugging tools
- Create script to validate MCP responses
- Add automatic testing on container start

---

**Ask the AI:**

For Challenge D:
- "What's the purpose of '/usr/local/bin/' for scripts? Why not just put them in /workspace?"
- "How do I make a shell script executable in Docker? Do I need to set permissions?"

---

## Challenge E: Docker Compose Multi-Service Setup

### Scenario

Create a complete development environment with multiple services: MCP server, database, and monitoring.

### Requirements

1. MCP server service
2. PostgreSQL database service
3. Redis cache service (optional)
4. All services networked together

### Your Task

**Step 1: Create docker-compose.dev.yml**

```yaml
version: '3.8'

services:
  mcp-server:
    build:
      context: .
      dockerfile: docker/Dockerfile
    volumes:
      - .:/workspace
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/mcp_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: python server.py

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mcp_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Step 2: Test the Setup**

```bash
# Start all services
docker compose -f docker-compose.dev.yml up -d

# Check services running
docker compose -f docker-compose.dev.yml ps

# Test database connection
docker compose -f docker-compose.dev.yml exec db psql -U postgres -d mcp_dev -c "SELECT 1;"

# Test Redis
docker compose -f docker-compose.dev.yml exec redis redis-cli ping

# View logs
docker compose -f docker-compose.dev.yml logs -f mcp-server

# Stop all
docker compose -f docker-compose.dev.yml down
```

### Success Criteria

- [ ] All services start successfully
- [ ] Services can communicate
- [ ] Database accessible from MCP server
- [ ] Redis accessible from MCP server
- [ ] Volumes persist data

### Bonus

- Add health checks
- Add monitoring (Prometheus/Grafana)
- Add nginx reverse proxy

---

**Ask the AI:**

For Challenge E:
- "In docker-compose.yml, what does 'depends_on' do? Does it wait for services to be ready?"
- "Why use named volumes for PostgreSQL data? What happens if I don't?"
- "How do services communicate in Docker Compose? Can the MCP server reach the database at 'localhost'?"

---

## Validation

### Self-Assessment

For each challenge you completed:

1. **Does it build without errors?**
2. **Does it meet all requirements?**
3. **Have you tested it thoroughly?**
4. **Is the Dockerfile well-commented?**
5. **Would someone else understand your changes?**

### Testing Checklist

- [ ] All Docker images build successfully
- [ ] No security warnings during build
- [ ] Images are reasonably sized
- [ ] All required tools are available
- [ ] MCP SDK works in all images
- [ ] Images are properly documented

---

## Submission (Optional)

If working with an instructor or peer review:

1. **Document your changes**:
   - Create `DOCKER_CHANGES.md` explaining what you did
   - Include build commands
   - Include test commands

2. **Share your Dockerfiles**:
   - Commit to git (if applicable)
   - Or create a gist

3. **Demonstrate**:
   - Show successful builds
   - Show test results
   - Explain design decisions

---

## Reflection Questions

Answer these after completing the challenges:

1. **What was most challenging about Docker customization?**

2. **How does multi-stage builds improve your images?**

3. **Why separate development and production images?**

4. **What security considerations did you encounter?**

5. **How would you further optimize these images?**

---

## Additional Resources

- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

## Next Steps

1. **Complete the checkpoint**: [Module 02 Checkpoint](../checkpoint.md)
2. **Review solutions**: [Solutions Guide](./solutions/challenge-1-solution.md)
3. **Move to Module 03**: Start building real MCP servers!

---

## How to Use AI Assistance

Docker challenges benefit from guided learning. Here's how to ask for help:

### Understanding Docker Concepts

For conceptual questions:

```
I'm working on Challenge B (multi-stage builds). Can you explain what 
multi-stage builds are and why they reduce image size? Don't write the 
Dockerfile yet, explain the concept.
```

```
What's the difference between the 'builder' stage and 'runtime' stage in 
multi-stage builds? Help me understand the purpose of each.
```

### Dockerfile Syntax

When learning syntax:

```
I see 'FROM python:3.11-slim as builder'. What does the 'as builder' part 
do?
```

```
What's the difference between RUN, CMD, and ENTRYPOINT in a Dockerfile? 
When should I use each?
```

### Challenge-Specific Guidance

For each challenge:

```
I'm starting Challenge A (adding database tools). What are the key things 
I need to consider when adding PostgreSQL to a Docker image? Guide my 
thinking, don't give me the commands.
```

```
Challenge C asks for separate dev/prod images. What are the security 
implications of running containers as root vs non-root?
```

### Debugging Build Errors

When builds fail:

```
My Docker build is failing with: [error message]. I'm working on [Challenge X]. 
What does this error typically mean, and what should I check?
```

```
The image builds but when I run it I get "command not found". What are the 
common causes of this in Docker?
```

### Optimization Questions

For performance:

```
Challenge B asks to reduce image size by 30%. What are the common 
techniques for reducing Docker image size? Let me try to apply them myself.
```

```
I'm comparing 'python:3.11' vs 'python:3.11-slim'. What's the difference 
and what are the trade-offs?
```

### Security Considerations

For Challenge C:

```
I'm creating a non-root user in Challenge C. Why is this important for 
security? What attacks does this prevent?
```

```
The prod image should be minimal. What types of tools should I definitely 
exclude for security reasons?
```

### Docker Compose Questions

For Challenge E:

```
I'm setting up docker-compose.yml with multiple services. Can you explain 
how 'depends_on' works and what it guarantees?
```

```
What's the purpose of creating a named volume for PostgreSQL data? What 
happens to the data without it?
```

### Testing Your Work

Validation questions:

```
I've built my image for Challenge A. How can I verify that PostgreSQL 
client is actually installed and working inside the container?
```

```
For Challenge B, how do I properly compare image sizes to verify I achieved 
30% reduction?
```

### Progressive Learning

Work through step-by-step:

```
Challenge A Step 1: I need to add PostgreSQL client. Should I install it 
with apt-get or is there another way? What should I consider?
```

Then:

```
OK, I'll use apt-get. What's best practice for keeping the image size down 
when installing system packages?
```

### Design Decisions

For architectural choices:

```
Challenge D wants me to add helper scripts. Should these go in the 
Dockerfile with COPY or built into the image with RUN? What are the pros 
and cons?
```

```
For the multi-service setup in Challenge E, should each service have its 
own network or share one? What factors should influence this decision?
```

### What NOT to Ask

Avoid these shortcuts:

- "Write the complete Dockerfile for Challenge A"
- "Give me all the commands to run"
- "Solve Challenge B for me"
- "Here's my Dockerfile, fix it" (without showing your understanding)

### Example Problem-Solving Conversation

**Effective:**

1. "I'm adding PostgreSQL to the Docker image. What package provides the psql client on Debian-based images?"
2. Get the package name
3. "OK, it's postgresql-client. Now how do I install it while keeping the image small?"
4. Learn about --no-install-recommends and cleaning up
5. "Let me write the RUN command... [shows command]... Does this look right?"
6. Get feedback and learn from it

**Less effective:**

1. "How do I add PostgreSQL to Docker?"
2. Get complete commands
3. Copy-paste without understanding
4. Can't debug when something goes wrong

### Learning from Errors

Turn errors into learning:

```
I got this error: [error]. Before you tell me how to fix it, can you help 
me understand what the error message is telling me?
```

```
My build succeeded but the image is huge (2GB). What tools can I use to 
analyze what's taking up space?
```

### Comparing Approaches

For decision-making:

```
I can use either 'python:3.11' or 'python:3.11-alpine' as my base image. 
Can you help me understand the trade-offs so I can make an informed choice?
```

```
Challenge C shows different ways to handle dev vs prod. What are the pros 
and cons of using build args vs separate Dockerfiles?
```

### Bonus Challenges

For advanced topics:

```
The bonus suggests using distroless images. What are distroless images and 
why would I use them? Is it worth the complexity?
```

```
I want to add health checks (bonus). What should a good health check for an 
MCP server verify?
```

---

## Tips for Success

- Start with the Dockerfile that's already working
- Make incremental changes and test often
- Use `docker build --no-cache` if caching causes issues
- Check image sizes with `docker images`
- Read error messages carefully
- Use `.dockerignore` to exclude unnecessary files
- Ask AI for guidance on concepts, not just solutions
- Test each change before moving to the next

**Good luck with the challenges!**

---

**Estimated Time**: 60-90 minutes (depending on challenges attempted)

**Difficulty**: Intermediate

**Next**: [Module 02 Checkpoint](../checkpoint.md)

