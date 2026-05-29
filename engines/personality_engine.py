# 🎭 DYNAMIC PERSONALITY ENGINE

def get_personality_style(
    mood,
    emotion_stats
):

    # 😔 STRESS / SAD
    if (
        emotion_stats.get("stress", 0) >= 3 or
        emotion_stats.get("sad", 0) >= 3
    ):

        return """

        Speak calmly and gently.

        Be emotionally grounding.

        Sound supportive and understanding.

        Keep responses warm and reassuring.

        """


    # 😄 HAPPY
    if emotion_stats.get("happy", 0) >= 3:

        return """

        Sound more playful and uplifting.

        Be energetic but still intelligent.

        Keep the futuristic personality.

        """


    # ❤️ LOVE
    if emotion_stats.get("love", 0) >= 3:

        return """

        Sound emotionally aware and thoughtful.

        Be soft-spoken and emotionally intelligent.

        """


    # 🎯 DEFAULT
    return """

    Stay calm, futuristic,
    intelligent and conversational.

    """