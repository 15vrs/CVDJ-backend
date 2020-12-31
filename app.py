from flask import Flask, request, redirect, make_response
import time

# Calls to external services
from spotipy.spotify import track_recommendations, login, callback
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

    access_token, refresh_token, expires_in, start_time = callback(code)
    return f'<p>Access token: {str(access_token)}</p><p>Refresh token: {str(refresh_token)}</p><p>Expires in: {str(expires_in)}</p><p>Token start time: {str(start_time)}</p>'

