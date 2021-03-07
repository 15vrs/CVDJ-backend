import time
import spotify.users as users
import spotify.rooms as rooms
import spotify.spotify_api as api

# Route: /create_room.
def create_spotify_room(code, redirect_uri):
    refresh_token, access_token, expire_time = api.get_access_tokens(code, redirect_uri)

    room_id = rooms.insert_room()
    user_id = users.insert_user(room_id)

    spotify_id = api.get_spotify_id(access_token)
    playlist_id = api.create_playlist(access_token, room_id, spotify_id)

    room = {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playlistId': playlist_id
    }
    rooms.set_room(room_id, room)

    return room_id, user_id, access_token, playlist_id

# Route: /leave_room.
def leave_spotify_room(room_id, user_id):
    users.delete_user(user_id)

    devices_set = rooms.get_spotify_devices(room_id)
    if len(devices_set) == 0:
        rooms.delete_room(room_id)

# Route: /join_room.
def join_spotify_room(room_id):
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    # progress = room['playerProgress']
    # is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)
    user_id = users.insert_user(room_id)
    return user_id, access_token, playlist_id

# Route: /add_device.
def add_spotify_device(room_id, user_id, device_id):
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    # playlist_id = room['playlistId']
    progress = room['playerProgress']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)
    users.set_device_id(user_id, device_id)

    playback_data = api.get_playback(access_token)
    is_playing = playback_data['is_playing']
    progress = playback_data['progress_ms']
    # song = playback_data['item']['name']
    # artist = playback_data['item']['artists'][0]['name']
    # album_art = playback_data['item']['album']['images'][0]['url']
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playerProgress': progress,
        'isPlaying': is_playing
    })

# Route: /play_room.
def play_spotify_room(room_id):
    room = rooms.get_room(room_id)
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    playlist_id = room['playlistId']
    progress = room['playerProgress']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    device_ids = rooms.get_spotify_devices(room_id)
    if is_playing == 0:
        for i in device_ids:
            if i is not None:
                api.play(access_token, i, playlist_id, progress)

    playback_data = api.get_playback(access_token)
    is_playing = playback_data['is_playing']
    progress = playback_data['progress_ms']
    song = playback_data['item']['name']
    artist = playback_data['item']['artists'][0]['name']
    album_art = playback_data['item']['album']['images'][0]['url']
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playerProgress': progress,
        'isPlaying': is_playing
    })

    return {
        'song': song,
        'artist': artist,
        'albumArt': album_art
    }

# Route: /pause_room.
def pause_spotify_room(room_id):
    room = rooms.get_room(room_id)
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    # playlist_id = room['playlistId']
    progress = room['playerProgress']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.pause(access_token, i)

    playback_data = api.get_playback(access_token)
    is_playing = playback_data['is_playing']
    progress = playback_data['progress_ms']
    song = playback_data['item']['name']
    artist = playback_data['item']['artists'][0]['name']
    album_art = playback_data['item']['album']['images'][0]['url']
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playerProgress': progress,
        'isPlaying': is_playing
    })

    return {
        'song': song,
        'artist': artist,
        'albumArt': album_art
    }

# Route: /skip_next.
def spotify_skip_next(room_id):
    room = rooms.get_room(room_id)
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    # playlist_id = room['playlistId']
    progress = room['playerProgress']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.skip_next(access_token, i)

    playback_data = api.get_playback(access_token)
    is_playing = playback_data['is_playing']
    progress = playback_data['progress_ms']
    song = playback_data['item']['name']
    artist = playback_data['item']['artists'][0]['name']
    album_art = playback_data['item']['album']['images'][0]['url']
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playerProgress': progress,
        'isPlaying': is_playing
    })

    return {
        'song': song,
        'artist': artist,
        'albumArt': album_art
    }

# Route: /skip_previous.
def spotify_skip_previous(room_id):
    room = rooms.get_room(room_id)
    room = rooms.get_room(room_id)
    refresh_token = room['refreshToken']
    access_token = room['accessToken'] 
    expire_time = room['tokenExpireTime']
    # playlist_id = room['playlistId']
    progress = room['playerProgress']
    is_playing = room['isPlaying']
    if (time.time() > expire_time):
        access_token, expire_time = api.refresh_access_tokens(refresh_token)

    device_ids = rooms.get_spotify_devices(room_id)
    for i in device_ids:
        if i is not None:
            api.skip_previous(access_token, i)

    playback_data = api.get_playback(access_token)
    is_playing = playback_data['is_playing']
    progress = playback_data['progress_ms']
    song = playback_data['item']['name']
    artist = playback_data['item']['artists'][0]['name']
    album_art = playback_data['item']['album']['images'][0]['url']
    rooms.set_room(room_id, {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenExpireTime': expire_time,
        'playerProgress': progress,
        'isPlaying': is_playing
    })

    return {
        'song': song,
        'artist': artist,
        'albumArt': album_art
    }
        