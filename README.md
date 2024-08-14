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

### Running the Application
#### 1. Clone the Repository:
   ```bash
   git clone https://github.com/Spacesmac/SonicPi_Looper.git
   cd [Repository]
   ```
#### 2. Run the Application
  ```bash
  python main.py
  ```
  This will start the application. The main window will open, allowing you to interact with the drum pads.
#### 3. Open Sonic Pi file (.rb) with Sonic Pi
  If you want to hear sound you will have to open the .rb at the root of the project with Sonic Pi. Once the file is open, you will just have to click on the Run button. Now if you fill the grid in the drum pad app, you should be able to hear what you are playing.
  
## Usage

### Starting the Application
When you start the application, a window with a grid layout will appear. The grid contains rows for each sample and columns for each beats. At the top, there are controls for BPM, loop speed, and other features.

### Playing Samples
**- Keyboard Controls:** Press the keys mapped to specific samples to play them. You can see the current mapping on the buttons in the first column or see bellow:
```python
 {
  'a': 'drum_heavy_kick',
  's': 'drum_snare_hard',
  'd': 'hat_bdu',
  'f': 'drum_cymbal_closed',
  'e': 'drum_tom_hi_hard',
  'z': 'drum_tom_lo_hard',
  'g': 'drum_tom_mid_hard'
}
```
You can change the mapping in the code if you want, it's in the _`drum_pad_widget.py`_ if you want starting at line `32`

**- Grid Controls:** Click on the grid to activate pads. When the loop is running, activated pads will trigger their respective samples at the correct time.

### Recording
**Start/Stop Recording:** Click the "Rec" button or press the "R" key to start and stop recording.
While recording, pressing a key will activate the corresponding pad in the grid.

### Code Generation
**Generate Code:** Click the "Generate Code" button toopen a window with the generated Sonic Pi code. You can also use the "Quick Generated Copy button to copy the code directly to your clipboard. With the generated code, you will be able to understand better the actions you are doing in the drum pad app, and what's actually the transalation to code of what you were playing. I recomend you to open another file next to the SonicPi file from the repository if you want to see clearly the code. You can click on `Stop` for the playing code, and then click `Run` with the other code so that you don't have two differents instances playing at the same time.

### Sending OSC Messages
**- Automatic:** The application automatically sends OSC messages to Sonic Pi whenever a sample is played.
**- Custom Effects:** Define custom effects using the effect input fields. These effects will be applied when sending OSC messages using another method of reception.


  
