from biometric_auth import verify_face, verify_voice

print("🚀 Starting Face Verification...")

face_ok = verify_face()

if face_ok:

    print("✅ Face verified.")

    print("🚀 Starting Voice Verification...")

    voice_ok = verify_voice()

    if voice_ok:

        print("✅ Voice verified.")

        print("🔓 ACCESS GRANTED")

    else:

        print("❌ Voice verification failed.")

else:

    print("❌ Face verification failed.")