import requests
from config import OPENWEATHER_KEY

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    r = requests.get(url).json()
    if r.get("cod") != 200:
        return f"Sorry, I couldn't find weather for {city}."
    temp = r["main"]["temp"]
    desc = r["weather"][0]["description"]
    return f"It's {temp}°C with {desc} in {city}."