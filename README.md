# Simple MCP Calculator

This project demonstrates a simple MCP client-server application using FastMCP.

## Server
- Exposes calculation tools: add, subtract, multiply, divide
- Run with: `python server.py`
- Listens on: http://localhost:8000

## Client
- Prompts user for operation and numbers
- Sends request to MCP server and prints result
- Run with: `python client.py`

## Requirements
- Python 3.8+
- fastmcp, fastapi, uvicorn, requests

## Usage
1. Start the server: `python server.py`
2. In another terminal, run the client: `python client.py`
