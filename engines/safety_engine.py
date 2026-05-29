# 🚨 EMOTIONAL SAFETY ENGINE

def detect_crisis(text):

    text = text.lower()

    crisis_keywords = [

        "i want to die",
        "kill myself",
        "suicide",
        "end my life",
        "self harm",
        "no reason to live",
        "i give up",
        "i hate my life"

    ]

    for phrase in crisis_keywords:

        if phrase in text:

            return True

    return False


# ❤️ SAFE RESPONSE
def crisis_response():

    return """

    I'm really glad you told me.

    You do not have to carry this alone.

    Right now, focus only on getting through this moment.

    Please reach out to someone you trust or a mental health professional.

    You matter more than this moment feels like.

    """