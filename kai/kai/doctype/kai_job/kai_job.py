# Copyright (c) 2024, Kemal Korucu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class KAIJob(Document):
	def run(self):
		kai_crew_name = self.crew
		crew = frappe.get_doc("KAI Crew",kai_crew_name)
		inputs = json.loads(self.inputs)
		output = crew.kickoff(inputs=inputs)
		self.output = output
		self.save()
		return output
