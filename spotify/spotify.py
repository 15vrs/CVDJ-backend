# Interface for spotify and database calls calls.
from spotify.users import User
from spotify.spotify_room import SpotifyRoom

# Global variables to manage objects.
SPOTIFY_ROOMS = dict() # [int, SpotifyRoom]
USERS = dict() # [int, User]

# Route: /create_room.
def create_spotify_room(code, redirect_uri):
    spotify_room = SpotifyRoom(code, redirect_uri)
    room_id = spotify_room.get_room_id()
    SPOTIFY_ROOMS[str(room_id)] = spotify_room
    print(SPOTIFY_ROOMS)

    creator = User(room_id)
    creator_id = creator.get_user_id()
    USERS[str(creator_id)] = creator
    print(USERS)

    access_token = spotify_room.get_access_token()
    playlist_id = spotify_room.get_playlist_id()
    return room_id, creator_id, access_token, playlist_id

# Route: /join_room.
def join_spotify_room(room_id):
    user = User(room_id)
    user_id = user.get_user_id()
    USERS[str(user_id)] = user

    spotify_room = SPOTIFY_ROOMS[str(room_id)]

    access_token = spotify_room.get_access_token()
    playlist_id = spotify_room.get_playlist_id()
    return user_id, access_token, playlist_id

# Route: /leave_room.
def leave_spotify_room(user_id):
    user = USERS.pop(str(user_id))
    del user

    room_id = user.get_room_id()
    spotify_room = SPOTIFY_ROOMS.pop(str(room_id))
    devices_set = spotify_room.get_spotify_devices()
    if len(devices_set) == 0:
        del spotify_room

# Route: /add_device.
def add_spotify_device(user_id, device_id):
    user = USERS[str(user_id)]
    user.set_device_id(device_id)

    room_id = user.get_room_id()
    spotify_room = SPOTIFY_ROOMS[str(room_id)]
    spotify_room.transfer(device_id)

# Route: /play_room.
def play_spotify_room(room_id):
    spotify_room = SPOTIFY_ROOMS[str(room_id)]
    return spotify_room.play()

# Route: /pause_room.
def pause_spotify_room(room_id):
    spotify_room = SPOTIFY_ROOMS[str(room_id)]
    return spotify_room.pause_room()

# Route: /skip_next.
def spotify_skip_next(room_id):
    spotify_room = SPOTIFY_ROOMS[str(room_id)]
    return spotify_room.skip_next()

# Route: /skip_previous.
def spotify_skip_previous(room_id):
    spotify_room = SPOTIFY_ROOMS[str(room_id)]
    return spotify_room.skip_previous()
        
# Update user emotion data.
def update_user_emotions(user_id, emotion_data):
    user = USERS[str(user_id)]
    user.set_emotion_data(emotion_data)
