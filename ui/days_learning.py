from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QGridLayout, QLabel, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QColor, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QTimer
import os

class DaysLearning(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Modern light background with a slight blue tint
        self.setStyleSheet("background-color: #EEF2F7;")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(20)

        # Header section with reduced height
        header_frame = QFrame()
        header_frame.setFixedHeight(120)  # Reduced from 170
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 #4B79A1, stop:1 #283E51);
                border-radius: 15px;
                padding: 8px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 5, 10, 5)
        header_layout.setSpacing(10)
        
        # Back button - reduced size
        back_button = QPushButton()
        back_button.setIcon(QIcon("assets/back_arrow.png"))
        back_button.setIconSize(QSize(18, 18))  # Reduced from 24x24
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 8px;
                min-width: 35px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        back_button.clicked.connect(self.go_back)

        # Header title
        header_label = QLabel("Days of the Week")
        header_label.setFont(QFont("Segoe UI", 26, QFont.Bold))  # Reduced from 28
        header_label.setStyleSheet("""
            QLabel {
                color: white;
                margin-left: 10px;
            }
        """)
        
        header_layout.addWidget(back_button)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addWidget(header_frame)

        # Days grid container
        grid_frame = QFrame()
        grid_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                padding: 20px;
            }
        """)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)  # Reduced from 30
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)  # Reduced from 5
        grid_frame.setGraphicsEffect(shadow)
        
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(15)  # Reduced from 20
        
        days_data = [
            {"row": 0, "days": ["SATURDAY", "SUNDAY", "MONDAY", "TUESDAY"]},
            {"row": 1, "days": ["WEDNESDAY", "THURSDAY", "FRIDAY"]}
        ]
        
        # Add buttons for each row
        for row_data in days_data:
            row = row_data["row"]
            days = row_data["days"]
            
            if row == 0:
                # First row: SATURDAY, SUNDAY, MONDAY, TUESDAY
                for i, day in enumerate(days):
                    button = self.create_day_button(day)
                    grid_layout.addWidget(button, row, i * 2, 1, 2)  # Each button spans 2 columns
            else:
                # Second row: WEDNESDAY, THURSDAY, FRIDAY centered
                start_col = 1  # Start from second column to center
                for i, day in enumerate(days):
                    button = self.create_day_button(day)
                    grid_layout.addWidget(button, row, start_col, 1, 2)  # Each button spans 2 columns
                    start_col += 2

        # Set equal column stretches
        for i in range(8):
            grid_layout.setColumnStretch(i, 1)
            
        main_layout.addWidget(grid_frame)

    def create_day_button(self, day):
        button = QPushButton(day)
        button.setFixedSize(220, 120)  # Reduced from 250x150
        button.setFont(QFont("Segoe UI", 14, QFont.Bold))  # Reduced from 16
        button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #e8e8e8;
                border-radius: 18px;
                color: #2c3e50;
                padding: 8px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 #4B79A1, stop:1 #283E51);
                color: white;
                border: none;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
            }
        """)
        
        # Button shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Reduced from 20
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 3)  # Reduced from 4
        button.setGraphicsEffect(shadow)
        
        button.clicked.connect(lambda: self.show_sign(day))
        return button

    def go_back(self):
        main_window = self.window()
        main_window.content_area.setCurrentIndex(4)

    def show_sign(self, day):
        # Close any existing video display
        if hasattr(self, 'sign_display') and self.sign_display:
            self.close_video()
        
        # Create the video display pop-up
        self.create_video_display(day)

    def create_video_display(self, day):
        self.sign_display = QFrame(self)
        self.sign_display.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """)
        
        layout = QVBoxLayout(self.sign_display)
        
        # Day label
        day_label = QLabel(f"Learning: {day}")
        day_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin: 8px;
        """)
        day_label.setAlignment(Qt.AlignCenter)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(380, 380)  # Reduced from 400x400
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)
        
        # Control buttons
        control_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                margin: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c0392b, stop:1 #a93226);
            }
        """)
        close_button.clicked.connect(self.close_video)
        control_layout.addWidget(close_button)
        
        # Add widgets to layout
        layout.addWidget(day_label)
        layout.addWidget(self.video_widget)
        layout.addLayout(control_layout)
        
        # Position and show the pop-up
        self.sign_display.setFixedSize(450, 550)  # Reduced from 500x600
        self.sign_display.move(
            self.width()//2 - self.sign_display.width()//2,
            self.height()//2 - self.sign_display.height()//2
        )
        self.sign_display.show()
        # Play the video for the selected day
        self.play_video(day)

    def play_video(self, day):
        video_path = self.get_video_path(day)
        if video_path:
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.mediaStatusChanged.connect(self.handle_media_status)
            self.media_player.play()
        else:
            self.show_error_popup(f"Video for {day} not found")

    def get_video_path(self, day):
        # Replace with the actual path to your video files
        possible_paths = [
            os.path.abspath(f"assets/days_videos/{day.lower()}.mp4"),
            os.path.abspath(f"assets/days_videos/{day.upper()}.mp4")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None

    def replay_video(self):
        self.media_player.setPosition(0)
        self.media_player.play()

    def handle_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def close_video(self):
        if hasattr(self, 'media_player'):
            self.media_player.stop()
        
        if hasattr(self, 'sign_display') and self.sign_display:
            if not self.sign_display.isHidden():
                self.sign_display.deleteLater()
                self.sign_display = None

    def show_error_popup(self, message):
        error_popup = QFrame(self)
        error_popup.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: none;
                box-shadow: 0 4px 6px rgba(231, 76, 60, 0.2);
            }
        """)
        
        layout = QVBoxLayout(error_popup)
        
        error_label = QLabel(message)
        error_label.setAlignment(Qt.AlignCenter)
        
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        ok_button.clicked.connect(error_popup.deleteLater)
        
        layout.addWidget(error_label)
        layout.addWidget(ok_button)
        
        error_popup.setFixedSize(280, 140)  # Reduced from 300x150
        error_popup.move(
            self.width()//2 - error_popup.width()//2,
            self.height()//2 - error_popup.height()//2
        )
        error_popup.show()
