from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit,
    QToolButton, QMenu, QAction, QMainWindow, QApplication, QPlainTextEdit, QDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIntValidator, QClipboard
from functools import partial
import sys

class CodeWindow(QDialog):
    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generated Code")
        self.layout = QVBoxLayout()
        self.code_edit = QPlainTextEdit()
        self.code_edit.setPlainText(code)
        self.code_edit.setReadOnly(True)
        self.layout.addWidget(self.code_edit)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)

        self.setLayout(self.layout)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_edit.toPlainText())