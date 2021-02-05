import sqlite3
from sqlite3 import Error

def add_new_user(access_token, refresh_token, start_time):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    user_id = 0

    try:
        query = """ INSERT INTO users (spotifyAccessToken, spotifyRefreshToken, spotifyAccessTime)
                    VALUES (?, ?, ?); """
        params = (access_token, refresh_token, start_time)

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

def add_user_to_room(room_id, user_id):
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

def get_user_spotify_tokens(user_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT spotifyAccessToken, spotifyRefreshToken, spotifyAccessTime FROM users
                    WHERE userId = ?; """
        params = (user_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return rsp

def update_spotify_tokens(access_token, start_time, user_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE users
                    SET spotifyAccessToken = ?, spotifyAccessTime = ?
                    WHERE userId = ?; """
        params = (access_token, start_time, user_id)

        cursor.execute(query, params)
        conn.commit()
        print("Refreshed spotify access tokens.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()