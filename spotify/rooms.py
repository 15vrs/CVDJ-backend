# Access "rooms" table in "cvdj.db", to store room level data.

import json
import sqlite3
from sqlite3 import Error

# Insert room.
def insert_room(accessToken, refreshToken, tokenExpireTime):
    query = 'INSERT INTO rooms (accessToken, refreshToken, tokenExpireTime) VALUES (?);'
    params = (accessToken, refreshToken, tokenExpireTime)
    room_id = 0

    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()

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
    query = 'DELETE FROM rooms WHERE roomId = ?; '
    params = (room_id, )

    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update room from a dict.
def set_room(room_id, room):
    sql = ', '.join('='.join(i) for i in room.items())
    query = 'UPDATE table SET ? WHERE roomId = ?'
    params = (sql, room_id)

    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Get room as dict.
def get_room(room_id):
    query = 'SELECT 1 FROM rooms WHERE roomId = ?'
    params = (room_id, )
    room = dict()

    try:
        conn = sqlite3.connect('cvdj,db')
        conn.row_factory = __dict_factory
        cursor = conn.cursor()

        cursor.execute(query, params)
        room = dict(cursor.fetchone())
    
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room

## Private functions.
def __dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Select users emotions list.
def get_users_emotions(room_id):
    emotions = set()
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ SELECT emotionData FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        emotions = set([json.loads(row[0]) for row in rsp])

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return emotions

# Select users device IDs.
def get_spotify_devices(room_id):
    device_ids = set()
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ SELECT spotifyDevice FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        device_ids = set([row[0] for row in rsp])

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return device_ids
# # Set tokens.
# def set_tokens(room_id, refresh_token, access_token, expire_time):
#     try:
#         conn = sqlite3.connect('cvdj.db')
#         cursor = conn.cursor()
#         query = """ UPDATE rooms
#                     SET spotifyRefreshToken = ?, spotifyAccessToken = ?, spotifyTokenExpireTime = ?
#                     WHERE roomId = ?; """
#         params = (refresh_token, access_token, expire_time, room_id)

#         cursor.execute(query, params)
#         conn.commit()

#     except Error as e:
#         print(e)

#     finally:
#         cursor.close()
#         conn.close()

# # Get tokens.
# def get_tokens(room_id):
#     refresh_token, access_token, expire_time = None, None, None
#     try:
#         conn = sqlite3.connect('cvdj.db')
#         cursor = conn.cursor()
#         query = """ SELECT spotifyAccessToken, spotifyRefreshToken, spotifyTokenExpireTime FROM rooms
#                     WHERE roomId = ?; """
#         params = (room_id, )
                
#         cursor.execute(query, params)
#         refresh_token, access_token, expire_time = cursor.fetchone()
    
#     except Error as e:
#         print(e)

#     finally:
#         cursor.close()
#         conn.close()
#         return refresh_token, access_token, expire_time

# # Set playlist id.
# def set_playlist(room_id, playlist_id):
#     try:
#         conn = sqlite3.connect('cvdj.db')
#         cursor = conn.cursor()
#         query = """ UPDATE rooms
#                     SET spotifyPlaylistId = ?
#                     WHERE roomId = ?; """
#         params = (playlist_id, room_id)

#         cursor.execute(query, params)
#         conn.commit()

#     except Error as e:
#         print(e)

#     finally:
#         cursor.close()
#         conn.close()

# # Get playlist id.
# def get_playlist(room_id):
#     playlist_id = None
#     try:
#         conn = sqlite3.connect('cvdj.db')
#         cursor = conn.cursor()
#         query = """ SELECT spotifyPlaylistId FROM rooms
#                     WHERE roomId = ?; """
#         params = (room_id, )
                
#         cursor.execute(query, params)
#         playlist_id = cursor.fetchone()
    
#     except Error as e:
#         print(e)

#     finally:
#         cursor.close()
#         conn.close()
#         return playlist_id
