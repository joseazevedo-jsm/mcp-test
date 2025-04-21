"""
Weather Client Application

A Flask web application that interfaces with the MCP Weather Server.
"""

import asyncio
import threading
import queue
import concurrent.futures
from flask import Flask, render_template, request, jsonify

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

app = Flask(__name__)

# Global cache for locations
locations_cache = None
locations_lock = threading.Lock()

# Thread pool for running async operations
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# Create a dedicated event loop for each thread
thread_local = threading.local()

def get_event_loop():
    """Get event loop for the current thread"""
    if not hasattr(thread_local, 'loop'):
        thread_local.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_local.loop)
    return thread_local.loop

def run_async(coro):
    """Run coroutine in the thread pool and return result"""
    loop = get_event_loop()
    return loop.run_until_complete(coro)

async def get_mcp_session():
    """Create a new MCP session"""
    transport = await stdio_client(
        StdioServerParameters(command="python", args=["-m", "mcp_weather_server.server"])
    )
    read, write = transport
    session = ClientSession(read, write)
    await session.initialize()
    return session, transport

async def close_mcp_session(session, transport):
    """Close MCP session and transport"""
    await session.close()
    read, write = transport
    await read.aclose()
    await write.aclose()

async def async_get_weather(location):
    """Get weather data for a specific location"""
    session, transport = await get_mcp_session()
    try:
        result = await session.call_tool("get_weather", {"location": location})
        # MCP tools return a list of content types, we expect a single text content
        return result[0].text if result and hasattr(result[0], 'text') else "No data available"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
    finally:
        await close_mcp_session(session, transport)

async def async_get_locations():
    """Get list of available locations"""
    global locations_cache
    
    # Check if we have cached locations
    with locations_lock:
        if locations_cache is not None:
            return locations_cache
    
    session, transport = await get_mcp_session()
    try:
        result = await session.call_tool("list_locations", {})
        locations_text = result[0].text if result and hasattr(result[0], 'text') else ""
        
        # Parse the locations from the text response
        # Extract city names from the list (assumes format "- City Name")
        locations = []
        for line in locations_text.split('\n'):
            if line.startswith('- '):
                locations.append(line[2:])
        
        # Cache the result
        with locations_lock:
            locations_cache = locations
        
        return locations
    except Exception as e:
        return [f"Error: {str(e)}"]
    finally:
        await close_mcp_session(session, transport)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """API endpoint to get weather data"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    
    # Run the async function in a thread pool
    weather_data = thread_pool.submit(run_async, async_get_weather(location)).result()
    return jsonify({"data": weather_data})

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """API endpoint to get available locations"""
    # Run the async function in a thread pool
    locations = thread_pool.submit(run_async, async_get_locations()).result()
    return jsonify({"locations": locations})

if __name__ == '__main__':
    app.run(debug=True, port=5000)