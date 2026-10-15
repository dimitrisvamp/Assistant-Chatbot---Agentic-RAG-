from service.agent_initializer import initialize_agent

def ask(session_id: str, question: str):
    agent = initialize_agent()
    response = agent.invoke(
        {
            "messages": [{"role": "user", "content": question}]}, config={
                "configurable": {
                    "session_id": session_id
                }
    })
    return response["messages"][2].content


