import pytest
import sys 
from pathlib import Path 
from unittest.mock import MagicMock, patch
## Adjust the path to import the module under test
SRC_PATH = Path(__file__).resolve().parents[2]
MAIN_PATH = SRC_PATH / "main"
sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(MAIN_PATH))
from main.service.agent_initializer import initialize_agent, initialize_tools, initialize_agent_llm
import main.service.agent_initializer as agent_initializer

# ============================================================ 
# # initialize_tools() #
# ============================================================

def test_initialize_tools_returns_expected_tools(): 
    """ 
    initialize_tools() should return the tools used by the agent. 
    """ 
    tools = initialize_tools() 
    assert tools == [ agent_initializer.retrieve_knowledge_tool, agent_initializer.save_vacation_request_tool, ]

def test_initialize_tools_returns_list():
    """ 
    initialize_tools() should return a list. 
    """ 
    tools = initialize_tools() 
    assert isinstance(tools, list)

def test_initialize_tools_contains_two_tools(): 
    """ 
    The agent should be initialized with exactly two tools. 
    """ 
    tools = initialize_tools() 
    assert len(tools) == 2

# ============================================================ 
# # initialize_agent_llm() # 
# ============================================================

@patch("main.service.agent_initializer.ChatOllama") 
def test_initialize_agent_llm(mock_chat_ollama): 
    """ 
    initialize_agent_llm() should initialize ChatOllama with the expected model and temperature. 
    """ 
    mock_llm = MagicMock() 
    mock_chat_ollama.return_value = mock_llm 
    result = initialize_agent_llm() 
    mock_chat_ollama.assert_called_once_with( model="llama3.2", temperature=0.5, )

    assert result == mock_llm

# ============================================================ 
# # initialize_agent() # 
# ============================================================

@patch("main.service.agent_initializer.create_agent") 
@patch("main.service.agent_initializer.initialize_tools") 
@patch("main.service.agent_initializer.initialize_agent_llm") 
def test_initialize_agent( mock_initialize_agent_llm, mock_initialize_tools, mock_create_agent, ): 
    """ 
    initialize_agent() should: 1. Initialize the LLM. 2. Initialize the tools. 3. Create the agent with the LLM, tools and system prompt. 4. Return the created agent. 
    """
    # Reset global state 
    agent_initializer.agent_executor = None 

    # Create fake objects 
    mock_llm = MagicMock() 
    mock_tools = [MagicMock(), MagicMock()] 
    mock_agent = MagicMock() 

    # Configure mocks 
    mock_initialize_agent_llm.return_value = mock_llm 
    mock_initialize_tools.return_value = mock_tools 
    mock_create_agent.return_value = mock_agent 

    # Execute 
    result = initialize_agent() 

    # -------------------------------------------------------- 
    # Verify LLM initialization 
    # -------------------------------------------------------- 
    mock_initialize_agent_llm.assert_called_once() 

    # -------------------------------------------------------- 
    # Verify tools initialization 
    # -------------------------------------------------------- 
    mock_initialize_tools.assert_called_once() 

    # -------------------------------------------------------- 
    # Verify agent creation 
    # -------------------------------------------------------- 
    mock_create_agent.assert_called_once_with( model=mock_llm, tools=mock_tools, system_prompt=agent_initializer.AGENTIC_PROMPT, ) 

    # -------------------------------------------------------- 
    # Verify returned agent 
    # -------------------------------------------------------- 
    assert result == mock_agent 

    # Clean up global state 
    agent_initializer.agent_executor = None

@patch("main.service.agent_initializer.create_agent") 
@patch("main.service.agent_initializer.initialize_tools") 
@patch("main.service.agent_initializer.initialize_agent_llm") 
def test_initialize_agent_reuses_existing_agent( mock_initialize_agent_llm, mock_initialize_tools, mock_create_agent, ): 
    """ 
    initialize_agent() should return the existing agent if it has already been initialized. 
    """ 
    # Create an already initialized agent 
    existing_agent = MagicMock() 
    agent_initializer.agent_executor = existing_agent 

    # Execute 
    result = initialize_agent() 

    # Should return the existing agent 
    assert result == existing_agent 

    # Nothing should be initialized again 
    mock_initialize_agent_llm.assert_not_called() 
    mock_initialize_tools.assert_not_called() 
    mock_create_agent.assert_not_called() 

    # Clean up global state 
    agent_initializer.agent_executor = None