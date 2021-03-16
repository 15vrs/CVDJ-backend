import services.spotify as spotify
from tests.test_variables import ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID, DEVICE_ID, SPOTIFY_ID, CODE, REDIRECT_URI, PLAYBACK_DATA, SONG, ARTIST, ALBUM_ART

# Check create room response from spotify.
def test_create_spotify_room(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID, SPOTIFY_ID, CODE, REDIRECT_URI

    mocker.patch('services.spotify_api.get_access_tokens', return_value=(ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME))
    mocker.patch('database.rooms.insert_room', return_value=ROOM_ID)
    mocker.patch('database.users.insert_user', return_value=USER_ID)
    mocker.patch('services.spotify_api.get_spotify_id', return_value=SPOTIFY_ID)
    mocker.patch('services.spotify_api.create_playlist', return_value=PLAYLIST_ID)
    mocker.patch('database.rooms.set_room')

    # Test1: success case.
    rsp = spotify.create_spotify_room(CODE, REDIRECT_URI)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'roomId': ROOM_ID,
        'userId': USER_ID,
        'accessToken': ACCESS_TOKEN,
        'playlistUri': PLAYLIST_ID
    }
    assert rsp == expected

# Check leave room in spotify.
def test_leave_spotify_room(mocker):
    global ROOM_ID, USER_ID, DEVICE_ID

    # Test1: success case.
    mocker.patch('database.users.delete_user')
    mocker.patch('database.rooms.get_spotify_devices', return_value=[DEVICE_ID])
    rsp = spotify.leave_spotify_room(ROOM_ID, USER_ID)
    assert rsp is None

    # Test2: success case.
    mocker.patch('database.rooms.get_spotify_devices', return_value=[])
    mocker.patch('database.rooms.delete_room')
    rsp = spotify.leave_spotify_room(ROOM_ID, USER_ID)
    assert rsp is None

# Check join room response from spotify.
def test_join_spotify_room(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('time.time', return_value=EXPIRE_TIME)
    mocker.patch('database.users.insert_user', return_value=USER_ID)

    # Test1: success case.
    rsp = spotify.join_spotify_room(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'userId': USER_ID,
        'accessToken': ACCESS_TOKEN,
        'playlistUri': PLAYLIST_ID
    }
    assert rsp == expected

# Check add device in spotify.
def test_add_spotify_device(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID, DEVICE_ID

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('database.users.set_device_id')
    mocker.patch('services.spotify_api.transfer')
    
    # Test1: success case.
    rsp = spotify.add_spotify_device(ROOM_ID, USER_ID, DEVICE_ID)
    assert rsp is None

# Check play room response from spotify.
def test_play_spotify_room(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, DEVICE_ID, PLAYBACK_DATA, SONG, ARTIST, ALBUM_ART

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('time.time', return_value=EXPIRE_TIME)
    mocker.patch('database.rooms.get_spotify_devices', return_value=[DEVICE_ID])
    mocker.patch('services.spotify_api.play')
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.set_room')

    # Test1: success case.
    rsp = spotify.play_spotify_room(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'song': SONG,
        'artist': ARTIST,
        'albumArt': ALBUM_ART
    }
    assert rsp == expected

# Check pause room response from spotify.
def test_pause_spotify_room(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, DEVICE_ID, PLAYBACK_DATA, SONG, ARTIST, ALBUM_ART

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('time.time', return_value=EXPIRE_TIME)
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.get_spotify_devices', return_value=[DEVICE_ID])
    mocker.patch('services.spotify_api.pause')
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.set_room')

    # Test1: success case.
    rsp = spotify.pause_spotify_room(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'song': SONG,
        'artist': ARTIST,
        'albumArt': ALBUM_ART
    }
    assert rsp == expected

# Check skip to next track response from spotify.
def test_spotify_skip_next(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, DEVICE_ID, PLAYBACK_DATA, SONG, ARTIST, ALBUM_ART

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('time.time', return_value=EXPIRE_TIME)
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.get_spotify_devices', return_value=[DEVICE_ID])
    mocker.patch('services.spotify_api.pause')
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.set_room')

    # Test1: success case.
    rsp = spotify.spotify_skip_next(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'song': SONG,
        'artist': ARTIST,
        'albumArt': ALBUM_ART
    }
    assert rsp == expected

# Check skip back to previous track response from spotify.
def test_spotify_skip_previous(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, DEVICE_ID, PLAYBACK_DATA, SONG, ARTIST, ALBUM_ART

    mocker.patch('database.rooms.get_room', return_value={
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    })
    mocker.patch('time.time', return_value=EXPIRE_TIME)
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.get_spotify_devices', return_value=[DEVICE_ID])
    mocker.patch('services.spotify_api.pause')
    mocker.patch('services.spotify_api.get_playback', return_value=PLAYBACK_DATA)
    mocker.patch('database.rooms.set_room')

    # Test1: success case.
    rsp = spotify.spotify_skip_previous(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict
    expected = {
        'song': SONG,
        'artist': ARTIST,
        'albumArt': ALBUM_ART
    }
    assert rsp == expected
