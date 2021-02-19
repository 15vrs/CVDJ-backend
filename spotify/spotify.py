# Handle all calls directly from app.py.

from spotify.spotify_api import add_track_to_playlist, create_playlist, get_devices, get_playback, get_playlist_tracks, get_user_id, spotify_pause, spotify_play
from spotify.spotify_helper import get_tokens, track_recommendations
from spotify.spotify_auth import get_access_token
from database.users import add_new_user, add_new_user_to_room, add_user_to_room, get_spotify_devices, get_user_emotion, set_user_spotify_device
from database.creators import add_new_creator, add_creator_to_room
from database.rooms import add_new_room, add_playlist_to_room, update_room_emotion, get_playlist_from_room

# Logging a user in. Return user ID (not creator ID).
def callback(code):
    user_id = add_new_user()
    access_token, refresh_token, start_time = get_access_token(code)
    add_new_creator(user_id, access_token, refresh_token, start_time)
    return user_id

# Joining a room. Return room's playlist and user ID.
def join_room(room_id):
    playlist_id = get_playlist_from_room(room_id) #DB
    user_id = add_new_user_to_room(room_id)

    # Get tokens
    access_token = get_tokens("room", room_id) #Helper
    if access_token == 0:
        return 0

    return user_id, playlist_id[0], access_token

# Creating a new room.
# Input:  Int - user ID of creator of new room.
# Output: List - room ID, playlist ID of newly created room.
def new_room(user_id):

    # Get tokens
    access_token = get_tokens("user", user_id) #Helper
    if access_token == 0:
        return 0

    # Create a new room and add the creator to it
    room_id = add_new_room() #DB
    if room_id == 0:
        print("Error creating room in database.")
        return 0
    add_creator_to_room(room_id, user_id)
    add_user_to_room(room_id, user_id) #DB

    # Get spotify user id and create playlist for room.
    spotify_user_id = get_user_id(access_token) #API
    playlist_id = create_playlist(access_token, spotify_user_id, room_id) #API
    add_playlist_to_room(playlist_id, room_id) #DB

    return room_id, playlist_id, access_token

# Average the room level emotion.
# Input:  Int - room code/ID.
# Output: String - dominant room emotion (or error message).
def update_room(room_id):

    # Get average emotion (NOT 'neutral') from all emotionData for every user in the room.
    users = get_user_emotion(room_id) #DB
    if len(users) == 0:
        return "Room is empty."
        
    emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'sadness': 0, 'surprise': 0}
    for e in emotions:
        emotions[e] = sum([i[e] for i in users]) / len(users)

    # Update the dominant emotion in the room.
    max_emotion = max(emotions, key=emotions.get)
    update_room_emotion(max_emotion, room_id) #DB

    # Get tokens.
    access_token = get_tokens("room", room_id) #Helper
    if access_token == 0:
        return "Error accessing Spotify."

    # Call track_recommendations to get one track recommendation for the room, and add to playlist.
    playlist_id = get_playlist_from_room(room_id)[0] #DB
    curr_items = get_playlist_tracks(access_token, playlist_id) #API
    curr_tracks = set([i['track']['id'] for i in curr_items if i['track'] is not None])

    tracks = track_recommendations(access_token, emotions, max_emotion, 1, curr_tracks) #Helper
    new_track = tracks[0]['track']['uri']
    add_track_to_playlist(access_token, new_track, playlist_id) #API

    # Return the dominant emotion.
    return max_emotion

# Add the device ID to the database.
def set_device(device_id, user_id):
    set_user_spotify_device(device_id, user_id)
    return ''

# Playback...
def playback(id):

    # Get tokens.
    access_token = get_tokens("room", id) #Helper
    if access_token == 0:
        return False

    # Test
    return get_playback(access_token)

# Play...
def play(id):

    # Get tokens.
    access_token = get_tokens("room", id) #Helper
    if access_token == 0:
        return False

    devices = get_spotify_devices(room_id=id)
    for d in devices:
        if d is not None:
            spotify_play(access_token, d)
    return True

# Pause...
def pause(id):

    # Get tokens.
    access_token = get_tokens("room", id) #Helper
    if access_token == 0:
        return False

    devices = get_spotify_devices(room_id=id)
    for d in devices:
        if d is not None:
            spotify_pause(access_token, d)
    return True

# Devices...
def test_devices(room_id):
    
    # Get tokens.
    access_token = get_tokens("room", room_id) #Helper
    if access_token == 0:
        return 'False'

    return get_devices(access_token)
