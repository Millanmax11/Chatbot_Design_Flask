from flask import Flask, request, jsonify, render_template
import requests
import os

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API Key is missing. Please set it in the environment.")

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/gpt2"
HEADERS = {"Authorization": f"Bearer {api_key}"}

def query_huggingface(payload):
    """Query the Hugging Face Inference API."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

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
            return jsonify({"response": "Sorry, the model is currently unavailable."})
        
        # Extract the generated text
        answer = hf_response.get("generated_text", "Sorry, no response generated.")
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": "An error occurred. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)
