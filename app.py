from flask import Flask, redirect
from datetime import datetime
import re
from spotify import search

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

# Spotify calls
@app.route("/search/<query>")
def spotify_search(query):
    return search(query)