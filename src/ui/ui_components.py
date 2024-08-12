from PyQt5.QtWidgets import QCheckBox, QSlider, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

def create_checkbox(text, status, slot):
    checkbox = QCheckBox(text)
    checkbox.setChecked(status)
    checkbox.stateChanged.connect(slot)
    return checkbox

def create_slider(orientation, min_value, max_value, default_value, status):
    slider = QSlider(orientation)
    slider.setRange(min_value, max_value)
    slider.setValue(default_value)
    slider.setEnabled(status)
    return slider

def create_labeled_input(label_text, label_width, default_value, validator, line_width, slot):
    label = QLabel(label_text)
    label.setFixedWidth(label_width)
    line_edit = QLineEdit(default_value)
    if validator != None:
        line_edit.setValidator(validator)
    line_edit.setFixedWidth(line_width)
    if slot != None:
        line_edit.editingFinished.connect(slot)
    return {'label': label, 'input': line_edit}
