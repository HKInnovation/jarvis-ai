import urllib.parse
import webbrowser

def get_video_prompt_and_link(user_text):
    prompt = user_text.lower()
    for kw in ["generate video of", "create video of", "make video of",
                "generate a video of", "create a video of", "make a video of",
                "generate video", "create video", "make video",
                "text to video", "video of"]:
        prompt = prompt.replace(kw, "").strip()

    enhanced = prompt
    if "cinematic" not in prompt and "animation" not in prompt:
        enhanced = f"cinematic, high quality, smooth motion, {prompt}"

    # Auto-open Kling AI in browser
    webbrowser.open("https://app.klingai.com")

    return {
        "original_prompt": prompt,
        "enhanced_prompt": enhanced,
        "sites": [
            {
                "name": "Kling AI (66 free credits/day)",
                "url": "https://app.klingai.com",
                "note": "Just opened — paste your prompt there"
            },
            {
                "name": "Vidu AI (free tier)",
                "url": "https://www.vidu.io",
                "note": "Good motion, multi-shot scenes"
            },
            {
                "name": "HuggingFace WAN (fully free)",
                "url": "https://huggingface.co/spaces/Wan-AI/Wan2.1",
                "note": "Open source, no account needed"
            }
        ]
    }