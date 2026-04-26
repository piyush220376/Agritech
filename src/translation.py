"""
translation.py  –  Translate text to/from English using googletrans.

Known issue with googletrans==4.0.0-rc1 (the pip version):
  The Translator object is NOT thread-safe and can fail with httpx errors
  when called from multiple Qt threads. We create a fresh instance per call
  to avoid these issues.
"""

from googletrans import Translator

LANG_MAP = {
    "Hindi":   "hi",
    "Gujarati": "gu",
    "Telugu":  "te",
}


def _translate(text, dest):
    """Create a fresh Translator per call (thread-safe workaround)."""
    try:
        t = Translator()
        result = t.translate(text, dest=dest)
        return result.text if result and result.text else text
    except Exception:
        return text  # fail silently – return original text


def translate_to_english(text, lang):
    if lang == "English" or not text:
        return text
    return _translate(text, dest="en")


def translate_from_english(text, lang):
    if lang == "English" or not text:
        return text
    dest = LANG_MAP.get(lang, "en")
    if dest == "en":
        return text
    return _translate(text, dest=dest)
