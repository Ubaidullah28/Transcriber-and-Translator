# speech/services/transcription.py
import os
import tempfile
import whisper

_model = None  # lazy-loaded singleton model

def _get_model():
    global _model
    if _model is None:
        # "base" is a good trade-off between speed and accuracy
        _model = whisper.load_model("base")
    return _model

def transcribe_audio_file(django_file) -> str:
    """
    Takes a Django UploadedFile, saves to a temp file,
    runs Whisper transcription, and returns plain text.
    """
    model = _get_model()

    # save uploaded chunks into a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        for chunk in django_file.chunks():
            tmp.write(chunk)
        temp_path = tmp.name

    try:
        result = model.transcribe(temp_path)
        return result.get("text", "").strip()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
