import pytest
import sys 
from pathlib import Path 
from unittest.mock import MagicMock, patch
## Adjust the path to import the module under test
SRC_PATH = Path(__file__).resolve().parents[2]
MAIN_PATH = SRC_PATH / "main"
sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(MAIN_PATH))
from main.tools.tools import retrieve_knowledge_tool, save_vacation_request_tool

# ============================================================ 
# # retrieve_knowledge_tool() # 
# ============================================================

@patch("main.tools.tools.initialize_chat_history") 
@patch("main.tools.tools.initialize_rag") 
def test_retrieve_knowledge_tool( mock_initialize_rag, mock_initialize_chat_history, ): 
    """ 
    retrieve_knowledge_tool() should: 
    1. Initialize the RAG. 
    2. Get the session_id from config. 
    3. Initialize chat history. 
    4. Invoke the RAG with the question and chat history. 
    5. Save the user question to chat history. 
    6. Save the assistant answer to chat history. 
    7. Return the RAG answer. 
    """ 
    # -------------------------------------------------------- 
    # # Mock RAG # 
    # -------------------------------------------------------- 
    mock_rag = MagicMock() 
    mock_initialize_rag.return_value = mock_rag 

    # -------------------------------------------------------- 
    # # Mock chat history # 
    # --------------------------------------------------------
    mock_chat_history = MagicMock() 
    mock_chat_history.messages = [ MagicMock(), MagicMock(), ] 
    mock_initialize_chat_history.return_value = mock_chat_history 

    # -------------------------------------------------------- 
    # # Mock RAG response # 
    # -------------------------------------------------------- 
    expected_answer = ( 
        "According to the company policy, " 
        "employees must notify their manager when sick." )
    mock_rag.invoke.return_value = { "answer": expected_answer }

    # -------------------------------------------------------- 
    # # Test input # 
    # -------------------------------------------------------- 
    question = "What should I do when I am sick?" 
    config = { "configurable": { "session_id": "test-session-123" } }

    # -------------------------------------------------------- 
    # # Execute # 
    # -------------------------------------------------------- 
    result = retrieve_knowledge_tool.func(
        question=question,
        config=config
    )


    # -------------------------------------------------------- 
    # # Verify initialize_rag() #
    # -------------------------------------------------------- 
    mock_initialize_rag.assert_called_once() 

    # -------------------------------------------------------- 
    # # Verify chat history initialization # 
    # -------------------------------------------------------- 
    mock_initialize_chat_history.assert_called_once_with( session_id="test-session-123" ) 

    # -------------------------------------------------------- 
    # # Verify RAG invocation #
    # -------------------------------------------------------- 
    mock_rag.invoke.assert_called_once_with( { "input": question, "chat_history": mock_chat_history.messages, } ) 

    # -------------------------------------------------------- 
    # # Verify chat history updates # 
    # -------------------------------------------------------- 
    mock_chat_history.add_user_message.assert_called_once_with( question ) 
    mock_chat_history.add_ai_message.assert_called_once_with( expected_answer ) 

    # -------------------------------------------------------- 
    # # Verify returned answer # 
    # -------------------------------------------------------- 
    assert result == expected_answer 

# ============================================================ 
# save_vacation_request_tool() # 
# ============================================================ 
@patch("main.tools.tools.save_vacation_request") 
def test_save_vacation_request_tool(mock_save_vacation_request): 
    """ 
    save_vacation_request_tool() should pass all extracted vacation information to save_vacation_request() and return its result. 
    """ 
    # -------------------------------------------------------- 
    # Mock function result # 
    # -------------------------------------------------------- 
    expected_result = ( "Dimitris Vampiris, " "I have saved successfully your vacation request." ) 
    mock_save_vacation_request.return_value = expected_result 

    # -------------------------------------------------------- 
    # Test input # 
    # -------------------------------------------------------- 
    month = "November" 
    employee_name = "Dimitris Vampiris" 
    start_date = 28 
    end_date = 30 

    # -------------------------------------------------------- 
    # Execute # 
    # -------------------------------------------------------- 
    result = save_vacation_request_tool.invoke( { "month": month, "employee_name": employee_name, "start_date": start_date, "end_date": end_date, } ) 

    # -------------------------------------------------------- 
    # Verify underlying function # 
    # -------------------------------------------------------- 
    mock_save_vacation_request.assert_called_once_with( month, employee_name, start_date, end_date, ) 

    # -------------------------------------------------------- 
    # Verify returned result # 
    # -------------------------------------------------------- 
    assert result == expected_result 