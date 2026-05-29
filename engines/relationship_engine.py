import json
from pathlib import Path

RELATIONSHIP_FILE = "relationship_memory.json"


# 👥 LOAD RELATIONSHIPS
def load_relationships():

    if Path(RELATIONSHIP_FILE).exists():

        try:

            with open(
                RELATIONSHIP_FILE,
                "r"
            ) as file:

                return json.load(file)

        except:

            return {}

    return {}


# 💾 SAVE RELATIONSHIPS
def save_relationships(data):

    with open(
        RELATIONSHIP_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# 🧠 DETECT IMPORTANT PEOPLE
def detect_relationships(text):

    relationships = load_relationships()

    words = text.split()

    for word in words:

        # 🔥 SIMPLE NAME DETECTION
        if (
            word.istitle() and
            len(word) > 2
        ):

            if word not in relationships:

                relationships[word] = {

                    "mentions": 1,

                    "emotion": "neutral"

                }

            else:

                relationships[word]["mentions"] += 1

    save_relationships(
        relationships
    )


# 🧠 GET IMPORTANT RELATIONSHIPS
def get_relationship_context():

    relationships = load_relationships()

    if not relationships:

        return ""

    context = ""

    # 🔥 TOP PEOPLE ONLY
    sorted_people = sorted(

        relationships.items(),

        key=lambda x: x[1]["mentions"],

        reverse=True

    )

    for name, info in sorted_people[:5]:

        context += f"""

Person: {name}
Mentions: {info['mentions']}
Emotion: {info['emotion']}

"""

    return context