from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
import random
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

print("🚀 SNOWY AI SYSTEM INITIALIZING...")


# 🧠 PERSISTENT MEMORY SYSTEM
MEMORY_FILE = "memory.json"


def load_memory():

    if Path(MEMORY_FILE).exists():

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return {
        "favorite_music": "Karan Aujla",
        "favorite_food": "Butter Chicken",
        "hobbies": ["Coding", "Guitar", "AI"],
        "mood_history": []
    }


memory = load_memory()


# 💾 SAVE MEMORY
def save_memory():

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


# ❄️ PERSONALITY ENGINE
def personality_response(category):

    responses = {

        "presence": [
            "For you… always.",
            "Still here. Systems fully operational.",
            "Always online. Always listening."
        ],

        "greeting": [
            "Hello boss.",
            "Welcome back.",
            "Good to see you again."
        ],

        "status": [
            "All SNOWY systems operational.",
            "Running smoothly.",
            "Everything is functioning perfectly."
        ],

        "thanks": [
            "You're welcome.",
            "Always a pleasure.",
            "Happy to help."
        ],

        "fallback": [
            "I didn't quite understand that.",
            "Could you repeat that?",
            "Still learning that command."
        ]
    }

    return random.choice(
        responses.get(category, responses["fallback"])
    )


# 🎵 MOOD DETECTION ENGINE
def detect_mood(cmd):

    cmd = cmd.lower()

    mood_songs = {

        "sad": [
            "songs/sad/sad1.mp3",
            "songs/sad/sad2.mp3",
            "songs/sad/sad3.mp3"
        ],

        "happy": [
            "songs/happy/happy1.mp3",
            "songs/happy/happy2.mp3",
            "songs/happy/happy3.mp3"
        ],

        "focus": [
            "songs/focus/focus1.mp3",
            "songs/focus/focus2.mp3",
            "songs/focus/focus3.mp3"
        ],

        "chill": [
            "songs/chill/chill1.mp3",
            "songs/chill/chill2.mp3",
            "songs/chill/chill3.mp3"
        ]
    }

    # 😢 SAD
    if (
        "sad" in cmd or
        "depressed" in cmd or
        "upset" in cmd or
        "hurt" in cmd
    ):

        return {
            "mood": "sad",
            "song": random.choice(
                mood_songs["sad"]
            )
        }

    # 😄 HAPPY
    elif (
        "happy" in cmd or
        "excited" in cmd or
        "great" in cmd
    ):

        return {
            "mood": "happy",
            "song": random.choice(
                mood_songs["happy"]
            )
        }

    # 🎯 FOCUS
    elif (
        "focus" in cmd or
        "study" in cmd or
        "work" in cmd
    ):

        return {
            "mood": "focus",
            "song": random.choice(
                mood_songs["focus"]
            )
        }

    # 🌊 CHILL
    elif (
        "chill" in cmd or
        "relax" in cmd or
        "calm" in cmd
    ):

        return {
            "mood": "chill",
            "song": random.choice(
                mood_songs["chill"]
            )
        }

    return {
        "mood": "default",
        "song": None
    }


