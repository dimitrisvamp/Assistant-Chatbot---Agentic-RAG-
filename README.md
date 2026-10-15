# AI Agentic RAG Chatbot

An AI-powered internal support assistant that answers questions about company processes and can help submit vacation requests. The application combines Retrieval-Augmented Generation (RAG) with an AI agent that selects the appropriate tool for each user request.

## Features

- **Document-based Q&A:** Retrieves relevant passages from internal process documentation in PDF format.
- **Retrieval-Augmented Generation (RAG):** Uses retrieved document context to ground answers in company documentation.
- **Agentic tool selection:** Routes policy and process questions to the knowledge-retrieval tool and vacation requests to the vacation-management tool.
- **Vector search:** Uses FAISS for similarity-based retrieval.
- **Local language models:** Uses Ollama to run the `llama3.2` chat model and `nomic-embed-text` embeddings locally.
- **Conversation history:** Stores messages in a SQLite database, separated by session ID.
- **REST API:** Exposes the chatbot through FastAPI.

## Architecture

```text
Client
  |
  v
FastAPI endpoint
  |
  v
Agent (LangChain / LangGraph)
  |
  +-------------------------------+
  |                               |
  v                               v
Knowledge retrieval tool     Vacation request tool
  |                               |
  v                               v
RAG chain                    Vacation manager
  |
  v
FAISS vector store
  |
  v
Retrieved PDF chunks
  |
  v
Ollama LLM generates an answer
```

## Technology stack

- Python
- FastAPI and Uvicorn
- LangChain / LangGraph
- Ollama
- Llama 3.2
- `nomic-embed-text`
- FAISS
- PyPDF
- SQLite for chat history

> Package APIs can vary between LangChain versions. Install the dependencies listed in `requirements.txt` and keep the versions compatible with the imports used by the project.

## Prerequisites

Before starting, install:

1. **Python 3.10 or a compatible Python version** supported by the packages in `requirements.txt`.
2. **Git**, if you plan to clone the repository.
3. **Ollama**, available at https://ollama.com/download.

Download the models used by the application:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Ensure Ollama is running before starting the application. Depending on your operating system, Ollama may run as a background application; otherwise, start it with:

```bash
ollama serve
```

If Ollama is already running, you do not need to start a second server.

## Installation

### 1. Clone the repository

Replace `<repository-url>` with the URL of your GitHub repository.

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv chatbot
.\chatbot\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can activate the environment from Command Prompt instead:

```bat
chatbot\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv chatbot
source chatbot/bin/activate
```

### 3. Install the requirements

If `requirements.txt` is in the repository root, run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you have not created `requirements.txt` yet, generate it from the project's activated environment:

```bash
python -m pip freeze > requirements.txt
```

Review the generated file before committing it so it contains the dependencies needed by the project rather than unrelated packages from your environment.

### 4. Add the internal documentation

Place the PDF that the RAG system should search at the path expected by the application:

```text
src/main/resources/documents/Your_Internal_Processes.pdf
```

The path is relative to the process's working directory in the current implementation. Start the application from the expected directory, or update the loader to construct an absolute path based on `__file__` so it works regardless of the current working directory.

**Important:** Do not commit confidential company documents to a public repository. Use a permitted, anonymized sample document or keep the internal PDF out of Git.

### 5. Check configuration and local data directories

Make sure the directories required by your implementation exist, including the locations for:

- Internal PDF documents
- The FAISS index (`Internal_Processes_index`, in the current implementation)
- SQLite chat history (`resources/chat_history/chat_history.db`, in the current implementation)

The application may create the vector index and SQLite database when it runs, depending on your code. Verify the paths and permissions before launching it.

## Run the application

Run the following commands from the directory that contains the `main` package/module expected by your imports. In the development layout discussed for this project, that is typically `src/main`.

```bash
cd src/main
python -m uvicorn main:app --reload
```

If your FastAPI instance is defined in `app.py` rather than `main.py`, use:

```bash
python -m uvicorn app:app --reload
```

Use the command matching the file that defines your FastAPI object, for example:

```python
app = FastAPI()
```

The `--reload` option is intended for development and automatically restarts the server when source files change. For deployment, run without `--reload` and configure the server appropriately.

When the server starts, Uvicorn prints the local address. If using its default settings, open:

- API: http://127.0.0.1:8000
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API usage

