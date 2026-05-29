import face_recognition
import cv2
import os
import sounddevice as sd
from scipy.io.wavfile import write
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

VOICE_MODEL = VoiceEncoder()

AUTH_FOLDER = "auth"

OWNER_FACE = f"{AUTH_FOLDER}/owner_face.jpg"
OWNER_VOICE = f"{AUTH_FOLDER}/owner_voice.wav"

SAMPLE_RATE = 16000
DURATION = 8


# 👁️ FACE VERIFICATION
def verify_face():

    if not os.path.exists(OWNER_FACE):

        return False

    known_image = face_recognition.load_image_file(
        OWNER_FACE
    )

    known_encodings = face_recognition.face_encodings(
        known_image
    )

    if len(known_encodings) == 0:

        return False

    known_encoding = known_encodings[0]

    cam = cv2.VideoCapture(0)

    verified = False

    while True:

        ret, frame = cam.read()

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_encodings = face_recognition.face_encodings(
            rgb_frame
        )

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(
                [known_encoding],
                face_encoding,
                tolerance=0.50
            )

            if True in matches:

                verified = True

                break

        cv2.imshow(
            "SNOWY Face Verification",
            frame
        )

        if verified:
            break

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    return verified


# 🎙️ VOICE VERIFICATION
def verify_voice():

    if not os.path.exists(OWNER_VOICE):

        return False

    print("🎙️ Speak now...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )

    sd.wait()

    write(
        "auth/test_voice.wav",
        SAMPLE_RATE,
        recording
    )

    owner_wav = preprocess_wav(
        OWNER_VOICE
    )

    test_wav = preprocess_wav(
        "auth/test_voice.wav"
    )

    owner_embed = VOICE_MODEL.embed_utterance(
        owner_wav
    )

    test_embed = VOICE_MODEL.embed_utterance(
        test_wav
    )

    similarity = np.dot(
        owner_embed,
        test_embed
    )

    print(f"🔍 Voice Similarity: {similarity}")

    return similarity > 0.75