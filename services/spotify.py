import time
import database.users as users
import database.rooms as rooms
import services.spotify_api as api

THRESHOLD = 0.09

# Route: /create_room.
def create_spotify_room(code, redirect_uri):
    access_token, refresh_token, expire_time = api.get_access_tokens(code, redirect_uri)

    room_id = rooms.insert_room()
    user_id = users.insert_user(room_id)

    spotify_id = api.get_spotify_id(access_token)
    playlist_id = api.create_playlist(access_token, room_id, spotify_id)
    
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playlistId': playlist_id,
        'isPlaying': 0
    })

    return {
        'roomId': room_id,
        'userId': user_id,
        'accessToken': access_token,
        'playlistUri': playlist_id
    }

# Route: /leave_room.
def leave_spotify_room(room_id, user_id):
    users.delete_user(user_id)

    devices_set = rooms.get_spotify_devices(room_id)
    if len(devices_set) == 0:
        rooms.delete_room(room_id)

# Route: /join_room.
def join_spotify_room(room_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Add user to room and return.
    user_id = users.insert_user(room_id)
    return {
        'userId': int(user_id),
        'accessToken': str(access_token),
        'playlistUri': str(playlist_id)
    }

# Route: /add_device.
def add_spotify_device(room_id, user_id, device_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Add device to user.
    users.set_device_id(user_id, device_id)
    api.transfer(access_token, device_id, is_playing)

# Route: /play_room.
def play_spotify_room(room_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Check context URI and position for accuracy.
    uri = f'spotify:playlist:{playlist_id}'
    position = 0
    try:
        playback_data = api.get_playback(access_token)
        curr = playback_data['context']['uri']
        if curr == uri:
            uri = None
            position = None
    
    # Start playing, if the room is currently paused.
    finally:
        device_ids = rooms.get_spotify_devices(room_id)
        if is_playing == 0:
            for i in device_ids:
                if i is not None:
                    api.play(access_token, i, uri, position)
    return __room_player(room_id, playlist_id, refresh_token, access_token, expire_time)

# Route: /pause_room.
def pause_spotify_room(room_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Pause room playback.
    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.pause(access_token, i)
    return __room_player(room_id, playlist_id, refresh_token, access_token, expire_time)

# Route: /skip_next.
def spotify_skip_next(room_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Skip to next track in room playlist.
    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.skip_next(access_token, i)
    return __room_player(room_id, playlist_id, refresh_token, access_token, expire_time)

# Route: /skip_previous.
def spotify_skip_previous(room_id):

    # Get room status and update access token.
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    # Skip back to previous track in room playlist.
    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.skip_previous(access_token, i)
    return __room_player(room_id, playlist_id, refresh_token, access_token, expire_time)

# Update room emotion and playlist.
def _room_update(access_token, room_id, playlist_id):

    # Run update code if it exists with users.
    user_emotions = rooms.get_users_emotions(room_id)
    num_users = len(user_emotions)
    if num_users > 0:
        emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral':0, 'sadness': 0, 'surprise': 0}
        for e in emotions:
            emotions[e] = sum([i[e] for i in user_emotions]) / num_users
        max_emotion = max(emotions, key=emotions.get)

        # Metrics for finding a new track.
        existing = api.get_playlist_tracks(access_token, playlist_id)
        target_energy = __room_energy(emotions)
        target_valence = __room_valence(emotions)

        # Find a new track id to add to playlist.
        playlist_ids = api.search_playlist(access_token, max_emotion)
        for i in playlist_ids:
            track_ids = api.get_playlist_tracks(access_token, i)
            audio_features = api.get_audio_features(access_token, track_ids)
            for j in audio_features:
                check_duplicate = not (j['id'] in existing)
                check_energy = (abs(j['energy'] - target_energy) < THRESHOLD)
                check_valence = (abs(j['valence'] - target_valence) < THRESHOLD)

                # If a fitting track is found, break out of all nested loops.
                if check_duplicate and check_energy and check_valence:
                    new_track_id = j['id']
                    api.add_track_to_playlist(access_token, playlist_id, new_track_id)
                    return

## Private helper functions.
# Get playback data for the room from the API, for database update and response to frontend.
def __room_player(room_id, playlist_id, refresh_token, access_token, expire_time):
    try:
        playback_data = api.get_playback(access_token)
        is_playing = playback_data['is_playing']
        song = playback_data['item']['name']
        artist = playback_data['item']['artists'][0]['name']
        album_art = playback_data['item']['album']['images'][0]['url']
    except:
        print('Failed to get playback data from Spotify.')
        is_playing = 0
        song = None
        artist = None
        album_art = None
    rooms.set_room(room_id, dict({
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playlistId': playlist_id,
        'isPlaying': is_playing
    }))
    return {
        'song': song,
        'artist': artist,
        'albumArt': album_art
    }

# Calculate target energy for the room.
def __room_energy(emotions):
    anger = emotions['anger']
    contempt = emotions['contempt']
    disgust = emotions['disgust']
    fear = emotions['fear']
    happiness = emotions['happiness']
    # neutral = emotions['neutral']
    # sadness = emotions['sadness']
    surprise = emotions['surprise']

    energy = (5*surprise + 4*anger + 3*fear + 2*contempt + 2*disgust + happiness) / 5
    return energy

# Calculate target valence for the room.
def __room_valence(emotions):
    anger = emotions['anger']
    contempt = emotions['contempt']
    disgust = emotions['disgust']
    fear = emotions['fear']
    happiness = emotions['happiness']
    # neutral = emotions['neutral']
    sadness = emotions['sadness']
    surprise = emotions['surprise']

    valence = ((happiness + surprise) - (anger + contempt + disgust + fear + sadness) + 1) / 2
    return valence