# Drum Pad Kit - User Guide
## Overview
The Drum Pad Kit is a customizable drum machine application built with Python using the PyQt5 framework for the graphical user interface (GUI). This application allows users to map various drum samples to keyboard keys, sequence them in a grid, and control playback speed, effects, and more. It also supports recording sequences directly from key presses and generating code for Sonic Pi, a live coding music creation tool.

## Installation
### Requirements
- **Python 3**
- **PyQt5:** The GUI is built using PyQt5, so you will need to install this package.
- **Python-OSC:** This package is used for sending OSC messages to Sonic Pi.

### Dependencies
You can install the necessary dependencies using pip:
```bash
pip install PyQt5 python-osc
```

### Setting Up Sonic Pi
Ensure that you have Sonic Pi installed on your machine. It should be configured to accept OSC messages. By default, the drum pad sends OSC messages to `127.0.0.1` on port `4560`, which is the default for Sonic Pi.
