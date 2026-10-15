import pytest
import sys 
from pathlib import Path 
from unittest.mock import MagicMock, patch
## Adjust the path to import the module under test
SRC_PATH = Path(__file__).resolve().parents[2]
MAIN_PATH = SRC_PATH / "main"
sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(MAIN_PATH))
from fastapi.testclient import TestClient 
from fastapi import FastAPI 
from main.routers.user import router

# Create a small FastAPI application for testing the router 
app = FastAPI() 
app.include_router(router) 
client = TestClient(app)

@patch("main.routers.user.ask") 
def test_chatbot(mock_ask): 
    """ 
    The chatbot endpoint should: 
    1. Receive session_id and question. 
    2. Call ask() with those parameters. 
    3. Return the answer as PlainTextResponse. 
    """ 
    # -------------------------------------------------------- 
    # # Mock ask() # 
    # -------------------------------------------------------- 
    expected_answer = "The vacation policy allows employees to take 20 days." 
    mock_ask.return_value = expected_answer 

    # -------------------------------------------------------- 
    # # Call endpoint # 
    # -------------------------------------------------------- 
    response = client.get( "/chatbot/", params={ "session_id": "test-session-123", "question": "What is the vacation policy?" } ) 

    # -------------------------------------------------------- 
    # # Verify HTTP response # 
    # -------------------------------------------------------- 
    assert response.status_code == 200 

    # Verify response body 
    assert response.text == expected_answer 

    # Verify response content type 
    assert response.headers["content-type"].startswith("text/plain") 

    # -------------------------------------------------------- 
    # # Verify ask() was called correctly # 
    # -------------------------------------------------------- 
    mock_ask.assert_called_once_with( session_id="test-session-123", question="What is the vacation policy?" )