import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):

    print("Transcribing:", file_path)

    result = model.transcribe(
        file_path,
        fp16=False
    )

    text = result["text"]

    print("Transcript preview:")
    print(text[:300])

    return text