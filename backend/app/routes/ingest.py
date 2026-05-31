from fastapi import APIRouter

from app.schemas.ingest_schema import IngestRequest

from app.services.video_processor import process_video

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

    return {
        "status": "success",
        "video_a_chunks": len(video_a["chunks"]),
        "video_b_chunks": len(video_b["chunks"])
    }