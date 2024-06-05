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

# Variable to handle playback
playback_thread = None
is_playing = False
record_end_time = 0

# Function to send OSC message
def send_osc_message(sample):
    client.send_message("/drum_pad", sample)

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
    global is_recording, record_end_time
    is_recording = False
    record_end_time = time.time()
    record_button.config(text="Start Recording", command=start_recording)

# Function to play back recorded events
def playback():
    def playback_thread_func():
        global is_playing
        if not recorded_events:
            return
        is_playing = True
        playback_button.config(text="Stop Playback", command=stop_playback)
        while is_playing:
            start_playback_time = time.time()
            for sample, timestamp in recorded_events:
                if not is_playing:
                    break
                elapsed = time.time() - start_playback_time
                if elapsed < timestamp:
                    time.sleep(timestamp - elapsed)
                send_osc_message(sample)
            
            final_delay = record_end_time - (start_time + recorded_events[-1][1])
            if final_delay > 0:
                time.sleep(final_delay)
        is_playing = False
        playback_button.config(text="Play Recording", command=start_playback)

    global playback_thread
    if not is_playing:
        playback_thread = Thread(target=playback_thread_func, daemon=True)
        playback_thread.start()

# Function to start playback
def start_playback():
    playback()

# Function to stop playback
def stop_playback():
    global is_playing
    is_playing = False

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

# Create record button
record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack()

# Create playback button
playback_button = tk.Button(root, text="Play Recording", command=start_playback)
playback_button.pack()

# Bind keys to the on_key_press function
root.bind("<KeyPress>", on_key_press)

# Run the Tkinter event loop
root.mainloop()
