import os
from dotenv import load_dotenv
load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")