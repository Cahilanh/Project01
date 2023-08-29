import os
from os.path import join,dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("mongodb+srv://test:sparta@cluster1.z20fjyy.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("dbsparta")

client = MongoClient (MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list (db.diary.find({}, {"_id": False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_recieve = request.form['title_give']
    content_recieve = request.form['content_give']
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)
    
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)
    
    doc = {
      'file': filename,
      'profile': profilename,
      'title': title_recieve,
      'content': content_recieve,
      'time': today.strftime('%Y-%m-%d-%H-%M-%S')
    }  
    db.diary.insert_one(doc)
    
    return jsonify({'message':'Upload complete'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)