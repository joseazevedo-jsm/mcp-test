#!/bin/bash

# Script to set up and run the Weather MCP ecosystem
# This includes both the server and client components

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install server package
echo "Installing Weather MCP Server..."
cd mcp-weather-server
uv pip install -e .
cd ..

# Install client package
echo "Installing Weather MCP Client..."
cd weather-client
uv pip install -e .
cd ..

# Start the Flask client application
echo "Starting Weather Client application..."
echo "Once the server starts, navigate to http://localhost:5000 in your browser"
cd weather-client
flask --app weather_client.app run