import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 16000
DURATION = 8

print("🎙️ SNOWY Voice Registration")
print("🗣️ Say clearly:")
print("'Snowy authorize access'")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype=np.int16
)

sd.wait()

write(
    "auth/owner_voice.wav",
    SAMPLE_RATE,
    recording
)

print("✅ New owner voice registered.")