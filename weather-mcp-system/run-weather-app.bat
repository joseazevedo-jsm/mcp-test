@echo off
SETLOCAL

REM Script to set up and run the Weather MCP ecosystem
REM This includes both the server and client components

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    uv venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install server package
echo Installing Weather MCP Server...
cd mcp-weather-server
uv pip install -e .
cd ..

REM Install client package
echo Installing Weather MCP Client...
cd weather-client
uv pip install -e .
cd ..

REM Start the Flask client application
echo Starting Weather Client application...
echo Once the server starts, navigate to http://localhost:5000 in your browser
cd weather-client
flask --app weather_client.app run

ENDLOCAL
