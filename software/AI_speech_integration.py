"""
AI-Speech Integration code, that does:

    1- Speech to text conversion
    2- Generates AI model's response
    3- Converts Text to Speech

"""

# ------------------- Import Libraries -------------------
import vosk
import pyaudio
import json
import pygame
import google.generativeai as genai
import pyttsx3
import atexit
# ------------------- Global State Management -------------------
class VoskController:
    def __init__(self, model_path):
        self.model = vosk.Model(model_path)
        self.recognizer = None
        self.active = True

    def get_recognizer(self):
        if not self.active:
            raise RuntimeError("Vosk controller already closed")
        if not self.recognizer:
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        return self.recognizer

    def shutdown(self):
        if self.active:
            # Cleanup order is critical
            if self.recognizer:
                del self.recognizer
                self.recognizer = None
            del self.model
            self.active = False

# Global initialization
vosk_ctrl = VoskController("Resources/vosk-model-en-us-0.22")
atexit.register(vosk_ctrl.shutdown)

# ------------------- Initializations -------------------

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize VOSK model
model = vosk.Model("Resources/vosk-model-en-us-0.22")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Configure Gemini API with your API key
genai.configure(api_key="Gemini_API_Key")  # Replace with your actual API key


# ------------------- Utility Functions -------------------

def play_sound(file_path):
    """
    Plays an audio file using pygame.

    Args:
        file_path (str): Path to the audio file.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
        pygame.time.Clock().tick(5)

# ------------------- Speech-to-Text Function -------------------

def listen_with_vosk():
    """
    Captures audio from the microphone and converts it to text using VOSK.

    Returns:
        str: Transcribed text from speech.
    """
    mic = pyaudio.PyAudio()  # Initialize microphone
    stream = None
    try:
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()
        print("Listening ...")
        play_sound("Resources\listen.mp3")  # Play listening sound

        while True:
          data = stream.read(8192)
          if len(data) == 0:  # Skip if no audio data
            continue

          if recognizer.AcceptWaveform(data):  # Recognize speech
            play_sound("Resources\convert.mp3")  # Play conversion sound
            result = recognizer.Result()  # Get result from recognizer
            text = json.loads(result)["text"]  # Extract text
            print("You said: " + text)
            return text
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        mic.terminate()  # Critical for cleanup
    return text
# ------------------- AI Text Generation Function -------------------

def gemini_api(text):
    
    # Initialize a genAI model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

    # Generate a response based on the input text
    response = model.generate_content(text)
    print(response.text)  # Print the response
    return response.text

# ------------------- Text-to-Speech Function -------------------

def text_to_speech(text, voice_index=0, rate=150, volume=1.0):
    """Convert text to speech using a specified voice."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Set properties
        engine.setProperty('voice', voices[voice_index].id)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        # Speak and clean up
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        if 'engine' in locals():
            engine.stop()
            del engine

# ------------------- Main Loop -------------------

# Continuously listen, process, and respond
try:
    while True:
        text = listen_with_vosk()
        ai_response = gemini_api(text)
        text_to_speech(ai_response)
except KeyboardInterrupt:
    vosk_ctrl.shutdown()
    print("Clean exit")
    
