# Copyright (c) 2024, Kemal Korucu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from crewai import Crew, Agent, Task, Process
import json
from kai.crewbuilder import CrewBuilder

class KAICrew(Document):
		
	def kickoff(self,**kwargs):
		kai_crew_name = self.name
		crewbuilder = CrewBuilder(kai_crew_name)
		inputs = kwargs.get("inputs")
		output = crewbuilder.kickoff(inputs=inputs)
		return output

