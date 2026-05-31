# import os
# from app.services.transcriber import transcribe_audio

# files = os.listdir("downloads")

# print("Files:", files)

# file_path = os.path.join(
#     "downloads",
#     files[0]
# )

# print("Testing:", file_path)

# text = transcribe_audio(file_path)

# print("\nLength:", len(text))
# print("\nPreview:")
# print(text[:500])

from app.services.transcriber import transcribe_audio

file_path = r"E:\Video-rag-chatbot\backend\downloads\DY9o3tBgQJ_.m4a"

text = transcribe_audio(file_path)

print("Length:", len(text))
print("Preview:")
print(text[:500])