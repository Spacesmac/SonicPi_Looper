def start_metronome(widget):
    widget.metronome_timer.start()

def stop_metronome(widget):
    if not widget.metronome_timer.isActive():
        widget.playing_column = 0
        for col in range(widget.cols_max):
            widget.indicator_lines[col].setStyleSheet("background-color: red;")
        widget.indicator_lines[widget.playing_column].setStyleSheet("background-color: green;")
    widget.metronome_timer.stop()

def restart_metronome(widget):
    widget.interval_per_pad = int(60 / (widget.bpm * widget.cols_loop_speed) * 1000)
    widget.metronome_timer.setInterval(widget.interval_per_pad)

    if not widget.metronome_timer.isActive():
        widget.metronome_timer.start()
    else:
        widget.metronome_timer.stop()
        widget.metronome_timer.start()
