# MCP Weather Server

A simple MCP (Model Context Protocol) server that provides weather data for various locations.

## Features

- Get current weather conditions for different cities
- View temperature, humidity, wind speed, and other weather metrics
- Get short-term forecast for locations
- List available locations with detailed weather data

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/mcp-weather-server.git
cd mcp-weather-server

# Install using uv (recommended)
uv venv
uv pip install -e .
```

## Usage

Start the server using either stdio (default) or SSE transport:

```bash
# Using stdio transport (default)
uv run mcp-weather-server

# Using SSE transport on custom port
uv run mcp-weather-server --transport sse --port 8000
```

The server exposes two tools:

1. `get_weather` - Get weather data for a specific location
   - Required parameter: `location` (string)

2. `list_locations` - List available locations with detailed weather data
   - No parameters required

## Example Client Usage

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def main():
    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "mcp-weather-server"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

            # Get weather for New York
            result = await session.call_tool("get_weather", {"location": "New York"})
            print(result)

            # List available locations
            locations = await session.call_tool("list_locations", {})
            print(locations)

asyncio.run(main())
```

## Note

This server uses mock data for demonstration purposes. In a production environment, you would replace the `fetch_weather` function with calls to a real weather API.
