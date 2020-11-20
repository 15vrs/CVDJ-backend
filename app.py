from flask import Flask, redirect, request
from datetime import datetime
import re

# Calls to external services
from spotify import search
from azure_cognitive import emotion

app = Flask(__name__)

rooms = []
user_ids = {}

@app.route("/join/<room_code>", methods=['POST'])
def user_join(room_code):
    uid = request.form.get('userId')
    rooms.append(room_code)
    user_ids[uid] = room_code
    return "You're in."

@app.route("/emotion", methods=['POST'])
def determine_emotion():
    return emotion(request.form.get('imageUrl'))

# Spotify calls
@app.route("/search/<query>")
def spotify_search(query):
    return search(query)