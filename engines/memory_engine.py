import json
from pathlib import Path

MEMORY_FILE = "conversation_memory.json"


# 🧠 LOAD MEMORIES
def load_conversations():

    if Path(MEMORY_FILE).exists():

        try:

            with open(MEMORY_FILE, "r") as file:

                return json.load(file)

        except:

            return []

    return []


# 🎭 DETECT EMOTION
def detect_emotion(text):

    text = text.lower()

    emotional_keywords = {

        "sad": [
            "sad",
            "lonely",
            "hurt",
            "depressed",
            "cry",
            "broken"
        ],

        "stress": [
            "stress",
            "anxiety",
            "overthink",
            "pressure",
            "tired"
        ],

        "happy": [
            "happy",
            "excited",
            "great",
            "amazing"
        ],

        "love": [
            "love",
            "relationship",
            "miss",
            "care"
        ]

    }

    for emotion, words in emotional_keywords.items():

        for word in words:

            if word in text:

                return emotion

    return "neutral"


# ⭐ IMPORTANCE SCORE
def calculate_importance(text):

    text = text.lower()

    important_words = [

        "sad",
        "lonely",
        "love",
        "hurt",
        "dream",
        "future",
        "fear",
        "relationship",
        "anxiety",
        "overthink",
        "stress"

    ]

    score = 1

    for word in important_words:

        if word in text:

            score += 2

    return min(score, 10)


# 💾 SAVE MEMORY
def save_conversation(user, assistant):

    conversations = load_conversations()

    emotion = detect_emotion(user)

    importance = calculate_importance(user)

    conversations.append({

        "user": user,

        "assistant": assistant,

        "emotion": emotion,

        "importance": importance

    })

    # 🔥 SORT BY IMPORTANCE
    conversations = sorted(

        conversations,

        key=lambda x: x["importance"],

        reverse=True

    )

    # 🔥 KEEP BEST MEMORIES
    conversations = conversations[:40]

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            conversations,
            file,
            indent=4
        )


# 🧠 GET RELEVANT MEMORIES
def get_relevant_memories(query):

    conversations = load_conversations()

    if not conversations:

        return ""

    query = query.lower()

    scored_memories = []

    for convo in conversations:

        score = 0

        # 🔥 EMOTION MATCH
        if convo["emotion"] in query:

            score += 4

        # 🔥 KEYWORD MATCH
        for word in query.split():

            if word in convo["user"].lower():

                score += 1

        # 🔥 IMPORTANCE BONUS
        score += convo["importance"]

        scored_memories.append(
            (score, convo)
        )

    # 🔥 SORT BEST MATCHES
    scored_memories.sort(

        reverse=True,

        key=lambda x: x[0]

    )

    memory_text = ""

    # 🔥 TOP MEMORIES ONLY
    for score, convo in scored_memories[:5]:

        memory_text += f"""

User: {convo['user']}
SNOWY: {convo['assistant']}
Emotion: {convo['emotion']}
Importance: {convo['importance']}

"""

    return memory_text


# 📊 EMOTION PATTERN ANALYSIS
def analyze_emotions():

    conversations = load_conversations()

    emotion_count = {}

    for convo in conversations:

        emotion = convo.get(
            "emotion",
            "neutral"
        )

        if emotion not in emotion_count:

            emotion_count[emotion] = 0

        emotion_count[emotion] += 1

    return emotion_count