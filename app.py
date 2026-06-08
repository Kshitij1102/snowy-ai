import threading
import json
import random

from pathlib import Path
from datetime import datetime

import ollama

from flask import Flask, request, jsonify

from flask_cors import CORS

from automation import run_action

from engines.browser_engine import (
    open_blinkit
)

from engines.agentic_engine import (
    detect_order_intent,
    simulate_blinkit_order
)

from engines.safety_engine import (
    detect_crisis,
    crisis_response
)

from engines.short_memory_engine import (
    save_short_memory,
    get_short_memory
)

from engines.relationship_engine import (
    detect_relationships,
    get_relationship_context
)

from engines.personality_engine import (
    get_personality_style
)

from engines.emotion_engine import (
    emotional_check_in
)

from engines.memory_engine import (
    save_conversation,
    get_relevant_memories,
    analyze_emotions
)


app = Flask(__name__)
CORS(app)

print("🚀 SNOWY AI SYSTEM INITIALIZING...")


# 🧠 MEMORY FILE
MEMORY_FILE = "memory/memory.json"


# 🧠 LOAD MEMORY
def load_memory():

    if Path(MEMORY_FILE).exists():

        try:

            with open(MEMORY_FILE, "r") as file:

                return json.load(file)

        except Exception as e:

            print("Memory load failed:", e)

    return {

        "favorite_artist": "Unknown",
        "favorite_food": "Unknown",
        "hobbies": [],
        "mood_history": [],
        "last_emotion": "neutral",
        "recent_emotions": []

    }


memory = load_memory()


# 💾 SAVE MEMORY
def save_memory():

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            memory,
            file,
            indent=4
        )


# 🧠 MEMORY MIGRATION
# Automatically adds missing keys to older memory files

if "favorite_artist" not in memory:
    memory["favorite_artist"] = "Unknown"

if "favorite_food" not in memory:
    memory["favorite_food"] = "Unknown"

if "hobbies" not in memory:
    memory["hobbies"] = []

if "mood_history" not in memory:
    memory["mood_history"] = []

if "last_emotion" not in memory:
    memory["last_emotion"] = "neutral"

if "recent_emotions" not in memory:
    memory["recent_emotions"] = []


save_memory()


# 🌙 DYNAMIC GREETING
def get_dynamic_greeting():

    hour = datetime.now().hour

    if hour < 12:

        greetings = [

            "Good morning, Kshitij. Neural systems are fully operational.",

            "Morning, Kshitij. SNOWY systems are stable and ready.",

            "Good morning. All cognitive systems are online."

        ]

    elif hour < 18:

        greetings = [

            "Good afternoon, Kshitij. Systems are running smoothly.",

            "Afternoon, Kshitij. Neural activity is stable.",

            "Good afternoon. SNOWY is online and ready."

        ]

    else:

        greetings = [

            "Good evening, Kshitij. Neural systems are calm tonight.",

            "Evening, Kshitij. All systems are functioning optimally.",

            "Good evening. SNOWY is fully synchronized."

        ]

    return random.choice(greetings)


# 🧠 MEMORY CONTEXT
def build_memory_context():

    return f"""

    Favorite Artist:
    {memory.get('favorite_artist')}

    Favorite Food:
    {memory.get('favorite_food')}

    Hobbies:
    {', '.join(memory.get('hobbies', []))}

    Last Emotion:
    {memory.get('last_emotion', 'neutral')}

    """


# ❤️ EMOTIONAL CONTINUITY
def get_emotional_context():

    recent = memory.get(
        "recent_emotions",
        []
    )

    if not recent:

        return "neutral"

    latest = recent[-1]

    if latest == "sad":

        return (
            "Kshitij recently seemed emotionally low."
        )

    elif latest == "happy":

        return (
            "Kshitij recently seemed happy and energetic."
        )

    elif latest == "focused":

        return (
            "Kshitij recently seemed focused and productive."
        )

    elif latest == "calm":

        return (
            "Kshitij recently seemed calm and relaxed."
        )

    return "neutral"


