## KAI

KAI is a custom app for Frappe Framework that implements CrewAI framework to integrate AI Agents with Frappe Framework.
If you are not familiar with these platforms please take a look at the following web sites.

- https://www.crewai.com/
- https://frappeframework.com/

#### KEY CONCEPTS

- LLM
:: Large Language Models are machine learning models that can comprehend and generate human language text.
- CREW
:: A crew represents a collaborative group of agents working together to achieve a set of tasks.
- AGENT
:: An agent is an autonomous unit programmed to perform TASKS, make decisions and communicate with other agents.
- TASK
:: Specific assignments completed by agents.
- TOOL
:: A tool in is a skill or function that agents can utilize to perform various actions. 
- JOB
:: Set of Inputs given to a crew to be used by agents to produce a result or output.

#### INSTALLATION

Since KAI is a Custom Frappe App it can be installed using frapp bench commands.
```
bench get-app https://github.com/KorucuTech/kai.git
...
bench --site your-site-name install kai
```
#### License

MIT

## How to Run

1. Via UI --
Create a KAI Job and enter your JSON data in to "Inputs" field then click "Run".

2. Via Code --

Call the "run" method in api.py file.

3. Via Code --
 
