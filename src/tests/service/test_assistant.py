import pytest
import sys 
from pathlib import Path 
from unittest.mock import MagicMock, patch
## Adjust the path to import the module under test
SRC_PATH = Path(__file__).resolve().parents[2]
MAIN_PATH = SRC_PATH / "main"
sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(MAIN_PATH))
from main.service.assistant import ask

@patch("main.service.assistant.initialize_agent") 
def test_ask(mock_initialize_agent): 
    """ 
    ask() should initialize the agent, invoke it with the user's question and session_id, and return the content of the third message. 
    """ 
    # -------------------------------------------------------- 
    # # Create mock agent # 
    # -------------------------------------------------------- 
    mock_agent = MagicMock() 

    # Configure initialize_agent() to return our mock agent 
    mock_initialize_agent.return_value = mock_agent 

    # -------------------------------------------------------- 
    # # Mock agent response # 
    # -------------------------------------------------------- 
    expected_answer = "The vacation policy allows employees to take 20 days." 
    mock_response = { "messages": [ MagicMock(), MagicMock(), MagicMock(content=expected_answer), ] } 
    mock_agent.invoke.return_value = mock_response 

    # -------------------------------------------------------- 
    # # Execute # 
    # -------------------------------------------------------- 
    result = ask( session_id="test-session-123", question="What is the vacation policy?" ) 

    # -------------------------------------------------------- 
    # # Verify initialize_agent() was called # 
    # -------------------------------------------------------- 
    mock_initialize_agent.assert_called_once() 

    # -------------------------------------------------------- 
    # # Verify agent.invoke() was called correctly # 
    # -------------------------------------------------------- 
    mock_agent.invoke.assert_called_once_with( { "messages": [ { "role": "user", "content": "What is the vacation policy?" } ] }, config={ "configurable": { "session_id": "test-session-123" } } ) 

    # -------------------------------------------------------- 
    # # Verify returned answer # 
    # -------------------------------------------------------- 
    assert result == expected_answer