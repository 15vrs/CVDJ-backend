# Access "rooms" table in "cvdj.db", to store room level data.

import json
import sqlite3
from sqlite3 import Error

# Insert room.
def insert_room():
    room_id = 0

    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ INSERT INTO rooms (accessToken)
                    VALUES (?); """
        params = (None, )

        cursor.execute(query, params)
        room_id = cursor.lastrowid
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room_id

# Delete room.
def delete_room(room_id):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ DELETE FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update room from a dict.
def set_room(room_id, room):
    print(room['playlist_id'])
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ UPDATE rooms
                    SET accessToken = ?,
                        refreshToken = ?,
                        tokenExpireTime = ?,
                        playlistId = ?,
                        playerProgress = ?,
                        isPlaying = ?
                    WHERE roomId = ?; """
        params = (room['access_token'], room['refresh_token'], room['expire_time'], room['playlist_id'], room['progress'], room['is_playing'], room_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Get room as dict.
def get_room(room_id):
    room = dict()

    try:
        conn = sqlite3.connect('cvdj.db')
        conn.row_factory = __dict_factory
        cursor = conn.cursor()
        query = """ SELECT *
                    FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        room = dict(cursor.fetchone())
    
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room

# Private function.
def __dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Select users emotions list.
def get_users_emotions(room_id):
    emotions = list()
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ SELECT emotionData FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        emotions = [json.loads(row[0]) for row in rsp]

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return emotions

# Select users device IDs.
def get_spotify_devices(room_id):
    device_ids = list()
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ SELECT spotifyDevice FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        device_ids = [row[0] for row in rsp]

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return device_ids
