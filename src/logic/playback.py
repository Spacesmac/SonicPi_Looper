import time
from threading import Thread
from logic.osc_client import send_osc_message
from logic.recording import get_recorded_events, get_end_time

is_playing = False
playback_thread = None

def playback():
    def playback_thread_func(events):
        global is_playing
        print(events)
        if not events:
            return
        is_playing = True
        while is_playing:
            start_playback_time = time.time()
            for sample, timestamp in events:
                if not is_playing:
                    break
                elapsed = time.time() - start_playback_time
                if elapsed < timestamp:
                    time.sleep(timestamp - elapsed)
                send_osc_message("/drum_pad", sample)
            if get_end_time() > 0:
                time.sleep(get_end_time() - events[-1][1])
        is_playing = False

    global playback_thread
    if not is_playing:
        events = get_recorded_events()
        playback_thread = Thread(target=playback_thread_func, args=(events,), daemon=True)
        playback_thread.start()

def start_playback():
    playback()

def stop_playback():
    global is_playing
    is_playing = False
    # Update any UI controls related to playback
    # Example: main_window.playback_button.setText("Play Recording")
