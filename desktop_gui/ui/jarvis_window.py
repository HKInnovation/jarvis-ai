import requests
import threading
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

BACKEND_URL = "http://localhost:5000/ask"


class Communicator(QObject):
    reply_received = pyqtSignal(str)


class JarvisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S.")
        self.setGeometry(200, 200, 500, 600)
        self.setStyleSheet("background-color: #0b0f1a; color: #00e5ff;")

        self.comm = Communicator()
        self.comm.reply_received.connect(self.display_reply)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("J.A.R.V.I.S.")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #00e5ff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet(
            "background-color: #11182b; border: 1px solid #00e5ff; font-size: 14px; padding: 8px;"
        )
        layout.addWidget(self.chat_box)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet(
            "background-color: #11182b; border: 1px solid #00e5ff; padding: 6px; color: white;"
        )
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        send_btn.setStyleSheet("background-color: #00e5ff; color: black; padding: 6px 16px;")
        input_layout.addWidget(send_btn)

        mic_btn = QPushButton("Mic")
        mic_btn.clicked.connect(self.listen_voice)
        mic_btn.setStyleSheet("background-color: #00e5ff; color: black; padding: 6px 12px;")
        input_layout.addWidget(mic_btn)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.append_chat("You", text)
        self.input_field.clear()
        threading.Thread(target=self.query_backend, args=(text,), daemon=True).start()

    def listen_voice(self):
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.comm.reply_received.emit("(Listening...)")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                text = recognizer.recognize_google(audio)
                self.append_chat("You (voice)", text)
                self.query_backend(text)
        except Exception as e:
            self.comm.reply_received.emit(f"(Couldn't hear you: {e})")

    def query_backend(self, text):
        try:
            response = requests.post(BACKEND_URL, json={"text": text, "speak": True}, timeout=30)
            reply = response.json().get("reply", "No response.")
        except Exception as e:
            reply = f"Error reaching backend: {e}"
        self.comm.reply_received.emit(reply)

    def display_reply(self, reply):
        self.append_chat("JARVIS", reply)

    def append_chat(self, sender, message):
        self.chat_box.append(f"<b>{sender}:</b> {message}")