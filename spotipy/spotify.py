# Handle all calls directly from app.py.

import time
from spotipy.spotify_api import create_playlist, get_user_id, search, get_audio_features
from spotipy.spotify_helper import format_emotion_data, prune_audio_features
from spotipy.spotify_auth import get_access_token, refresh_access_token
from database.users import add_new_user, add_user_to_room, get_user_spotify_tokens, update_spotify_tokens
from database.rooms import add_new_room, add_playlist_to_room

# Params:   azure_cognitive emotion JSON for one person
#           n number of recommendations to return
# Returns:  list of n Spotify track objects
def track_recommendations(emotion_json, n):

    # Validate inputs
    if int(sum(emotion_json[i] for i in emotion_json.keys())) != 1:
        print("Inputs to track_recommendations are not valid.")
        return

    # Reformat emotion data into spotify-queryable quantities
    emotion = max(emotion_json, key=lambda x: emotion_json[x])
    valence, energy = format_emotion_data(emotion_json)

    # Find n track recommendations
    tracks = []
    i = 0
    while len(tracks) < n and i <= 2000:

        # Search spotify tracks for dominant emotion
        search_res = search(emotion, i)
        track_objects = list(search_res["tracks"]["items"])
        ids = [i["id"] for i in track_objects]

        # Get audio features for tracks
        if ids == list():
            print("No tracks match input valence and energy.")
            break
        audio_features = get_audio_features(ids)

        # Prune audio features by target valence and energy
        prune_audio_features(audio_features=audio_features, target_type='valence', target_value=valence)
        prune_audio_features(audio_features=audio_features, target_type='energy', target_value=energy)

        # Add matching track objects to tracks list
        audio_features_objects = list(audio_features['audio_features'])
        ids = set([i["id"] for i in audio_features_objects])
        tracks += [i for i in track_objects if i["id"] in ids]

        # Increment offset by 50, the max limit for spotify search results  
        i += 50
    
    return tracks[:n]

# Logging a user in.
def callback(code):
    access_token, refresh_token, start_time = get_access_token(code)
    user_id = add_new_user(access_token, refresh_token, start_time)
    return user_id

# Creating a new room.
def new_room(user_id):

    # Get the user from users table, and make sure access refresh time stuff is not null.
    spotify_tokens = get_user_spotify_tokens(user_id) #DB
    if spotify_tokens is None:
        print("The user has not logged in.")
        return 0
    access_token = spotify_tokens[0]
    refresh_token = spotify_tokens[1]
    start_time = spotify_tokens[2]
    if access_token is None or refresh_token is None or start_time is None:
        print("The user does not have valid spotify tokens.")
        return 0

    # Create a new room and add the creator to it
    room_id = add_new_room() #DB
    if room_id is 0:
        print("Error creating room in database.")
        return 0
    add_user_to_room(room_id, user_id) #DB

    # Refresh the token if required, and update in DB.
    if (time.time() - start_time) > 3600:
        access_token, start_time = refresh_access_token(refresh_token) #AUTH
        update_spotify_tokens(access_token, start_time, user_id) #DB

    # Get spotify user id and create playlist for room.
    spotify_user_id = get_user_id(access_token) #API
    playlist_id, playlist_uri = create_playlist(access_token, spotify_user_id, room_id) #API
    add_playlist_to_room(playlist_id, playlist_uri, room_id) #DB

    return room_id, playlist_uri
