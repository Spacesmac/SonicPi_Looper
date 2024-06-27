import time

is_recording = False
recorded_events = []
start_time = None
record_end_time = 0

def start_recording():
    global is_recording, recorded_events, start_time
    is_recording = True
    recorded_events = []
    start_time = time.time()

def stop_recording():
    global is_recording, record_end_time
    is_recording = False
    record_end_time = time.time() - start_time
    print(recorded_events)

def add_recorded_event(sample):
    global recorded_events, start_time
    if is_recording:
        recorded_events.append((sample, time.time() - start_time))

def get_recorded_events():
    return recorded_events

def get_end_time():
    return record_end_time