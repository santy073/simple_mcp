import yaml
import os

def read_yaml_file(yaml_file_name: str) -> dict:
    """
    Reads a YAML file and returns its content.
    Returns:
        The content of the YAML file as a dictionary.
    """
    if not yaml_file_name.endswith(".yaml"):
        raise ValueError("Configuration file must be a YAML file.")
    if not os.path.exists(yaml_file_name):
        raise FileNotFoundError(f"Configuration file {yaml_file_name} does not exist.")
    
    # Open the YAML file and load its content
    print(f"Reading configuration from {yaml_file_name}")
    with open(yaml_file_name, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    

def prepare_db_url(connection_details: dict) -> str:
    """
    Prepares a database connection URL based on the provided parameters.
    Args:
        db_type: Type of the database (e.g., 'postgres', 'mysql', etc.)
        host: Hostname of the database server
        port: Port number of the database server
        database: Name of the database
        user: Username for the database connection
        password: Password for the database connection
    Returns:
        A formatted database connection URL.
    """
    db_type = connection_details.get("db_type")
    host = connection_details.get("host")
    port = connection_details.get("port")
    database = connection_details.get("database")
    user = connection_details.get("user")
    password = connection_details.get("password")

    if db_type == "postgres":
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    elif db_type == "mysql":
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    elif db_type == "oracle":
        return f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")