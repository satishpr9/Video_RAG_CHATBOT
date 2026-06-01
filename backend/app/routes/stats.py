from fastapi import APIRouter
import app.rag.state as state

router = APIRouter()

@router.get("/stats")
def stats():

    return state.VIDEO_STATS