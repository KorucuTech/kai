from crewai_tools import tool
import frappe
import json

def GetTool(function_name,tool_config):
    print("ENTERING:frappe_tools.GetTool("+function_name+")")
    if function_name=="GetFrappeUserTool":
        return GetFrappeUserTool




@tool("GetFrappeUserTool")
def GetFrappeUserTool(email):
    """Given a user email address as input this tool returns detailed information about the user as output."""
    print("ENTERING:frappe_tools.GetFrappeUserTool("+email+")")
    output = {}
    try:
        user_doc = frappe.get_doc("User",email)

        output["email"] = user_doc.email 
        output["first_name"] = user_doc.first_name
        output["last_name"] = user_doc.last_name
        output["full_name"] = user_doc.full_name
        output["enabled"] = (user_doc.enabled==1)
    except:
        output="User NOT Found"
    return json.dumps(output)


