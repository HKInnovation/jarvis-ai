from groq import Groq
from config import GROQ_KEY

client = Groq(api_key=GROQ_KEY)

LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "ml": "Malayalam",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ja": "Japanese",
    "zh": "Chinese"
}

def chat_with_jarvis(user_text, history=None, language="en"):
    messages = history or []
    messages.append({"role": "user", "content": user_text})

    lang_name = LANGUAGE_NAMES.get(language, "English")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are JARVIS, a knowledgeable, witty, and concise AI assistant. "
                    f"Always reply in {lang_name}. "
                    f"Answer any question clearly — general knowledge, math, science, "
                    f"coding, advice, definitions, casual conversation, and more. "
                    f"Keep answers clear and not overly long unless asked for detail."
                )
            }
        ] + messages,
        max_tokens=500
    )
    return response.choices[0].message.content