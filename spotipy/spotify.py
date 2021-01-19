# Handle all calls directly from app.py.

from spotipy.spotify_api import search, get_audio_features, create_playlist, get_user_id
from spotipy.spotify_helper import format_emotion_data, prune_audio_features
from spotipy.spotify_auth import authorization_code, get_access_token
from objects.room import Room

# Params:   azure_cognitive emotion JSON for one person
#           n number of recommendations to return
# Returns:  list of n Spotify track objects
def track_recommendations(emotion_json, n):

    # Validate inputs
    if int(sum(emotion_json[i] for i in emotion_json.keys())) != 1:
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

# Logging a user in
def login():
    return authorization_code()

def callback(code):
    return get_access_token(code)

def create_room(access_token, refresh_token, expires_in, start_time):
    
    # TEMP: set-up room code (will probably auto-fill when added to database)
    room_id = 1001

    user_id = get_user_id(access_token)

    # Create playlist for the room.
    playlist_id, playlist_uri = create_playlist(access_token, user_id, room_id)

    room = Room(room_id, user_id, access_token, refresh_token, playlist_id, playlist_uri)

    return room
