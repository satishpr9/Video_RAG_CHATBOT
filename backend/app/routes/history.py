from fastapi import APIRouter
import app.rag.state as state

router = APIRouter()


@router.get("/history")
def get_history():

    return state.CHAT_HISTORY