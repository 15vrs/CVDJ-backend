import math
import database.rooms as rooms

"""
Aggregate Azure emotion data from all users in the room.
Params: room ID
Return: aggregated emotions from Azure
"""
def room_emotion(room_id):
    rsp = {"anger": 0, "contempt": 0, "disgust": 0, "fear": 0, "happiness": 0, "neutral":0, "sadness": 0, "surprise": 0}
    user_emotions = rooms.get_users_emotions(room_id)
    num_users = len(user_emotions)
    if num_users > 0:
        for e in rsp:
            rsp[e] = sum([i[e] for i in user_emotions]) / num_users
    return rsp

"""
Calculate energy and valence for the following emotions.
Params: Modified Ekman's from Azure
Return: Modified Russel's for Spotify
    Emotion     Energy  Valence
    anger       0.7071  0.1464
    contempt    0.5     0.067
    disgust     0.5     0.067
    fear        0.866   0.25
    happiness   0.5     0.933
    neutral     0       0
    sadness     0.0     0.0
    surprise    1.0     0.5
"""
def convert_emotion(emotions):
    angles = {
        "anger": 3 * math.pi / 4,
        "contempt": 5 * math.pi / 6,
        "disgust": 5 * math.pi / 6,
        "fear": 2 * math.pi / 3,
        "happiness": math.pi / 6,
        "neutral": None,
        "sadness": math.pi,
        "surprise": math.pi / 2
    }

    # Initialize to neutral.
    max_emotion = "neutral"
    energy = 0
    valence = 0

    # Calculate max emotion, energy, valence.
    for i in emotions:
        if angles[i] is not None:
            energy += round(math.sin(angles[i]) * emotions[i], 4)
            valence += round(((math.cos(angles[i]) + 1) / 2) * emotions[i], 4)
    if max(emotions) > 0:
        max_emotion = max(emotions, key=emotions.get)
    
    # Return max emotion, energy, valence.
    return max_emotion, energy, valence

"""
"""
def room_update(access_token, room_id, playlist_id):

    emotions = room_emotion(room_id)
    max_emotion, target_energy, target_valence = convert_emotion(emotions)

    # List of tracks IDs that have already been recommended.
    existing = api.get_playlist_tracks(access_token, playlist_id)

    # Find a new track id to add to playlist.
    playlist_ids = api.search_playlist(access_token, max_emotion)
    for i in playlist_ids:
        track_ids = api.get_playlist_tracks(access_token, i)
        audio_features = api.get_audio_features(access_token, track_ids)
        for j in audio_features:
            check_duplicate = not (j["id"] in existing)
            check_energy = (abs(j["energy"] - target_energy) < THRESHOLD)
            check_valence = (abs(j["valence"] - target_valence) < THRESHOLD)

            # If a fitting track is found, break out of all nested loops.
            if check_duplicate and check_energy and check_valence:
                new_track_id = j["id"]
                api.add_track_to_playlist(access_token, playlist_id, new_track_id)
                return

"""
Test values
{
    "anger": 0.011,
    "contempt": 0,
    "disgust": 0,
    "fear": 0,
    "happiness": 0.006,
    "neutral": 0.824,
    "sadness": 0,
    "surprise": 0.158
}
"""