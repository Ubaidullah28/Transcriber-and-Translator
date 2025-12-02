"""
Translation Utility Module
Provides helper functions for text translation using googletrans.
Handles initialization errors safely and exposes a simple API.
"""

from typing import Optional

_translator = None
_init_error: Optional[Exception] = None


def _get_translator():
    """
    Safely initializes and returns a Translator instance.
    If initialization fails, it stores the exception for later use.
    """
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
    """
    Translates text from source_lang to target_lang.
    Returns an empty string for invalid input.
    """
    if not text or not text.strip():
        return ""

    translator = _get_translator()
    if translator is None:
        return "[Translation service unavailable in this environment]"

    result = translator.translate(text, dest=target_lang, src=source_lang)
    return result.text


def is_translation_available() -> bool:
    """
    Returns True if translator is successfully initialized, else False.
    This helper is useful for checking service availability before calling translate.
    """
    return _get_translator() is not None
