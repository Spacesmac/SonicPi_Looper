from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator
from logic.osc_client import send_osc_message
from logic.recording import add_recorded_event

class DrumPadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bpm = 120
        self.cols_max = 8
        self.cols_loop_speed = 4
        self.playing_column = 0
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()

        # Control buttons layout
        self.controls_layout = QGridLayout()
        self.bpm_label = QLabel("BPM:")
        self.bpm_label.setFixedWidth(30)
        self.controls_layout.addWidget(self.bpm_label, 0, 0)
        self.bpm_input = QLineEdit(str(self.bpm))
        self.bpm_input.setValidator(QIntValidator(60, 240))  # Set the range for BPM
        self.bpm_input.setFixedWidth(50)
        self.bpm_input.editingFinished.connect(self.update_bpm_from_input)
        self.controls_layout.addWidget(self.bpm_input, 0, 1)

        self.pad_speed_label = QLabel("Pads/BPM:")
        self.pad_speed_label.setFixedWidth(70)
        self.controls_layout.addWidget(self.pad_speed_label, 0, 2)
        self.pad_speed = QLineEdit(str(self.cols_loop_speed))
        self.pad_speed.setValidator(QIntValidator(2, 16))
        self.pad_speed.setFixedWidth(50)
        self.pad_speed.editingFinished.connect(self.update_cols_speed_bpm)
        self.controls_layout.addWidget(self.pad_speed, 0, 3)

        self.pad_number_label = QLabel("Pads Number:")
        self.pad_number_label.setFixedWidth(70)
        self.controls_layout.addWidget(self.pad_number_label, 0, 4)
        self.pad_number = QLineEdit(str(self.cols_max))
        self.pad_number.setValidator(QIntValidator(2, 16))
        self.pad_number.setFixedWidth(50)
        self.pad_number.editingFinished.connect(self.update_max_pads)
        self.controls_layout.addWidget(self.pad_number, 0, 5)

        play_button = QPushButton("Play")
        play_button.clicked.connect(self.start_metronome)
        self.controls_layout.addWidget(play_button, 0, self.cols_max - 2)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_metronome)
        self.controls_layout.addWidget(stop_button, 0, self.cols_max - 1)

        generate_button = QPushButton("Generate Code")
        generate_button.clicked.connect(self.generate_code_from_grid)
        self.controls_layout.addWidget(generate_button, 0, self.cols_max)

        # Add controls layout to main layout
        self.main_layout.addLayout(self.controls_layout)

        # Grid layout
        self.grid_layout = QGridLayout()
        self.init_grid_layout()
        self.main_layout.addLayout(self.grid_layout)

        self.setLayout(self.main_layout)

        # Start metronome
        self.metronome_timer = QTimer(self)
        self.metronome_timer.timeout.connect(self.play_next_column)
        self.restart_metronome()

    def init_grid_layout(self):
        # Clear the old grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.indicator_lines = [QLabel() for _ in range(self.cols_max)]
        for col in range(self.cols_max):
            self.indicator_lines[col].setStyleSheet("background-color: red;")
            self.indicator_lines[col].setFixedHeight(20)
            self.grid_layout.addWidget(self.indicator_lines[col], 0, col + 1)

        self.key_sample_map = {
            'a': 'bd_haus',
            's': 'sn_dub',
            'd': 'elec_hi_snare',
            'f': 'drum_cymbal_closed'
        }
        self.rows_max = len(self.key_sample_map)
        self.sequence_grid = [[False for _ in range(self.cols_max)] for _ in range(self.rows_max)]

        self.interval_per_pad = 60 / (self.bpm * self.cols_loop_speed) * 1000

        # Create buttons for pads
        for row, (key, sample) in enumerate(self.key_sample_map.items()):
            name_button = QPushButton(f"Play {sample} (Key: {key.upper()})")
            name_button.clicked.connect(lambda _, s=sample: self.on_name_button_press(s))
            name_button.setStyleSheet("background-color: lightgrey")
            self.grid_layout.addWidget(name_button, row + 1, 0)

            for col in range(self.cols_max):
                pad_button = QPushButton()
                pad_button.clicked.connect(lambda _, r=row, c=col: self.toggle_sequence_grid(r, c))
                self.update_button_color(pad_button, self.sequence_grid[row][col])  # Set initial color based on sequence_grid
                self.grid_layout.addWidget(pad_button, row + 1, col + 1)

    def update_bpm_from_input(self):
        try:
            self.bpm = int(self.bpm_input.text())
            self.restart_metronome()
        except ValueError:
            self.bpm_input.setText(str(self.bpm))

    def update_max_pads(self):
        try:
            new_cols_max = int(self.pad_number.text())
            if new_cols_max >= self.cols_loop_speed:
                self.cols_max = new_cols_max
                self.playing_column = 0
                self.init_grid_layout()  # Reinitialize grid layout with new number of pads
                self.restart_metronome()
        except ValueError:
            self.pad_number.setText(str(self.cols_max))

    def update_cols_speed_bpm(self):
        try:
            self.bpm = int(self.bpm_input.text())
            self.cols_loop_speed = int(self.pad_speed.text())
            self.restart_metronome()
        except ValueError:
            self.bpm_input.setText(str(self.bpm))
            self.pad_speed.setText(str(self.cols_loop_speed))

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
        self.interval_per_pad = int(60 / (self.bpm * self.cols_loop_speed) * 1000)
        self.metronome_timer.setInterval(self.interval_per_pad)

        if not self.metronome_timer.isActive():
            self.metronome_timer.start()
        else:
            self.metronome_timer.stop()
            self.metronome_timer.start()

    def start_metronome(self):
        self.metronome_timer.start()

    def stop_metronome(self):
        if not self.metronome_timer.isActive():
            self.playing_column = 0
            for col in range(self.cols_max):
                self.indicator_lines[col].setStyleSheet("background-color: red;")
            self.indicator_lines[self.playing_column].setStyleSheet("background-color: green;")
        self.metronome_timer.stop()

    def generate_code_from_grid(self):
        sonic_pi_code = "use_bpm {}\n".format(self.bpm)
        pad_sleep = 1 / self.cols_loop_speed

        for row, (key, sample) in enumerate(self.key_sample_map.items()):
            sonic_pi_code += "live_loop :{} do\n".format(sample)
            accumulated_sleep = 0.0
            for col in range(self.cols_max):
                if self.sequence_grid[row][col]:
                    if accumulated_sleep > 0:
                        sonic_pi_code += "  sleep {}\n".format(accumulated_sleep)
                        accumulated_sleep = 0.0
                    sonic_pi_code += "  sample :{}\n".format(sample)
                    accumulated_sleep += pad_sleep
                else:
                    accumulated_sleep += pad_sleep
            if accumulated_sleep > 0:
                sonic_pi_code += "  sleep {}\n".format(accumulated_sleep)
            sonic_pi_code += "end\n"
        print(sonic_pi_code)

    def play_next_column(self):
        for col in range(self.cols_max):
            self.indicator_lines[col].setStyleSheet("background-color: red;")
        self.indicator_lines[self.playing_column].setStyleSheet("background-color: green;")
        for row in range(self.rows_max):
            if self.sequence_grid[row][self.playing_column]:
                print("Playing cols")
                sample = self.key_sample_map[list(self.key_sample_map.keys())[row]]
                send_osc_message("/drum_pad", sample)
        self.playing_column = (self.playing_column + 1) % self.cols_max

    def handle_key_press(self, event):
        key = event.text()
        print(f"Key press event in DrumPadWidget: {key}")  # Debug print
        if key in self.key_sample_map:
            self.on_name_button_press(self.key_sample_map[key])
    
    def set_playing_column(self, column):
        self.indicator_line.setGeometry((column + 1) * 50, 0, 2, self.height())
