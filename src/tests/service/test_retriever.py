import pytest
from main.service.retriever import pdf_load, split_pdf_to_chunks, get_vector_store, get_retriever

def test_pdf_load():
    documents = pdf_load()

    assert documents
    assert all(document.page_content.strip() for document in documents)


def test_split_pdf_to_chunks():
    chunks = split_pdf_to_chunks()

    assert chunks
    assert all(chunk.page_content.strip() for chunk in chunks)


def test_vector_store():
    chunks = split_pdf_to_chunks()
    vector_store = get_vector_store(chunks)

    results = vector_store.similarity_search(
        "What is the vacation policy?",
        k=4
    )

    assert results


def test_retriever_returns_vacation_information():
    retriever = get_retriever()

    documents = retriever.invoke(
        "What is the vacation policy?"
    )

    assert documents

    combined_text = " ".join(
        document.page_content.lower()
        for document in documents
    )

    assert "vacation" in combined_text