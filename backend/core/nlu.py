IMAGE_KEYWORDS = [
    "generate image", "create image", "make image", "draw",
    "generate a picture", "create a picture", "make a picture",
    "generate an image", "create an image", "make an image",
    "generate a photo", "create a photo", "paint", "illustrate",
    "show me an image", "show me a picture", "design"
]

def detect_intent(text):
    text_lower = text.lower().strip()

    # Image generation — check first before other intents
    for keyword in IMAGE_KEYWORDS:
        if keyword in text_lower:
            return "image"

    # System commands
    if text_lower.startswith("open ") or text_lower.startswith("shutdown") or "set volume" in text_lower:
        return "system"

    # Weather
    if "weather" in text_lower:
        return "weather"

    # News
    if "news" in text_lower or "headline" in text_lower:
        return "news"

    # Wikipedia
    if text_lower.startswith("who is ") or text_lower.startswith("wikipedia "):
        return "wikipedia"

    # Everything else → Groq LLM
    return "chat"