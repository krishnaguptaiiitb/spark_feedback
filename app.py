from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
feedback_collection = db[os.getenv("COLLECTION_NAME")]

@app.route('/')
def feedback_form():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    feedback = {
        "overall_experience": request.form.get('overall_experience'),
        "difficulty_level": request.form.get('difficulty_level'),
        "technical_issues": request.form.get('technical_issues'),
        "suggestions": request.form.get('suggestions'),
        "submitted_at": datetime.utcnow()
    }
    feedback_collection.insert_one(feedback)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
