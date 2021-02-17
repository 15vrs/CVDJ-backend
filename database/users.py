# Access "users" table in "cvdj.db", to store user level data.

import json
import sqlite3
from sqlite3 import Error

DEFAULT_EMOTION_JSON = json.dumps({
        "anger": 0.0,
        "contempt": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "happiness": 0.0,
        "neutral": 1.0,
        "sadness": 0.0,
        "surprise": 0.0
    })

def add_new_user(): # Only called by add_new_creator().
    global DEFAULT_EMOTION_JSON
    
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    user_id = 0

    try:
        query = """ INSERT INTO users (emotionData)
                    VALUES (?); """
        params = (DEFAULT_EMOTION_JSON, )

        cursor.execute(query, params)
        user_id = cursor.lastrowid
        conn.commit()
        print("New user added to table")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return user_id

def add_user_to_room(room_id, user_id): # Only called by add_new_creator().
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE users
                    SET roomId = ?
                    WHERE userId = ?; """
        params = (room_id, user_id)

        cursor.execute(query, params)
        conn.commit()
        print("Added user to room.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def add_new_user_to_room(room_id): # Join room.
    global DEFAULT_EMOTION_JSON
    
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    user_id = 0

    try:
        query = """ INSERT INTO users (roomId, emotionData)
                    VALUES (?, ?); """
        params = (room_id, DEFAULT_EMOTION_JSON, )

        cursor.execute(query, params)
        user_id = cursor.lastrowid
        conn.commit()
        print("New user added to table")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return user_id

def get_user_emotion(room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT emotionData FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return [json.loads(row[0]) for row in rsp]

def get_spotify_devices(room_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT spotifyDevice FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return [row[0] for row in rsp]

def set_user_spotify_device(device_id, user_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE users
                    SET spotifyDevice = ?
                    WHERE userId = ?; """
        params = (device_id, user_id)

        cursor.execute(query, params)
        conn.commit()
        print("Added device ID to user.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()