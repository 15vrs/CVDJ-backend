# # Handle all calls directly from app.py.
# from typing import Dict
from database.users import User
from spotify.spotify_room import SpotifyRoom

# Global variables to manage objects.
SPOTIFY_ROOMS = dict() #[int, SpotifyRoom])
USERS = dict() #[int, User])

# Route: /create_room.
def create_spotify_room(code, redirect_uri):
    spotify_room = SpotifyRoom(code, redirect_uri)
    room_id = spotify_room.get_room_id()
    SPOTIFY_ROOMS[room_id] = spotify_room

    creator = User(room_id)
    creator_id = creator.get_user_id()
    USERS[creator_id] = creator

    access_token = spotify_room.get_access_token()
    return room_id, creator_id, access_token

# Route: /join_room.
def join_spotify_room(room_id):
    user = User(room_id)
    user_id = user.get_user_id()
    USERS[user_id] = user

    spotify_room = SPOTIFY_ROOMS[room_id]

    access_token = spotify_room.get_access_token()
    return user_id, access_token

# Route: /leave_room.
def leave_spotify_room(user_id):
    del USERS[user_id]

# Route: /add_device.
def add_spotify_device(user_id, device_id):
    user = USERS[user_id]
    user.set_device_id(device_id)

    room_id = user.get_room_id()
    spotify_room = SPOTIFY_ROOMS[room_id]
    spotify_room.transfer(device_id)

# Route: /update_room.
def update_room():
    return ''

# Route: /play_room.
def play_spotify_room(room_id):
    spotify_room = SPOTIFY_ROOMS[room_id]
    spotify_room.play()

# Route: /pause_room.
def pause_spotify_room(room_id):
    spotify_room = SPOTIFY_ROOMS[room_id]
    spotify_room.pause_room()

# Route: /skip_next.
def spotify_skip_next(room_id):
    spotify_room = SPOTIFY_ROOMS[room_id]
    spotify_room.skip_next()

# Route: /skip_previous.
def spotify_skip_previous(room_id):
    spotify_room = SPOTIFY_ROOMS[room_id]
    spotify_room.skip_previous()
        
# Update user emotion data.
def update_user_emotions(user_id, emotion_data):
    user = USERS[user_id]
    user.set_emotion_data(emotion_data)
