from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="sk_fa1ee89dc5e7670c97f829f0fded916ab91fc3e700e4a35d"
)

audio = client.text_to_speech.convert(
    voice_id="4tRn1lSkEn13EVTuqb0g",
    text="Hello Kshitij. I am Snowy. Neural systems are online.",
    model_id="eleven_multilingual_v2"
)

with open("snowy_test.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("✅ Rachel voice generated successfully")