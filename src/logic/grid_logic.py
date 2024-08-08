from PyQt5.QtWidgets import QLabel, QPushButton, QMenu, QAction, QToolButton
from PyQt5.QtCore import QSize
from functools import partial

def init_grid_layout(widget):
    # Clear the old grid layout
    for i in reversed(range(widget.grid_layout.count())):
        old_widget = widget.grid_layout.itemAt(i).widget()
        if old_widget:
            old_widget.deleteLater()
    widget.indicator_lines = [QLabel() for _ in range(widget.cols_max)]
    for col in range(widget.cols_max):
        widget.indicator_lines[col].setStyleSheet("background-color: red;")
        widget.indicator_lines[col].setFixedHeight(20)
        widget.grid_layout.addWidget(widget.indicator_lines[col], 0, col + 1)
    widget.rows_max = len(widget.key_sample_map)
    widget.sequence_grid = [[False for _ in range(widget.cols_max)] for _ in range(widget.rows_max)]
    button_size = QSize(250, 30)
    widget.interval_per_pad = 60 / (widget.bpm * widget.cols_loop_speed) * 1000

    for row, (key, sample) in enumerate(widget.key_sample_map.items()):
        name_button = QToolButton()
        name_button.setText(f"Play {sample} (Key: {key.upper()})")
        name_button.setStyleSheet("background-color: lightgrey")
        name_button.setFixedSize(button_size)
        widget.grid_layout.addWidget(name_button, row + 1, 0)

        menu = QMenu()
        for category, instruments in widget.drum_samples.items():
            category_menu = QMenu(category, widget)
            for instrument in instruments:
                action = QAction(instrument, widget)
                action.triggered.connect(partial(widget.change_sample, key, instrument, name_button))
                category_menu.addAction(action)
            menu.addMenu(category_menu)
        name_button.setMenu(menu)
        name_button.setPopupMode(QToolButton.InstantPopup)

        for col in range(widget.cols_max):
            pad_button = QPushButton()
            pad_button.setStyleSheet("background-color: white")
            pad_button.clicked.connect(partial(widget.toggle_sequence_grid, row, col))
            widget.grid_layout.addWidget(pad_button, row + 1, col + 1)

def toggle_sequence_grid(widget, row, col):
    widget.sequence_grid[row][col] = not widget.sequence_grid[row][col]
    update_button_color(widget, widget.grid_layout.itemAtPosition(row + 1, col + 1).widget(), row, col)

def update_button_color(widget, button, row, col):
    if widget.sequence_grid[row][col]:
        button.setStyleSheet("background-color: blue")
    else:
        button.setStyleSheet("background-color: white")
