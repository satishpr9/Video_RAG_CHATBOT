from app.services.downloader import download_video
from app.services.transcriber import transcribe_audio

url = input("Enter YouTube URL: ")

video = download_video(url)

print("Downloaded:", video["file_path"])

text = transcribe_audio(video["file_path"])

print("\nTRANSCRIPT:\n")
print(text)