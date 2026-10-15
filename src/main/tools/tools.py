from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from service.vacation_manager import save_vacation_request
from service.rag_initializer import initialize_rag, initialize_chat_history

@tool
def retrieve_knowledge_tool(question: str, config: RunnableConfig) -> str:
    """
    Retrieve answers from company documentation.

    Use this tool whenever the user requests information about:
    - vacation policy
    - sickness policy
    - company procedures
    - working hours
    - office attendance
    - payments
    - business trips

    The returned response is the final answer.
    Do not modify it.

    Args:
        session_id: The user's session identifier.
        question: The user's complete question.
    """
    print(config)
    rag = initialize_rag()
    session_id = config["configurable"]["session_id"]
    chat_history = initialize_chat_history(session_id= session_id)
    llm_answer = rag.invoke({"input": question, "chat_history": chat_history.messages})
    assistant_answer = llm_answer["answer"]

    # Save the question and answer in the chat history of the user
    chat_history.add_user_message(question)
    chat_history.add_ai_message(assistant_answer)

    return assistant_answer 

@tool
def save_vacation_request_tool(month: str, employee_name: str, start_date: int, end_date: int) -> str:
    """
    Submits a vacation request for an employee.

    Example:
    User: "Add vacation for Dimitris Vampiris from 28 November to 30 November"

    Extract:
    employee_name = "Dimitris Vampiris"
    month = "November"
    start_date = 28
    end_date = 30

    Args:
        month: Month of the vacation.
        employee_name: Full name of the employee.
        start_date: First vacation day.
        end_date: Last vacation day.
    """
    print(month, employee_name, start_date, end_date)
    request_result = save_vacation_request(month, employee_name, start_date, end_date)
    return request_result

