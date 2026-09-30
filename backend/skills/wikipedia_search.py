import wikipedia

def search_wikipedia(text):
    query = text.lower().replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That's a bit ambiguous. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return f"I couldn't find anything on '{query}'."
    except Exception:
        return "Something went wrong searching Wikipedia."