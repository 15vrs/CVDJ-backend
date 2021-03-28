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
