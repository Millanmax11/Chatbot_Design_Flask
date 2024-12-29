from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "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"  # Replace with your token
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

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
        
        answer = hf_response[0]["generated_text"]
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": "An error occurred. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)
