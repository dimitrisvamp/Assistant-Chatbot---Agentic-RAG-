from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_ollama import OllamaEmbeddings
import os 

def get_retriever() -> BaseRetriever:
    chunks = split_pdf_to_chunks()
    vector_store = get_vector_store(chunks=chunks)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold", search_kwargs={"score_threshold":0.5, "k":4})
    return retriever

def get_vector_store(chunks: list[Document]) -> FAISS:
    """Add the chunks to the vector store and returns it, 
      if the vector store already exists, it will load it from the local path.
    Args:
        chunks (list[Document]): chunks from the loaded document
    """
    INDEX_PATH = "Internal_Processes_index"
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    if os.path.exists(INDEX_PATH):
        vector_store = FAISS.load_local(INDEX_PATH, embeddings=embedding, allow_dangerous_deserialization=True)
    else:
        vector_store = FAISS.from_documents(documents=chunks, embedding=embedding)
        vector_store.save_local(INDEX_PATH)
    return vector_store

def split_pdf_to_chunks() -> list[Document]:
    """
    Split pdf into chunks
    """
    document = pdf_load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_documents(document)
    return chunks

def pdf_load() -> list[Document]:
    """PDF Loader
    """
    pdf_path = os.path.join("main/resources/documents/Internal_Processes.pdf")
    document = PyPDFLoader(pdf_path).load()
    return document



