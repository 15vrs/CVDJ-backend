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

def check_room_exists(room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT roomId FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        
        if rsp is None:
            return False
        return True