from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from logic.osc_client import send_osc_message
from logic.recording import start_recording, stop_recording, add_recorded_event, recorded_events

class DrumPadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Define the buttons and their corresponding sounds
        self.key_sample_map = {
            'a': 'bd_haus',
            's': 'sn_dub',
            'd': 'elec_hi_snare',
            'f': 'drum_cymbal_closed'
        }

        for key, sample in self.key_sample_map.items():
            button = QPushButton(f"Play {sample} (Key: {key.upper()})")
            button.clicked.connect(lambda _, s=sample: self.on_button_press(s))
            layout.addWidget(button)

        self.setLayout(layout)

    def on_button_press(self, sample):
        print(f"Playing sample: {sample}")
        send_osc_message("/drum_pad", sample)
        add_recorded_event(sample)

    def handle_key_press(self, event):
        key = event.text()
        print(f"Key press event in DrumPadWidget: {key}")  # Debug print
        if key in self.key_sample_map:
            self.on_button_press(self.key_sample_map[key])

