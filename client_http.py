import asyncio
from fastmcp import Client
import requests

# async def example():
#     async with Client("http://127.0.0.1:8000/mcp/") as client:
#         await client.ping()

# if __name__ == "__main__":
#     asyncio.run(example())




MCP_SERVER_URL = "http://localhost:8000/mcp/"

async def main():
    client = Client(MCP_SERVER_URL)

    # await client.ping()  # Test the connection to the server
    async with client:
        print("Welcome to the MCP Calculator!")
        list_tools = await client.list_tools()  # List available tools
        print("Available tools:", list_tools)
        operation = input("Enter operation - add (A), subtract(S), multiply(M), divide(D): ").strip().lower()
        if operation not in {"a", "s", "m", "d"}:
            print("Invalid operation.")
            return
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid number input.")
            return
        if operation == "a": # Add
            operation="add"
        elif operation == "s":  # Subtract
            operation="subtract"
        elif operation == "m":  # Multiply
            operation="multiply"
        elif operation == "d":  # Divide
            operation="divide"
        # Now print the result
        try:
            result = await client.call_tool(operation, arguments={"num1": a, "num2": b})
            if result is None:
                print("No result returned from the server.")
            else:
                print(f"Result: {result.data}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())