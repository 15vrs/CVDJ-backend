import json
import pymssql
import database.rooms as rooms
import database.users as users
from tests.test_variables import ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID, USER_ID, EMOTION_DATA, DEVICE_ID

# Database connection values.
server = 'cvdj.database.windows.net'
database = 'cvdj'
username = 'cvdjadmin'
password = 'elec498!' 

# Check insert room response from rooms.
def test_insert_room():
    global ROOM_ID

    rsp = rooms.insert_room()
    assert rsp is not None
    assert type(rsp) == int
    ROOM_ID = rsp

    # Check database contents.
    expected = {
        'roomId': ROOM_ID,
        'accessToken': None,
        'refreshToken': None,
        'tokenExpireTime': None,
        'playlistId': None,
        'isPlaying': 0
    }
    __check_rooms([expected], 1)

# Check set room from rooms.
def test_set_room():
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID

    expected = {
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    }
    rooms.set_room(ROOM_ID, expected)

    # Check database contents.
    __check_rooms([expected], 1)

# Test get room response from rooms.
def test_get_room():
    global ROOM_ID, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRE_TIME, PLAYLIST_ID

    rsp = rooms.get_room(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == dict

    expected = {
        'roomId': ROOM_ID,
        'accessToken': ACCESS_TOKEN,
        'refreshToken': REFRESH_TOKEN,
        'tokenExpireTime': EXPIRE_TIME,
        'playlistId': PLAYLIST_ID,
        'isPlaying': 0
    }
    assert rsp == expected

# Test insert user response from users.
def test_insert_user():
    global USER_ID, ROOM_ID, EMOTION_DATA
    
    rsp = users.insert_user(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == int
    USER_ID = rsp

    # Check database contents.
    expected = {
        'userId': USER_ID,
        'roomId': ROOM_ID,
        'emotionData': json.dumps(EMOTION_DATA),
        'spotifyDevice': None
    }
    __check_users([expected], 1)

# Test set emotion data from users.
def test_set_emotion_data():
    global USER_ID, ROOM_ID, EMOTION_DATA

    users.set_emotion_data(USER_ID, EMOTION_DATA)

    # Check database contents.
    expected = {
        'userId': USER_ID,
        'roomId': ROOM_ID,
        'emotionData': json.dumps(EMOTION_DATA),
        'spotifyDevice': None
    }
    __check_users([expected], 1)

# Test set device id from users.
def test_set_device_id():
    global USER_ID, ROOM_ID, EMOTION_DATA, DEVICE_ID

    users.set_device_id(USER_ID, DEVICE_ID)

    # Check database contents.
    expected = {
        'userId': USER_ID,
        'roomId': ROOM_ID,
        'emotionData': json.dumps(EMOTION_DATA),
        'spotifyDevice': DEVICE_ID
    }
    __check_users([expected], 1)

# Test get users emotion data response from rooms.
def test_get_users_emotions():
    global USER_ID, ROOM_ID, EMOTION_DATA

    rsp = rooms.get_users_emotions(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == list
    assert len(rsp) == 1

    expected = [EMOTION_DATA]
    assert rsp == expected

# Test get spotify devices response from rooms (not empty).
def test_get_spotify_devices():
    global USER_ID, ROOM_ID, DEVICE_ID

    rsp = rooms.get_spotify_devices(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == list
    assert len(rsp) == 1

    expected = [DEVICE_ID]
    assert rsp == expected

# Test delete user from users.
def test_delete_user():
    global USER_ID

    users.delete_user(USER_ID)

    # Check database contents.
    __check_users([], 0)

# Test get spotify devices response from rooms (empty).
def test_get_spotify_devices():
    global USER_ID, ROOM_ID, DEVICE_ID

    rsp = rooms.get_spotify_devices(ROOM_ID)
    assert rsp is not None
    assert type(rsp) == list
    assert len(rsp) == 0

    expected = []
    assert rsp == expected

# Test delete room from rooms.
def test_delete_room():
    global ROOM_ID
    
    rooms.delete_room(ROOM_ID)

    # Check database contents.
    __check_rooms([], 0)

## Private helper functions.
# Check rooms table test contents.
def __check_rooms(expected_rows, expected_count):
    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor(as_dict=True)

    cursor.execute(
        'SELECT * FROM rooms WHERE roomId = %s', (ROOM_ID, )
    )
    rows = cursor.fetchall()
    count = cursor.rowcount
    assert rows == expected_rows
    assert count == expected_count
    
    cursor.close()
    conn.close()

# Check users table test contents.
def __check_users(expected_rows, expected_count):
    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor(as_dict=True)

    cursor.execute(
        'SELECT * FROM users WHERE userId = %s', (USER_ID, )
    )
    rows = cursor.fetchall()
    count = cursor.rowcount
    assert rows == expected_rows
    assert count == expected_count
    
    cursor.close()
    conn.close()