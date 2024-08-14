from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QApplication, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.drum_pad_widget import DrumPadWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drum Pad Kit")
        self.setGeometry(100, 100, 600, 600)

        main_layout = QVBoxLayout()
        
        self.drum_pad = DrumPadWidget()
        main_layout.addWidget(self.drum_pad)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        print(f"Key pressed: {event.text()}")  # Debug print
        if event.text() == 'r': #Record button
            self.drum_pad.toggle_recording()
        else:
            self.drum_pad.handle_key_press(event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
