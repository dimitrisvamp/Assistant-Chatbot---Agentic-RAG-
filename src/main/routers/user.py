from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from service.assistant import ask


router = APIRouter(prefix="/chatbot", tags=["user"])

@router.get("/")
async def chatbot(session_id: str, question: str) -> PlainTextResponse:
    answer= ask(session_id=session_id, question= question)
    return PlainTextResponse(answer)


