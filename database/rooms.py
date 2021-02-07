# Access "rooms" table in "cvdj.db", to store room level data.

import sqlite3
from sqlite3 import Error

def add_new_room():
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    room_id = 0

    try:
        query = """ INSERT INTO rooms (spotifyPlaylistId, averageEmotion)
                    VALUES (?, ?); """
        params = (None, None)

        cursor.execute(query, params)
        room_id = cursor.lastrowid
        conn.commit()
        print("New room added to table")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return room_id

def add_playlist_to_room(playlist_id, room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE rooms
                    SET spotifyPlaylistId = ?
                    WHERE roomId = ?; """
        params = (playlist_id, room_id)

        cursor.execute(query, params)
        conn.commit()
        print("Added playlist to room.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def update_room_emotion(emotion, room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE rooms
                    SET averageEmotion = ?
                    WHERE roomId = ?; """
        params = (emotion, room_id)

        cursor.execute(query, params)
        conn.commit()
        print("Updated emotion in room.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def get_playlist_from_room(room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT spotifyPlaylistId FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return rsp