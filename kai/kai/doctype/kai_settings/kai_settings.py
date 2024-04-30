# Copyright (c) 2024, Kemal Korucu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from jinja2 import Template,Environment
from ollama import Client
from openai import OpenAI
from groq import Groq
from pydantic import BaseModel	

class KAISettings(Document):
	pass

@frappe.whitelist()
def ai_call(**args):

	cmd = args.get("cmd")
	if cmd != "kai.kai.doctype.kai_settings.kai_settings.ai_call":
		raise Exception("Invalid command")	
	
	if args.get("enabled")=="1":
		llm_name = args.get("llm")
		connection = frappe.get_doc("KAI LLM",llm_name)
		settings = json.loads(connection.settings)

		if settings=={}:
			raise Exception("Invalid KAI Connection Settings")
		
		if connection.type=="Ollama":
			return ollama_call(settings,**args)
		elif connection.type=="OpenAI":
			return openai_call(settings,**args)
		elif connection.type=="AWS Bedrock":
			return aws_bedrock_call(settings,**args)
		elif connection.type=="GroqCloud":
			return groqcloud_call(settings,**args)
		else:
			raise Exception("Invalid KAI Connection Type")
	else:
		raise Exception("KAI is not enabled")
	return 

#=================================================================================================================
def openai_call(settings,**args):

	client = OpenAI(organization="org-JER4FXhVu4MFXOvivkVp8VGJ",
				 project="proj_akxU2ChkyMciKKTLymW77Nho",

		api_key=args.get("api_access_key"))

	agent_instruction_prompt = args.get("agent_instruction_prompt")
	print(agent_instruction_prompt)

	environment = Environment()
	template = environment.from_string(args.get("system_prompt"))
	system_prompt = template.render(agent_instruction_prompt=agent_instruction_prompt)

	print(system_prompt)


	response = client.  Completion.create(
		engine="text-davinci-003",  # Model to use for completion
		prompt=system_prompt,
		temperature=0.7,  # Controls randomness of the response
		max_tokens=50,  # Maximum number of tokens (words) in the response
	)

	print(response)
	return response

#=================================================================================================================
def ollama_call(settings,**args):

	agent_instruction_prompt = args.get("agent_instruction_prompt")

	environment = Environment()
	template = environment.from_string(args.get("system_prompt"))
	system_prompt = template.render(agent_instruction_prompt=agent_instruction_prompt)

	print(system_prompt)

	client = Client(settings["host"])
	response = client.chat(model=settings["model"],stream=settings["stream"],options=settings["options"], messages=[
		{
			'role': 'system',
			'content': system_prompt
		},
		{
			'role': 'user',
			'content': args.get("user_request")
		}
	])

	response = json.loads(json.dumps(response))
	answer = response["message"]["content"]
	print(answer)
	return str(answer)

#=================================================================================================================
def aws_bedrock_call(settings,**args):
	return args

#=================================================================================================================
def groqcloud_call(settings,**args):
	client = Groq(api_key=settings["api_key"])

	agent_instruction_prompt = args.get("agent_instruction_prompt")

	environment = Environment()
	template = environment.from_string(args.get("system_prompt"))
	system_prompt = template.render(agent_instruction_prompt=agent_instruction_prompt)

	print(system_prompt)

	response = client.chat.completions.create(messages=[
			{
				'role': 'system',
				'content': system_prompt
			},
			{
				'role': 'user',
				'content': args.get("user_request")
			}
		],
		model=settings["model"],
		temperature=settings["temperature"]
	)
	print(response)

	return response.choices[0].message.content


