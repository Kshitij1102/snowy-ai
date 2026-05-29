from resemblyzer import VoiceEncoder, preprocess_wav
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import time

encoder = VoiceEncoder()

SAMPLE_RATE = 16000
DURATION = 5


def record_voice(filename):

    print("🎙️ Recording starts in 3 seconds...")
    time.sleep(3)

    print("🎤 SPEAK NOW!")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )

    sd.wait()

    write(filename, SAMPLE_RATE, recording)

    print(f"✅ Saved as {filename}")


# 🚀 FIRST TIME REGISTRATION
if not os.path.exists("owner_voice.wav"):

    print("🧠 No owner profile found.")
    print("🚀 Creating owner voice profile...")

    record_voice("owner_voice.wav")

    print("✅ Owner voice registered successfully.")

# 🔐 VOICE VERIFICATION
else:

    print("🔐 Voice verification required.")

    record_voice("test_voice.wav")

    owner_wav = preprocess_wav("owner_voice.wav")
    test_wav = preprocess_wav("test_voice.wav")

    owner_embed = encoder.embed_utterance(owner_wav)
    test_embed = encoder.embed_utterance(test_wav)

    similarity = np.dot(owner_embed, test_embed)

    print(f"🔍 Similarity Score: {similarity}")

    if similarity > 0.75:

        print("✅ Access Granted. Welcome back Kshitij.")

    else:

        print("❌ Voice not recognized.")