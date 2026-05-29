# 🤖 AGENTIC TASK ENGINE

def detect_order_intent(cmd):

    cmd = cmd.lower()

    food_keywords = [

        "coke",
        "chips",
        "ice cream",
        "burger",
        "pizza",
        "chocolate",
        "cold drink"

    ]

    order_words = [

        "order",
        "buy",
        "get",
        "bring",
        "place order"

    ]

    found_items = []

    # 🔥 DETECT ITEMS
    for item in food_keywords:

        if item in cmd:

            found_items.append(item)

    # 🔥 DETECT ORDER INTENT
    if any(word in cmd for word in order_words):

        if found_items:

            return {

                "intent": "order_food",

                "items": found_items

            }

    return None


# 🛒 BLINKIT SIMULATION
def simulate_blinkit_order(items):

    item_text = ", ".join(items)

    return f"""

    On it, sir.

    Preparing your Blinkit cart with:
    {item_text}

    Awaiting final payment authorization.

    """