import os
from app.services.transcriber import transcribe_audio

files = os.listdir("downloads")

print("Files:", files)

file_path = os.path.join(
    "downloads",
    files[0]
)

print("Testing:", file_path)

text = transcribe_audio(file_path)

print("\nLength:", len(text))
print("\nPreview:")
print(text[:500])