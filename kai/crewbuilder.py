import frappe
from crewai import Crew, Agent, Task, Process
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI, OpenAI
from langchain_groq import ChatGroq
from kai.toolbuilder import ToolBuilder
import json
import pprint
import os

class CrewBuilder:
    def __init__(self,kai_crew_name):
        print("ENTERING:__init__("+kai_crew_name+")")
        #These act as cache for created objects
        self.llm_list = {}
        self.tool_list = {}
        self.task_list = {}
        self.agent_list = {}

        # Variables for passing obejcts to crew at the end
        self.crew = None    
        self.crew_tasks = []
        self.crew_agents = []
        self.crew_manager_llm = None
        self.crew_function_calling_llm = None

        # Get "KAI Crew" Doc by crew name
        self.kai_crew_doc = frappe.get_doc("KAI Crew",kai_crew_name)
        print("CREW.AGENTS:",self.kai_crew_doc.agents)
        print("CREW.TASKS:",self.kai_crew_doc.tasks)

        # Set Crew Config from doc
        self.crew_config = {
            'process': self.kai_crew_doc.process_flow,
            'verbose': self.kai_crew_doc.verbose,
            'max_rpm': self.kai_crew_doc.max_rpm,
            'full_output': self.kai_crew_doc.full_output,
            'memory': self.kai_crew_doc.memory
            }

        # Set Manager LLM for Crew from doc
        m_llm = self.get_llm(self.kai_crew_doc.manager_llm)
        if m_llm:
            self.crew_manager_llm = m_llm

        # Set Function Calling LLM for Crew
        f_llm = self.get_llm(self.kai_crew_doc.function_calling_llm)
        if f_llm:
            self.crew_function_calling_llm = f_llm

        # Set Agents for Crew
        if self.kai_crew_doc.agents==[]:
            raise Exception("KAI Crew has no actions assigned")
        else:
            for kai_agent in self.kai_crew_doc.agents:
                kai_agent_name = kai_agent.agent
                agent = self.get_agent(kai_agent_name)
                if agent:
                    self.crew_agents.append(agent)

        #  Set Tasks for Crew
        if self.kai_crew_doc.tasks==[]:
            raise Exception("KAI Crew has no tasks assigned")
        else:
            for kai_task in self.kai_crew_doc.tasks:
                kai_task_name = kai_task.task
                task = self.get_task(kai_task_name)
                if task:
                    self.crew_tasks.append(task)

        # Build Crew  
        self.crew = Crew(agents=self.crew_agents,
                    tasks=self.crew_tasks,
                    process=self.kai_crew_doc.process_flow,
                    verbode=self.kai_crew_doc.verbose,
                    manager_llm=self.crew_manager_llm,
                    function_calling_llm=self.crew_function_calling_llm
                    )


    # Create or return an existing LLM
    def get_llm(self,kai_llm_name):
        print("ENTERING:get_llm("+kai_llm_name+")")
        # if llm name not provided return None
        if not kai_llm_name:
            return None
        # if LLM is already created just return it
        if kai_llm_name in self.llm_list:
            return self.llm_list[kai_llm_name]
        else:
            kai_llm_doc = frappe.get_doc("KAI LLM",kai_llm_name)
            llm_provider = kai_llm_doc.llm_provider
            llm_settings = json.loads(kai_llm_doc.settings)

            # Create llm based on llm provider type
            if llm_provider=='Ollama':
                os.environ["OPENAI_API_KEY"] = "NA"
                llm = ChatOpenAI(model=llm_settings["model"],
                                 base_url = llm_settings["base_url"])
                if llm:
                    self.llm_list[kai_llm_name] = llm
                return llm
            elif llm_provider=='OpenAI':
                pass
            elif llm_provider=='AWS Bedrock':
                pass
            elif llm_provider=='GroqCloud':
                    llm = ChatGroq(
                        #groq_api_base=llm_settings["groq_api_base"],
                        temperature=llm_settings["temperature"], 
                        groq_api_key=llm_settings["groq_api_key"], 
                        model_name=llm_settings["model_name"],
                        streaming=llm_settings["streaming"],
                        max_retries=llm_settings["max_retries"],
                        max_tokens=llm_settings["max_tokens"],
                        verbose=llm_settings["verbose"]
                    )
                    if llm:
                        self.llm_list[kai_llm_name] = llm                    
                    return llm
            else:
                raise Exception("Unknow LLM Provider")            

    # Create or return an existing Agent
    def get_agent(self,kai_agent_name):
        print("ENTERING:get_agent("+kai_agent_name+")")
        # if agent name is not provided return None
        if not kai_agent_name:
            return None
        # If agent is already created just rewutn it
        if kai_agent_name in self.agent_list:
            return self.agent_list[kai_agent_name]
        else:
            kai_agent_doc = frappe.get_doc("KAI Agent",kai_agent_name)
            agent_tools=[]
            for kai_agent_tool in kai_agent_doc.tools:
                kai_agent_tool_name = kai_agent_tool.tool
                kai_tool = frappe.get_doc("KAI Tool",kai_agent_tool_name)
                tool = self.get_tool(kai_tool.name)
                if tool:
                    agent_tools.append(tool)

            agent = Agent(role=kai_agent_doc.role,
                          goal=kai_agent_doc.goal,
                          backstory=kai_agent_doc.backstory,
                          llm=self.get_llm(kai_agent_doc.llm),
                          function_calling_llm=self.get_llm(kai_agent_doc.function_calling_llm),
                          max_iter=kai_agent_doc.max_iterations,
                          max_rpm=kai_agent_doc.max_rpm,
                          max_execution_time=kai_agent_doc.max_execution_time,
                          verbose=kai_agent_doc.verbose,
                          allow_delegation=kai_agent_doc.allow_delegation,
                          tools=agent_tools
                          )
            # Save the created Agent
            if agent:
                self.agent_list[kai_agent_name] = agent
            return agent   
        
    # Create or return an existing Task
    def get_task(self,kai_task_name):
        print("ENTERING:get_task("+kai_task_name+")")
        # if task name is not provided return None
        if not kai_task_name:
            return None
        # If task is already created just return it
        if kai_task_name in self.task_list:
            return self.task_list[kai_task_name]
        else:
            kai_task_doc = frappe.get_doc("KAI Task",kai_task_name)
            # Get Tools for the Task
            task_tools=[]
            for kai_task_tool in kai_task_doc.tools:
                kai_task_tool_name = kai_task_tool.tool
                kai_tool = frappe.get_doc("KAI Tool",kai_task_tool_name)
                tool = self.get_tool(kai_tool.name)
                if tool:
                    task_tools.append(tool)
            # Get Context Tasks for the Task
            task_context=[]
            for kai_context in kai_task_doc.context:
                kai_context_name = kai_context.task
                context = self.get_task(kai_context_name)
                if context:
                    task_context.append(context)

            task = Task(agent=self.get_agent(kai_task_doc.agent),
                        description=kai_task_doc.description,
                        expected_output=kai_task_doc.expected_output,
                        tools=task_tools,
                        context=task_context
                        )
            if task:
                self.task_list[kai_task_name] = task
            return task

    # Create or return an existing Tool
    def get_tool(self,kai_tool_name):
        print("ENTERING:crewbuilder.get_tool("+kai_tool_name+")")
        # if tool name is not provided return None
        if not kai_tool_name:
            return None
        # If tool is already created just return it
        if kai_tool_name in self.tool_list:
            return self.tool_list[kai_tool_name]
        else:
            tool = self.make_tool(kai_tool_name)
            if tool:
                self.tool_list[kai_tool_name] = tool
            return tool    

    # Return the generated Crew
    def get_crew(self):
        print("ENTERING:get_crew()")
        return self.crew
    
    # Run the Crew
    def kickoff(self,**kwargs):
        print("ENTERING:kickoff()")
        return self.crew.kickoff(inputs=kwargs.get("inputs"))
    

    def make_tool(self,kai_tool_name):
        # if tool name is not provided return None
        if not kai_tool_name:
            print("ENTERING:crewbuilder.make_tool(NONE)")
            return None
        try:
            print("ENTERING:crewbuilder.make_tool("+kai_tool_name+")")
            kai_tool_doc = frappe.get_doc("KAI Tool",kai_tool_name)
            kai_tool_package = kai_tool_doc.from_package
            kai_tool_function = kai_tool_doc.tool_function
            kai_tool_config = kai_tool_doc.tool_config
            tool = ToolBuilder.make_tool(kai_tool_package,kai_tool_function,kai_tool_config)
        except Exception:
            print("ERROR: make_tool")
            return None    

        return tool



