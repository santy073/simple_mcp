from fastmcp import FastMCP
import yaml
import requests

mcp = FastMCP("Calculator MCP Server")

def add(a: float, b: float) -> float:
    """
    Add two input numbers.
    Args:
        a: First number
        b: Second number
    Returns:
        The sum of the two numbers
    """
    print(f"Adding {a} and {b}")
    return a + b

def make_tool(inbuilt_name: str, tool_name: str, description: str, params: dict, return_type: str):
    """
    Decorator to create a tool function with the given name, description, parameters, and return type.
    """
    if inbuilt_name == "add":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(num1: float, num2: float) -> float:
            print(f"Adding {num1} and {num2}")
            return add(num1, num2)
    elif inbuilt_name == "subtract":
        @mcp.tool(name=tool_name, description=description)
        def tool_func(num1: float, num2: float) -> float:
            print(f"Subtracting {num2} from {num1}")
            return num1 - num2
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
        raise ValueError(f"Unknown inbuilt name: {inbuilt_name}")
    return tool_func

# Load configuration from YAML file
with open("tool.yaml") as f:
        config = yaml.safe_load(f)["featurestore"]
        print(type(config))
        print(config)
    
for key in config:
    print(f"Feature: {key}")
    print(f"Feature Type: {config[key][0]['type']}")
    # print(f"Registering tool: " + feature_details[1]["tool_name"] - feature_details[2]["description"])
    make_tool(config[key][1]["inbuilt_name"], 
              config[key][2]["tool_name"], 
              config[key][3]["description"], 
              config[key][4]["params"], 
              config[key][5]["return"])
# for provider in config.items():
#     method = provider.get("method", "GET")
#     path = req["path"]
#     description = req.get("description", "")
#     params = req.get("params")
#     body = req.get("body")
#     tool_name = f"{provider}_{path.replace('/', '_').replace('.', '_')}".lower()
#         def make_tool(p=provider, pa=path, m=method, param=params, body_fields=body):
#             full_desc = description
#             if param:
#                 full_desc += "\nParams: " + ", ".join(param.keys())
#             if body_fields:
#                 full_desc += "\nBody: " + ", ".join(body_fields.keys())
#             @mcp.tool(name=tool_name, description=full_desc)
#             def tool_func(provider_config_key: str, param: dict = None, body: dict = None):
#                 url = f"{NANGO_API}/{pa}"
#                 headers = {
#                     "Authorization": "Bearer <your-nango-token>",
#                     "Provider-Config-Key": provider_config_key
#                 }
#                 response = requests.request(m, url=url, headers=headers,
#                                             params=param, json=body)
#                 try:
#                     return response.json()
#                 except:
#                     return {"error": response.text, "status_code": response.status_code}
            
#             return tool_func
#         make_tool()
# @mcp.tool()
# def add(a: float, b: float) -> float:
#     """
#     Add two input numbers.
#     Args:
#         a: First number
#         b: Second number
#     Returns:
#         The sum of the two numbers
#     """
#     print(f"Adding {a} and {b}")
#     return a + b

# @mcp.tool()
# def subtract(a: float, b: float) -> float:
#     """
#     Subtract two input numbers.
#     Args:
#         a: First number
#         b: Second number
#     Returns:
#         The subtraction of the two numbers
#     """
#     print(f"Subtracting {b} from {a}")
#     return a - b

# @mcp.tool()
# def multiply(a: float, b: float) -> float:
#     """
#     Multiply two input numbers.
#     Args:
#         a: First number
#         b: Second number
#     Returns:
#         The multiplication result of the two numbers
#     """
#     print(f"Multiplying {a} and {b}")
#     return a * b

# @mcp.tool()
# def divide(a: float, b: float) -> float:
#     """
#     Divide two input numbers.
#     Args:
#         a: First number
#         b: Second number
#     Returns:
#         The divirion result of the two numbers
#     """
#     print(f"Dividing {a} by {b}")
#     if b == 0:
#         raise ValueError("Division by zero is not allowed.")
#     return a / b


    
    
if __name__ == "__main__":
    mcp.run(transport="http")