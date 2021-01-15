from flask import Flask, request, redirect, make_response
import time

from flask.json import jsonify

# Calls to external services
from spotipy.spotify import track_recommendations, login, callback, new_room
from azure_cognitive import emotion

app = Flask(__name__)

rooms = []
user_ids = {}

# fix for CORS issue
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/")
def home_page():
    return "CVDJ!"

@app.route("/join/<room_code>", methods=['POST'])
def user_join(room_code):
    uid = request.form.get('userId')
    rooms.append(room_code)
    user_ids[uid] = room_code
    return "You're in."

# Creating a new CVDJ room with a user that is signed into Spotify.
@app.route("/create_room/<user_id>")
def create_room(user_id):
    rsp = new_room(user_id)
    if rsp is 0:
        return "Error creating room."
    return f"{rsp[0]}, {rsp[1]}"

# Logging a user into Spotify to obtain access to their Spotify account.
@app.route("/login")
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
        return error

    if state is None or state != stored_state:
        return "State mismatch error"

    cvdj_user_id = callback(code)
    if cvdj_user_id is 0:
        return "Error creating and adding user to DB."
    
    return f"{cvdj_user_id}"

# Call to Face API for emotion (test).
@app.route("/emotion")
def determine_emotion():
    # visit https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg to see image
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

# Calls to spotify code (test).
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