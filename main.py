from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
import spacy
from pathlib import Path

model_path = Path(spacy.util.get_package_path("en_core_web_md"))  # Or use the explicit path if required
nlp = spacy.load(model_path)

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
    joke = random.choice(jokes)
    return jsonify({"question": joke["question"], "hint": joke["hint"], "answer": joke["answer"]})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = nlp(data['answer'])
    correct_answer = nlp(data['correct_answer'])
    similarity_score  = user_answer.similarity(correct_answer)
    
    if similarity_score > 0.7:
        return jsonify({"response": "Haha! You got it! 🎉"})
    else:
        return jsonify({"response": "Nice try! Would you like a hint?"})

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
