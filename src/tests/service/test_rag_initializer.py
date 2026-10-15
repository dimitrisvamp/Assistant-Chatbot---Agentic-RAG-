import pytest
import sys 
from pathlib import Path 
from unittest.mock import MagicMock, patch 
from langchain_core.prompts import ChatPromptTemplate
## Adjust the path to import the module under test
SRC_PATH = Path(__file__).resolve().parents[2]
MAIN_PATH = SRC_PATH / "main"
sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(MAIN_PATH))
from main.service.rag_initializer import initialize_rag, initialize_chain, initialize_rag_prompt, initialize_rag_llm, initialize_chat_history
import main.service.rag_initializer as rag_initializer

# ============================================================ 
# # initialize_rag() # 
# ============================================================

@patch("main.service.rag_initializer.initialize_chain") 
def test_initialize_rag_initializes_chain(mock_initialize_chain): 
    """ 
    The first call to initialize_rag() should initialize the RAG chain by calling initialize_chain().
    """ 
    # Reset global state before the test 
    rag_chain = None 

    # Fake RAG chain 
    mock_chain = MagicMock() 
    mock_initialize_chain.return_value = mock_chain 

    result = initialize_rag() 

    # The returned object should be the initialized chain 
    assert result == mock_chain 

    # initialize_chain() should have been called exactly once 
    mock_initialize_chain.assert_called_once()

@patch("main.service.rag_initializer.initialize_chain") 
def test_initialize_rag_reuses_existing_chain(mock_initialize_chain): 
    """ 
    If the RAG chain has already been initialized, initialize_rag() should not initialize it again. 
    """ 
    # Simulate an already initialized chain 
    existing_chain = MagicMock() 
    rag_initializer.rag_chain = existing_chain 

    result = initialize_rag() 
    # Should return the existing chain 
    assert result == existing_chain 

    # initialize_chain() must NOT be called again 
    mock_initialize_chain.assert_not_called() 

    # Clean global state after test 
    rag_chain = None

# ============================================================ 
# # initialize_chain() # 
# ============================================================

@patch("main.service.rag_initializer.create_retrieval_chain") 
@patch("main.service.rag_initializer.get_retriever") 
@patch("main.service.rag_initializer.create_stuff_documents_chain") 
@patch("main.service.rag_initializer.initialize_rag_llm") 
@patch("main.service.rag_initializer.initialize_rag_prompt") 
def test_initialize_chain( mock_initialize_rag_prompt, mock_initialize_rag_llm, mock_create_stuff_documents_chain, mock_get_retriever, mock_create_retrieval_chain, ): 
    """ 
    initialize_chain() should correctly connect: prompt ↓ LLM ↓ document chain ↓ retriever ↓ retrieval chain 
    """ 
    # Create fake objects 
    mock_prompt = MagicMock() 
    mock_llm = MagicMock() 
    mock_document_chain = MagicMock() 
    mock_retriever = MagicMock() 
    mock_retrieval_chain = MagicMock() 

    # Configure mocks 
    mock_initialize_rag_prompt.return_value = mock_prompt 
    mock_initialize_rag_llm.return_value = mock_llm 
    mock_create_stuff_documents_chain.return_value = mock_document_chain 
    mock_get_retriever.return_value = mock_retriever 
    mock_create_retrieval_chain.return_value = mock_retrieval_chain 

    # Execute 
    result = initialize_chain() 

    # -------------------------------------------------------- 
    # Verify prompt initialization 
    # -------------------------------------------------------- 
    mock_initialize_rag_prompt.assert_called_once() 

    # -------------------------------------------------------- 
    # Verify LLM initialization 
    # -------------------------------------------------------- 
    mock_initialize_rag_llm.assert_called_once() 

    # -------------------------------------------------------- 
    # Verify document chain 
    # -------------------------------------------------------- 
    mock_create_stuff_documents_chain.assert_called_once_with( prompt=mock_prompt, llm=mock_llm, ) 

    # -------------------------------------------------------- 
    # Verify retriever 
    # -------------------------------------------------------- 
    mock_get_retriever.assert_called_once() 

    # -------------------------------------------------------- 
    # Verify retrieval chain 
    # -------------------------------------------------------- 
    mock_create_retrieval_chain.assert_called_once_with( retriever=mock_retriever, combine_docs_chain=mock_document_chain, ) 

    # -------------------------------------------------------- 
    # Verify returned value 
    # -------------------------------------------------------- 
    assert result == mock_retrieval_chain

# ============================================================ 
# # initialize_rag_prompt() # 
# ============================================================ 
def test_initialize_rag_prompt_returns_chat_prompt_template(): 
    """ 
    initialize_rag_prompt() should return a ChatPromptTemplate. 
    """ 
    prompt = initialize_rag_prompt() 
    assert isinstance(prompt, ChatPromptTemplate)

def test_initialize_rag_prompt_contains_input_variable(): 
    """ 
    The prompt should contain the {input} variable. 
    """ 
    prompt = initialize_rag_prompt() 
    assert "input" in prompt.input_variables

def test_initialize_rag_prompt_contains_chat_history(): 
    """ 
    The prompt should contain the chat_history placeholder. 
    """ 
    prompt = initialize_rag_prompt() 
    # MessagesPlaceholder variables are included in input_variables 
    assert "chat_history" in prompt.input_variables

# ============================================================ 
# # initialize_rag_llm() # 
# ============================================================ 
@patch("main.service.rag_initializer.ChatOllama") 
def test_initialize_rag_llm(mock_chat_ollama): 
    """ 
    initialize_rag_llm() should create ChatOllama with the expected configuration. 
    """ 
    mock_llm = MagicMock() 
    mock_chat_ollama.return_value = mock_llm 

    result = initialize_rag_llm() 
    # Verify ChatOllama configuration 
    mock_chat_ollama.assert_called_once_with( model="llama3.2", temperature=0.5, ) 

    # Verify returned LLM assert 
    assert result == mock_llm

# ============================================================ 
# # initialize_chat_history() # 
# ============================================================ 
@patch("main.service.rag_initializer.SQLChatMessageHistory") 
def test_initialize_chat_history(mock_sql_chat_history): 
    """ 
    initialize_chat_history() should create the chat history with the provided session 
    ID and correct SQLite database. 
    """ 
    mock_history = MagicMock() 
    mock_sql_chat_history.return_value = mock_history 

    result = initialize_chat_history("test-session-123") 

    # Verify constructor arguments 
    mock_sql_chat_history.assert_called_once_with( session_id="test-session-123", connection="sqlite:///main/resources/chat_history/chat_history.db", ) 

    # Verify returned history 
    assert result == mock_history