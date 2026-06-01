import whisper
import threading
import traceback

_model = None
_model_lock = threading.Lock()

def get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = whisper.load_model("base", device="cpu")
    return _model


def transcribe_audio(file_path):
    global _model
    print("Transcribing:", file_path)
    model = get_model()
    try:
        result = model.transcribe(file_path, fp16=False, language=None)
    except KeyError as e:
        print("KeyError during transcription, will reload model and retry:", e)
        traceback.print_exc()
        # Attempt to reload the model and retry once
        with _model_lock:
            try:
                _model = whisper.load_model("base", device="cpu")
            except Exception as reload_err:
                print("Failed to reload whisper model:", reload_err)
                raise
            model = _model
        result = model.transcribe(file_path, fp16=False)
    
    return {
        "text": result["text"],
        "segments": result["segments"]
    }
    
    