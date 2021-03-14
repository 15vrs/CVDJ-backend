import json
import services.spotify as spotify

## Global variables ##
# Room test variables.
ROOM_ID = 1
ACCESS_TOKEN = 'BQDi23QDxX5MFHjvy7PV2pz7dlqFCcsISfvvh-Tprdt1KAd4UfCBo0O9faJH9ZIJlgtvGEKWp4j_JDgnQq5iNFq-qE3fg3rhPRQZekWil2KyWdXWhTh8ukZzbpNkLMZIIxIUmO7_sbiWDragFnIDRbbwfNKCfcPtXnXagJc_i7kOFmef8usndjaDSpcIN37a6tfKnl9hZ-wES0yymdNQP0FVBnDrRKq3M_81MVdJrwzEwwCwN0Zz4m072sXC'
REFRESH_TOKEN = 'AQC-gL7DnvESak5L8yTZ8UJM1Tq95Bwh_jifKb-8uakbPtmm0hZKUrxmBZIiWrjzcJ16qMlMLlxSUSH-EKrLT-tCEqkCLq0Az0qs6hkp5HtRxZ6gJCKGts_TIcbUbvWTENQ'
EXPIRE_TIME = 1615301838
PLAYLIST_ID = '6rzDJ7iqTwKjVsqHf7oxTy'

# User test variables.
USER_ID = 1
EMOTION_DATA = json.dumps({
        "anger": 0.0,
        "contempt": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "happiness": 0.0,
        "neutral": 1.0,
        "sadness": 0.0,
        "surprise": 0.0
    })
DEVICE_ID = '129279d8344a91e94463269df2bd8451135768e5'

# Spotify API test variables.
SPOTIFY_ID = 'xxaabpbc03uwqhxuzrcadqhey'
CODE = 'test_code_value'
REDIRECT_URI = 'test_redirect_uri'

## Tests ##
# Not tested - leave_spotify_room, add_device
# Check create room response from spotify.
def test_create_spotify_room(mocker):
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID, SPOTIFY_ID, CODE, REDIRECT_URI

    mocker.patch('services.spotify_api.get_access_tokens', return_value=(REFRESH_TOKEN, ACCESS_TOKEN, EXPIRE_TIME))
    mocker.patch('database.rooms.insert_room', return_value=ROOM_ID)
    mocker.patch('database.users.insert_user', return_value=USER_ID)
    mocker.patch('services.spotify_api.get_spotify_id', return_value=SPOTIFY_ID)
    mocker.patch('services.spotify_api.create_playlist', return_value=PLAYLIST_ID)
    mocker.patch('database.rooms.set_room')

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

    rsp = spotify.join_spotify_room(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict

    expected = {
        'userId': USER_ID,
        'accessToken': ACCESS_TOKEN,
        'playlistUri': PLAYLIST_ID
    }
    assert rsp == expected