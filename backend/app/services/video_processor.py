from app.services.downloader import download_video
from app.services.transcriber import transcribe_audio
from app.utils.chunker import chunk_text
import os


def process_video(url, video_id):

    video = download_video(url)

    print("\n===== VIDEO INFO =====")
    print("Video ID:", video_id)
    print("File Path:", video["file_path"])

    # check file existence and size before transcribing
    file_path = video.get("file_path")
    if not file_path or not os.path.exists(file_path):
        print("Error: downloaded file not found:", file_path)
        return {
            "video_id": video_id,
            "metadata": video.get("metadata"),
            "transcript": "",
            "chunks": []
        }

    size = os.path.getsize(file_path)
    print("Downloaded file size:", size)
    if size == 0:
        print("Error: downloaded file is empty:", file_path)
        return {
            "video_id": video_id,
            "metadata": video.get("metadata"),
            "transcript": "",
            "chunks": []
        }

    transcript = transcribe_audio(file_path)

    print("\n===== TRANSCRIPT =====")
    print("Transcript Length:", len(transcript))

    if len(transcript) > 0:
        print(transcript[:500])

    chunks = chunk_text(transcript)

    print("\n===== CHUNKS =====")
    print("Chunk Count:", len(chunks))

    return {
        "video_id": video_id,
        "metadata": video["metadata"],
        "transcript": transcript,
        "chunks": chunks
    }