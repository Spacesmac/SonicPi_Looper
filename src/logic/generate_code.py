from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from logic.recording import get_recorded_events, get_end_time
from logic.osc_client import send_osc_message

# Create a global variable to hold the code window reference
code_window = None

def generate_sonic_pi_code():
    recorded_events = get_recorded_events()
    if not recorded_events:
        QMessageBox.information(None, "Info", "No recorded events to generate code.")
        return

    code_lines = ["live_loop :drum_rec do"]
    previous_timestamp = 0

    for sample, timestamp in recorded_events:
        wait_time = timestamp - previous_timestamp
        code_lines.append(f"  sleep {wait_time}")
        code_lines.append(f"  sample :{sample}")
        previous_timestamp = timestamp

    final_delay = get_end_time() - recorded_events[-1][1]
    if final_delay > 0:
        code_lines.append(f"  sleep {final_delay}")

    code_lines.append("end")

    code = "\n".join(code_lines)
    show_generated_code(code)
    send_sonic_pi_code(code)

def show_generated_code(code):
    global code_window
    if code_window is None:
        code_window = QWidget()
        code_window.setWindowTitle("Generated Sonic Pi Code")
        layout = QVBoxLayout()

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setText(code)

        layout.addWidget(text_area)
        code_window.setLayout(layout)
    
    # Ensure the window is visible and focused
    code_window.show()
    code_window.activateWindow()
    code_window.raise_()  # Bring to front

def send_sonic_pi_code(code):
    try:
        send_osc_message("/run-code", code)
        QMessageBox.information(None, "Success", "Code sent to Sonic Pi successfully.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to send code to Sonic Pi: {e}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    generate_sonic_pi_code()  # Call your function to generate and display code
    sys.exit(app.exec_())
