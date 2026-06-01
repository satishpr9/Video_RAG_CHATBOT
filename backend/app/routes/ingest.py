from fastapi import APIRouter

from app.schemas.ingest_schema import IngestRequest
from app.services.video_processor import process_video
from app.services.analytics import engagement_rate

from app.rag.store import (
    create_vectorstore,
    add_chunks
)

import app.rag.state as state

router = APIRouter()


@router.post("/ingest")
def ingest(payload: IngestRequest):

    print("\n===== PROCESSING VIDEO A =====")

    video_a = process_video(
        payload.youtube_url,
        "A"
    )

    print("\n===== PROCESSING VIDEO B =====")

    video_b = process_video(
        payload.instagram_url,
        "B"
    )

    # Create Vector Store
    db = create_vectorstore()

    print("\n===== VIDEO A =====")
    print("Transcript Length:", len(video_a["transcript"]))
    print("Chunks:", len(video_a["chunks"]))

    print("\n===== VIDEO B =====")
    print("Transcript Length:", len(video_b["transcript"]))
    print("Chunks:", len(video_b["chunks"]))

    # Add Video A chunks
    if len(video_a["chunks"]) > 0:

        add_chunks(
            db,
            video_a["chunks"],
            "A"
        )

    else:
        print("Video A has no chunks")

    # Add Video B chunks
    if len(video_b["chunks"]) > 0:

        add_chunks(
            db,
            video_b["chunks"],
            "B"
        )

    else:
        print("Video B has no chunks")

    # Save globally
    state.VIDEOS["A"] = video_a
    state.VIDEOS["B"] = video_b

    state.VECTORSTORE = db

    print("\nVECTORSTORE SAVED")

    # -----------------------------
    # Engagement Rate Calculation
    # -----------------------------

    rate_a = engagement_rate(
        video_a["metadata"].get(
            "like_count",
            0
        ),
        video_a["metadata"].get(
            "comment_count",
            0
        ),
        video_a["metadata"].get(
            "view_count",
            0
        )
    )

    rate_b = engagement_rate(
        video_b["metadata"].get(
            "like_count",
            0
        ),
        video_b["metadata"].get(
            "comment_count",
            0
        ),
        video_b["metadata"].get(
            "view_count",
            0
        )
    )

    # -----------------------------
    # Store Video A Stats
    # -----------------------------

    state.VIDEO_STATS["A"] = {

        "title":
            video_a["metadata"].get(
                "title"
            ),

        "creator":
            video_a["metadata"].get(
                "uploader"
            ),

        "likes":
            video_a["metadata"].get(
                "like_count",
                0
            ),

        "comments":
            video_a["metadata"].get(
                "comment_count",
                0
            ),

        "views":
            video_a["metadata"].get(
                "view_count",
                0
            ),

        "duration":
            video_a["metadata"].get(
                "duration"
            ),

        "upload_date":
            video_a["metadata"].get(
                "upload_date"
            ),
         "hook":
        video_a["hook"],

        "engagement_rate":
            rate_a
    }

    # -----------------------------
    # Store Video B Stats
    # -----------------------------

    state.VIDEO_STATS["B"] = {

        "title":
            video_b["metadata"].get(
                "title"
            ),

        "creator":
            video_b["metadata"].get(
                "uploader"
            ),

        "likes":
            video_b["metadata"].get(
                "like_count",
                0
            ),

        "comments":
            video_b["metadata"].get(
                "comment_count",
                0
            ),

        "views":
            video_b["metadata"].get(
                "view_count",
                0
            ),

        "duration":
            video_b["metadata"].get(
                "duration"
            ),

        "upload_date":
            video_b["metadata"].get(
                "upload_date"
            ),
          "hook":
             video_b["hook"],


        "engagement_rate":
            rate_b
    }

    print("\n===== VIDEO STATS =====")
    print(state.VIDEO_STATS)

    return {
        "status": "success",
        "video_a_chunks": len(video_a["chunks"]),
        "video_b_chunks": len(video_b["chunks"]),
        "video_a_title": video_a["metadata"].get("title"),
        "video_b_title": video_b["metadata"].get("title"),
        "video_a_engagement": rate_a,
        "video_b_engagement": rate_b
    }