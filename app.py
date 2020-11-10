from flask import Flask, redirect
from datetime import datetime
import re
from spotify import search
from azure_cognitive import emotion

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/azure/cognitive/emotion")
def get_emotion():
    return emotion()

# Spotify calls
@app.route("/search/<query>")
def spotify_search(query):
    return search(query)