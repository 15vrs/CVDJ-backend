# Access "rooms" table in "cvdj.db", to store room level data.

import json
import pickle
import sqlite3
from sqlite3 import Error

# Insert room.
def insert_room(spotify_room):
    room_id = 0
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ INSERT INTO rooms (spotifyRoom)
                    VALUES (?); """
        params = (pickle.dump(spotify_room), )

        cursor.execute(query, params)
        room_id = cursor.lastrowid
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room_id

# 
def set_room(room_id, spotify_room):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ UPDATE rooms
                    SET spotifyRoom = ?
                    WHERE roomId = ?; """
        params = (pickle.dump(spotify_room), room_id)
                
        cursor.execute(query, params)
        conn.commit()
    
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# 
def get_room(room_id):
    spotify_room = None
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ SELECT spotifyRoom FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )
                
        cursor.execute(query, params)
        rsp = cursor.fetchone()
        spotify_room = pickle.loads(rsp)
    
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return spotify_room

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