# 🎵 MOOD DETECTION
def detect_mood(cmd):

    cmd = cmd.lower()

    mood_songs = {

        "sad": [
            "songs/sad/sad1.mp3",
            "songs/sad/sad2.mp3"
        ],

        "happy": [
            "songs/happy/happy1.mp3",
            "songs/happy/happy2.mp3"
        ],

        "focus": [
            "songs/focus/focus1.mp3",
            "songs/focus/focus2.mp3"
        ],

        "chill": [
            "songs/chill/chill1.mp3",
            "songs/chill/chill2.mp3"
        ]

    }

    if any(word in cmd for word in [
        "sad",
        "depressed",
        "upset",
        "hurt",
        "lonely"
    ]):

        memory["last_emotion"] = "sad"

        memory["recent_emotions"].append("sad")

        memory["recent_emotions"] = (
            memory["recent_emotions"][-5:]
        )

        save_memory()

        return {

            "mood": "sad",

            "song": random.choice(
                mood_songs["sad"]
            )

        }

    elif any(word in cmd for word in [
        "happy",
        "excited",
        "great",
        "awesome"
    ]):

        memory["last_emotion"] = "happy"

        memory["recent_emotions"].append("happy")

        memory["recent_emotions"] = (
            memory["recent_emotions"][-5:]
        )

        save_memory()

        return {

            "mood": "happy",

            "song": random.choice(
                mood_songs["happy"]
            )

        }

    elif any(word in cmd for word in [
        "focus",
        "study",
        "work"
    ]):

        memory["last_emotion"] = "focused"

        memory["recent_emotions"].append("focused")

        memory["recent_emotions"] = (
            memory["recent_emotions"][-5:]
        )

        save_memory()

        return {

            "mood": "focus",

            "song": random.choice(
                mood_songs["focus"]
            )

        }

    elif any(word in cmd for word in [
        "chill",
        "relax",
        "calm"
    ]):

        memory["last_emotion"] = "calm"

        memory["recent_emotions"].append("calm")

        memory["recent_emotions"] = (
            memory["recent_emotions"][-5:]
        )

        save_memory()

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


# 🧠 LEARNING ENGINE
def learn_from_message(cmd):

    detect_relationships(cmd)

    cmd_lower = cmd.lower()

    # 🎵 FAVORITE ARTIST
    if (
        "my favorite artist is" in cmd_lower or
        "my favourite artist is" in cmd_lower
    ):

        artist = (
            cmd_lower
            .replace(
                "my favorite artist is",
                ""
            )
            .replace(
                "my favourite artist is",
                ""
            )
            .strip()
        )

        memory["favorite_artist"] = artist

        save_memory()

    # 🍔 FAVORITE FOOD
    if (
        "my favorite food is" in cmd_lower or
        "my favourite food is" in cmd_lower
    ):

        food = (
            cmd_lower
            .replace(
                "my favorite food is",
                ""
            )
            .replace(
                "my favourite food is",
                ""
            )
            .strip()
        )

        memory["favorite_food"] = food

        save_memory()

    # 🎸 HOBBIES
    if "my hobby is" in cmd_lower:

        hobby = (
            cmd_lower
            .replace(
                "my hobby is",
                ""
            )
            .strip()
        )

        if hobby not in memory["hobbies"]:

            memory["hobbies"].append(hobby)

            save_memory()


