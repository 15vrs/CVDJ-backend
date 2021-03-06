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

        self.is_playing = False
        self.room_id = Room()
        creator = User(
            room_id=self.room_id
        )
        self.users = set(creator)
        return creator.get_user_id()

    # Route: /join_room
    def join_room(self, device_id):
        user = User(
            room_id=self.room_id,
            device_id=device_id
        )
        self.users.add(user)
        return user.get_user_id()

    # Route: /leave_room

    # Route: /update_room

    # Route: /play_room

    # Route: /pause_room

    # Route: /skip_next

    # Route: /skip_previous

#TODO:delete below
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

## HELPER
# VALENCE_ENERGY_THRESHOLD = 0.09

# # Params:   azure_cognitive emotion JSON for one person
# # Returns:  dominant emotion
# #           valence (0.000 to 1.000)
# #           energy (0.000 to 1.000)
# def format_emotion_data(emotion_json):

#     A = emotion_json['anger']
#     C = emotion_json['contempt']
#     D = emotion_json['disgust']
#     F = emotion_json['fear']
#     H = emotion_json['happiness']
#     SA = emotion_json['sadness']
#     SU = emotion_json['surprise']

#     # Calculate target valence
#     valence = ((H+SU) - (A+C+D+F+SA) + 1) / 2 

#     # Calculate target energy
#     energy = (5*SU + 4*A + 3*F + 2*C + 2*D + H) / 5 

#     return valence, energy

# # Params:   list of audio features objects
# #           target value type 
# #           target value
# # Returns:  None, modifies audio_features object
# def prune_audio_features(audio_features, target_type, target_value):
#     global VALENCE_ENERGY_THRESHOLD

#     # Validate inputs
#     if target_type != 'energy' and target_type != 'valence':
#         return
#     if audio_features == None:
#         return
#     if audio_features['audio_features'] == None or list(audio_features['audio_features']) == list():
#         return

#     # Prune
#     temp = [i for i in list(audio_features['audio_features']) 
#     if type(i) == type(dict()) 
#     and abs(i[target_type] - target_value) < VALENCE_ENERGY_THRESHOLD]
#     audio_features['audio_features'] = temp

# # Params:   azure_cognitive emotion JSON for one person
# #           n number of recommendations to return
# # Returns:  list of n Spotify track objects
# def track_recommendations(token, emotion_json, emotion, n, curr_playlist):

#     # Reformat emotion data into spotify-queryable quantities
#     # emotion = max(emotion_json, key=lambda x: emotion_json[x])
#     valence, energy = format_emotion_data(emotion_json)
#     tracks = []

#     # Search Spotify playlist on dominant emotion.
#     search_res = search(emotion)
#     i = 0

#     while len(tracks) < n and i < len(search_res):

#         # Get tracks from current playlist.
#         curr_id = search_res[i]
#         track_objects = get_playlist_tracks(token, curr_id)
#         ids = [i['track']['id'] for i in track_objects if i['track'] is not None]

#         # Prune recs by current tracks, so you don't have the same song twice.
#         ids = [i for i in ids if i not in curr_playlist]

#         # Get audio features for tracks
#         if len(ids) != 0:
#             audio_features = get_audio_features(ids) #API

#         # Prune audio features by target valence and energy
#         prune_audio_features(audio_features=audio_features, target_type='valence', target_value=valence)
#         prune_audio_features(audio_features=audio_features, target_type='energy', target_value=energy)

#         # Add matching track objects to tracks list
#         audio_features_objects = list(audio_features['audio_features'])
#         ids = set([i['id'] for i in audio_features_objects])
#         if len(ids) != 0:
#             tracks += [i for i in track_objects if i['track']['id'] in ids]

#         i += 1
    
#     return tracks[:n]

# # Params:   type of ID passed in
# #           value of ID (user ID or room ID)
# # Returns:  Spotify access tokeb
# def get_tokens(id_type, id):

#     # Get the user from users table.
#     spotify_tokens = None
#     if id_type == "room":
#         spotify_tokens = get_room_spotify_tokens(id) #DB
#     if id_type == "user":
#         spotify_tokens = get_user_spotify_tokens(id)
#     if spotify_tokens is None:
#         print("The user has not logged in.")
#         return 0
    
#     # Ensure tokens are up to date
#     access_token = spotify_tokens[0]
#     refresh_token = spotify_tokens[1]
#     start_time = spotify_tokens[2]
#     if access_token is None or refresh_token is None or start_time is None:
#         print("The user does not have valid spotify tokens.")
#         return 0

#     # Refresh the token if required, and update in DB.
#     if (time.time() - start_time) > 3600:
#         access_token, start_time = refresh_access_token(refresh_token) #AUTH
#         if id_type == "room":
#             update_room_spotify_tokens(access_token, start_time, id)
#         if id_type == "user":
#             update_user_spotify_tokens(access_token, start_time, id)
    
#     return access_token
    
# # Transfer...
# def transfer(id, play):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return False

#     devices = get_spotify_devices(id) #DB
#     for d in set(devices):
#         if d is not None:
#             spotify_transfer(access_token, d, play)

#     return True

# # Playback...
# def playback(id):

#     # Get tokens.
#     access_token = get_tokens("room", id) #Helper
#     if access_token == 0:
#         return None

#     # If there is no playback data, start playing from the first track in the playlist.
#     return get_playback(access_token)

# # Get required data for player from playback. Input room_id.
# def player_data(id):
#     ret = None
#     try:
#         data = playback(id)
#         album_art = data['item']['album']['images'][0]['url']
#         artist = data['item']['artists'][0]['name']
#         song = data['item']['name']
#         ret = {
#             'song': song,
#             'artist': artist,
#             'albumArt': album_art
#         }
#     finally:
#         return ret
