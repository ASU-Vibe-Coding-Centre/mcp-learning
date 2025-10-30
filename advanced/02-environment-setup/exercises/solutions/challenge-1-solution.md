# Challenge 1 Solutions: Docker Customization

This guide provides complete solutions for all Docker customization challenges.

---

## Challenge A: Add Database Tools

### Complete Dockerfile.db

```dockerfile
FROM python:3.11-slim

# Install system dependencies and database tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    sqlite3 \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install base Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install database libraries
RUN pip install --no-cache-dir \
    psycopg2-binary \
    aiosqlite \
    asyncpg \
    sqlalchemy

WORKDIR /workspace

CMD ["bash"]
```

### Testing Commands

```bash
# Build
docker build -t mcp-db:dev -f docker/Dockerfile.db .

# Test PostgreSQL client
docker run --rm mcp-db:dev psql --version
# Expected: psql (PostgreSQL) 15.x

# Test SQLite
docker run --rm mcp-db:dev sqlite3 --version
# Expected: 3.x.x

# Test Python libraries
docker run --rm mcp-db:dev python -c "import psycopg2, aiosqlite, asyncpg, sqlalchemy; print('✓ All DB libraries work!')"
```

### Bonus: With pgcli and Docker Compose

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    sqlite3 \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir \
    psycopg2-binary \
    aiosqlite \
    asyncpg \
    sqlalchemy \
    alembic \
    pgcli

WORKDIR /workspace

CMD ["bash"]
```

**docker-compose.db.yml:**

```yaml
version: '3.8'

services:
  mcp-db:
    build:
      context: .
      dockerfile: docker/Dockerfile.db
    volumes:
      - .:/workspace
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/mcp_dev
    depends_on:
      - db

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

volumes:
  postgres_data:
```

---

## Challenge B: Multi-Stage Build Optimization

### Complete Dockerfile.optimized

```dockerfile
# Stage 1: Builder - Has build tools
FROM python:3.11 as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies to user directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Minimal image
FROM python:3.11-slim

# Copy only the Python packages from builder
COPY --from=builder /root/.local /root/.local

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create working directory
WORKDIR /workspace

# No build tools, just runtime Python
CMD ["bash"]
```

### Comparison Results

```bash
# Build both images
docker build -t mcp-learning:dev -f docker/Dockerfile .
docker build -t mcp-learning:optimized -f docker/Dockerfile.optimized .

# Compare sizes
docker images | grep mcp-learning
# Original: ~400-500MB
# Optimized: ~250-300MB
# Reduction: ~40-50%

# Verify functionality
docker run --rm mcp-learning:optimized python -c "import mcp; print(f'MCP {mcp.__version__} works!')"
docker run --rm mcp-learning:optimized pytest --version
```

### Bonus: Alpine-based Version

```dockerfile
# Builder stage
FROM python:3.11-alpine as builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-alpine

# Copy packages
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /workspace

CMD ["sh"]
```

**Alpine results**: ~150-200MB (even smaller!)

---

## Challenge C: Development vs Production Images

### Complete docker/Dockerfile.base

```dockerfile
FROM python:3.11-slim as base

WORKDIR /workspace

# Install MCP and base requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /workspace
```

### Complete docker/Dockerfile.dev

```dockerfile
FROM python:3.11-slim

WORKDIR /workspace

