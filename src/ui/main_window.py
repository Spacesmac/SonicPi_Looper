from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.drum_pad_widget import DrumPadWidget
from ui.controls_widget import ControlsWidget
from logic import recording  # Import the recording logic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drum Pad Kit")
        self.setGeometry(100, 100, 400, 300)

        main_layout = QVBoxLayout()

        title = QLabel("Drum Pad Kit")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.drum_pad = DrumPadWidget()
        main_layout.addWidget(self.drum_pad)

        self.controls = ControlsWidget()
        main_layout.addWidget(self.controls)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        print(f"Key pressed: {event.text()}")  # Debug print
        if event.text() == 'r': #Record button
            print("here")
            self.controls.handle_record_key(event.text())
        else:
            self.drum_pad.handle_key_press(event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
