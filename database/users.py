# Access "users" table in "cvdj.db", to store user level data.

import json
import sqlite3
from sqlite3 import Error

DEFAULT_EMOTION_JSON = {
        "anger": 0.0,
        "contempt": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "happiness": 0.0,
        "neutral": 1.0,
        "sadness": 0.0,
        "surprise": 0.0
    }

class User:

    def __init__(self, room_id, device_id):
        self.emotion_data = DEFAULT_EMOTION_JSON
        self.device_id = device_id

        # Create room object in database.users.
        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ INSERT INTO users (roomId, emotionData, spotifyDevice)
                        VALUES (?, ?, ?); """
            params = (room_id, json.dumps(DEFAULT_EMOTION_JSON), device_id)

            cursor.execute(query, params)
            self.id = cursor.lastrowid
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()    

    # Delete user from database.
    def __del__(self):
        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ DELETE FROM users
                        WHERE userId = ?; """
            params = (self.id, )

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
    
    ## Setters
    # Set emotion data in database.
    def set_emotion_data(self, emotion_data):
        self.emotion_data = emotion_data

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ UPDATE users
                        SET emotionData = ?
                        WHERE userId = ?; """
            params = (json.dumps(emotion_data), self.id)

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    ## Getters
    # Get user id.
    def get_user_id(self):
        return self.id

    # Get emotion data.
    def get_emotion_data(self):
        return self.emotion_data

    # Get device.
    def get_device_id(self):
        return self.device_id
