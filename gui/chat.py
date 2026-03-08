# gui_chat.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class JarvisChatGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS Assistant")
        self.setGeometry(300, 100, 600, 700)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("JARVIS AI ASSISTANT")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)

        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)

        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)

        self.send_button.clicked.connect(self.handle_send)

        self.show()

    def display_user(self, text):
        self.chat_area.append(f"<b>YOU:</b> {text}")

    def display_jarvis(self, text):
        self.chat_area.append(f"<span style='color:cyan;'><b>JARVIS:</b> {text}</span>")

    def handle_send(self):
        text = self.input_box.text()
        if text:
            self.display_user(text)
            self.input_box.clear()
