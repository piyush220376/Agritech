import os
import requests
from translation import translate_to_english, translate_from_english
from classifier import is_agriculture_related

LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "farmer-chatbot")


def is_lm_studio_available():
    try:
        r = requests.get(f"{LM_STUDIO_BASE_URL}/models", timeout=3)
        return r.status_code == 200
    except requests.RequestException:
        return False


def get_lm_studio_response(query):
    data = {
        "model": LM_STUDIO_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert agriculture assistant."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    r = requests.post(f"{LM_STUDIO_BASE_URL}/chat/completions", json=data, timeout=30)
    r.raise_for_status()  # raises HTTPError on 4xx/5xx
    payload = r.json()
    return payload["choices"][0]["message"]["content"].strip()


def get_response(prompt, language="English"):
    english_query = translate_to_english(prompt, language)

    if not is_agriculture_related(english_query):
        return "I can only answer agriculture-related questions."

    if not is_lm_studio_available():
        return "AI server not available. Please start LM Studio."

    try:
        reply = get_lm_studio_response(english_query)
        return translate_from_english(reply, language)
    except requests.HTTPError as e:
        return f"Server returned an error: {e}"
    except (KeyError, IndexError, ValueError):
        return "Received an unexpected response from the AI server."
    except requests.RequestException as e:
        return f"Network error: {e}"
