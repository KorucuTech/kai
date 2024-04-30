from typing import List
import frappe
import json
from crewai import Crew, Agent, Task, Process


@frappe.whitelist()
def run(*args,**kwargs):
    try:
        job_doc = frappe.parse_json(kwargs.get("doc"))
        if job_doc.__unsaved:
            frappe.throw("Please save the document before runing it")
        frappe.publish_progress(25, title='Running KAI Job', description='Working...')
        job_name = job_doc.name    
        job = frappe.get_doc("KAI Job",job_name)    
        crew = frappe.get_doc("KAI Crew",job.crew)
        inputs = json.loads(job.inputs)
        output = crew.kickoff(inputs=inputs)
        job.output = output
        job.save()

    except Exception as e:
        frappe.msgprint(repr(e))
    finally:
        frappe.publish_progress(100, title='Running KAI Job', description='Working...')




    

