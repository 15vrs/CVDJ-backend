from flask import Flask, request
from flask.json import jsonify

# Calls to external services
from spotify.spotify import track_recommendations, callback, new_room, join_room
from azure_cognitive import emotion, emotion_with_stream

app = Flask(__name__)

# fix for CORS issue
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/')
def home_page():
    return 'CVDJ!'

# Creating a new CVDJ room with a user that is signed into Spotify.
@app.route('/create_room/<user_id>', methods=['GET'])
def create_room(user_id):
    room = new_room(user_id)
    if room == 0:
        return "Error creating room."

    rsp = {
        'roomId': f'{room[0]}',
        'playlistUri': f'{room[1]}'
    }
    return jsonify(rsp)

@app.route('/join/<room_code>', methods=['GET'])
def user_join(room_code):
    cvdj_user_id = join_room(room_code)
    if cvdj_user_id == 0:
        return "Error creating and adding user to DB."
    
    return f'{cvdj_user_id}'

# Logging a user into Spotify to obtain access to their Spotify account.
@app.route('/callback/', methods=['GET'])
def spotify_callback():
    error = request.args.get('error')
    code = request.args.get('code')

    if error is not None:
        return error

    cvdj_user_id = callback(code)
    if cvdj_user_id == 0:
        return "Error creating and adding user to DB."
    
    return f'{cvdj_user_id}'

# Call to Face API with image to get emotion data
@app.route("/emotion", methods=['POST'])
def determine_emotion():
    if (request.data):
        return emotion_with_stream(request.data)
    return emotion('https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg')

@app.route('/emotion_with_stream')
def determine_emotion_from_stream():
    return emotion_with_stream()

# Spotify
@app.route('/spotifyrecs', methods=['POST'])
def spotify_track_recommendations_test():
    n = request.json['n']
    azure_emotion = request.json['emotion']

    # Call spotify
    tracks = track_recommendations(azure_emotion, n)

    # Format response
    rsp = [{
        'name': i['name'],
        'id': i['id'],
        'uri': i['uri']
    } for i in tracks]
    return jsonify(rsp)
