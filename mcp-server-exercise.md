# Docker-Based MCP Server: Complete Learning Exercise

## Overview

This hands-on exercise teaches you how to build, containerize, and use an **Model Context Protocol (MCP) server** with Docker. Based on your Docker experience, you'll learn what MCP is, how to create an MCP server in Python, and how to integrate it with AI clients like Claude Desktop.

**Duration**: 60-90 minutes  
**Prerequisites**: Docker Desktop, Python 3.11+, text editor

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI applications to securely connect to external data sources and tools. It acts as a universal bridge between Large Language Models (LLMs) and external systems.

### Architecture

- **MCP Hosts**: AI applications like Claude Desktop
- **MCP Clients**: Protocol clients within hosts 
- **MCP Servers**: Lightweight programs exposing capabilities

### Three Core Primitives

| Type | Control | Description | Example |
|------|---------|-------------|---------|
| **Tools** | Model-controlled | Functions AI can execute | API calls, calculations |
| **Resources** | Application-controlled | Data sources AI can read | Files, databases |
| **Prompts** | User-controlled | Conversation templates | Slash commands |

## Part 1: Project Setup

### Step 1: Create Project Directory

```bash
mkdir weather-mcp-server
cd weather-mcp-server
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install fastmcp>=0.3.0
```

## Part 2: Create the MCP Server

### The Complete Server Code

Create `server.py` with the weather service implementation:

```python
# server.py - Simple Weather MCP Server
from fastmcp import FastMCP
import random

# Initialize MCP server with a descriptive name
mcp = FastMCP("Weather Service")

# Tool 1: Get current weather for a city
@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary with weather information
    """
    # Simulate weather data (in production, call a real weather API)
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy"]
    
    return {
        "city": city,
        "temperature": random.randint(10, 35),
        "condition": random.choice(conditions),
        "humidity": random.randint(30, 90),
        "wind_speed": random.randint(5, 25)
    }

# Tool 2: Get weather forecast
@mcp.tool()
def get_forecast(city: str, days: int = 3) -> list:
    """
    Get weather forecast for the next few days.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (default: 3)
        
    Returns:
        List of daily forecasts
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
    forecast = []
    
    for day in range(1, days + 1):
        forecast.append({
            "day": day,
            "city": city,
            "temperature": random.randint(10, 35),
            "condition": random.choice(conditions)
        })
    
    return forecast

# Resource: City weather data
@mcp.resource("weather://{city}")
def get_city_weather_resource(city: str) -> str:
    """
    Resource providing weather context for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Formatted weather information
    """
    weather = get_weather(city)
    return f"Current weather in {weather['city']}: {weather['condition']}, " \
           f"{weather['temperature']}°C, Humidity: {weather['humidity']}%, " \
           f"Wind: {weather['wind_speed']} km/h"

# Prompt: Weather analysis template
@mcp.prompt()
def analyze_weather(city: str) -> str:
    """
    Provide a prompt template for weather analysis.
    
    Args:
        city: Name of the city
        
    Returns:
        Prompt for LLM to analyze weather
    """
    return f"Analyze the current weather conditions in {city} and provide " \
           f"recommendations for outdoor activities."

# CRITICAL: Run the server
if __name__ == "__main__":
    mcp.run()
```

### Test the Server Locally

```bash
# Run the server directly
python server.py
```

The server starts and waits for STDIO input. It's working correctly if it doesn't show errors and waits silently. Press `Ctrl+C` to stop.

## Part 3: Containerize with Docker

### Step 1: Create Dockerfile

```dockerfile
# Dockerfile for Weather MCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Set the entrypoint to run the server
ENTRYPOINT ["python", "server.py"]
```

### Step 2: Create requirements.txt

```text
fastmcp>=0.3.0
```

### Step 3: Build Docker Image

```bash
docker build -t weather-mcp-server:latest .
```

### Step 4: Test Containerized Server

```bash
docker run -i --rm weather-mcp-server:latest
```

Should start successfully and wait for input. Press `Ctrl+C` to stop.

### Optional: Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  weather-mcp:
    build: .
    container_name: weather-mcp-server
    stdin_open: true
    tty: true
    command: python server.py
