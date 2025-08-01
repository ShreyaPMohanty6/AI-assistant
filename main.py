# app.py
from flask import Flask, render_template, jsonify, request
from software.AI_integration2 import listen_with_whisper, gemini_api, text_to_speech

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    try:
        transcript = listen_with_whisper()
        response = gemini_api(transcript)
        text_to_speech(response)
        return jsonify({
            "transcribed": transcript,
            "response": response
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
