from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from logic.osc_client import send_osc_message
from logic.recording import add_recorded_event
import time

class DrumPadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bpm = 120
        self.cols_max = 8
        self.cols_loop_speed = 4
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Metronome controls
        bpm_label = QLabel(f"BPM: {self.bpm}")
        layout.addWidget(bpm_label, 0, 0)

        bpm_slider = QSlider(Qt.Horizontal)
        bpm_slider.setMinimum(60)  # Minimum BPM
        bpm_slider.setMaximum(240)  # Maximum BPM
        bpm_slider.setValue(self.bpm)  # Initial BPM value
        bpm_slider.setTickInterval(10)  # Tick interval for slider
        bpm_slider.setTickPosition(QSlider.TicksBelow)  # Tick marks below slider

        def update_bpm(value):
            self.bpm = value
            bpm_label.setText(f"BPM: {self.bpm}")
            # Restart metronome with new BPM
            self.restart_metronome()

        bpm_slider.valueChanged.connect(update_bpm)
        layout.addWidget(bpm_slider, 0, 1)
        self.indicator_lines = [QLabel() for _ in range(self.cols_max)]  # Create list of labels for indicator lines
        for col in range(self.cols_max):
            self.indicator_lines[col].setStyleSheet("background-color: red;")
            layout.addWidget(self.indicator_lines[col], 0, col + 1)

        self.key_sample_map = {
            'a': 'bd_haus',
            's': 'sn_dub',
            'd': 'elec_hi_snare',
            'f': 'drum_cymbal_closed'
        }
        self.rows_max = len(self.key_sample_map)
        self.sequence_grid = [[False for _ in range(self.cols_max)] for _ in range(self.rows_max)]  # Sequence grid
        self.playing_column = 0  # Current column being played

        self.interval_per_pad = 60 / (self.bpm * self.cols_loop_speed) * 1000
        for row, (key, sample) in enumerate(self.key_sample_map.items()):
            name_button = QPushButton(f"Play {sample} (Key: {key.upper()})")
            name_button.clicked.connect(lambda _, s=sample: self.on_name_button_press(s))
            name_button.setStyleSheet("background-color: lightgrey")
            layout.addWidget(name_button, row + 1, 0)

            for col in range(1, self.cols_max + 1):
                pad_button = QPushButton()
                pad_button.clicked.connect(lambda _, r=row, c=col-1: self.toggle_sequence_grid(r, c))
                self.update_button_color(pad_button, self.sequence_grid[row][col-1])  # Set initial color based on sequence_grid
                layout.addWidget(pad_button, row + 1, col)

        self.setLayout(layout)

        # Start metronome
        self.metronome_timer = QTimer(self)
        self.metronome_timer.timeout.connect(self.play_next_column)
        self.restart_metronome()

    def update_button_color(self, button, is_active):
        if is_active:
            button.setStyleSheet("background-color: #ccffcc; padding: 10px; border: 1px solid black;")
        else:
            button.setStyleSheet("background-color: #ffcccc; padding: 10px; border: 1px solid black;")

    def toggle_sequence_grid(self, row, col):
        self.sequence_grid[row][col] = not self.sequence_grid[row][col]
        button = self.sender()
        self.update_button_color(button, self.sequence_grid[row][col])

    def on_name_button_press(self, sample):
        print(f"Playing sample: {sample}")
        send_osc_message("/drum_pad", sample)
        add_recorded_event(sample)

    def restart_metronome(self):
        self.metronome_timer.setInterval(int(self.interval_per_pad))


        if not self.metronome_timer.isActive():
            self.metronome_timer.start()
        else:
            self.metronome_timer.stop()
            self.metronome_timer.start()

    def play_next_column(self):
        for col in range(self.cols_max):
            self.indicator_lines[col].setStyleSheet("background-color: red;")
        self.indicator_lines[self.playing_column].setStyleSheet("background-color: green;")
        for row in range(self.rows_max):
            if self.sequence_grid[row][self.playing_column]:
                print("Playing cols")
                sample = self.key_sample_map[list(self.key_sample_map.keys())[row]]  # Get sample name based on row index
                send_osc_message("/drum_pad", sample)
        self.playing_column = (self.playing_column + 1) % self.cols_max  # Move to the next column

    def handle_key_press(self, event):
        key = event.text()
        print(f"Key press event in DrumPadWidget: {key}")  # Debug print
        if key in self.key_sample_map:
            self.on_name_button_press(self.key_sample_map[key])
    
    def set_playing_column(self, column):
        self.indicator_line.setGeometry((column + 1) * 50, 0, 2, self.height())
