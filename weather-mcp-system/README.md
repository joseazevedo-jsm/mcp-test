# Weather MCP System

A weather monitoring and control system consisting of a server and web client.

## Project Structure

```
weather-mcp-system/
├── mcp-weather-server/       # MCP server implementation
│   ├── mcp_weather_server/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── server.py         # Main server implementation
│   ├── pyproject.toml
│   └── README.md
│
├── weather-client/           # Web client implementation
│   ├── weather_client/
│   │   ├── __init__.py
│   │   ├── app.py            # Flask application
│   │   ├── templates/
│   │   │   └── index.html    # HTML template
│   │   └── static/
│   │       ├── css/
│   │       │   └── style.css # CSS styles
│   │       └── js/
│   │           └── app.js    # Frontend JavaScript
│   ├── pyproject.toml
│   └── README.md
│
├── run-weather-app.sh        # Unix/Mac setup and run script
├── run-weather-app.bat       # Windows setup and run script
└── README.md                 # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-mcp-system
```

2. Install dependencies for both server and client:
```bash
# Install server dependencies
cd mcp-weather-server
pip install -e .

# Install client dependencies
cd ../weather-client
pip install -e .
```

## Running the Application

### Windows
Double-click `run-weather-app.bat` or run it from the command prompt:
```bash
.\run-weather-app.bat
```

### Unix/Mac
Make the script executable and run it:
```bash
chmod +x run-weather-app.sh
./run-weather-app.sh
```

## Accessing the Application

- Server: http://127.0.0.1:8888
- Client: http://127.0.0.1:5000

## Development

### Server Development
The server is implemented in Python using asyncio for asynchronous communication.

### Client Development
The client is a Flask web application with a modern, responsive interface.

## License

[Your License Here] 