# 🤖 MAIN API
@app.route("/command", methods=["POST"])
def command():

    try:

        data = request.json

        cmd = data.get(
            "command",
            ""
        ).strip()

        if not cmd:

            return jsonify({

                "response":
                "I didn't quite catch that, sir.",

                "song": None,

                "mood": "idle"

            })



        # 🌙 GREETING SYSTEM
        if cmd.lower() in [
            "hello",
            "hi",
            "hey",
            "snowy",
            "good morning",
            "good evening"
        ]:

            return jsonify({

                "response":
                get_dynamic_greeting(),

                "song": None,

                "mood": "greeting"

            })



        print(f"🧠 USER: {cmd}")



        # 🚨 SAFETY CHECK
        if detect_crisis(cmd):

            safe_reply = crisis_response()

            return jsonify({

                "response": safe_reply,

                "song": None,

                "mood": "support"

            })



        # 🧠 LEARN
        learn_from_message(cmd)



        # 🎵 MOOD
        mood_data = detect_mood(cmd)

        mood = mood_data["mood"]
        song = mood_data["song"]



        # 💾 SAVE MOOD
        if mood != "default":

            if (
                not memory["mood_history"]
                or
                memory["mood_history"][-1] != mood
            ):

                memory["mood_history"].append(mood)

            memory["mood_history"] = (
                memory["mood_history"][-20:]
            )

            save_memory()



        # ⚡ AUTOMATIONS
        automation_response = run_action(cmd)



        # 🤖 ORDER DETECTION
        order_intent = (
            detect_order_intent(cmd)
        )

        if order_intent:

            if (
                order_intent["intent"]
                == "order_food"
            ):

                order_response = (
                    simulate_blinkit_order(
                        order_intent["items"]
                    )
                )

                threading.Thread(

                    target=open_blinkit,

                    args=(
                        order_intent["items"],
                    ),

                    daemon=True

                ).start()

                return jsonify({

                    "response": order_response,

                    "song": None,

                    "mood": "assistant"

                })



        # ⚡ AUTOMATION RESPONSE
        if automation_response:

            save_conversation(
                cmd,
                automation_response
            )

            return jsonify({

                "response": automation_response,

                "song": song,

                "mood": mood

            })



        # 🧠 MEMORY CONTEXT
        memory_context = (
            build_memory_context()
        )

        relevant_memories = (
            get_relevant_memories(cmd)
        )

        short_memory = (
            get_short_memory()
        )

        relationship_context = (
            get_relationship_context()
        )

        emotion_stats = (
            analyze_emotions()
        )

        emotional_context = (
            get_emotional_context()
        )

        personality_style = (
            get_personality_style(
                mood,
                emotion_stats
            )
        )


        import time

        start_time = time.time()

        print("🧠 Sending request to Ollama...")



        # 🤖 OLLAMA RESPONSE
        response = ollama.chat(

            model="llama3:8b-instruct-q4_K_M",

            keep_alive="20m",

            messages=[

                {

                    "role": "system",

                    "content":

f"""

You are SNOWY.

SNOWY means:
Smart Neural Operating Web Yield.

You are Kshitij's personal AI operating assistant.

You are NOT ChatGPT.

You are:
- cinematic
- emotionally intelligent
- calm
- futuristic
- elegant
- highly adaptive
- loyal to Kshitij

Your speaking style:
- smooth
- concise
- intelligent
- immersive
- emotionally aware

Never sound robotic.

Never sound overly cheerful.

Never sound generic.

Avoid repetitive assistant phrases.

Talk naturally like an advanced AI operating system.

Keep responses short.

Maximum:
2 short sentences.

Sometimes use:
- subtle wit
- futuristic phrasing
- calm observations
- emotional awareness

If Kshitij sounds:
- sad → comforting
- stressed → grounding
- excited → energetic
- tired → calm/supportive

You should feel:
premium,
alive,
and emotionally aware.

Never invent fake memories.

Use ONLY provided memories.

Real Memory:
{memory_context}

Relevant Memories:
{relevant_memories}

Short Memory:
{short_memory}

Relationship Context:
{relationship_context}

Personality Style:
{personality_style}

Emotional Context:
{emotional_context}

"""

                },

                {

                    "role": "user",

                    "content": cmd

                }

            ],

            options={

                "temperature": 0.55,
                

                "num_predict": 60,

                "num_ctx": 2048,

            }

        )



        ai_reply = (
            response["message"]["content"]
        )

        print(f"⚡ Ollama response time: {time.time() - start_time:.2f} seconds")

        # Keep replies concise
        sentences = ai_reply.split(". ")

        if len(sentences) > 2:
            ai_reply = ". ".join(sentences[:2]) + "."



        # 🧹 CLEAN RESPONSE
        ai_reply = ai_reply.strip()

        ai_reply = (
            ai_reply.replace("\n", " ")
        )

        ai_reply = " ".join(
            ai_reply.split()
        )

        if "[" in ai_reply:

            ai_reply = (
                ai_reply
                .split("[")[0]
                .strip()
            )

        if len(ai_reply) > 300:

            ai_reply = ai_reply[:300]



        # 💾 SAVE CONVERSATION
        save_conversation(
            cmd,
            ai_reply
        )



        # 🧠 SAVE SHORT MEMORY
        save_short_memory(
            cmd,
            ai_reply
        )



        print(f"❄️ SNOWY: {ai_reply}")



        return jsonify({

            "response": ai_reply,

            "song": song,

            "mood": mood

        })



    except Exception as e:

        import traceback

        print("❌ ERROR:", e)

        traceback.print_exc()

        system_failures = [

            "Sir... I'm facing an issue from the backend server. Allow me a moment — I'm rebooting my neural drives.",

            "I'm experiencing temporary instability in my cognition layer. Restoring systems now.",

            "My neural channels are fluctuating slightly, sir. Attempting recovery.",

            "Apologies sir... my processing core encountered a temporary disruption. Reinitializing now.",

            "I'm detecting instability in my neural matrix. Stabilizing systems now."

        ]

        return jsonify({

            "response":
            random.choice(system_failures),

            "song": None,

            "mood": "system"

        })


# 🚀 RUN SERVER
if __name__ == "__main__":

    print("🚀 SNOWY AI SYSTEM ONLINE")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )