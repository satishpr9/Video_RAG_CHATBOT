from fastapi import APIRouter

from app.schemas.ingest_schema import IngestRequest


from app.services.video_processor import process_video


from app.rag.store import create_vectorstore,add_chunks
from app.rag.state import VIDEOS,VECTORSTORE
import app.rag.state as state


router = APIRouter()

@router.post("/ingest")
def ingest(payload: IngestRequest):

    video_a = process_video(
        payload.youtube_url,
        "A"
    )

    video_b = process_video(
        payload.instagram_url,
        "B"
    )

    db = create_vectorstore()

    add_chunks(
        db,
        video_a["chunks"],
        "A"
    )

    add_chunks(
        db,
        video_b["chunks"],
        "B"
    )

    VIDEOS["A"] = video_a
    VIDEOS["B"] = video_b
    state.VECTORSTORE = db
    return {
        "status":"success",
        "video_a_chunks":
            len(video_a["chunks"]),
        "video_b_chunks":
            len(video_b["chunks"])
    }