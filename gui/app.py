import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont


class JarvisGUI(QMainWindow):

    # 🔥 THREAD-SAFE SIGNALS
    status_signal = pyqtSignal(str)
    output_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS Assistant")
        self.setGeometry(400, 200, 800, 600)
        self.setStyleSheet("background-color: black;")

        # Connect signals
        self.status_signal.connect(self.set_status)
        self.output_signal.connect(self.insert_output)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # ==============================
        # TITLE
        # ==============================

        self.title_label = QLabel("JARVIS")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Orbitron", 30))
        self.title_label.setStyleSheet("color: cyan;")
        layout.addWidget(self.title_label)

        # ==============================
        # STATUS + SYSTEM INFO BAR
        # ==============================

        status_layout = QHBoxLayout()

        self.status_label = QLabel("Status: Waiting for wake word...")
        self.status_label.setFont(QFont("Consolas", 13))
        self.status_label.setStyleSheet("color: #00FFFF;")

        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Consolas", 13))
        self.clock_label.setStyleSheet("color: #00FFFF;")

        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.clock_label)

        layout.addLayout(status_layout)

        # ==============================
        # CHAT PANEL
        # ==============================

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Consolas", 12))
        self.chat_area.setStyleSheet("""
            background-color: black;
            color: #00FFFF;
            border: 1px solid #00FFFF;
        """)
        layout.addWidget(self.chat_area)

        # ==============================
        # PULSE ANIMATION
        # ==============================

        self.pulse = 0
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.animate)
        self.pulse_timer.start(500)

        # ==============================
        # CLOCK UPDATE TIMER
        # ==============================

        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    # ==================================
    # TITLE GLOW ANIMATION
    # ==================================

    def animate(self):
        self.pulse = (self.pulse + 1) % 2
        if self.pulse:
            self.title_label.setStyleSheet("color: #00FFFF;")
        else:
            self.title_label.setStyleSheet("color: #00BFFF;")

    # ==================================
    # CLOCK UPDATE
    # ==================================

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.setText(now)

    # ==================================
    # STATUS UPDATE
    # ==================================

    def set_status(self, text):
        self.status_label.setText(f"Status: {text}")

    # ==================================
    # INSERT OUTPUT WITH TIMESTAMP
    # ==================================

    def insert_output(self, user_text, jarvis_text):

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.chat_area.append(f"[{timestamp}] <b>USER:</b> {user_text}")
        self.chat_area.append(f"[{timestamp}] <b>JARVIS:</b> {jarvis_text}")
        self.chat_area.append("")

        # Smooth auto-scroll
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


# ======================================
# RUN GUI
# ======================================

def run_gui(pause_event=None):
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec())