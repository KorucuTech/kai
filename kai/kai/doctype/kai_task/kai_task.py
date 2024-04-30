# Copyright (c) 2024, Kemal Korucu and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from crewai import Crew, Agent, Task, Process

class KAITask(Document):
	def get_crewai_task(self):
		role = self.role
		goal = self.goal
		verbose = self.verbose
		return Task(role=role,goal=goal,verbose=verbose)
