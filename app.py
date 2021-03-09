from flask import Flask, request
from azure_cognitive import emotion, emotion_with_stream
import spotify.spotify as spotify

app = Flask(__name__)

# Fix for CORS issue.
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# Call to Face API with image to get emotion data.
@app.route("/emotion/<user_id>", methods=['POST'])
def determine_emotion(user_id):
    if (request.data):
        return emotion_with_stream(user_id, request.data)
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

## Calls to Spotify.
# Logging a user into Spotify to obtain access to their Spotify account.
@app.route('/create_room', methods=['POST'])
def create_room():
    error = request.args.get('error')
    code = request.args.get('code')
    redirect_uri = request.data.decode('utf-8')

    if error is not None:
        return error

    rsp = spotify.create_spotify_room(code, redirect_uri)
    return rsp

# Adding a new user to an existing CVDJ room.
@app.route('/join_room/<room_code>', methods=['GET'])
def join_room(room_code):
    rsp = spotify.join_spotify_room(room_code)
    return rsp

# Removing a user from an existing CVDJ room.
@app.route('/leave_room/<room_code>/<user_id>', methods=['GET'])
def leave_room(room_code, user_id):
    spotify.leave_spotify_room(room_code, user_id)
    return ''

# Add the web browser device to the users database.
@app.route('/add_device', methods=['POST'])
def add_device():
    device_id = request.json['deviceId']
    user_id = request.json['userId']
    room_id = request.json['roomId']
    spotify.add_spotify_device(room_id, user_id, device_id)
    return ''

## Player
@app.route('/play/<room_id>', methods=['GET'])
def room_play(room_id):
    rsp = spotify.play_spotify_room(room_id)
    return rsp

@app.route('/pause/<room_id>', methods=['GET'])
def room_pause(room_id):
    rsp = spotify.pause_spotify_room(room_id)
    return rsp

@app.route('/next/<room_id>', methods=['GET'])
def room_next(room_id):
    rsp = spotify.spotify_skip_next(room_id)
    return rsp

@app.route('/previous/<room_id>', methods=['GET'])
def room_previous(room_id):
    rsp = spotify.spotify_skip_previous(room_id)
    return rsp
