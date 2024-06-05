import tkinter as tk
from pythonosc import udp_client
import time
from threading import Thread

# Set up OSC client
ip = "127.0.0.1"
port = 4560
client = udp_client.SimpleUDPClient(ip, port)

# Variables to handle recording
is_recording = False
recorded_events = []
start_time = None

# Function to send OSC message
def send_osc_message(sample):
    client.send_message("/osc/drum_pad", sample)

# Function to handle button press
def on_button_press(sample):
    if is_recording:
        recorded_events.append((sample, time.time() - start_time))
    send_osc_message(sample)

# Function to handle key press
def on_key_press(event):
    key = event.char
    if key in key_sample_map:
        on_button_press(key_sample_map[key])

# Function to start recording
def start_recording():
    global is_recording, recorded_events, start_time
    is_recording = True
    recorded_events = []
    start_time = time.time()
    record_button.config(text="Stop Recording", command=stop_recording)

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False
    record_button.config(text="Start Recording", command=start_recording)

# Function to play back recorded events
def playback():
    def playback_thread():
        if not recorded_events:
            return
        start_playback_time = time.time()
        for sample, timestamp in recorded_events:
            elapsed = time.time() - start_playback_time
            if elapsed < timestamp:
                time.sleep(timestamp - elapsed)
            send_osc_message(sample)
    Thread(target=playback_thread).start()

# Create the main window
root = tk.Tk()
root.title("Drum Pad")

# Define the key to sample mapping
key_sample_map = {
    'a': 'bd_haus',
    's': 'sn_dub',
    'd': 'elec_hi_snare',
    'f': 'drum_cymbal_closed'
}

# Create buttons for each sample
for key, sample in key_sample_map.items():
    button = tk.Button(root, text=f"Play {sample} (Key: {key.upper()})", command=lambda s=sample: on_button_press(s))
    button.pack()

# Create record and playback buttons
record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack()

playback_button = tk.Button(root, text="Play Recording", command=playback)
playback_button.pack()

# Bind keys to the on_key_press function
root.bind("<KeyPress>", on_key_press)

# Run the Tkinter event loop
root.mainloop()
