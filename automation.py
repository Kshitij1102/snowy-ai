import webbrowser
import datetime
import os


# 🚀 MAIN ACTION ENGINE
def run_action(command):

    command = command.lower()


    # 🎵 SPOTIFY
    if "spotify" in command:

        webbrowser.open(
            "https://open.spotify.com"
        )

        return "Opening Spotify."


    # ▶️ YOUTUBE
    elif "youtube" in command:

        webbrowser.open(
            "https://youtube.com"
        )

        return "Opening YouTube."


    # 🍔 ZOMATO
    elif "zomato" in command:

        webbrowser.open(
            "https://www.zomato.com"
        )

        return "Opening Zomato."


    # ⚡ BLINKIT
    elif "blinkit" in command:

        webbrowser.open(
            "https://blinkit.com"
        )

        return "Opening Blinkit."


    # 🎬 NETFLIX
    elif "netflix" in command:

        webbrowser.open(
            "https://netflix.com"
        )

        return "Opening Netflix."


    # 📸 INSTAGRAM
    elif "instagram" in command:

        webbrowser.open(
            "https://instagram.com"
        )

        return "Opening Instagram."


    # 🕒 TIME
    elif "time" in command:

        current_time = (
            datetime.datetime.now()
            .strftime("%I:%M %p")
        )

        return (
            f"The current time is "
            f"{current_time}"
        )


    # 💻 CHROME
    elif "chrome" in command:

        os.system(
            "open -a 'Google Chrome'"
        )

        return "Opening Chrome."


    return None