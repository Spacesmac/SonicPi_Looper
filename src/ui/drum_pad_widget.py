from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QMenu, QAction, QToolButton,QCheckBox, QSlider
)
import random
from functools import partial
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIntValidator
from ui.code_window import CodeWindow
from logic.osc_client import send_osc_message
from logic.recording import add_recorded_event

class DrumPadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bpm = 120
        self.cols_max = 8
        self.cols_loop_speed = 4
        self.playing_column = 0
        self.is_recording = False
        self.drum_samples = {
            'Kicks:': ['drum_heavy_kick'],
            'Bass Drums': ['drum_bass_soft', 'drum_bass_hard', 'bd_808', 'bd_chip', 'bd_mehackit', 'bd_zum', 'bd_ada', 'bd_boom', 'bd_fat', 'bd_gas', 'bd_haus', 'bd_klub', 'bd_pure', 'bd_sone', 'bd_tek', 'bd_zome'],
            'Snare Drums': ['drum_snare_hard', 'drum_snare_soft', 'sn_dub', 'sn_dolf', 'sn_zome', 'sn_generic'],
            'Tom Drums': ['drum_tom_hi_hard', 'drum_tom_hi_soft', 'drum_tom_lo_hard', 'drum_tom_lo_soft', 'drum_tom_mid_hard', 'drum_tom_mid_soft'],
            'Cymbals': ['drum_cymbal_closed', 'drum_cymbal_hard', 'drum_cymbal_open', 'drum_cymbal_pedal', 'drum_cymbal_soft'],
            'Hi-hats': ['hat_bdu', 'hat_cab', 'hat_cats'],
            'Other Percussions': ['drum_cowbell', 'drum_roll', 'elec_blip', 'elec_blip2', 'elec_bong', 'elec_chime', 'elec_filt_snare', 'elec_flip', 'elec_fuzz_tom', 'elec_hollow_kick', 'elec_lo_snare', 'elec_mid_snare', 'elec_ping', 'elec_pop', 'elec_snare', 'elec_soft_kick', 'elec_twang', 'elec_wood'],
        }
        self.key_sample_map = {
            'a': 'drum_heavy_kick',
            's': 'drum_snare_hard',
            'd': 'hat_bdu',
            'f': 'drum_cymbal_closed',
            'e': 'drum_tom_hi_hard',
            'z': 'drum_tom_lo_hard',
            'g': 'drum_tom_mid_hard'
        }
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.controls_layout = QGridLayout()
        self.humanize_checkbox = QCheckBox("Humanize")
        self.humanize_checkbox.setChecked(False)  # Default to off
        self.controls_layout.addWidget(self.humanize_checkbox, 1, 0)

        self.humanize_slider = QSlider(Qt.Horizontal)
        self.humanize_slider.setRange(0, 100)  # 0 to 100% timing variation
        self.humanize_slider.setValue(20)  # Default to 20%
        self.humanize_slider.setEnabled(False)
        self.controls_layout.addWidget(self.humanize_slider, 1, 1, 1, 2)

        self.humanize_checkbox.stateChanged.connect(self.toggle_humanize_slider)

        # Control buttons layout
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
        self.pad_number_label.setFixedWidth(80)
        self.controls_layout.addWidget(self.pad_number_label, 0, 4)
        self.pad_number = QLineEdit(str(self.cols_max))
        self.pad_number.setValidator(QIntValidator(2, 16))
        self.pad_number.setFixedWidth(50)
        self.pad_number.editingFinished.connect(self.update_max_pads)
        self.controls_layout.addWidget(self.pad_number, 0, 5)

        play_button = QPushButton("Play")
        play_button.clicked.connect(self.start_metronome)
        self.controls_layout.addWidget(play_button, 0, 6)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_metronome)
        self.controls_layout.addWidget(stop_button, 0,7)

        rec_button = QPushButton("Rec")
        rec_button.setCheckable(True)
        rec_button.clicked.connect(self.toggle_recording)
        self.controls_layout.addWidget(rec_button, 0, 8)

        generate_button = QPushButton("Generate Code")
        generate_button.clicked.connect(self.generate_code_from_grid)
        self.controls_layout.addWidget(generate_button, 0, 9)

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
        self.rows_max = len(self.key_sample_map)
        self.sequence_grid = [[False for _ in range(self.cols_max)] for _ in range(self.rows_max)]
        button_size = QSize(250, 30)
        self.interval_per_pad = 60 / (self.bpm * self.cols_loop_speed) * 1000

        # Create buttons for pads and dropdown menus for instruments
        for row, (key, sample) in enumerate(self.key_sample_map.items()):
            name_button = QToolButton()
            name_button.setText(f"Play {sample} (Key: {key.upper()})")
            name_button.setStyleSheet("background-color: lightgrey")
            name_button.setFixedSize(button_size)
            self.grid_layout.addWidget(name_button, row + 1, 0)

            # Create dropdown menu for instrument selection
            menu = QMenu()
            for category, instruments in self.drum_samples.items():
                category_menu = QMenu(category, self)
                for instrument in instruments:
                    action = QAction(instrument, self)
                    action.triggered.connect(partial(self.change_sample, key, instrument, name_button))
                    category_menu.addAction(action)
                menu.addMenu(category_menu)
            name_button.setMenu(menu)
            name_button.setPopupMode(QToolButton.InstantPopup)

            for col in range(self.cols_max):
                pad_button = QPushButton()
                pad_button.clicked.connect(lambda _, r=row, c=col: self.toggle_sequence_grid(r, c))
                self.update_button_color(pad_button, self.sequence_grid[row][col])  # Set initial color based on sequence_grid
                self.grid_layout.addWidget(pad_button, row + 1, col + 1)

    def toggle_humanize_slider(self, state):
        self.humanize_slider.setEnabled(state == Qt.Checked)

    def change_sample(self, key, sample, button):
        self.key_sample_map[key] = sample
        button.setText(f"Play {sample} (Key: {key.upper()})")
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

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.start_metronome()  # Ensure the metronome is running when recording starts
            print("Recording started")
        else:
            print("Recording stopped")

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

        code_window = CodeWindow(sonic_pi_code, self)
        code_window.exec_()

    def play_next_column(self):
        osc_list = []
        for col in range(self.cols_max):
            self.indicator_lines[col].setStyleSheet("background-color: red;")
        self.indicator_lines[self.playing_column].setStyleSheet("background-color: green;")
        for row in range(self.rows_max):
            if self.sequence_grid[row][self.playing_column]:
                print("Playing cols")
                sample = self.key_sample_map[list(self.key_sample_map.keys())[row]]
                osc_list.append(sample)
                if self.humanize_checkbox.isChecked():
                    deviation_percent = self.humanize_slider.value() / 100
                    deviation_ms = self.interval_per_pad * deviation_percent
                    random_delay = random.uniform(-deviation_ms, deviation_ms)
                    random_delay = max(0, int(random_delay))  # Clamp to zero if negative
                    QTimer.singleShot(random_delay, partial(send_osc_message, "/drum_pad", sample))
        if not self.humanize_checkbox.isChecked() and osc_list:
            send_osc_message("/drum_pad", osc_list)
        self.playing_column = (self.playing_column + 1) % self.cols_max

    def handle_key_press(self, event):
        key = event.text()
        print(f"Key press event in DrumPadWidget: {key}")  # Debug print
        if key in self.key_sample_map:
            sample = self.key_sample_map[key]
            self.on_name_button_press(sample)
            
            if self.is_recording:
                current_col = self.playing_column
                row = list(self.key_sample_map.keys()).index(key)
                print(f"Recording at row {row}, column: {current_col}")
                if 0 <= row < len(self.sequence_grid):
                    if 0 <= current_col < len(self.sequence_grid[row]):
                        print(f"{current_col}, len = {len(self.sequence_grid[row])}")
                        if current_col == 0:
                            self.sequence_grid[row][len(self.sequence_grid[row])-1] = True
                        else:
                            self.sequence_grid[row][current_col -1] = True
                        print(f"{self.sequence_grid}")
                        if current_col == 0:
                            col_button = self.grid_layout.itemAtPosition(row+1, len(self.sequence_grid[row])).widget()
                        else:
                            col_button = self.grid_layout.itemAtPosition(row+1, current_col).widget()
                        self.update_button_color(col_button, True)
    
    def set_playing_column(self, column):
        self.indicator_line.setGeometry((column + 1) * 50, 0, 2, self.height())