# Install development system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    git \
    curl \
    wget \
    htop \
    man \
    && rm -rf /var/lib/apt/lists/*

# Install base requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development Python packages
RUN pip install --no-cache-dir \
    ipython \
    ipdb \
    pytest-cov \
    pytest-watch \
    pytest-xdist \
    rich \
    httpx

# Create user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /workspace

USER mcpuser

CMD ["bash"]
```

### Complete docker/Dockerfile.prod

```dockerfile
FROM python:3.11-slim

WORKDIR /workspace

# Minimal system dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install production requirements only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /workspace

# Copy application code
COPY --chown=mcpuser:mcpuser . .

USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import sys; sys.exit(0)"

# Run server
CMD ["python", "server.py"]
```

### Testing

```bash
# Build both
docker build -t mcp:dev -f docker/Dockerfile.dev .
docker build -t mcp:prod -f docker/Dockerfile.prod .

# Compare sizes
docker images | grep mcp:
# dev: ~350MB
# prod: ~200MB

# Test dev tools
docker run --rm mcp:dev which vim
# /usr/bin/vim

docker run --rm mcp:dev which ipython
# /usr/local/bin/ipython

# Test prod doesn't have dev tools
docker run --rm mcp:prod which vim
# (should fail - not found)

# Test both run as non-root
docker run --rm mcp:dev whoami
# mcpuser

docker run --rm mcp:prod whoami
# mcpuser
```

### Bonus: docker-compose with both

```yaml
version: '3.8'

services:
  dev:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    volumes:
      - .:/workspace
    command: bash

  prod:
    build:
      context: .
      dockerfile: docker/Dockerfile.prod
    ports:
      - "8000:8000"
    restart: unless-stopped
```

---

## Challenge D: Custom Tool Integration

### Complete docker/Dockerfile.tools

```dockerfile
FROM python:3.11-slim

# Install system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    jq \
    httpie \
    vim \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python base requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python tools
RUN pip install --no-cache-dir \
    httpx \
    rich \
    typer \
    pydantic-cli \
    jsonschema

# Copy helper scripts
COPY docker/scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

WORKDIR /workspace

CMD ["bash"]
```

### Complete docker/scripts/test-api.sh

```bash
#!/bin/bash
# Helper script to test MCP servers

set -e

SERVER_FILE=$1

if [ -z "$SERVER_FILE" ]; then
    echo "Usage: test-api.sh <server_file>"
    exit 1
fi

echo "🚀 Starting MCP server..."
python "$SERVER_FILE" &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo "🧪 Testing server health..."

# Check if process is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ Server failed to start"
    exit 1
fi

echo "✓ Server is running (PID: $SERVER_PID)"

# Clean up
echo "🛑 Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo "✅ Tests complete!"
```

### Complete docker/scripts/format-json.sh

```bash
#!/bin/bash
# Format MCP JSON responses beautifully

set -e

if [ -t 0 ]; then
    # Input from file
    if [ -z "$1" ]; then
        echo "Usage: format-json.sh <file>"
        echo "   or: cat file | format-json.sh"
        exit 1
    fi
    cat "$1" | jq --color-output '.'
else
    # Input from pipe
    jq --color-output '.'
fi
```

### Complete docker/scripts/validate-mcp.sh

```bash
#!/bin/bash
# Validate MCP server response format

set -e

RESPONSE=$1

if [ -z "$RESPONSE" ]; then
    echo "Usage: validate-mcp.sh <json-file>"
    exit 1
fi

echo "Validating MCP response format..."

# Check if valid JSON
if ! jq empty "$RESPONSE" 2>/dev/null; then
    echo "❌ Invalid JSON"
    exit 1
fi

echo "✓ Valid JSON"

# Check for required fields
if jq -e '.jsonrpc' "$RESPONSE" > /dev/null 2>&1; then
    echo "✓ Has jsonrpc field"
else
    echo "❌ Missing jsonrpc field"
    exit 1
fi

if jq -e '.id' "$RESPONSE" > /dev/null 2>&1; then
    echo "✓ Has id field"
else
    echo "⚠ No id field (might be notification)"
fi

if jq -e '.result or .error' "$RESPONSE" > /dev/null 2>&1; then
    echo "✓ Has result or error field"
else
    echo "❌ Missing both result and error fields"
    exit 1
fi

echo "✅ Valid MCP response format!"
```

### Testing

```bash
# Build
docker build -t mcp-tools:dev -f docker/Dockerfile.tools .

# Test tools
docker run --rm mcp-tools:dev curl --version
docker run --rm mcp-tools:dev jq --version
docker run --rm mcp-tools:dev http --version

# Test helper scripts
docker run --rm -v $(pwd):/workspace mcp-tools:dev test-api.sh server.py

# Test JSON formatting
echo '{"jsonrpc":"2.0","id":1,"result":{"status":"ok"}}' | \
  docker run --rm -i mcp-tools:dev format-json.sh
```

---

## Challenge E: Docker Compose Multi-Service Setup

### Complete docker-compose.dev.yml

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
      - REDIS_URL=redis://redis:6379/0
      - PYTHONUNBUFFERED=1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: python -m mcp.server
    networks:
      - mcp-network

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
      - ./docker/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - mcp-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - mcp-network

  # Bonus: Database admin UI
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - mcp-network

volumes:
  postgres_data:
  redis_data:

networks:
  mcp-network:
    driver: bridge
```

### Complete docker/init-db.sql

```sql
-- Initialize MCP database schema

CREATE TABLE IF NOT EXISTS servers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tools (
    id SERIAL PRIMARY KEY,
    server_id INTEGER REFERENCES servers(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO servers (name) VALUES ('example-server');
INSERT INTO tools (server_id, name, description) 
VALUES (1, 'example-tool', 'An example tool');
```

### Usage Commands

```bash
# Start all services
docker compose -f docker-compose.dev.yml up -d

# Check status
docker compose -f docker-compose.dev.yml ps

# View logs
docker compose -f docker-compose.dev.yml logs -f

# Test database
docker compose -f docker-compose.dev.yml exec db psql -U postgres -d mcp_dev -c "SELECT * FROM servers;"

# Test Redis
docker compose -f docker-compose.dev.yml exec redis redis-cli ping
# PONG

# Connect to MCP server
docker compose -f docker-compose.dev.yml exec mcp-server bash

# Stop all
docker compose -f docker-compose.dev.yml down

# Stop and remove volumes (clean slate)
docker compose -f docker-compose.dev.yml down -v
```

### Bonus: With Monitoring

Add to docker-compose.dev.yml:

```yaml
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./docker/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - mcp-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - mcp-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

---

## Key Learnings

### Challenge A: Database Tools
- System package management in Docker
- Python database drivers
- Library dependencies (libpq-dev for psycopg2)

### Challenge B: Optimization
- Multi-stage builds reduce image size significantly
- Separate build dependencies from runtime
- Alpine images are smallest but may have compatibility issues

### Challenge C: Dev vs Prod
- Security: Non-root users in production
- Tooling: Rich tools in dev, minimal in prod
- Size: Dev can be larger, prod should be lean

### Challenge D: Custom Tools
- Helper scripts improve developer experience
- JSON tools essential for API development
- Executable permissions matter

### Challenge E: Multi-Service
- Docker Compose orchestrates multiple containers
- Health checks ensure proper startup order
- Networks isolate and connect services
- Volumes persist data across restarts

---

## Next Steps

1. **Try your own variations**: Experiment with different base images, tools, or configurations
2. **Learn more**: Read Docker documentation on advanced topics
3. **Complete checkpoint**: [Module 02 Checkpoint](../checkpoint.md)
4. **Move forward**: [Module 03: Basic MCP Server](../../03-basic-mcp-server/README.md)

---

**Remember**: These are example solutions. Your solutions may differ and still be correct. The key is understanding the concepts and trade-offs!

