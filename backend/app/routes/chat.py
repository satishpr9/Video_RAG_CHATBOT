from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest

from app.services.chat_service import ask_question

router = APIRouter()

@router.post("/chat")
def chat(payload: ChatRequest):

    return ask_question(
        payload.question
    )