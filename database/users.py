# Store user level data.
import json
import pymssql
from pymssql import Error
from database.init import SERVER, USERNAME, PASSWORD, DATABASE

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
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()
    try:
        query = """ INSERT INTO users (roomId, emotionData)
                    VALUES (%s, %s); """
        params = (room_id, neutral)

        cursor.execute(query, params)
        user_id = cursor.lastrowid
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
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()
    try:
        query = """ UPDATE users
                    SET emotionData = %s
                    WHERE userId = %s; """
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
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()
    try:
        query = """ UPDATE users
                    SET spotifyDevice = %s
                    WHERE userId = %s; """
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
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()
    try:
        query = """ DELETE FROM users
                    WHERE userId = %s; """
        params = (user_id, )

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()
