# Miscellaneous helper functions for Spotify related code.

# Global variables
from database.users import get_spotify_devices
import time
from spotify.spotify_auth import refresh_access_token
from database.creators import get_room_spotify_tokens, get_user_spotify_tokens, update_room_spotify_tokens, update_user_spotify_tokens
from spotify.spotify_api import get_audio_features, get_playback, get_playlist_tracks, search, spotify_transfer

VALENCE_ENERGY_THRESHOLD = 0.09

# Params:   azure_cognitive emotion JSON for one person
# Returns:  dominant emotion
#           valence (0.000 to 1.000)
#           energy (0.000 to 1.000)
def format_emotion_data(emotion_json):

    A = emotion_json['anger']
    C = emotion_json['contempt']
    D = emotion_json['disgust']
    F = emotion_json['fear']
    H = emotion_json['happiness']
    SA = emotion_json['sadness']
    SU = emotion_json['surprise']

    # Calculate target valence
    valence = ((H+SU) - (A+C+D+F+SA) + 1) / 2 

    # Calculate target energy
    energy = (5*SU + 4*A + 3*F + 2*C + 2*D + H) / 5 

    return valence, energy

# Params:   list of audio features objects
#           target value type 
#           target value
# Returns:  None, modifies audio_features object
def prune_audio_features(audio_features, target_type, target_value):
    global VALENCE_ENERGY_THRESHOLD

    # Validate inputs
    if target_type != 'energy' and target_type != 'valence':
        return
    if audio_features == None:
        return
    if audio_features['audio_features'] == None or list(audio_features['audio_features']) == list():
        return

    # Prune
    temp = [i for i in list(audio_features['audio_features']) 
    if type(i) == type(dict()) 
    and abs(i[target_type] - target_value) < VALENCE_ENERGY_THRESHOLD]
    audio_features['audio_features'] = temp

# Params:   azure_cognitive emotion JSON for one person
#           n number of recommendations to return
# Returns:  list of n Spotify track objects
def track_recommendations(token, emotion_json, emotion, n, curr_playlist):

    # Reformat emotion data into spotify-queryable quantities
    # emotion = max(emotion_json, key=lambda x: emotion_json[x])
    valence, energy = format_emotion_data(emotion_json)
    tracks = []

    # Search Spotify playlist on dominant emotion.
    search_res = search(emotion)
    i = 0

    while len(tracks) < n and i < len(search_res):

        # Get tracks from current playlist.
        curr_id = search_res[i]
        track_objects = get_playlist_tracks(token, curr_id)
        ids = [i['track']['id'] for i in track_objects if i['track'] is not None]

        # Prune recs by current tracks, so you don't have the same song twice.
        ids = [i for i in ids if i not in curr_playlist]

        # Get audio features for tracks
        audio_features = get_audio_features(ids) #API

        # Prune audio features by target valence and energy
        prune_audio_features(audio_features=audio_features, target_type='valence', target_value=valence)
        prune_audio_features(audio_features=audio_features, target_type='energy', target_value=energy)

        # Add matching track objects to tracks list
        audio_features_objects = list(audio_features['audio_features'])
        ids = set([i['id'] for i in audio_features_objects])
        if ids == set():
            return None
        tracks += [i for i in track_objects if i['track']['id'] in ids]

        i += 1
    
    return tracks[:n]

# Params:   type of ID passed in
#           value of ID (user ID or room ID)
# Returns:  Spotify access tokeb
def get_tokens(id_type, id):

    # Get the user from users table.
    spotify_tokens = None
    if id_type == "room":
        spotify_tokens = get_room_spotify_tokens(id) #DB
    if id_type == "user":
        spotify_tokens = get_user_spotify_tokens(id)
    if spotify_tokens is None:
        print("The user has not logged in.")
        return 0
    
    # Ensure tokens are up to date
    access_token = spotify_tokens[0]
    refresh_token = spotify_tokens[1]
    start_time = spotify_tokens[2]
    if access_token is None or refresh_token is None or start_time is None:
        print("The user does not have valid spotify tokens.")
        return 0

    # Refresh the token if required, and update in DB.
    if (time.time() - start_time) > 3600:
        access_token, start_time = refresh_access_token(refresh_token) #AUTH
        if id_type == "room":
            update_room_spotify_tokens(access_token, start_time, id)
        if id_type == "user":
            update_user_spotify_tokens(access_token, start_time, id)
    
    return access_token
    
# Transfer...
def transfer(id, play):

    # Get tokens.
    access_token = get_tokens("room", id) #Helper
    if access_token == 0:
        return False

    devices = get_spotify_devices(id) #DB
    for d in set(devices):
        if d is not None:
            spotify_transfer(access_token, d, play)

    return True

# Playback...
def playback(id):

    # Get tokens.
    access_token = get_tokens("room", id) #Helper
    if access_token == 0:
        return None

    # If there is no playback data, start playing from the first track in the playlist.
    return get_playback(access_token)

# Get required data for player from playback. Input room_id.
def player_data(id):
    ret = None
    try:
        data = playback(id)
        album_art = data['item']['album']['images'][0]['url']
        artist = data['item']['artists'][0]['name']
        song = data['item']['name']
        ret = {
            'song': song,
            'artist': artist,
            'albumArt': album_art
        }
    finally:
        return ret
