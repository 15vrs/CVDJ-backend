# Store user level data.
import pyodbc
from pyodbc import Error
import json
from database.init import DRIVER, SERVER, USERNAME, PASSWORD, DATABASE

# Insert user in database with neutral emotion data.
def insert_user(room_id):
    neutral = json.dumps({
            "anger": 0.0,
            "contempt": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "happiness": 0.0,
            "neutral": 1.0,
            "sadness": 0.0,
            "surprise": 0.0
        })
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ INSERT INTO users (roomId, emotionData) 
                    OUTPUT INSERTED.userId 
                    VALUES (?, ?); """
        params = (room_id, neutral)

        cursor.execute(query, params)
        user_id = cursor.fetchone()[0]
        conn.commit()
        return int(user_id)

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update emotion data for user.
def set_emotion_data(user_id, emotion_data):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ UPDATE users
                    SET emotionData = ?
                    WHERE userId = ?; """
        params = (json.dumps(emotion_data), user_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update spotify device for user.
def set_device_id(user_id, spotify_device):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ UPDATE users
                    SET spotifyDevice = ?
                    WHERE userId = ?; """
        params = (spotify_device, user_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Delete user from users table.
def delete_user(user_id):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ DELETE FROM users
                    WHERE userId = ?; """
        params = (user_id, )

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()
