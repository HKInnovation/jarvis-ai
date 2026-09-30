import requests
from config import NEWSAPI_KEY

def get_news(query="India"):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWSAPI_KEY}&pageSize=5"
    r = requests.get(url).json()
    if r.get("status") != "ok":
        return "Sorry, I couldn't fetch the news right now."
    articles = r.get("articles", [])
    if not articles:
        return "No news found."
    headlines = [a["title"] for a in articles]
    return "Here are the top headlines: " + ". ".join(headlines)