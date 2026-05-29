# 🧠 SHORT-TERM ACTIVE MEMORY

short_term_memory = []


# 💾 SAVE SHORT MEMORY
def save_short_memory(
    user,
    assistant
):

    global short_term_memory

    short_term_memory.append({

        "user": user,

        "assistant": assistant

    })

    # 🔥 KEEP LAST 10 EXCHANGES
    short_term_memory = (
        short_term_memory[-10:]
    )


# 🧠 GET SHORT MEMORY
def get_short_memory():

    memory_text = ""

    for convo in short_term_memory:

        memory_text += f"""

User: {convo['user']}
SNOWY: {convo['assistant']}

"""

    return memory_text