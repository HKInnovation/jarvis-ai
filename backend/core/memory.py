from core.database import save_message, get_recent_history

class ConversationMemory:
    def __init__(self, max_turns=6):
        self.max_turns = max_turns

    def add(self, role, content):
        save_message(role, content)

    def get(self):
        return get_recent_history(limit=self.max_turns * 2)

memory = ConversationMemory()