import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import atexit
import os
import time
import subprocess
import wikipedia
import random
import pickle

recognizer = sr.Recognizer()

# ------------------------- SPEAK FUNCTION (FULLY STABLE) -------------------------
def speak(text):
    print("Jarvis:", text)

    # Create fresh engine (fix for silent output)
    engine = pyttsx3.init("sapi5")
    engine.setProperty('rate', 175)

    engine.say(text)
    engine.runAndWait()

    engine.stop()
    del engine
    time.sleep(0.15)


# ------------------------- RECORD AUDIO WITHOUT PYAUDIO -------------------------
def record_audio(filename="voice.wav", duration=5):
    fs = 44100
    print("\nListening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, audio, fs)
    return filename


# ------------------------- CONVERT AUDIO TO TEXT -------------------------
def listen():
    try:
        filename = record_audio()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)

        os.remove(filename)
        return text

    except Exception as e:
        print("Error:", e)
        return ""


# ------------------------- OPEN APPLICATIONS -------------------------
def open_app(app):
    apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vs code": r"C:\Users\aashutosh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "whatsapp": r"C:\Users\aashutosh\AppData\Local\WhatsApp\WhatsApp.exe"
    }

    if app in apps:
        subprocess.Popen(apps[app])
        speak(f"Opening {app}")
    else:
        speak(f"I cannot find {app} on your system.")


# ------------------------- JOKES -------------------------
def tell_joke():
    jokes = [
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "Why do Java developers wear glasses? Because they don't C sharp.",
        "I told my computer I needed a break, and it said: No problem, I will freeze.",
        "Why was the computer cold? Because it forgot to close Windows."
    ]
    speak(random.choice(jokes))


# ------------------------- WHATSAPP MESSAGE -------------------------
def send_whatsapp_message(number, message):
    try:
        speak(f"Sending WhatsApp message to {number}")
        pywhatkit.sendwhatmsg_instantly(number, message)
        speak("Message sent successfully.")
    except Exception as e:
        speak("Failed to send message.")
        print("Error:", e)


# ------------------------- MAIN JARVIS+ LOOP -------------------------
def run_jarvis():
    speak("Jarvis Plus activated. How can I assist you?")

    while True:
        command = listen()

        if command == "":
            continue

        if "jarvis" in command:
            command = command.replace("jarvis", "").strip()

        # Exit
        if any(x in command for x in ["stop", "bye", "exit"]):
            speak("Goodbye sir.")
            break

        # Open apps
        if "open" in command:
            app = command.replace("open", "").strip()
            open_app(app)

        # Play YouTube song
        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        # Time
        elif "time" in command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")

        # Wikipedia
        elif any(x in command for x in ["what is", "who is", "tell me about"]):
            topic = (
                command.replace("what is", "")
                .replace("who is", "")
                .replace("tell me about", "")
                .strip()
            )
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except:
                speak("I couldn't find information on that topic.")

        # Weather search
        elif "weather" in command:
            city = command.replace("weather in", "").replace("weather", "").strip()
            speak(f"Searching weather in {city}")
            pywhatkit.search(f"weather in {city}")

        # Joke
        elif "joke" in command:
            tell_joke()

        # WhatsApp message
        elif "send message" in command or "whatsapp" in command:
            speak("Whom do you want to message?")
            person = listen()

            speak("What is the message?")
            message = listen()

            number = "+91XXXXXXXXXX"  # Setup your own number
            send_whatsapp_message(number, message)

        # Google Search
        else:
            speak("Searching on Google")
            pywhatkit.search(command)


# ------------------------- JARVIS CLASS FOR PICKLE -------------------------
class JarvisAssistant:
    def start(self):
        run_jarvis()


# ------------------------- SAVE JARVIS AS PICKLE -------------------------
jarvis_obj = JarvisAssistant()

with open("jarvis.pkl", "wb") as f:
    pickle.dump(jarvis_obj, f)

print("JARVIS PICKLE FILE CREATED SUCCESSFULLY → jarvis.pkl")

# ------------------------- START JARVIS -------------------------
jarvis_obj.start()
