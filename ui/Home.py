import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QGraphicsOpacityEffect)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from ui.STT import STT
from ui.TTS import TTS
import subprocess
import sys

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Language Interpreter")
        self.setGeometry(100, 100, 1100, 700)  # Reduced window size
        self.setStyleSheet("""QMainWindow { background-color: #f7f9fc; }""")
        
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)  # Reduced spacing
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        content_area = self.create_scrollable_content()
        main_layout.addWidget(content_area)
        
        self.setCentralWidget(main_widget)

    def open_stt(self):
        self.stt_window = STT()
        self.stt_window.show()
        main_window = self.parent().parent()
        main_window.content_area.setCurrentIndex(1) 
        main_window.nav_button_dict["Sign to Text"].click()
        self.close()

    def open_tts(self):
        self.tts_window = TTS()
        self.tts_window.show()
        main_window = self.parent().parent()
        main_window.content_area.setCurrentIndex(2) 
        main_window.nav_button_dict["Text to Sign"].click()
        self.close()
        
    # Apply animation after initializing the main window
    def create_scrollable_content(self):
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)  # Reduced spacing
        content_layout.setContentsMargins(30, 15, 30, 15)  # Reduced margins
        
        welcome_label = QLabel("Welcome to Sign Language Interpreter")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""font-size: 32px; color: #7f8c8d; font-weight: bold; """)  # Reduced font size
        content_layout.addWidget(welcome_label, 1)
        
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(30)  # Reduced spacing
        
        sign_to_text_widget = self.create_option_widget(
            "Sign Language to Text",
            "assets/sign_to_text_image.jpg",
            "Convert sign language gestures into written text."
        )
        grid_layout.addWidget(sign_to_text_widget)
        
        text_to_sign_widget = self.create_option_widget(
            "Text to Sign Language",
            "assets/text_to_sign_image.jpg",
            "Convert written text into sign language animations."
        )
        grid_layout.addWidget(text_to_sign_widget)
        
        content_layout.addLayout(grid_layout, 10)
        
        return content_widget

    def create_option_widget(self, title, image_path, description):
        widget = QFrame()
        widget.setStyleSheet(" background-color: #ffffff; border-radius: 10px; ")  # Reduced border radius
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)  # Reduced spacing
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced margins
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""font-size: 22px; font-weight: bold; color: #2c3e50;""")  # Reduced font size
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Reduced image size
            image_label.setPixmap(pixmap.scaled(260, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
        start_button = QPushButton("Start Translation")
        start_button.setIcon(QIcon("assets/start_icon.png"))
        
        if title == "Sign Language to Text":
            start_button.clicked.connect(lambda: self.window().content_area.setCurrentIndex(1))
        else:
            start_button.clicked.connect(lambda: self.window().content_area.setCurrentIndex(2))
        
        # Reduced button size and padding
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 12px 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        
        layout.addWidget(start_button)
        
        return widget

    def open_stt(self):
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            stt_path = os.path.join(script_dir, "ui", "STT.py")
            print(f"Opening: {stt_path}")  # Debug print
            subprocess.Popen([sys.executable, stt_path])
            self.close()
        except Exception as e:
            print(f"Error opening STT: {e}")

    def open_tts(self):
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tts_path = os.path.join(script_dir, "ui", "TTS.py")
            print(f"Opening: {tts_path}")  # Debug print
            subprocess.Popen([sys.executable, tts_path])
            self.close()
        except Exception as e:
            print(f"Error opening TTS: {e}")

def main():
    app = QApplication([])
    window = Home()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
