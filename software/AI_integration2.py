"""
AI-Speech Integration code:

1. Speech to Text using Faster-Whisper (offline)
2. AI response using Gemini
3. Text to Speech using pyttsx3
"""

import os
import pygame
import pyaudio
import wave
import pyttsx3
import atexit
import google.generativeai as genai
from faster_whisper import WhisperModel

# ------------------- Configuration -------------------
MODEL_NAME = "small"
AUDIO_FILE = "temp_audio.wav"
WHISPER_DURATION = 10  
VOSK_RATE = 16000
API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual Gemini API key
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LISTEN_SOUND_PATH = os.path.join(BASE_DIR, "Resources", "listen.mp3")
CONVERT_SOUND_PATH = os.path.join(BASE_DIR, "Resources", "convert.mp3")

# ------------------- Initializations -------------------
pygame.mixer.init()
genai.configure(api_key=API_KEY)
model = WhisperModel(MODEL_NAME, compute_type="int8")

# ------------------- Sound Utility -------------------
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# ------------------- Audio Recording -------------------
def record_audio(filename=AUDIO_FILE, duration=WHISPER_DURATION):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = VOSK_RATE

    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Listening...")
    play_sound(LISTEN_SOUND_PATH)

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# ------------------- Speech to Text -------------------
def listen_with_whisper():
    record_audio(AUDIO_FILE, WHISPER_DURATION)
    play_sound(CONVERT_SOUND_PATH)

    print("Transcribing...")
    segments, _ = model.transcribe(AUDIO_FILE)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    os.remove(AUDIO_FILE)
    result = full_text.strip()
    print("You said:", result)
    return result

# ------------------- Gemini API -------------------
def gemini_api(text):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        response = model.generate_content(text)
        result_text = response.text.strip() if response.text else "[Empty response]"
        print("Gemini:", result_text)
        return result_text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I'm sorry, something went wrong."

# ------------------- Text to Speech -------------------
def text_to_speech(text, voice_index=0, rate=150, volume=1.0):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_index].id)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        if 'engine' in locals():
            engine.stop()
            del engine

# ------------------- Main Loop -------------------
if __name__ == "__main__":
    print("AI Speech Assistant Started (Ctrl+C to quit)")
    try:
        while True:
            user_input = listen_with_whisper()
            ai_response = gemini_api(user_input)
            text_to_speech(ai_response)
    except KeyboardInterrupt:
        print("Exiting gracefully.")
