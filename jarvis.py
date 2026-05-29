import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

engine = pyttsx3.init()

# Improve voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

def ask_ai(command):
    command = command.lower()

    if ("who" in command and "you" in command) or "hu r u" in command:
        return "I’m Jarvis. Your personal assistant. Still evolving, but already smarter than most."

    elif ("how" in command and "you" in command) or "how r u" in command:
        return "Functioning perfectly. Unlike humans before coffee."

    elif "joke" in command:
        return "Why do programmers hate nature? Too many bugs."

    elif "your name" in command:
        return "Jarvis. You named me, remember?"

    elif "hello" in command or "hi" in command:
        return "Hello. What can I do for you?"

    elif "bye" in command or "see you" in command:
        return "Goodbye. I’ll be right here when you need me."

    else:
        return "I didn’t fully get that, but I’m learning fast."

wake_word = "jarvis"

while True:
    command = listen()

    # DIRECT COMMANDS (works even without wake word)
    if command:
        if "chrome" in command:
            os.system("open -a 'Google Chrome'")
            speak("Opening Chrome")

        elif "finder" in command:
            os.system("open /System/Library/CoreServices/Finder.app")
            speak("Opening Finder")

    # WAKE WORD FLOW
    if command and wake_word in command:
        speak("Yes?")

        command = listen()

        if command == "":
            speak("I didn't catch that.")
            continue

        if "exit" in command or "goodbye" in command:
            speak("Goodbye. Shutting down.")
            break

        elif "time" in command:
            time = datetime.datetime.now().strftime("%H:%M")
            speak(f"It's {time}")

        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")

        elif "spotify" in command:
            os.system("open -a Spotify")
            speak("Opening Spotify")

        elif "chrome" in command:
            os.system("open -a 'Google Chrome'")
            speak("Opening Chrome")

        elif "finder" in command:
            os.system("open /System/Library/CoreServices/Finder.app")
            speak("Opening Finder")

        elif "whatsapp" in command:
            os.system("open -a WhatsApp")
            speak("Opening WhatsApp")

        else:
            answer = ask_ai(command)
            speak(answer)