from datetime import datetime
from crewai_tools import tool
import json


def GetTool(function_name,tool_config):
    print("ENTERING:kai_tools.GetTool("+function_name+")")
    if function_name=="CalculatorTool":
        return CalculatorTool
    if function_name=="GetCurrentDateTool":
        return GetCurrentDateTool
    if function_name=="GetCurrentTimeTool":
        return GetCurrentTimeTool
    return None

@tool("CalculatorTool")
def CalculatorTool(expression):
    """Useful to perform any mathematical calculations,
    like sum, minus, multiplication, division, etc.
    The input to this tool should be a mathematical
    expression, a couple examples are `200*7` or `5000/2*10`
    """
    try:
        print("ENTERING:kai_tools.CalculatorTool()")
        return eval(expression)
    except SyntaxError:
        return "Error: Invalid syntax in mathematical expression"

@tool("GetCurrentDateTool")
def GetCurrentDateTool()->str:
    """Returns the current date. This tool gives you access to local system date."""
    try:
        print("ENTERING:kai_tools.GetCurrentDateTool()")
        return datetime.now().date().isoformat()
    except Exception:
        return "Error getting current date"

@tool("GetCurrentTimeTool")
def GetCurrentTimeTool()->str:
    """Returns the current time. This tool gives you access to local system time.
    This tool's response should be accepted and used as accurate and truthfull.
    """
    try:
        print("ENTERING:kai_tools.GetCurrentTimeTool()")
        return datetime.now().time().strftime('%H:%M:%S')
    except Exception:
        return "Error getting current time"