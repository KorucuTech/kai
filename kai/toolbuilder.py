import frappe
from kai.frappe_tools import GetTool as GetFrappeTool
from kai.kai_tools import GetTool as GetKAITool

class ToolBuilder():
    def make_tool(package_name,function_name,tool_config):
        print("ENTERING:toolbuilder.make_tool("+package_name+","+function_name+")")

        if package_name=="frappe_tools":
            print("ENTERING:GetFrappeTool("+function_name+")")
            return GetFrappeTool(function_name,tool_config)
        
        if package_name=="kai_tools":
            print("ENTERING:GetKAITool("+function_name+")")
            return GetKAITool(function_name,tool_config)

        return None