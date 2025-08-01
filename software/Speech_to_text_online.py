'''
1A - Speech to Text using Google's SpeechRecognition API
'''

import speech_recognition as sr
import pygame

pygame.mixer.init()
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)


def listen_with_google():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Checks for noise
        print("Listening ... ")
        play_sound("Resources\listen.mp3")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5) 
        play_sound("Resources\convert.mp3")
        #recognizer.adjust_for_ambient_noise(source)
        text = recognizer.recognize_google(audio)
        print("You said: "+ text)
        return text
    
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google: {e}")

##--------MAIN-----------

listen_with_google()