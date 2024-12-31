from flask import Flask, request, jsonify, render_template
import os
import logging
from models import db, Chat  # Import SQLAlchemy database and Chat model
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'  # Change to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

# Get the API key from environment variables
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API Key is missing. Please set it in the environment.")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Routes
@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/response", methods=["POST"])
def get_response():
    """Handle user messages and provide AI-generated responses."""
    try:
        data = request.get_json()  # Parse JSON data from the request
        message = data.get("message", "")

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Generate AI response using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        answer = completion.choices[0].message.content

        # Save chat to the database
        new_chat = Chat(message=message, response=answer)
        db.session.add(new_chat)
        db.session.commit()

        return jsonify({'response': answer}), 200

    except Exception as e:
        logging.error(f"Error processing response: {e}")
        return jsonify({'error': 'Something went wrong'}), 500


if __name__ == "__main__":
    app.run(debug=True)