# Access "users" table in "cvdj.db", to store user level data.

import json
import sqlite3
from sqlite3 import Error
import pymssql

driver= '{ODBC Driver 17 for SQL Server}'
server = 'cvdj.database.windows.net'
database = 'cvdj'
username = 'cvdjadmin@cvdj'
password = 'elec498!' 
# conn = pymssql.connect(server, username, password, database)

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

# Insert user in database.
def insert_user(room_id):
    user_id = 0
    try:
        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()
        query = """ INSERT INTO users (roomId, emotionData)
                    VALUES (?, ?); """
        params = (room_id, DEFAULT_EMOTION_JSON)

        cursor.execute(query, params)
        user_id = cursor.lastrowid
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close() 
        return user_id

# Delete user.
def delete_user(user_id):
    try:
        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()
        query = """ DELETE FROM users
                    WHERE userId = ?; """
        params = (user_id, )

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update emotion data.
def set_emotion_data(user_id, emotion_data):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        query = """ UPDATE users
                    SET emotionData = ?
                    WHERE userId = ?; """
        params = (emotion_data, user_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update spotify device.
def set_device_id(user_id, spotify_device):
    try:
        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()
        query = """ UPDATE users
                    SET spotifyDevice = ?
                    WHERE userId = ?; """
        params = (spotify_device, user_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
