import gradio as gr
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import numpy as np
import os
import time

recognizer = sr.Recognizer()


# ------------------ SPEAK ------------------
def speak(text):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine
    time.sleep(0.1)


# ------------------ PROCESS AUDIO (FIX) ------------------
def save_audio_fix(audio, filename="mic.wav"):

    # Convert stereo -> mono
    if len(audio.shape) == 2:
        audio = np.mean(audio, axis=1)

    # Ensure float32 format
    audio = audio.astype(np.float32)

    sf.write(filename, audio, 44100)

    return filename


# ------------------ SPEECH TO TEXT ------------------
def speech_to_text(file="mic.wav"):
    try:
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio).lower()
        return text
    except:
        return ""


# ------------------ HANDLE COMMAND ------------------
def handle_command(cmd):
    if cmd == "":
        reply = "I could not hear anything."
        speak(reply)
        return reply

    if "time" in cmd:
        t = datetime.datetime.now().strftime("%I:%M %p")
        reply = f"The time is {t}"
        speak(reply)
        return reply

    if "play" in cmd:
        song = cmd.replace("play", "").strip()
        reply = f"Playing {song}"
        speak(reply)
        pywhatkit.playonyt(song)
        return reply

    if "what is" in cmd or "who is" in cmd:
        topic = cmd.replace("what is", "").replace("who is", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
            return summary
        except:
            reply = "I couldn't find information."
            speak(reply)
            return reply

    if "weather" in cmd:
        city = cmd.replace("weather", "").strip()
        reply = f"Showing weather for {city}"
        speak(reply)
        pywhatkit.search(f"weather in {city}")
        return reply

    reply = f"Searching Google for {cmd}"
    speak(reply)
    pywhatkit.search(cmd)
    return reply


# ------------------ MAIN PIPELINE ------------------
def jarvis_pipeline(audio):

    # FIX the audio first
    filename = save_audio_fix(audio)

    # Convert to text
    text = speech_to_text(filename)

    # Process command
    reply = handle_command(text)

    return text, reply


# ------------------ BUILD GRADIO UI ------------------
def start_ui():
    with gr.Blocks() as app:

        gr.Markdown(
            "<h1 style='text-align:center;color:#00eaff;'>🤖 JARVIS+ (Voice Assistant)</h1>"
        )

        mic = gr.Audio(sources=["microphone"], type="numpy", label="🎤 Speak Here")

        user_text = gr.Textbox(label="🗣 You said")
        bot_reply = gr.Textbox(label="🤖 Jarvis reply")

        mic.change(jarvis_pipeline, inputs=mic, outputs=[user_text, bot_reply])

    return app


app = start_ui()
app.launch()
