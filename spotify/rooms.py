# Access "rooms" table in "cvdj.db", to store room level data.

import json
import sqlite3
from sqlite3 import Error

class Room:

    # Create room object.
    def __init__(self):
        self.id = self.__insert_room()
        self.emotion = None

    # Delete room.
    def __del__(self):
        self.__delete_room(self.id)

    # Setters
    def set_emotion(self, emotion):
        self.emotion = emotion
        self.__update_average_emotion(self.id, emotion)

    # Getters
    def get_room_id(self):
        return self.id

    # def get_emotion(self):
    #     return self.emotion

    def get_user_emotion(self):
        return self.__select_users_emotions(self.id)

    def get_spotify_devices(self):
        user_devices = self.__select_users_devices(self.id)
        return user_devices

    ## Database functions.
    # Insert room.
    def __insert_room(self):
        room_id = 0

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ INSERT INTO rooms (averageEmotion)
                        VALUES (?); """
            params = ('', )

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
    def __delete_room(self, room_id):
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

    # Update average emotion.
    def __update_average_emotion(self, room_id, emotion):
        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ UPDATE rooms
                        SET averageEmotion = ?
                        WHERE roomId = ?; """
            params = (emotion, room_id)

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    # Select users emotions list.
    def __select_users_emotions(self, room_id):
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
    def __select_users_devices(self, room_id):
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