The exact endpoint and request schema depend on the router implementation. If the chatbot endpoint is registered under `/user/chatbot`, for example, a request might look like:

```bash
curl -X POST "http://127.0.0.1:8000/user/chatbot" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"demo-session\",\"question\":\"What is the vacation policy?\"}"
```

Adjust the URL and JSON fields to match your Pydantic request model and FastAPI route. You can inspect the actual endpoint and required fields in `/docs`.

Example questions:

- `What is the vacation policy?`
- `What should I do when I am sick?`
- `What are the working hours?`
- `How do I request vacation?`

A stable `session_id` should be reused for messages belonging to the same conversation. Use a different session ID for a separate conversation.

## How the RAG pipeline works

1. Load the internal PDF using the PDF loader.
2. Split the document into chunks using `RecursiveCharacterTextSplitter`.
3. Create embeddings with Ollama's `nomic-embed-text`.
4. Build or load the FAISS vector index.
5. Retrieve relevant chunks for the user's question using similarity search.
6. Pass the retrieved context and question to the `llama3.2` model.
7. Return the generated answer to the calling tool or agent.

The current retriever configuration uses similarity-score threshold retrieval, with a configured threshold of `0.5` and `k=4`. Retrieval quality depends on the document, chunking strategy, embedding model, and threshold; these values should be evaluated against representative questions rather than assumed to be optimal.

## How the agent works

The agent has access to two main tools:

- **`retrieve_knowledge_tool`** — answers questions about internal policies, procedures, working hours, sickness, business trips, payments, and other documented processes.
- **`save_vacation_request_tool`** — handles requests to submit vacation dates through the vacation-management logic.

The agent uses the tool descriptions and system instructions to choose the appropriate action. The vacation-management function should validate a request before reporting that it was saved. In production, return the actual outcome from that function rather than assuming every request succeeds.

## Testing

Run the automated tests with `pytest` from the repository root:

```bash
python -m pip install pytest
python -m pytest -v
```

Suggested test coverage:

- **Retriever tests:** PDF loading, chunk creation, vector-store loading/building, and retrieval of relevant documents.
- **RAG tests:** answers are grounded in retrieved context, expected facts are present, and unanswerable questions are handled appropriately.
- **Vacation-manager tests:** employee lookup, date validation, availability rules, and successful or rejected requests.
- **API tests:** endpoint status codes, request validation, response structure, and error handling.
- **Agent tests:** correct tool selection and correct use of tool results.

RAG answers may vary in wording, so tests should normally check required facts and behavior instead of requiring an exact full response string. Ragas or LangSmith can be added for systematic evaluation of retrieval and answer quality.

## Troubleshooting

### Ollama connection errors

- Confirm Ollama is installed and running.
- Confirm the required models are available:

  ```bash
  ollama list
  ```

- Pull any missing model with `ollama pull <model-name>`.

### PDF not found

- ***Notice*** -> The internal process document has been removed. Please use your example processes document.
- Confirm the PDF exists at the path used by the loader.
- Run Uvicorn from the expected working directory, or change the loader to use a path derived from the source file location.

### FAISS index issues

- Confirm the index directory is correct and writable.
- Rebuild the index if the source document or embedding model changes.
- Only load locally persisted FAISS indexes from trusted sources. The current implementation uses `allow_dangerous_deserialization=True`, which should only be used with trusted index files.

### Import errors

- Activate the intended virtual environment.
- Install packages from `requirements.txt` in that environment.
- Run Uvicorn from the correct directory and use a module path that matches the location of the FastAPI `app` object.
- Keep imports consistent with the project's package structure.

## Security and privacy notes

- Do not commit API keys, passwords, private company PDFs, chat-history databases, or other confidential data.
- Add local artifacts and secrets to `.gitignore`.
- Use authentication and authorization before exposing internal-process or vacation-management endpoints beyond a trusted development environment.
- Validate user input and verify the employee's identity and authorization before creating or modifying vacation records.
- Review data retention requirements for stored conversation history.

## Future improvements

- Automated RAG evaluation with Ragas or LangSmith.
- Improved document metadata and retrieval filtering.
- Structured tool outputs and explicit vacation-request success/failure results.
- Authentication, authorization, and audit logging.
- Containerized deployment and CI testing.

## License

Add a license appropriate for your project before publishing it. If this project contains employer-owned code or documentation, confirm that you are permitted to publish it first.
