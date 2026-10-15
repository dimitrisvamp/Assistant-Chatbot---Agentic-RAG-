from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from resources.prompts.system.agentic_prompt import AGENTIC_PROMPT
from tools.tools import retrieve_knowledge_tool, save_vacation_request_tool

agent_executor = None

def initialize_agent():
    """
    Initializes the agent with the necessary tools and language model.

    Returns:
        AgentExecutor: An instance of the agent executor.
    """
    global agent_executor
    if agent_executor is None:
        llm = initialize_agent_llm()
        tools = initialize_tools()
        agent_executor = create_agent(model=llm, tools=tools, system_prompt=AGENTIC_PROMPT)
    return agent_executor
   
def initialize_tools() -> list:
    """
    Initializes the tools for the agent.

    Returns:
        list: A list of initialized tools.
    """
    tools = [retrieve_knowledge_tool, save_vacation_request_tool]
    return tools

def initialize_agent_llm() -> ChatOllama:
    """LLM initialization

    Returns:
        ChatOllama: Returns the llm model that will be used in chatbot 
    """
    llm = ChatOllama(
       model= "llama3.2",
        temperature= 0.5
    )
    return llm


