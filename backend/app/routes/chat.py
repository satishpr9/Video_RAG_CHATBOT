from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest
from fastapi.responses import StreamingResponse
from app.services.chat_service import ask_stream
import json
router = APIRouter()

# @router.post("/chat")
# def chat(payload: ChatRequest):

#     return ask_question(
#         payload.question
#     )

@router.post("/chat/stream")
def chat_stream(payload: ChatRequest):

    def generate():

        for chunk in ask_stream(payload.question):

            yield f"data: {json.dumps({'text': chunk})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )