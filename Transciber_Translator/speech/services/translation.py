from typing import Optional

_translator = None
_init_error: Optional[Exception] = None


def _get_translator():
   
    global _translator, _init_error

   
    if _translator is not None or _init_error is not None:
        return _translator

    try:
        from googletrans import Translator  
        _translator = Translator()
    except Exception as exc:
        
        _init_error = exc
        _translator = None

    return _translator


def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
   
    if not text or not text.strip():
        return ""

    translator = _get_translator()
    if translator is None:
        return "[Translation service unavailable in this environment]"

    result = translator.translate(text, dest=target_lang, src=source_lang)
    return result.text
