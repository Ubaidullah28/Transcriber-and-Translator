# # speech/services/translation.py
# from googletrans import Translator

# _translator = Translator()

# def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
#     """
#     Uses Google Translation API (via googletrans) to translate text.
#     """
#     if not text.strip():
#         return ""
#     result = _translator.translate(text, dest=target_lang, src=source_lang)
#     return result.text










# # cgi.py - minimal shim for libraries expecting the old stdlib cgi module
# # This is enough for httpx / googletrans which only need parse_header.

# def parse_header(line):
#     """
#     Very small reimplementation of cgi.parse_header.
#     Returns (value, params_dict).
#     Example:
#         'text/html; charset=utf-8'
#         -> ('text/html', {'charset': 'utf-8'})
#     """
#     if not line:
#         return '', {}

#     parts = [p.strip() for p in line.split(';')]
#     value = parts[0]
#     params = {}

#     for item in parts[1:]:
#         if '=' in item:
#             k, v = item.split('=', 1)
#             k = k.strip()
#             v = v.strip().strip('"')
#             params[k] = v

#     return value, params













# speech/services/translation.py

from typing import Optional

_translator = None
_init_error: Optional[Exception] = None


def _get_translator():
    """
    Lazy-load the googletrans Translator so import errors or network
    issues don’t break Django management commands.
    """
    global _translator, _init_error

    # if we've already tried to init, just return what we have
    if _translator is not None or _init_error is not None:
        return _translator

    try:
        from googletrans import Translator  # type: ignore
        _translator = Translator()
    except Exception as exc:
        # store the error so we don't keep trying on every call
        _init_error = exc
        _translator = None

    return _translator


def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """
    Translate `text` from `source_lang` to `target_lang` using googletrans.

    If the translator can't be initialised (e.g. googletrans/httpx issues),
    returns a simple fallback message instead of crashing.
    """
    if not text or not text.strip():
        return ""

    translator = _get_translator()
    if translator is None:
        return "[Translation service unavailable in this environment]"

    result = translator.translate(text, dest=target_lang, src=source_lang)
    return result.text
