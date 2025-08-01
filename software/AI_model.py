"""
Step 2:
Text Generation using Gemini API
generate API key from: https://ai.google.dev/gemini-api/docs/api-key
"""

import google.generativeai as genai

# Configure the Gemini API with your API key.
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual Gemini API key


def gemini_api(text):
    # Initialize a genAI model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    # generate a response based on the input text.
    response = model.generate_content(text)

    print(response.text)


# -------------MAIN----------------

text = "Hi, be my personal AI robot. explain to me what an api is briefly?"
gemini_api(text)
