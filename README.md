# AI Speech Assistant

A Flask-based AI Speech Assistant that enables real-time voice interaction using offline speech recognition.  The assistant records the user's voice, converts it to text, generates an intelligent response, and speaks the response back to the user.

---

## Features

- Voice input using microphone
- Offline Speech-to-Text using Faster-Whisper
- AI response generation using Google Gemini
- Offline Text-to-Speech using pyttsx3
- Audio prompts for listening and processing
- Lightweight and easy to run locally

---

## Tech Stack

### Backend
- Python
- Flask

### AI & Speech
- Faster-Whisper
- Google Gemini API
- pyttsx3

### Audio Processing
- PyAudio
- Wave
- Pygame

### Other Libraries
- Google Generative AI SDK
- Vosk (imported for future expansion) for offline speech to text 

---


## Workflow

1. User clicks **Start** on the web interface.
2. Audio is recorded from the microphone.
3. A listening sound is played.
4. Faster-Whisper transcribes the recorded speech into text.
5. The transcribed text is sent to the Gemini API.
6. Gemini generates an AI response.
7. The response is converted into speech using pyttsx3.
8. The generated response is displayed on the webpage and spoken aloud.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI-Speech-Assistant
```

Install the required dependencies:

```bash
pip install flask
pip install faster-whisper
pip install google-generativeai
pip install pyttsx3
pip install pygame
pip install pyaudio
pip install vosk
```

---

## Configuration

Before running the project, configure your Gemini API key in the integration file:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

or

```bash
python3 app.py
```

The application will start locally at:

```
http://127.0.0.1:5000
```

## License

This project is intended for educational and research purposes.