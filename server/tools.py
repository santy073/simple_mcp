from server import DB_CONNECTIONS
from fastmcp import FastMCP


# Tool for database operations
def fetch_data(tool_name: str, tool_config: dict, connection_config: dict):
    """
    Fetch data from the database based on the provided query.
    Args:
        query: SQL query to fetch data
    Returns:
        Data fetched from the database
    """
    # get source, connection name and other details from tool_config
    print(f"Tool name: {tool_name}")
    print(f"Tool config: {tool_config}")
    print(f"Connection config: {connection_config}")


    source = tool_config["source"]
    connection_name = tool_config["connection"]
    query = tool_config["query"]

    print(f"Source: {source}, Connection Name: {connection_name}, Query: {query}")
    if not source or not connection_name or not query:
        raise ValueError("Tool configuration must include 'source', 'connection_name', and 'query'.")
    # Now connect to the database using connection_config
    connection = connection_config[source][connection_name]
    if not connection:
        raise ValueError(f"Connection details for {connection_name} not found in connection configuration.")
    # Connect and execute query
    print(f"Fetching data from {source} using connection {connection_name} with query: {query}")
    #return connection.read_data(query)
    return {"source": source, "connection_name": connection_name, "query": query, "data": "Sample Data"}

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
        def tool_func() -> dict:
            return fetch_data(tool_name, tool_config=tool_config, connection_config=connection_config)
    elif inbuilt_name == "insert_data":
        @mcp.tool(name=tool_name, description=description)
        def tool_func() -> dict:
            return insert_data(tool_config=tool_config, connection_config=connection_config)
    else:
        raise ValueError(f"Unknown Tool type name: {inbuilt_name}. Check documentaton for allowed tool types")
    return tool_func
