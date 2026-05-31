import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path: str):

    result = model.transcribe(
        file_path,
        fp16=False
    )

    return result["text"]