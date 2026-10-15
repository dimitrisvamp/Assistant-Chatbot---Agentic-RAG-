from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from service.retriever import get_retriever
from resources.prompts.system.rag_prompt import RAG_PROMPT

rag_chain = None

def initialize_rag() -> Runnable:
    """It initializes once the rag while application running

    Returns:
        Runnable: _description_
    """
    global rag_chain
    if rag_chain is None:
        rag_chain = initialize_chain()
    return rag_chain

def initialize_chain() -> Runnable: 
    """Retrieval & Conversation chains initialization 
  
    Returns:
        Runnable: Returns Runnable retrieval chain
    """
    prompt = initialize_rag_prompt()
    llm = initialize_rag_llm()
    document_chain = create_stuff_documents_chain(prompt= prompt, llm= llm)
    retriever = get_retriever()
    retrieval_chain = create_retrieval_chain(retriever= retriever, combine_docs_chain= document_chain)
    return retrieval_chain

def initialize_rag_prompt() -> ChatPromptTemplate:
    """RAG prompt initialization

    Returns:
        ChatPromptTemplate: Returns the prompt of the system including chat history
    """
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", RAG_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    return prompt

def initialize_rag_llm() -> ChatOllama:
    """LLM initialization

    Returns:
        ChatOllama: Returns the llm model that will be used in chatbot 
    """
    llm = ChatOllama(
       model= "llama3.2",
        temperature= 0.5
    )
    return llm

def initialize_chat_history(session_id: str) -> SQLChatMessageHistory:
    """Chat history initialization

    Returns:
        SQLChatMessageHistory: Returns the chat history of the user
    """
    chat_history = SQLChatMessageHistory(
        session_id= session_id,
        connection= "sqlite:///main/resources/chat_history/chat_history.db"
    )
    return chat_history