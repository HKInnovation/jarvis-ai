import base64
import os
from groq import Groq
from config import GROQ_KEY
import PyPDF2
import docx

client = Groq(api_key=GROQ_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path, user_question="Describe this image in detail."):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_question},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=600,
    )
    return response.choices[0].message.content

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def analyze_document(file_path, user_question="Summarize this document and highlight key points."):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        content = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        content = extract_text_from_docx(file_path)
    elif ext == ".txt":
        content = extract_text_from_txt(file_path)
    else:
        return "Unsupported file type. I can read PDF, DOCX, and TXT files."

    if not content.strip():
        return "I couldn't extract any readable text from that file."

    # Trim very long documents to stay within token limits
    content = content[:12000]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are JARVIS, an assistant that analyzes documents and answers questions about them clearly and concisely."},
            {"role": "user", "content": f"Document content:\n\n{content}\n\nUser request: {user_question}"}
        ],
        max_tokens=700,
    )
    return response.choices[0].message.content