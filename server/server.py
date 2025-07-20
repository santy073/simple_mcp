import sys

from fastmcp import FastMCP
import yaml
import requests

import utils.utils as utils
from sources import *
import tools as tools


DATABASE_ALLOWED = ["oracle", "postgres", "mssql"]
TOOLS_ALLOWED = ["fetch_data", "insert_data", "update_data", "delete_data"]

DB_CONNECTIONS: dict = {}

class Server():
    def __init__(self, config_file_name: str):
        if config_file_name is None:
            raise ValueError("Configuration file must be passed.")
        if not config_file_name.endswith(".yaml"):
            raise ValueError("Configuration file must be a YAML file.")
        self.config_file_name = config_file_name

        self.server_config_dict = utils.read_yaml_file(self.config_file_name)["server"]
        
        # Get the server name and configuration from the dictionary
        if not isinstance(self.server_config_dict, dict) or len(self.server_config_dict) == 0:
            raise ValueError("Invalid server configuration. It should be a non-empty dictionary.")
        for key in self.server_config_dict:
            self.server_name = key
            self.server_config = self.server_config_dict[key]

        self.mcp = FastMCP(name=self.server_name)

    def run(self):
        """ Starts the server with the loaded configuration.
        This method initializes the server and registers tools based on the configuration.
        It reads the configuration file, extracts the necessary details, and sets up the server.
        Raises:
            ValueError: If the configuration file is not valid or does not contain the required information.
            ServerError: If there is an issue starting the server.
            
        """
        transport = self.server_config["transport"]
        if transport not in ["http", "stdio", "sse"]:   
            raise ValueError(f"Unsupported transport type: {transport}. Supported types are 'http', 'stdio' and 'sse'.")
        print(f"Running {self.server_name} on {transport} transport.")
        # Start the server with the specified transport
        if transport == "http":
            self.mcp.run(transport=transport, port=self.server_config["port"], host=self.server_config["host"])
        elif transport == "stdio":
            self.mcp.run(transport=transport)
        elif transport == "sse":
            self.mcp.run(transport=transport)
        print("Server is running...")
        print("Registering tools...")

    def register_connections(self, connection_dict: dict):
        """ Registers database connections from the provided dictionary.
        Args:
            connection_dict (dict): A dictionary containing database connection details.
        Raises:
            ValueError: If the connection dictionary is not valid or does not contain the required information.
        """
        if not isinstance(connection_dict, dict) or len(connection_dict) == 0:
            raise ValueError("Invalid connection dictionary. It should be a non-empty dictionary.")
        for key in connection_dict:
            print(f"Database System : {key}")
            if key not in DATABASE_ALLOWED:
                raise ValueError(f"Unsupported database type: {key}. Supported types are {DATABASE_ALLOWED}.")
            connection_list = connection_dict[key]

            # if duplicate connection name exists in list raise error
            for connection_name in connection_list:
                connection_pool = {}
                # Make a databasemanager instance for each connection
                connection_config = connection_list[connection_name]
                db_url = utils.prepare_db_url(connection_config)

                # Initialize connections in MCP
                db_manager = DatabaseManager(db_url=db_url)
                db_manager.initialize_connection_pool(pool_size=5, max_overflow=10, pool_timeout=30)
                connection_pool[connection_name] = DatabaseManager(db_url=db_url)
            DB_CONNECTIONS[key] = connection_pool

        self.server_config["db_connections"] = connection_dict

        print(f"Registered database connections.")

    def register_tool(self, tool_name: str, tool_config: dict):
        """ Registers a tool with the server.
        Args:
            tool_name (str): The name of the tool to register.
            tool_config (dict): The configuration for the tool.
        Raises:
            ValueError: If the tool name is not supported or if the configuration is invalid.
        """
        if not isinstance(tool_config, dict) or len(tool_config) == 0:
            raise ValueError(f"Invalid configuration for tool {tool_name}. It should be a non-empty dictionary.")
                
        tools.make_db_tools(tool_name, tool_config)
        print(f"Tool {tool_name} registered successfully.")

    
if __name__ == "__main__":
    # get the input yaml file name from the command line arguments
 
    if len(sys.argv) < 2:
        raise ValueError("Configuration file name must be provided as a command line argument.")
    config_file_name = sys.argv[1]
    
    # Initialize the server with the configuration file
    server = Server(config_file_name)
    # server.run()

    # Register the datbase connections information
    db_yaml_file = server.server_config["database"]
    connection_dict = utils.read_yaml_file(db_yaml_file)
    server.register_connections(connection_dict)

    # Register tools for the MCP Server
    tool_yaml_file = server.server_config["tools"]
    tools_dict = utils.read_yaml_file(tool_yaml_file)
    for tool_name, tool_config in tools_dict.items():
        if tool_name not in TOOLS_ALLOWED:
            raise ValueError(f"Unsupported tool: {tool_name}. Supported tools are {TOOLS_ALLOWED}.")
        print(f"Registering tool: {tool_name}")
        server.register_tool(tool_name, tool_config)