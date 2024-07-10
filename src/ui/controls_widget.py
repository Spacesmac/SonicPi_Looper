from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QFont
from logic.recording import start_recording, stop_recording
from logic.playback import start_playback, stop_playback
from logic.generate_code import generate_sonic_pi_code

class ControlsWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()  # Horizontal layout for buttons

        self.record_button = QPushButton("Start Recording")
        self.record_button.setFont(QFont("Arial", 14))
        self.record_button.setStyleSheet("background-color: #ffcccc; padding: 10px;")
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)

        self.playback_button = QPushButton("Play")
        self.playback_button.setFont(QFont("Arial", 14))
        self.playback_button.setStyleSheet("background-color: #ccffcc; padding: 10px;")
        self.playback_button.clicked.connect(self.toggle_playback)
        layout.addWidget(self.playback_button)

        self.generate_code_button = QPushButton("Generate Sonic Pi Code")
        self.generate_code_button.setFont(QFont("Arial", 14))
        self.generate_code_button.setStyleSheet("background-color: #ccccff; padding: 10px;")
        self.generate_code_button.clicked.connect(generate_sonic_pi_code)
        layout.addWidget(self.generate_code_button)

        self.setLayout(layout)


    def handle_record_key(self, key):
        if key == "r":
            if self.record_button.text() == "Start Recording":
                start_recording()
                self.record_button.setText("Stop Recording")
            else:
                stop_recording()
                self.record_button.setText("Start Recording")

    def toggle_recording(self):
        if self.record_button.text() == "Start Recording":
            start_recording()
            self.record_button.setText("Stop Recording")
        else:
            stop_recording()
            self.record_button.setText("Start Recording")

    def toggle_playback(self):
            if self.playback_button.text() == "Play":
                start_playback()
                self.playback_button.setText("Stop")
            else:
                stop_playback()
                self.playback_button.setText("Play")
