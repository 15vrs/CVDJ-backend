# Handle all calls directly from app.py.

from spotify.spotify_api import add_track_to_playlist, create_playlist, get_playlist_tracks, get_user_id
from spotify.spotify_helper import get_tokens, track_recommendations
from spotify.spotify_auth import get_access_token
from database.users import add_new_user, add_new_user_to_room, add_user_to_room, get_user_emotion
from database.creators import add_new_creator, add_creator_to_room
from database.rooms import add_new_room, add_playlist_to_room, update_room_emotion, get_playlist_from_room

# Average the room level emotion.
def update_room(room_id):

    # Get average emotion (NOT 'neutral') from all emotionData for every user in the room.
    users = get_user_emotion(room_id)
    if len(users) == 0:
        return "Room is empty."
        
    emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'sadness': 0, 'surprise': 0}
    for e in emotions:
        emotions[e] = sum([i[e] for i in users]) / len(users)

    # Update the dominant emotion in the room.
    max_emotion = max(emotions, key=emotions.get)
    update_room_emotion(max_emotion, room_id)

    # Get tokens.
    access_token = get_tokens("room", room_id)
    if access_token == 0:
        return 0

    # Call track_recommendations to get one track recommendation for the room, and add to playlist.
    playlist_id = get_playlist_from_room(room_id)[0]
    curr_tracks = get_playlist_tracks(access_token, playlist_id)
    tracks = track_recommendations(emotions, max_emotion, 1, curr_tracks)
    new_track = tracks[0]['uri']
    add_track_to_playlist(access_token, new_track, playlist_id)

    # Return the dominant emotion.
    return max_emotion

# Logging a user in.
def callback(code):
    user_id = add_new_user()
    access_token, refresh_token, start_time = get_access_token(code)
    add_new_creator(user_id, access_token, refresh_token, start_time)
    return user_id

# Joining a room.
def join_room(room_id):
    playlist_id = get_playlist_from_room(room_id)
    user_id = add_new_user_to_room(room_id)
    return user_id, playlist_id[0]

# Creating a new room.
def new_room(user_id):

    # Get tokens
    access_token = get_tokens("user", user_id)
    if access_token == 0:
        return 0

    # Create a new room and add the creator to it
    room_id = add_new_room() #DB
    if room_id is 0:
        print("Error creating room in database.")
        return 0
    add_creator_to_room(room_id, user_id)
    add_user_to_room(room_id, user_id) #DB

    # Get spotify user id and create playlist for room.
    spotify_user_id = get_user_id(access_token) #API
    playlist_id = create_playlist(access_token, spotify_user_id, room_id) #API
    add_playlist_to_room(playlist_id, room_id) #DB

    return room_id, playlist_id
