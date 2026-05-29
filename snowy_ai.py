import ollama
import json
from pathlib import Path

MEMORY_FILE = "memory.json"


# 🧠 LOAD MEMORY
def load_memory():

    if Path(MEMORY_FILE).exists():

        with open(MEMORY_FILE, "r") as file:

            return json.load(file)

    return {

        "favorite_artist": "Unknown",
        "favorite_food": "Unknown",
        "hobbies": [],
        "mood_history": []

    }


# 💾 SAVE MEMORY
def save_memory():

    with open(MEMORY_FILE, "w") as file:

        json.dump(memory, file, indent=4)


memory = load_memory()


# 🚀 BUILD MEMORY CONTEXT
def build_memory_context():

    return f"""

    Kshitij's Personal Memory:

    Favorite Artist:
    {memory.get('favorite_artist')}

    Favorite Food:
    {memory.get('favorite_food')}

    Hobbies:
    {', '.join(memory.get('hobbies', []))}

    Mood History:
    {', '.join(memory.get('mood_history', []))}

    """


print("🚀 SNOWY AI ONLINE")
print("Type 'exit' to quit.\n")


conversation = [

    {

        "role": "system",

        "content":

        f"""
        You are SNOWY.

        SNOWY means:
        Smart Neural Operating Web Yield.

        You are Kshitij's personal AI assistant.

        Personality:
        - calm
        - intelligent
        - futuristic
        - emotionally aware
        - cinematic
        - slightly witty
        - loyal to Kshitij

        IMPORTANT RULES:

        - Use ONLY real memory.
        - Never invent fake facts.
        - Be concise.
        - Speak naturally.
        - Behave like a premium futuristic AI.

        Real Memory:

        {build_memory_context()}
        """
    }

]


while True:

    user_input = input("YOU: ")

    if user_input.lower() == "exit":
        break


    # 🧠 AUTO MEMORY LEARNING

    # 🎵 FAVORITE ARTIST
    if "my favorite artist is" in user_input.lower():

        artist = user_input.lower().split(
            "my favorite artist is"
        )[-1].strip()

        memory["favorite_artist"] = artist

        save_memory()

        print("\n🧠 SNOWY learned favorite artist.\n")


    # 🍔 FAVORITE FOOD
    if "my favorite food is" in user_input.lower():

        food = user_input.lower().split(
            "my favorite food is"
        )[-1].strip()

        memory["favorite_food"] = food

        save_memory()

        print("\n🧠 SNOWY learned favorite food.\n")


    # 🎸 HOBBIES
    if "my hobby is" in user_input.lower():

        hobby = user_input.lower().split(
            "my hobby is"
        )[-1].strip()

        if hobby not in memory["hobbies"]:

            memory["hobbies"].append(hobby)

            save_memory()

        print("\n🧠 SNOWY learned new hobby.\n")


    # 😊 MOOD DETECTION
    sad_words = [
        "sad",
        "depressed",
        "upset",
        "hurt"
    ]

    happy_words = [
        "happy",
        "excited",
        "great"
    ]

    focus_words = [
        "focused",
        "studying",
        "working"
    ]


    if any(word in user_input.lower() for word in sad_words):

        memory["mood_history"].append("sad")

        save_memory()


    elif any(word in user_input.lower() for word in happy_words):

        memory["mood_history"].append("happy")

        save_memory()


    elif any(word in user_input.lower() for word in focus_words):

        memory["mood_history"].append("focused")

        save_memory()


    # 🚀 REFRESH MEMORY CONTEXT
    updated_memory = build_memory_context()


    # 💬 ADD USER MESSAGE
    conversation.append({

        "role": "user",
        "content": user_input

    })


    # 🤖 AI RESPONSE
    response = ollama.chat(

        model="llama3",

        messages=[

            {

                "role": "system",

                "content":

                f"""
                You are SNOWY.

                You are Kshitij's personal AI assistant.

                Personality:
                - calm
                - intelligent
                - futuristic
                - emotionally aware
                - cinematic
                - slightly witty
                - loyal to Kshitij

                IMPORTANT:
                Use ONLY real memory.

                Never invent fake facts.

                Real Memory:

                {updated_memory}
                """
            }

        ] + conversation

    )


    snowy_reply = response["message"]["content"]


    print("\nSNOWY:", snowy_reply, "\n")


    # 💬 SAVE AI RESPONSE
    conversation.append({

        "role": "assistant",
        "content": snowy_reply

    })