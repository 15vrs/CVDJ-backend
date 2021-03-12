# Access "rooms" table in "cvdj.db", to store room level data.

import json
import pymssql
from pymssql import Error

driver= '{ODBC Driver 17 for SQL Server}'
server = 'cvdj.database.windows.net'
database = 'cvdj'
username = 'cvdjadmin'
password = 'elec498!' 

# Insert room.
def insert_room():
    room_id = 0

    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ INSERT INTO rooms (accessToken)
                    VALUES (%s); """
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
    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ DELETE FROM rooms
                    WHERE roomId = %d; """
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
    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ UPDATE rooms
                    SET accessToken = %s,
                        refreshToken = %s,
                        tokenExpireTime = %s,
                        playlistId = %s,
                        isPlaying = %d
                    WHERE roomId = %d; """
        params = (room['access_token'], room['refresh_token'], room['expire_time'], room['playlist_id'], room['is_playing'], room_id)

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

    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ SELECT *
                    FROM rooms
                    WHERE roomId = %s; """
        params = (room_id, )

        cursor.execute(query, params)
        room = dict(cursor.fetchone())
    
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room

# Select users emotions list.
def get_users_emotions(room_id):
    emotions = list()

    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ SELECT emotionData FROM users
                    WHERE roomId = %d; """
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

    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()
    try:
        query = """ SELECT spotifyDevice FROM users
                    WHERE roomId = %d; """
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
