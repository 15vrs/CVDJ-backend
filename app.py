from flask import Flask, request, redirect, make_response
import time

from flask.json import jsonify

# Calls to external services
from spotipy.spotify import track_recommendations, login, callback, create_room
from azure_cognitive import emotion

app = Flask(__name__)

rooms = []
user_ids = {}

@app.route("/")
def home_page():
    return "CVDJ!"

@app.route("/join/<room_code>", methods=['POST'])
def user_join(room_code):
    uid = request.form.get('userId')
    rooms.append(room_code)
    user_ids[uid] = room_code
    return "You're in."

@app.route("/emotion")
def determine_emotion():
    # visit https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg to see image
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

## Calls to spotify code
@app.route("/test/spotifyrecs")
def spotify_track_recommendations_test():
    start_time = time.time()

    # TEMP: setup vars for number of recs and emotion test data
    n = 10
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

    # Call spotify
    tracks = track_recommendations(azure_emotion, n)

    # TEMP: temporary formatting for app return
    names = f"<p>{'</p><p>'.join([i['name'] for i in tracks])}</p><p>{time.time() - start_time} seconds</p>'"
    return names

# Create Room forces spotify premium user to log in.
@app.route("/create_room")
def spotify_login():
    url, cookies = login()

    res = make_response(redirect(url))
    res.set_cookie('spotify_auth_state', cookies)

    return res
@app.route("/callback/")
def spotify_callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = request.cookies.get('spotify_auth_state')

    if error is not None:
        return "Sign-in error"

    if state is None or state != stored_state:
        return "State mismatch error"

    # If there is no sign in error, create and return a new room.
    access_token, refresh_token, start_time = callback(code)
    out = create_room(access_token, refresh_token, start_time)
    
    return jsonify(
        room_code = out.room_number,
        access_token = out.access_token,
        refresh_token = out.refresh_token,
        start_time = out.start_time,
        playlist_uri = out.playlist_uri
    )

