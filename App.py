from flask import Flask, request, jsonify, render_template
import requests
import os
import logging

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API Key is missing. Please set it in the environment.")

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/gpt2"
HEADERS = {"Authorization": f"Bearer {api_key}"}

# Setup logging to capture detailed errors
logging.basicConfig(level=logging.DEBUG)

def query_huggingface(payload):
    """Query the Hugging Face Inference API."""
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request failed: {str(e)}")
        return {"error": "Request failed."}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/response", methods=["POST"])
def chatbot_response():
    user_message = request.form.get("message")
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    # Query Hugging Face API
    try:
        payload = {"inputs": user_message}
        hf_response = query_huggingface(payload)
        
        if "error" in hf_response:
            app.logger.error(f"Hugging Face API returned an error: {hf_response.get('error')}")
            return jsonify({"response": "Sorry, the model is currently unavailable."})
        
        # Since the response is a list, access the first item and extract the text
        if isinstance(hf_response, list):
            answer = hf_response[0].get("generated_text", "Sorry, no response generated.")
        else:
            answer = "Sorry, no response generated."
        
        return jsonify({"response": answer})
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"response": "An error occurred. Please try again later."})


if __name__ == "__main__":
    app.run(debug=True)
