# Access and store room level data.
import pyodbc
from pyodbc import Error
import json
from database.init import DRIVER, SERVER, USERNAME, PASSWORD, DATABASE

# Insert room.
def insert_room():
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ INSERT INTO rooms (accessToken) 
                    OUTPUT INSERTED.roomId 
                    VALUES (?); """
        params = (None, )

        cursor.execute(query, params)
        room_id = cursor.fetchone()[0]
        conn.commit()
        return int(room_id)

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Update room from a dict.
def set_room(room_id, room):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ UPDATE rooms
                    SET accessToken = ?,
                        refreshToken = ?,
                        tokenExpireTime = ?,
                        playlistId = ?,
                        isPlaying = ?
                    WHERE roomId = ?; """
        params = (room['accessToken'], room['refreshToken'], room['tokenExpireTime'], room['playlistId'], room['isPlaying'], room_id)

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Get room as dict.
def get_room(room_id):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ SELECT *
                    FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        room = dict(zip(columns, cursor.fetchone()))
        return room
    
    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Delete room.
def delete_room(room_id):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ DELETE FROM rooms
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        conn.commit()

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Select users emotions list.
def get_users_emotions(room_id):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ SELECT emotionData FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        emotions = [json.loads(row[0]) for row in rsp]
        return emotions

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()

# Select users device IDs.
def get_spotify_devices(room_id):
    conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = conn.cursor()
    try:
        query = """ SELECT spotifyDevice FROM users
                    WHERE roomId = ?; """
        params = (room_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchall()
        device_ids = [row[0] for row in rsp]
        return device_ids

    except Error as e:
        conn.rollback()
        print(e)

    finally:
        cursor.close()
        conn.close()
