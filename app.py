from flask import Flask, redirect, request
from datetime import datetime
import re

# Calls to external services
from spotify import search, get_audio_features
from spotify_helper import format_emotion_data, prune_audio_features
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

# Spotify
@app.route("/test/spotifyrecs")
def spotify_track_recommendations_test():

    # setup temp var for number of recs
    n = 10
    # setup temp emotion test data
    azure_emotion = {
        "anger": 0.575,
        "contempt": 0,
        "disgust": 0.006,
        "fear": 0.008,
        "happiness": 0.394,
        "neutral": 0.013,
        "sadness": 0,
        "surprise": 0.004
    }

    # Reformat emotion data into spotify-queryable quantities
    emotion, valence, energy = format_emotion_data(azure_emotion)

    # Find n track recommendations
    tracks = []
    i = 0
    while len(tracks) < n and i <= 2000:

        # Search spotify tracks for dominant emotion
        search_res = search(emotion, i)
        track_objects = list(search_res["tracks"]["items"])
        ids = [i["id"] for i in track_objects]

        # Get audio features for tracks
        if ids == list():
            break
        audio_features = get_audio_features(ids)

        # Prune audio features by target valence and energy
        prune_audio_features(audio_features=audio_features, target_type='valence', target_value=valence)
        prune_audio_features(audio_features=audio_features, target_type='energy', target_value=energy)

        # Add matching track objects to tracks list
        audio_features_objects = list(audio_features['audio_features'])
        ids = set([i["id"] for i in audio_features_objects])
        tracks += [i for i in track_objects if i["id"] in ids]

        # Increment offset by 50, the max limit for spotify search results  
        i += 50
    
    # temporary formatting for app return
    names = '<p>' + '</p><p>'.join([i["name"] for i in tracks]) + '</p>'
    return names