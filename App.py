from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Flask app
app = Flask(__name__)

# Load the Hugging Face model and tokenizer
MODEL_NAME = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['POST'])
def get_response():
    if request.method == 'POST':
        user_message = request.form.get('message', '')
        if not user_message:
            return jsonify({'response': 'Please type a message!'})

        # Generate response from model
        inputs = tokenizer.encode(user_message, return_tensors='pt')
        outputs = model.generate(inputs, max_length=150, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({'response': response})

    return jsonify({'response': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)

