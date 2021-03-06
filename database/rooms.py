# Access "rooms" table in "cvdj.db", to store room level data.

import json
import sqlite3
from sqlite3 import Error

class Room:

    # Create room object in database.rooms.
    def __init__(self):
        self.id = 0
        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ INSERT INTO rooms (averageEmotion)
                        VALUES (?); """
            params = ('', )

            cursor.execute(query, params)
            self.id = cursor.lastrowid
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    # Delete room from database.rooms.
    def __del__(self):
        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ DELETE FROM rooms
                        WHERE roomId = ?; """
            params = (self.id, )

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    ## Setters
    # Set playlist id in database.rooms.
    def set_playlist_id(self, playlist_id):
        self.playlist_id = playlist_id

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ UPDATE rooms
                        SET spotifyPlaylistId = ?
                        WHERE roomId = ?; """
            params = (playlist_id, self.id)

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    # Set emotion in database.rooms.
    def set_emotion(self, emotion):
        self.emotion = emotion

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ UPDATE rooms
                        SET averageEmotion = ?
                        WHERE roomId = ?; """
            params = (emotion, self.id)

            cursor.execute(query, params)
            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    ## Getters
    # Get room id.
    def get_room_id(self):
        return self.id

    # Get playlist id.
    def get_playlist_id(self):
        return self.playlist_id

    # Get emotion.
    def get_emotion(self):
        return self.emotion

    # Get list of emotion data from database.users.
    def get_user_emotion(self):
        emotions = None

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ SELECT emotionData FROM users
                        WHERE roomId = ?; """
            params = (self.id, )

            cursor.execute(query, params)
            rsp = cursor.fetchall()
            emotions = [json.loads(row[0]) for row in rsp]

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

        return emotions

    # Get list of spotify device ids from database.users.
    def get_spotify_devices(self):
        device_ids = None

        try:
            conn = sqlite3.connect('cvdj.db')
            cursor = conn.cursor()
            query = """ SELECT spotifyDevice FROM users
                        WHERE roomId = ?; """
            params = (self.id, )

            cursor.execute(query, params)
            rsp = cursor.fetchall()
            device_ids = [row[0] for row in rsp]

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

        return device_ids
