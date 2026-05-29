# ❤️ EMOTIONAL CHECK-IN ENGINE

def emotional_check_in(emotion_stats):

    if not emotion_stats:

        return None


    # 😔 STRESS
    if emotion_stats.get("stress", 0) >= 3:

        return (
            "You’ve seemed mentally exhausted lately. "
            "Want to slow down for a bit?"
        )


    # 😢 SAD
    if emotion_stats.get("sad", 0) >= 3:

        return (
            "You’ve sounded low recently. "
            "I’m here if you want to talk."
        )


    # ❤️ LOVE / RELATIONSHIP
    if emotion_stats.get("love", 0) >= 3:

        return (
            "You’ve been thinking deeply about someone lately."
        )


    # 😄 HAPPY
    if emotion_stats.get("happy", 0) >= 5:

        return (
            "You’ve seemed happier lately. "
            "That’s genuinely nice to see."
        )


    return None