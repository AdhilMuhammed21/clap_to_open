
import sounddevice as sd
import numpy as np
import subprocess
import time

SAMPLE_RATE = 44100
THRESHOLD = 0.25

# Clap state
clap_detected = False

# Timing
last_clap_time = 0

# Clap counter
clap_count = 0

# Wait after last clap
CLAP_TIMEOUT = 1

# Prevent repeated actions
action_triggered = False


def handle_claps(count):

    if count == 1:

        print("Opening YouTube")

        subprocess.run([
            "say",
            "Opening YouTube"
        ])

        subprocess.run([
            "open",
            "https://youtube.com"
        ])

    elif count == 2:

        print("Opening GitHub")

        subprocess.run([
            "say",
            "Opening GitHub"
        ])

        subprocess.run([
            "open",
            "https://github.com"
        ])

    elif count == 3:

        print("Opening ChatGPT")

        subprocess.run([
            "say",
            "Opening ChatGPT"
        ])

        subprocess.run([
            "open",
            "https://chat.openai.com"
        ])


def detect_clap(indata, frames, time_info, status):

    global clap_detected
    global last_clap_time
    global clap_count
    global action_triggered

    volume = np.linalg.norm(indata)

    current_time = time.time()

    # Detect clap edge
    if volume > THRESHOLD and not clap_detected:

        clap_detected = True

        # If starting fresh, allow actions again
        if clap_count == 0:
            action_triggered = False

        clap_count += 1

        last_clap_time = current_time

        print(f"👏 Clap count: {clap_count}")

    # Reset clap detector
    elif volume < THRESHOLD * 0.5:
        clap_detected = False

    # Execute ONLY ONCE
    if (
        clap_count > 0
        and not action_triggered
        and current_time - last_clap_time > CLAP_TIMEOUT
    ):

        handle_claps(clap_count)

        action_triggered = True

        clap_count = 0


print("🎤 Listening for claps...")

with sd.InputStream(
    callback=detect_clap,
    channels=1,
    samplerate=SAMPLE_RATE
):

    while True:
        sd.sleep(100)

