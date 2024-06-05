import tkinter as tk
from pythonosc import udp_client

# Set up OSC client
ip = "127.0.0.1"
port = 4560
client = udp_client.SimpleUDPClient(ip, port)

# Function to send OSC message
def send_osc_message(sample):
    client.send_message("/drum_pad", sample)

# Function to handle button press
def on_button_press(sample):
    send_osc_message(sample)

# Function to handle key press
def on_key_press(event):
    key = event.char
    if key in key_sample_map:
        send_osc_message(key_sample_map[key])

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
    button.pack(pady=10)

# Bind keys to the on_key_press function
root.bind("<KeyPress>", on_key_press)

# Run the Tkinter event loop
root.mainloop()
