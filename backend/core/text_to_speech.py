import pyttsx3

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except RuntimeError:
        pass  # engine busy, skip rather than crash