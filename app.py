from flask import Flask, request
import time

# Calls to external services
from spotify_helper import track_recommendations
from azure_cognitive import emotion, emotion_with_stream

app = Flask(__name__)

rooms = []
user_ids = {}

@app.route("/join/<room_code>", methods=['POST'])
def user_join(room_code):
    uid = request.form.get('userId')
    rooms.append(room_code)
    user_ids[uid] = room_code
    return "You're in."

@app.route("/emotion")
def determine_emotion():
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

@app.route("/emotion_with_stream")
def determine_emotion_from_stream():
    return emotion_with_stream()

# Spotify
@app.route("/test/spotifyrecs")
def spotify_track_recommendations_test():
    start_time = time.time()

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

    tracks = track_recommendations(azure_emotion, n)

    # temporary formatting for app return
    names = f"<p>{'</p><p>'.join([i['name'] for i in tracks])}</p><p>{time.time() - start_time} seconds</p>'"
    # names = '<p>' + '</p><p>'.join([i["name"] for i in tracks]) + f'</p><p>{time.time() - start_time}</p>'
    return names