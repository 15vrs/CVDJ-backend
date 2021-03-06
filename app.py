from flask import Flask, request
from flask import json
from flask.json import jsonify

# Calls to external services
from azure_cognitive import emotion, emotion_with_stream

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

# Logging a user into Spotify to obtain access to their Spotify account.
@app.route('/create_room/', methods=['POST'])
def spotify_callback():
    error = request.args.get('error')
    code = request.args.get('code')
    redirect_uri = request.data.decode('utf-8') 

    if error is not None:
        return error

    cvdj_user_id = callback(code, redirect_uri)
    if cvdj_user_id == 0:
        return "Error creating and adding user to DB."
    # rsp = {
    #     'userId'
    #     'roomId': f'{room[0]}',
    #     'playlistUri': f'{room[1]}',
    #     'accessToken': f'{room[2]}'
    # }
    return f'{cvdj_user_id}'

# Adding a new user to an existing CVDJ room.
@app.route('/join/<room_code>', methods=['GET'])
def user_join(room_code):
    join = join_room(room_code)
    cvdj_user_id = join[0]
    playlistUri = join[1]
    if cvdj_user_id == 0:
        return "Error creating and adding user to DB."
    
    rsp = {
        'userId': f'{cvdj_user_id}',
        'playlistUri': f'{playlistUri}',
        'accessToken': f'{join[2]}'
    }
    return rsp

# Add the web browser device to the users database.
@app.route('/add_device', methods=['POST'])
def add_device():
    device_id = request.json['deviceId']
    user_id = request.json['userId']
    room_id = request.json['roomId']
    rsp = set_device(device_id, user_id)

    playback_data = playback(room_id)
    is_playing = False
    if playback_data is not None:
        is_playing = playback_data['is_playing']
    
    transfer(room_id, is_playing)

    return rsp

# Call to Face API with image to get emotion data
@app.route("/emotion/<user_id>", methods=['POST'])
def determine_emotion(user_id):
    if (request.data):
        return emotion_with_stream(user_id, request.data)
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

# Update the room level emotion, and the playlist.
@app.route('/update_room/<room_id>', methods=['GET'])
def room_emotion(room_id):
    return update_room(room_id)

# Spotify player API methods below for sync play.
@app.route('/play/<room_id>', methods=['GET'])
def room_play(room_id):
    rsp = play(room_id)
    return jsonify(rsp)

@app.route('/pause/<room_id>', methods=['GET'])
def room_pause(room_id):
    rsp = pause(room_id)
    return jsonify(rsp)

@app.route('/next/<room_id>', methods=['GET'])
def room_next(room_id):
    rsp = skip(room_id)
    return jsonify(rsp)

@app.route('/previous/<room_id>', methods=['GET'])
def room_previous(room_id):
    rsp = previous(room_id)
    return jsonify(rsp)
