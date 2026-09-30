import os
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from core.nlu import detect_intent
from core.memory import memory
from core.database import init_db, get_all_history, clear_history
from core.text_to_speech import speak
from skills.weather import get_weather
from skills.general_chat import chat_with_jarvis
from skills.wikipedia_search import search_wikipedia
from skills.news import get_news
from skills.system_control import open_app, shutdown_pc, set_volume
from skills.file_analysis import analyze_image, analyze_document
from skills.image_generation import generate_image
from skills.video_generation import get_video_prompt_and_link

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
init_db()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
DOC_EXTENSIONS = {".pdf", ".docx", ".txt"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    text = data.get("text", "")
    speak_reply = data.get("speak", False)
    language = data.get("language", "en")
    intent = detect_intent(text)

    if intent == "image":
        prompt = text.lower()
        for kw in ["generate image of", "create image of", "make image of",
                   "generate a picture of", "create a picture of", "draw",
                   "generate an image of", "create an image of",
                   "generate a photo of", "paint", "illustrate", "design",
                   "generate image", "create image", "make image",
                   "show me an image of", "show me a picture of"]:
            prompt = prompt.replace(kw, "").strip()
        result = generate_image(prompt)
        if result["success"]:
            return jsonify({
                "reply": f"Here's your generated image for: *{result['prompt']}*",
                "image_url": result["url"]
            })
        else:
            return jsonify({"reply": f"Sorry, I couldn't generate that image: {result['error']}"})

    elif intent == "video":
        result = get_video_prompt_and_link(text)
        return jsonify({
            "reply": "I've prepared your enhanced video prompt and opened the best free generator. Copy the prompt below and paste it there:",
            "video_data": result
        })

    elif intent == "weather":
        city = text.split("in")[-1].strip() if "in" in text else "Chennai"
        reply = get_weather(city)

    elif intent == "wikipedia":
        reply = search_wikipedia(text)

    elif intent == "news":
        reply = get_news()

    elif intent == "system":
        lower = text.lower()
        if "shutdown" in lower:
            reply = shutdown_pc()
        elif "volume" in lower:
            digits = "".join([c for c in lower if c.isdigit()])
            reply = set_volume(int(digits)) if digits else "Please specify a volume level."
        elif "open" in lower:
            app_name = lower.replace("open", "").strip()
            reply = open_app(app_name)
        else:
            reply = "I'm not sure what system action you want."

    else:
        memory.add("user", text)
        reply = chat_with_jarvis(text, memory.get(), language=language)
        memory.add("assistant", reply)

    if speak_reply:
        threading.Thread(target=speak, args=(reply,), daemon=True).start()

    return jsonify({"reply": reply})

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"reply": "No file received."}), 400

    file = request.files["file"]
    question = request.form.get("question", "").strip()
    if not question:
        question = "Analyze this and tell me what it is and any key information."

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    try:
        if ext in IMAGE_EXTENSIONS:
            reply = analyze_image(save_path, question)
        elif ext in DOC_EXTENSIONS:
            reply = analyze_document(save_path, question)
        else:
            reply = "Unsupported file type. I can analyze images (png, jpg, webp) and documents (pdf, docx, txt)."
    except Exception as e:
        reply = f"Something went wrong analyzing the file: {e}"
    finally:
        try:
            os.remove(save_path)
        except Exception:
            pass

    memory.add("user", f"[Uploaded file: {filename}] {question}")
    memory.add("assistant", reply)
    return jsonify({"reply": reply})

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": get_all_history()})

@app.route("/clear", methods=["POST"])
def clear():
    clear_history()
    return jsonify({"status": "Chat history cleared."})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "JARVIS backend is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)