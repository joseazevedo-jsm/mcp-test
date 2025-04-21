# Weather MCP Client

A web-based client application that interfaces with the MCP Weather Server to display weather information for various locations.

## Features

- Clean, responsive UI for viewing weather data
- Real-time connection with the MCP Weather Server
- Search for any location's weather
- View current conditions and forecast
- List of available locations for quick selection

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/weather-client.git
cd weather-client

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package and dependencies
uv pip install -e .

# Ensure the mcp-weather-server is installed as well
uv pip install -e ../mcp-weather-server  # Adjust path as needed
```

## Usage

1. Make sure the MCP Weather Server is properly installed
2. Run the client application:

```bash
# Run the Flask app
flask --app weather_client.app run
```

3. Open your web browser and navigate to http://localhost:5000
4. Use the search box to find weather for different locations

## Architecture

The application consists of:

1. **Flask Backend**: Serves the web interface and communicates with the MCP server
2. **MCP Client**: Uses the Model Context Protocol to interact with the Weather Server
3. **Frontend**: HTML/CSS/JS for user interaction and data display

## Note

This client uses mock data provided by the MCP Weather Server. In a production environment, you would connect to a real weather API service.

## Dependencies

- Flask (web framework)
- MCP Python SDK (for server communication)
- MCP Weather Server (provides the weather data)
