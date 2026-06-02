import sounddevice as sd
import numpy as np
import subprocess
import time

SAMPLE_RATE = 44100
THRESHOLD = 0.25

# Track clap state
clap_detected = False

# Cooldown timing
last_clap_time = 0
CLAP_COOLDOWN = 0.4


def detect_clap(indata, frames, time_info, status):
    global clap_detected
    global last_clap_time

    volume = np.linalg.norm(indata)

    current_time = time.time()

    # Rising edge detection
    if volume > THRESHOLD and not clap_detected:

        # Cooldown protection
        if current_time - last_clap_time > CLAP_COOLDOWN:

            print("👏 Clap detected!")

            subprocess.run(["open", "-a", "Brave Browser"])

            last_clap_time = current_time

        clap_detected = True

    # Reset state when sound becomes quiet
    elif volume < THRESHOLD * 0.5:
        clap_detected = False


print("Listening for claps...")

with sd.InputStream(callback=detect_clap,
                    channels=1,
                    samplerate=SAMPLE_RATE):

    while True:
        sd.sleep(1000)