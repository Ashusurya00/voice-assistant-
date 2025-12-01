🚀 JARVIS+ — Offline Voice Assistant (Python + Flask + AudioWorklet)

JARVIS+ is a fully offline, voice-controlled AI assistant inspired by Marvel’s JARVIS.
It listens to your voice, understands commands, performs tasks, and responds back with natural speech — all running locally on your machine.

This project includes a custom browser-based WAV recorder, Flask backend, real-time speech recognition, TTS engine, system automation, and a modern responsive UI.

🌟 Features
🎤 1. Real-Time Voice Recording (AudioWorklet)

Custom AudioWorkletProcessor

High-quality Float32 PCM → 16-bit WAV encoder

Works without ffmpeg or browser extensions

100% client-side recording

🧠 2. Speech Recognition (Offline Pipeline)

Uses Python’s speech_recognition library

Converts the WAV audio into text

Automatically detects errors or empty audio

🔊 3. Text-to-Speech Voice Responses

Powered by pyttsx3 (SAPI5)

Fully offline TTS

Saves output to WAV

Plays instantly in the browser

⚙️ 4. System Automation

JARVIS+ can open installed apps such as:

Google Chrome

VS Code

WhatsApp

Notepad

Calculator

🎶 5. YouTube Control

Just say:

Play Believer


And JARVIS+ opens YouTube and plays the song.

🔍 6. Smart Search

Wikipedia summaries

Weather lookups

Google search fallback

General question answering

😂 7. Fun Interaction

Random jokes

Friendly responses

Error handling

💻 8. Modern UI

Clean, responsive web interface

Log timeline

Debug panel

Audio playback & download buttons

🔒 9. Fully Offline

No cloud APIs

No external STT/TTS services

Complete privacy

🏗 Tech Stack
🚀 Frontend

HTML

CSS

JavaScript

AudioWorklet API

Fetch API

🔧 Backend

Python

Flask

SpeechRecognition

pyttsx3

pywhatkit

Wikipedia API

📁 Project Structure
jarvis-web/
│── server.py
│── jarvis.pkl            (optional data)
│── input.wav             (temp audio)
│── reply.wav             (TTS output)
│
├── templates/
│     └── index.html
│
└── static/
      └── recorderWorklet.js

▶️ How to Run the Project
1. Clone the repository
git clone https://github.com/Ashusurya00/voice-assistant-
cd JARVIS-Plus/jarvis-web

2. Create/Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install Dependencies
pip install flask flask-cors SpeechRecognition pyttsx3 pywhatkit wikipedia sounddevice soundfile

4. Run the Backend
python server.py


If successful:

🚀 Starting Jarvis+ Backend...
🌐 Open in browser: http://127.0.0.1:5000

5. Open UI

Go to:

http://127.0.0.1:5000

🎤 How to Use

Click Record

Speak your command

Click Stop

Click Send to Jarvis

Jarvis responds with:

Transcript

Voice reply

System action

🧠 Example Commands
🔹 Open Apps
Open Chrome
Open WhatsApp
Open VS Code

🔹 Ask Questions
Who is Elon Musk
What is Machine Learning
Tell me about India

🔹 YouTube Music
Play Faded
Play Believer

🔹 Weather
Weather in Mumbai

🔹 Fun
Tell me a joke

🌱 Future Enhancements

Wake-word activation (“Hey Jarvis”)

Multi-agent architecture

AI-powered reasoning (GPT / local LLM)

Vision module (Object detection)

Desktop application (PyInstaller)

Android app version

Chat history memory system
