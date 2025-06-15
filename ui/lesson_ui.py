import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, 
    QStackedWidget, QApplication, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .lessons.beginner_mode import BeginnerMode
from .lessons.intermediate_mode import IntermediateMode

class QuizUI(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.beginner_mode = BeginnerMode()
        self.intermediate_mode = IntermediateMode()
        self.init_ui()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_layout()
        
    def update_responsive_layout(self):
        window_width = self.width()
        window_height = self.height()
        
        # Dynamic sizing calculations
        header_size = min(36, max(24, window_width // 30))
        card_width = min(550, max(380, window_width // 2.1))  # Slightly reduced from previous
        image_height = min(230, window_height // 3.2)  # Slightly reduced from previous
        margin = window_width // 40
        
        # Update header
        self.header.setStyleSheet(f"""
            font-size: {header_size}px;
            color: #2c3e50;
            font-weight: bold;
            margin: {margin}px;
        """)
        
        # Update cards
        for card in self.findChildren(QFrame):
            if hasattr(card, 'card_type') and card.card_type == 'mode_card':
                card.setMinimumWidth(card_width)
            elif hasattr(card, 'card_type') and card.card_type == 'image_container':
                card.setFixedHeight(image_height)
                
        # Update labels and descriptions to be smaller
        for label in self.findChildren(QLabel):
            if hasattr(label, 'label_type'):
                if label.label_type == 'description':
                    label.setStyleSheet(f"""
                        color: #000000;
                        margin: 10px 0;
                        font-size: 14px;
                        font-weight: bold;
                        background-color: #f8f9fa;
                        padding: 8px;
                        border-radius: 5px;
                    """)
                elif label.label_type == 'feature':
                    label.setStyleSheet(f"""
                        color: #000000;
                        font-size: 13px;
                        font-weight: bold;
                        padding: 3px;
                    """)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.setup_mode_selection()
        self.main_layout.addWidget(self.stacked_widget)

    def setup_mode_selection(self):
        self.mode_selection = QWidget()
        self.mode_selection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mode_layout = QVBoxLayout(self.mode_selection)
        self.header = QLabel("ASL Learning Center")
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header.setAlignment(Qt.AlignCenter)
        # Create a container widget for the cards
        cards_container = QWidget()
        cards_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Apply the layout to the container
        cards_layout = QHBoxLayout(cards_container)
        margin = self.width() // 40
        cards_layout.setSpacing(margin)
        cards_layout.setContentsMargins(margin, margin, margin, margin)
        self.create_mode_cards(cards_layout)
        
        self.mode_layout.addWidget(self.header)
        self.mode_layout.addWidget(cards_container)  # Add the container instead of the layout
        self.stacked_widget.addWidget(self.mode_selection)
        self.stacked_widget.addWidget(self.beginner_mode)
        self.stacked_widget.addWidget(self.intermediate_mode)

    def create_mode_cards(self, cards_layout):
        modes = [
            {
                "title": "Beginner Mode",
                "image": "assets/beginner.jpg",
                "color": "#3498db",
                "description": "Start your ASL journey with alphabet basics",
                "features": ["Learn A-Z Signs", "Interactive Quizzes", "Progress Tracking"]
            },
            {
                "title": "Intermediate Mode",
                "image": "assets/intermediate.png",
                "color": "#e67e22",
                "description": "Advance to common words and phrases",
                "features": ["Word Practice", "Video Lessons", "Performance Metrics"]
            }
        ]
        for mode in modes:
            card = self.create_mode_card(mode)
            cards_layout.addWidget(card)

    def create_mode_card(self, mode_info):
        card = QFrame()
        card.card_type = 'mode_card'
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(self.height() // 50)
        
        title = QLabel(mode_info["title"])
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        image_container = QFrame()
        image_container.card_type = 'image_container'
        image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(5, 5, 5, 5)
        
        image_label = QLabel()
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(mode_info["image"])
        if not pixmap.isNull():
            # Slightly reduced dimensions from previous
            scaled_pixmap = pixmap.scaled(
                1300, 220,  # Reduced from 1500x240 to 1300x220
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)
            
        # Set minimum width for the image label
        image_label.setMinimumWidth(520)  # Reduced from 550 to 520
        
        image_layout.addWidget(image_label)
        
        desc = QLabel(mode_info["description"])
        desc.label_type = 'description'
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #000000;
            margin: 10px 0;
            font-size: 14px;
            font-weight: bold;
            background-color: #f8f9fa;
            padding: 8px;
            border-radius: 5px;
        """)
        desc.setAlignment(Qt.AlignCenter)
        
        features_frame = QFrame()
        features_frame.setStyleSheet("""
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 8px;
        """)
        features_layout = QVBoxLayout(features_frame)
        features_layout.setSpacing(2)
        
        for feature in mode_info["features"]:
            feature_label = QLabel(f"✓ {feature}")
            feature_label.label_type = 'feature'
            feature_label.setStyleSheet("""
                color: #000000;
                font-size: 13px;
                font-weight: bold;
                padding: 3px;
            """)
            features_layout.addWidget(feature_label)
        
        start_btn = QPushButton("Start Learning")
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {mode_info['color']};
                color: white;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 8px;
            }}
            QPushButton:hover {{
                background-color: {mode_info['color']}dd;
            }}
        """)
        start_btn.clicked.connect(lambda: self.start_mode(mode_info["title"]))
        
        layout.addWidget(title)
        layout.addWidget(image_container)
        layout.addWidget(desc)
        layout.addWidget(features_frame)
        layout.addWidget(start_btn)
        layout.setSpacing(10)
        
        return card

    def start_mode(self, mode_title):
        if mode_title == "Beginner Mode":
            self.stacked_widget.setCurrentWidget(self.beginner_mode)
        elif mode_title == "Intermediate Mode":
            self.stacked_widget.setCurrentWidget(self.intermediate_mode)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizUI()
    window.setWindowTitle("ASL Learning Center")
    window.show()
    sys.exit(app.exec())
