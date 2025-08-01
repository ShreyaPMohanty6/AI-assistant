'''
1A - Speech to Text using Faster-Whisper (Offline, Accurate)
'''

import pygame
import pyaudio
import wave
import os
from faster_whisper import WhisperModel

# Initialize pygame mixer for sound playback
pygame.mixer.init()

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

def record_audio(filename="temp_audio.wav", duration=10):  
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000  

    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Listening...")
    play_sound("Resources\listen.mp3")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording done.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def listen_with_whisper():
    audio_file = "temp_audio.wav"
    record_audio(audio_file, duration=10)  
    play_sound("Resources\convert.mp3")

    print("Transcribing...")
    model = WhisperModel("small", compute_type="int8")

    segments, info = model.transcribe(audio_file)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    print("You said:", full_text.strip())

    if os.path.exists(audio_file):
        os.remove(audio_file)

    return full_text.strip()

##--------MAIN-----------
listen_with_whisper()