```

## Part 4: Connect to Claude Desktop

### Step 1: Locate Configuration File

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Add Server Configuration

Create or edit the configuration file:

```json
{
  "mcpServers": {
    "weather-service": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "weather-mcp-server:latest"
      ]
    }
  }
}
```

### Step 3: Restart Claude Desktop

1. **Completely quit** Claude Desktop (don't just close window)
2. **Restart** the application
3. The MCP server should load automatically

### Step 4: Verify Connection

In Claude Desktop:
- Look for MCP indicators in the interface
- Check Settings → Developer for server status
- Should show "weather-service" as Connected

## Part 5: Test with Real Queries

### Test Queries to Try

#### Query 1: Current Weather
```
What's the weather like in Tokyo right now?
```

**Expected**: Claude uses the `get_weather` tool and returns current conditions.

#### Query 2: Weather Forecast  
```
Can you show me the 5-day weather forecast for Paris?
```

**Expected**: Claude calls `get_forecast` with `days=5` parameter.

#### Query 3: Weather Resource
```
Give me detailed weather information for London using the weather resource.
```

**Expected**: Claude accesses the `weather://London` resource.

#### Query 4: Weather Analysis
```
Use the weather analysis prompt for New York.
```

**Expected**: Claude invokes the `analyze_weather` prompt and provides activity recommendations.

## Troubleshooting

### Server Not Connecting

**Issue**: Claude shows server as disconnected

**Solutions**:
1. Verify Docker is running: `docker ps`
2. Check image exists: `docker images | grep weather-mcp-server`
3. Test manually: `docker run -i --rm weather-mcp-server:latest`
4. Check Claude logs (macOS: `~/Library/Logs/Claude/`)

### Tools Not Available

**Issue**: Claude doesn't show weather tools

**Solutions**:
1. Restart Claude Desktop completely
2. Verify JSON syntax in config file
3. Check server runs without errors
4. Ensure `mcp.run()` is called in server code

### Permission Errors

**Issue**: Docker permission denied

**Solutions**:
1. Ensure Docker Desktop is running
2. On Linux: `sudo usermod -aG docker $USER`
3. Restart terminal session

## Alternative Testing: HTTP Transport

If STDIO gives issues, try HTTP transport:

### Run Server with HTTP
```bash
fastmcp run server.py --transport http --port 8000
```

### Configure Claude with HTTP
```json
{
  "mcpServers": {
    "weather-service": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```

## Advanced Exercises

### Exercise A: Add Real Weather API

1. Sign up for OpenWeatherMap API
2. Install `requests`: `pip install requests` 
3. Add to requirements.txt
4. Modify `get_weather()` to call real API
5. Pass API key as environment variable in Docker config

### Exercise B: Add Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def get_weather(city: str) -> dict:
    logger.info(f"Fetching weather for: {city}")
    # ... rest of implementation
```

### Exercise C: Multi-Server Setup

Create multiple servers and configure both in Claude:

```json
{
  "mcpServers": {
    "weather-service": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "weather-mcp-server:latest"]
    },
    "currency-service": {
      "command": "docker", 
      "args": ["run", "-i", "--rm", "currency-mcp-server:latest"]
    }
  }
}
```

## Key Takeaways

1. **MCP standardizes AI-tool integration** with a simple client-server protocol
2. **FastMCP makes server creation easy** with Python decorators
3. **Docker provides isolation and consistency** for MCP server deployment
4. **STDIO transport works for local development** and testing
5. **Claude Desktop integration is straightforward** with JSON configuration

## Next Steps

- Explore official MCP docs: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- Browse example servers: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)  
- Try other MCP clients: Cursor, Continue.dev
- Build servers with real APIs and databases
- Learn about HTTP/SSE transport for production

## Resources

- **FastMCP Documentation**: [gofastmcp.com](https://gofastmcp.com)
- **MCP Python SDK**: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Claude Desktop**: [claude.ai/download](https://claude.ai/download)
- **Docker Documentation**: [docs.docker.com](https://docs.docker.com)

---

**Congratulations!** You've successfully created, containerized, and deployed your first MCP server. You now understand how MCP enables AI applications to interact with external tools and data sources through a standardized protocol.