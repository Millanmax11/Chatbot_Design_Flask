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

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)

def query_huggingface(payload):
    """Query the Hugging Face Inference API."""
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request to Hugging Face failed: {e}")
        return {"error": "Request failed."}

@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/response", methods=["POST"])
def chatbot_response():
    """Handle the chatbot's response."""
    user_message = request.form.get("message")
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    # Query Hugging Face API
    payload = {"inputs": user_message}
    hf_response = query_huggingface(payload)

    # Log the raw response for debugging
    app.logger.debug(f"Full Hugging Face response: {hf_response}")

    # Extract response or handle errors
    if "error" in hf_response:
        app.logger.error(f"Hugging Face API returned an error: {hf_response.get('error')}")
        return jsonify({"response": "Sorry, the model is currently unavailable."})
    
    # Extract generated text
    if isinstance(hf_response, list) and len(hf_response) > 0:
        answer = hf_response[0].get("generated_text", "Sorry, no response generated.")
    else:
        answer = "Sorry, no response generated."

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
