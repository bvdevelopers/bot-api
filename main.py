from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import random
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load jokes from the JSON file
def load_jokes():
    with open('jokes.json', 'r') as file:
        jokes = json.load(file)
    return jokes

# Load jokes at the start
jokes = load_jokes()

@app.route('/ask_joke', methods=['GET'])
def ask_joke():
    joke = random.choice(jokes)  # Get a random joke from the list
    return jsonify({"question": joke["question"], "hint": joke["hint"], "answer": joke["answer"]})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data['answer']
    correct_answer = data['correct_answer']
    
    if user_answer.strip().lower() == correct_answer.strip().lower():
        return jsonify({"response": "Haha! You got it! 🎉"})
    else:
        return jsonify({"response": "Nice try! Would you like a hint?"})

if __name__ == '__main__':
    app.run(debug=True)
