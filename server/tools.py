from server import DB_CONNECTIONS
from fastmcp import FastMCP


# Tool for database operations
def fetch_data(tool_config: dict, connection_config: dict):
    """
    Fetch data from the database based on the provided query.
    Args:
        query: SQL query to fetch data
    Returns:
        Data fetched from the database
    """
    # get source, connection name and other details from tool_config
    source = tool_config.get("source")
    connection_name = tool_config.get("connection_name")
    query = tool_config.get("query")
    if not source or not connection_name or not query:
        raise ValueError("Tool configuration must include 'source', 'connection_name', and 'query'.")
    # now connect to the database using connection_config
    connection_details = connection_config.get(connection_name)
    if not connection_details:
        raise ValueError(f"Connection details for {connection_name} not found in connection configuration.")
    # connect and execute query
    print(f"Fetching data from {source} using connection {connection_name} with query: {query}")
    return DB_CONNECTIONS.read_data(query)

def insert_data(tool_config: dict, connection_config: dict):
    """
    Insert data from the database based on the provided query.
    Args:
        query: SQL query to fetch data
    Returns:
        Data fetched from the database
    """
    # get source, connection name and other details from tool_config
    source = tool_config.get("source")
    connection_name = tool_config.get("connection_name")
    query = tool_config.get("query")
    if not source or not connection_name or not query:
        raise ValueError("Tool configuration must include 'source', 'connection_name', and 'query'.")
    # now connect to the database using connection_config
    connection_details = connection_config.get(connection_name)
    if not connection_details:
        raise ValueError(f"Connection details for {connection_name} not found in connection configuration.")
    # connect and execute query
    print(f"Fetching data from {source} using connection {connection_name} with query: {query}")
    return DB_CONNECTIONS.read_data(query)



def make_db_tools(tool_name: str, tool_config: dict, connection_config:dict, mcp:FastMCP):
    """
    Decorator to create a tool function with the given name, description, parameters, and return type.
    """
    inbuilt_name = tool_config.get("type")
    description = tool_config.get("description", "")
    if inbuilt_name == "fetch_data":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(query: str) -> dict:
            return fetch_data(tool_config=tool_config, connection_config=connection_config)
    elif inbuilt_name == "insert_data":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(query: str) -> dict:
            return insert_data(tool_config=tool_config, connection_config=connection_config)
    elif inbuilt_name == "multiply":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(num1: float, num2: float) -> float:
            print(f"Multiplying {num1} and {num2}")
            return num1 * num2
    elif inbuilt_name == "divide":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(num1: float, num2: float) -> float:
            print(f"Dividing {num1} by {num2}")
            if num2 == 0:
                raise ValueError("Division by zero is not allowed.")
            return num1 / num2
    else:
        raise ValueError(f"Unknown Tool type name: {inbuilt_name}. Check documentaton for allowed tool types")
    return tool_func
