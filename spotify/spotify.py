# Handle all calls directly from app.py.
from spotify.spotify_api import SpotifyApi
from database.rooms import Room
from database.users import User

class Spotify:

    # Route: /create_room
    def __init__(self, code, redirect_uri):
        self.spotify_api = SpotifyApi(
            code=code,
            redirect_uri=redirect_uri
        )
        self.room_id = Room()
        self.is_playing = False
        
        creator_id = User(
            room_id=self.room_id
        )
        return creator_id

    # Route: /join_room
    def join_room(self, device_id):
        user_id = User(
            room_id=self.room_id,
            device_id=device_id
        )
        return user_id

    # Route: /update_room

    # Route: /play_room

    # Route: /pause_room

    # Route: /skip_next

    # Route: /skip_previous

# from spotify.spotify_api import add_track_to_playlist, get_playlist_tracks, get_user_id, spotify_next, spotify_pause, spotify_play, spotify_previous
# from spotify.spotify_helper import get_tokens, playback, player_data, track_recommendations
# from database.users import add_new_user, add_new_user_to_room, add_user_to_room, get_spotify_devices, get_user_emotion, set_user_spotify_device
# from database.creators import add_new_creator, add_creator_to_room
# from database.rooms import Room, add_new_room, add_playlist_to_room, update_room_emotion, get_playlist_from_room

# # Average the room level emotion.
# # Input:  Int - room code/ID.
# # Output: String - dominant room emotion (or error message).
# def update_room(room_id):

#     # Get average emotion (NOT 'neutral') from all emotionData for every user in the room.
#     users = get_user_emotion(room_id) #DB
#     if len(users) == 0:
#         return "Room is empty."
        
#     emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral':0, 'sadness': 0, 'surprise': 0}
#     for e in emotions:
#         emotions[e] = sum([i[e] for i in users]) / len(users)

#     # Update the dominant emotion in the room.
#     max_emotion = max(emotions, key=emotions.get)
#     update_room_emotion(max_emotion, room_id) #DB

#     # Get tokens.
#     access_token = get_tokens("room", room_id) #Helper
#     if access_token == 0:
#         return "Error accessing Spotify."

#     # Call track_recommendations to get one track recommendation for the room, and add to playlist.
#     playlist_id = get_playlist_from_room(room_id)[0] #DB
#     curr_items = get_playlist_tracks(access_token, playlist_id) #API
#     curr_tracks = set([i['track']['id'] for i in curr_items if i['track'] is not None])

#     tracks = track_recommendations(access_token, emotions, max_emotion, 1, curr_tracks) #Helper
#     if tracks is None:
#         return "No tracks match input valence and energy."
#     new_track = tracks[0]['track']['uri']
#     add_track_to_playlist(access_token, new_track, playlist_id) #API

#     # Return the dominant emotion.
#     return max_emotion

# # Add the device ID to the database.
# def set_device(device_id, user_id):
#     set_user_spotify_device(device_id, user_id)
#     return ''

# ## Handle synchronous play calls from FE.
# # Play...
# def play(id):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return None

#     # Get playlist URI
#     playlist_id = get_playlist_from_room(id)[0]
#     uri = f'spotify:playlist:{playlist_id}'
#     position = 0

#     # Get playback
#     data = playback(id)
#     if data is not None and 'context' in data:
#         curr_uri = data['context']['uri']
#         if curr_uri == uri:
#             uri = None
#             position = None

#     # Call play from Spotify
#     devices = get_spotify_devices(room_id=id)
#     for d in set(devices):
#         if d is not None:
#             spotify_play(access_token, d, uri, position)

#     # Get album art
#     art = player_data(id)
#     return art

# # Pause...
# def pause(id):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return None

#     devices = get_spotify_devices(room_id=id)
#     for d in set(devices):
#         if d is not None:
#             spotify_pause(access_token, d)

#     # Get album art
#     art = player_data(id)
#     return art

# # Next...
# def skip(id):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return None

#     devices = get_spotify_devices(room_id=id)
#     for d in set(devices):
#         if d is not None:
#             spotify_next(access_token, d)

#     # Get album art
#     art = player_data(id)
#     return art

# # Previous
# def previous(id):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return None

#     devices = get_spotify_devices(room_id=id)
#     for d in set(devices):
#         if d is not None:
#             spotify_previous(access_token, d)

#     # Get album art
#     art = player_data(id)
#     return art