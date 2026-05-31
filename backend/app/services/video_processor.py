from app.services.downloader import download_video
from app.services.transcriber import transcribe_audio

from app.utils.chunker import chunk_text
def process_video(url, video_id):

    video = download_video(url)

    transcript = transcribe_audio(
        video["file_path"]
    )

    chunks = chunk_text(
        transcript
    )

    return {
        "video_id": video_id,
        "transcript": transcript,
        "metadata": video["metadata"],
        "chunks": chunks
    }