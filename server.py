from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import base64
import os
import time
import subprocess
import random

app = Flask(__name__)
CORS(app)

recognizer = sr.Recognizer()

# ----------------------------------------------------------
# TEXT → SPEECH (Save to reply.wav)
# ----------------------------------------------------------
def synthesize_to_wav(text, out_path="reply.wav"):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 175)

    if os.path.exists(out_path):
        os.remove(out_path)

    engine.save_to_file(text, out_path)
    engine.runAndWait()
    time.sleep(0.1)

    return out_path


# ----------------------------------------------------------
# MAIN COMMAND HANDLER (BRAIN OF JARVIS+)
# ----------------------------------------------------------
def handle_command(text):
    text = (text or "").lower().strip()

    if text == "":
        return "I did not hear anything."

    # Remove wake word
    if "jarvis" in text:
        text = text.replace("jarvis", "").strip()

    # ------------------- OPEN APPLICATIONS -------------------
    if text.startswith("open"):
        appname = text.replace("open", "").strip()

        known_apps = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "google": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "vs code": r"C:\Users\aashutosh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "code": r"C:\Users\aashutosh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "whatsapp": r"C:\Users\aashutosh\AppData\Local\WhatsApp\WhatsApp.exe",
        }

        if appname in known_apps:
            try:
                subprocess.Popen(known_apps[appname])
                return f"Opening {appname}"
            except Exception as e:
                return f"Failed to open {appname}: {e}"

        return f"I cannot find {appname} on your system."

    # ------------------- PLAY YOUTUBE -------------------
    if text.startswith("play"):
        song = text.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song}"

    # ------------------- TIME -------------------
    if "time" in text:
        t = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {t}"

    # ------------------- WIKIPEDIA -------------------
    if (
        text.startswith("who is")
        or text.startswith("what is")
        or text.startswith("tell me about")
    ):
        topic = (
            text.replace("who is", "")
            .replace("what is", "")
            .replace("tell me about", "")
            .strip()
        )

        if topic == "":
            return "Please repeat the topic."

        try:
            summary = wikipedia.summary(topic, sentences=2)
            return summary
        except:
            return f"I could not find information about {topic}."

    # ------------------- WEATHER -------------------
    if "weather" in text:
        city = text.replace("weather in", "").replace("weather", "").strip()
        pywhatkit.search(f"weather in {city}")
        return f"Showing weather for {city}"

    # ------------------- JOKE -------------------
    if "joke" in text:
        jokes = [
            "Why did the computer go to therapy? It had too many tabs open.",
            "Why do Java developers wear glasses? Because they don't C sharp.",
            "I told my PC I needed a break… it froze.",
            "Why did Python live on the computer? Because it had too many bytes.",
        ]
        return random.choice(jokes)

    # ------------------- DEFAULT GOOGLE SEARCH -------------------
    pywhatkit.search(text)
    return f"Searching Google for {text}"


# ----------------------------------------------------------
# PROCESS AUDIO (CALLED BY FRONTEND)
# ----------------------------------------------------------
@app.route("/process", methods=["POST"])
def process_audio():
    if "audio_data" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    input_path = "input.wav"
    request.files["audio_data"].save(input_path)

    # Speech Recognition
    try:
        with sr.AudioFile(input_path) as src:
            audio = recognizer.record(src)
        transcript = recognizer.recognize_google(audio)
    except Exception:
        transcript = ""

    # Process command
    reply = handle_command(transcript)

    # Create TTS audio file
    output_path = synthesize_to_wav(reply)

    # Encode WAV to base64
    with open(output_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    return jsonify({
        "transcript": transcript,
        "reply": reply,
        "audio_base64": audio_b64
    })


# ----------------------------------------------------------
# HOME ROUTE (SERVES THE FRONTEND)
# ----------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------------------------------------
# START SERVER
# ----------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Starting Jarvis+ Backend...")
    print("🌐 Open in browser: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
