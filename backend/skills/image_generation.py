import requests
import urllib.parse

def generate_image(prompt, width=1024, height=1024):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&enhance=true&nologo=true"

        # Verify the URL is reachable
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            return {
                "success": True,
                "url": image_url,
                "prompt": prompt
            }
        else:
            return {
                "success": False,
                "error": f"Image generation failed with status {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }