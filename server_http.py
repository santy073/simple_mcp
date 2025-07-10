from fastmcp import FastMCP

mcp = FastMCP("Calculator MCP Server")

@mcp.tool()
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

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtract two input numbers.
    Args:
        a: First number
        b: Second number
    Returns:
        The subtraction of the two numbers
    """
    print(f"Subtracting {b} from {a}")
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiply two input numbers.
    Args:
        a: First number
        b: Second number
    Returns:
        The multiplication result of the two numbers
    """
    print(f"Multiplying {a} and {b}")
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide two input numbers.
    Args:
        a: First number
        b: Second number
    Returns:
        The divirion result of the two numbers
    """
    print(f"Dividing {a} by {b}")
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


if __name__ == "__main__":
    mcp.run(transport="http")