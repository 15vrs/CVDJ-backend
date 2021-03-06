from flask import Flask, request
from flask import json
from flask.json import jsonify

# Calls to external services
from azure_cognitive import emotion, emotion_with_stream
import spotify.spotify as spotify

SPOTIFY = spotify
app = Flask(__name__)

# fix for CORS issue
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# BE home route.
@app.route('/')
def home_page():
    return 'CVDJ!'

# Call to Face API with image to get emotion data
@app.route("/emotion/<user_id>", methods=['POST'])
def determine_emotion(user_id):
    if (request.data):
        return emotion_with_stream(user_id, request.data)
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

# Logging a user into Spotify to obtain access to their Spotify account.
@app.route('/create_room', methods=['POST'])
def create_room():
    error = request.args.get('error')
    code = request.args.get('code')
    redirect_uri = request.data.decode('utf-8') 

    if error is not None:
        return error

    create = SPOTIFY.create_spotify_room(code, redirect_uri)
    rsp = {
        'roomId': str(create[0]),
        'userId': str(create[1]),
        'accessToken': str(create[2]),
        'playlistUri': str(create[3])
    }
    return rsp

# Adding a new user to an existing CVDJ room.
@app.route('/join_room/<room_code>', methods=['GET'])
def join_room(room_code):
    join = SPOTIFY.join_spotify_room(room_code)
    rsp = {
        'userId': str(join[0]),
        'accessToken': str(join[1]),
        'playlistUri': str(join[2])
    }
    return rsp

# Removing a user from an existing CVDJ room.
@app.route('/leave_room/<user_id>', methods=['GET'])
def leave_room(user_id):
    SPOTIFY.leave_spotify_room(user_id)
    return ''

# Add the web browser device to the users database.
@app.route('/add_device', methods=['POST'])
def add_device():
    device_id = request.json['deviceId']
    user_id = request.json['userId']
    SPOTIFY.add_spotify_device(user_id, device_id)
    return ''

# Spotify player API methods below for sync play.
@app.route('/play/<room_id>', methods=['GET'])
def room_play(room_id):
    return SPOTIFY.play_spotify_room(room_id)

@app.route('/pause/<room_id>', methods=['GET'])
def room_pause(room_id):
    return SPOTIFY.pause_spotify_room(room_id)

@app.route('/next/<room_id>', methods=['GET'])
def room_next(room_id):
    return SPOTIFY.spotify_skip_next(room_id)

@app.route('/previous/<room_id>', methods=['GET'])
def room_previous(room_id):
    return SPOTIFY.spotify_skip_previous(room_id)
