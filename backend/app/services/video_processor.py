from app.services.downloader import download_video
from app.services.transcriber import transcribe_audio
from app.utils.chunker import chunk_text


def process_video(url, video_id):

    video = download_video(url)

    print("\n===== VIDEO INFO =====")
    print("Video ID:", video_id)
    print("File Path:", video["file_path"])

    transcript = transcribe_audio(
        video["file_path"]
    )

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