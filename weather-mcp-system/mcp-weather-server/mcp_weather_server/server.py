"""
MCP Weather Server

A simple MCP server that provides weather data for different locations.
"""

import anyio
import click
import httpx
import logging
import mcp.types as types
from mcp.server.lowlevel import Server
from pydantic import BaseModel
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeatherData(BaseModel):
    """Weather data model"""
    location: str
    temperature: float
    conditions: str
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    forecast: Optional[List[Dict[str, str]]] = None


async def fetch_weather(location: str) -> WeatherData:
    """
    In a real implementation, this would call a weather API.
    For demonstration purposes, we'll return mock data based on the location.
    """
    # Simulate an API call delay
    await anyio.sleep(0.5)
    
    # Mock weather data based on location
    weather_data = {
        "new york": WeatherData(
            location="New York, NY",
            temperature=72.5,
            conditions="Partly Cloudy",
            humidity=65.0,
            wind_speed=8.2,
            forecast=[
                {"day": "Tomorrow", "conditions": "Sunny", "high": "75°F", "low": "62°F"},
                {"day": "Wednesday", "conditions": "Cloudy", "high": "68°F", "low": "60°F"}
            ]
        ),
        "san francisco": WeatherData(
            location="San Francisco, CA",
            temperature=65.3,
            conditions="Foggy",
            humidity=72.0,
            wind_speed=12.8,
            forecast=[
                {"day": "Tomorrow", "conditions": "Partly Cloudy", "high": "66°F", "low": "55°F"},
                {"day": "Wednesday", "conditions": "Sunny", "high": "70°F", "low": "56°F"}
            ]
        ),
        "miami": WeatherData(
            location="Miami, FL",
            temperature=85.2,
            conditions="Sunny",
            humidity=78.0,
            wind_speed=6.5,
            forecast=[
                {"day": "Tomorrow", "conditions": "Partly Cloudy", "high": "86°F", "low": "74°F"},
                {"day": "Wednesday", "conditions": "Thunderstorms", "high": "82°F", "low": "75°F"}
            ]
        ),
        "seattle": WeatherData(
            location="Seattle, WA",
            temperature=58.7,
            conditions="Rainy",
            humidity=85.0,
            wind_speed=7.3,
            forecast=[
                {"day": "Tomorrow", "conditions": "Showers", "high": "60°F", "low": "52°F"},
                {"day": "Wednesday", "conditions": "Cloudy", "high": "62°F", "low": "54°F"}
            ]
        ),
        "chicago": WeatherData(
            location="Chicago, IL",
            temperature=68.9,
            conditions="Windy",
            humidity=62.0,
            wind_speed=15.7,
            forecast=[
                {"day": "Tomorrow", "conditions": "Partly Cloudy", "high": "72°F", "low": "58°F"},
                {"day": "Wednesday", "conditions": "Sunny", "high": "75°F", "low": "61°F"}
            ]
        )
    }
    
    # Default fallback data
    default_data = WeatherData(
        location=location.title(),
        temperature=70.0,
        conditions="Clear",
        humidity=60.0,
        wind_speed=5.0,
        forecast=[
            {"day": "Tomorrow", "conditions": "Sunny", "high": "72°F", "low": "58°F"},
            {"day": "Wednesday", "conditions": "Partly Cloudy", "high": "70°F", "low": "55°F"}
        ]
    )
    
    # Return weather data for the location or default if not found
    return weather_data.get(location.lower(), default_data)


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="sse",  # Changed default to sse for better visibility
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    logger.info(f"Starting MCP Weather Server with transport={transport}, port={port}")
    app = Server("mcp-weather-server")

    @app.call_tool()
    async def weather_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent]:
        logger.info(f"Received tool call: {name} with arguments: {arguments}")
        if name == "get_weather":
            if "location" not in arguments:
                logger.warning("Missing required argument 'location'")
                raise ValueError("Missing required argument 'location'")
            
            location = arguments["location"]
            logger.info(f"Fetching weather for location: {location}")
            weather_data = await fetch_weather(location)
            
            # Format the weather data as a readable text response
            response = f"Weather for {weather_data.location}:\n"
            response += f"Temperature: {weather_data.temperature}°F\n"
            response += f"Conditions: {weather_data.conditions}\n"
            
            if weather_data.humidity is not None:
                response += f"Humidity: {weather_data.humidity}%\n"
            
            if weather_data.wind_speed is not None:
                response += f"Wind Speed: {weather_data.wind_speed} mph\n"
            
            if weather_data.forecast:
                response += "\nForecast:\n"
                for day in weather_data.forecast:
                    response += f"- {day['day']}: {day['conditions']}, High: {day['high']}, Low: {day['low']}\n"
            
            logger.info(f"Returning weather data for {location}")
            return [types.TextContent(type="text", text=response)]
        
        elif name == "list_locations":
            logger.info("Listing available locations")
            # Return a list of supported locations
            locations = ["New York", "San Francisco", "Miami", "Seattle", "Chicago"]
            response = "Available locations for detailed weather information:\n"
            response += "\n".join([f"- {loc}" for loc in locations])
            response += "\n\nYou can also search for any location, but detailed data may be limited."
            
            return [types.TextContent(type="text", text=response)]
        
        else:
            logger.warning(f"Unknown tool called: {name}")
            raise ValueError(f"Unknown tool: {name}")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        logger.info("Listing available tools")
        return [
            types.Tool(
                name="get_weather",
                description="Get current weather and forecast for a location",
                inputSchema={
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location to get weather for",
                        }
                    },
                },
            ),
            types.Tool(
                name="list_locations",
                description="List all available locations with detailed weather data",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            )
        ]

    if transport == "sse":
        logger.info("Starting SSE server")
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            logger.info("New SSE connection established")
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn
        logger.info(f"Starting uvicorn server on port {port}")
        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        logger.info("Starting stdio server")
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0


if __name__ == "__main__":
    main()
