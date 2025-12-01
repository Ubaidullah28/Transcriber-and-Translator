# speech/services/transcription.py
import os
import tempfile
import whisper

_model = None 

def _get_model():
    global _model
    if _model is None:
        
        _model = whisper.load_model("base")
    return _model

def transcribe_audio_file(django_file) -> str:
    
    model = _get_model()

   
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