# 🧠 MAIN AI ENGINE
def handle_command(cmd):

    cmd = cmd.lower().strip()

    print("🧠 COMMAND:", cmd)

    # 🎵 Detect Mood
    mood_data = detect_mood(cmd)

    mood = mood_data["mood"]
    song = mood_data["song"]

    # 🧠 Save mood history
    if mood != "default":

        memory["mood_history"].append(mood)

        save_memory()

    # ❄️ Presence
    if (
        ("snowy" in cmd and "there" in cmd) or
        ("are you there" in cmd)
    ):

        response = personality_response("presence")

    # 👋 Greetings
    elif (
        "hello" in cmd or
        "hi" in cmd or
        "hey" in cmd
    ):

        response = personality_response("greeting")

    # 📊 Status
    elif "how are you" in cmd:

        response = personality_response("status")

    # 🙏 Thanks
    elif "thank" in cmd:

        response = personality_response("thanks")

    # 🤖 Identity
    elif (
        "who are you" in cmd or
        "what are you" in cmd
    ):

        response = (
            "I am SNOWY. "
            "Smart Neural Operating Web Yield. "
            "Your intelligent AI operating system."
        )

    # 🎵 Mood Responses
    elif mood == "sad":

        response = (
            "You sound a little down. "
            "Playing something calming for you."
        )

    elif mood == "happy":

        response = (
            "I like this energy. "
            "Playing something upbeat."
        )

    elif mood == "focus":

        response = (
            "Focus mode activated."
        )

    elif mood == "chill":

        response = (
            "Relaxation mode enabled."
        )

    # 🧠 REMEMBER FAVORITE / FAVOURITE ARTIST
    elif (
        "remember that my favorite artist is" in cmd or
        "remember that my favourite artist is" in cmd
    ):

        artist = (
            cmd.replace(
                "remember that my favorite artist is",
                ""
            )
            .replace(
                "remember that my favourite artist is",
                ""
            )
            .strip()
        )

        memory["favorite_music"] = artist

        save_memory()

        response = (
            f"Got it. I'll remember that your favorite artist is {artist}."
        )

    # 🍔 REMEMBER FAVORITE / FAVOURITE FOOD
    elif (
        "remember that my favorite food is" in cmd or
        "remember that my favourite food is" in cmd
    ):

        food = (
            cmd.replace(
                "remember that my favorite food is",
                ""
            )
            .replace(
                "remember that my favourite food is",
                ""
            )
            .strip()
        )

        memory["favorite_food"] = food

        save_memory()

        response = (
            f"I'll remember that your favorite food is {food}."
        )

    # 🎸 REMEMBER HOBBY
    elif "remember that my hobby is" in cmd:

        hobby = cmd.replace(
            "remember that my hobby is",
            ""
        ).strip()

        memory["hobbies"].append(hobby)

        save_memory()

        response = (
            f"Saved. I'll remember that you enjoy {hobby}."
        )

    # 🎵 RECALL ARTIST
    elif (
        "who is my favorite artist" in cmd or
        "who is my favourite artist" in cmd
    ):

        response = (
            f"Your favorite artist is {memory['favorite_music']}."
        )

    # 🍗 RECALL FOOD
    elif (
        "what is my favorite food" in cmd or
        "what is my favourite food" in cmd
    ):

        response = (
            f"Your favorite food is {memory['favorite_food']}."
        )

    # 🎯 RECALL HOBBIES
    elif "what are my hobbies" in cmd:

        hobbies = ", ".join(memory["hobbies"])

        response = (
            f"Your hobbies include {hobbies}."
        )

    # 🧠 MEMORY SUMMARY
    elif "what do you know about me" in cmd:

        response = (
            f"You enjoy {memory['favorite_music']}, "
            f"love {memory['favorite_food']}, "
            f"and your hobbies include "
            f"{', '.join(memory['hobbies'])}."
        )

    # 🕒 TIME
    elif "time" in cmd:

        response = (
            "It's " +
            datetime.datetime.now().strftime("%I:%M %p")
        )

    # 🌐 YOUTUBE
    elif "youtube" in cmd:

        os.system("open https://youtube.com")

        response = "Opening YouTube."

    # 🌍 CHROME
    elif (
        "chrome" in cmd or
        "browser" in cmd
    ):

        os.system("open -a 'Google Chrome'")

        response = "Opening Chrome."

    # 📁 FINDER
    elif "finder" in cmd:

        os.system(
            "open /System/Library/CoreServices/Finder.app"
        )

        response = "Opening Finder."

    # 🎵 PLACEHOLDERS
    elif "spotify" in cmd:

        response = (
            "Spotify integration is not connected yet."
        )

    elif "play music" in cmd:

        response = (
            "Music system will be available soon."
        )

    # ❓ FALLBACK
    else:

        response = personality_response("fallback")

    return {
        "response": response,
        "song": song,
        "mood": mood
    }


# 🔗 API ROUTE
@app.route("/command", methods=["POST"])
def command():

    data = request.json

    cmd = data.get("command", "")

    result = handle_command(cmd)

    return jsonify(result)


# 🚀 RUN SERVER
if __name__ == "__main__":

    print("🚀 SNOWY AI SYSTEM ONLINE")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )