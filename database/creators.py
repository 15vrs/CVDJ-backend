import sqlite3
from sqlite3 import Error

def add_new_creator(user_id, access_token, refresh_token, start_time):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ INSERT INTO creators (userId, spotifyAccessToken, spotifyRefreshToken, spotifyAccessTime)
                    VALUES (?, ?, ?, ?); """
        params = (user_id, access_token, refresh_token, start_time)

        cursor.execute(query, params)
        conn.commit()
        print("New creator added to table")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def add_creator_to_room(room_id, user_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE creators
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

def get_user_spotify_tokens(creator_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()
    rsp = ()

    try:
        query = """ SELECT spotifyAccessToken, spotifyRefreshToken, spotifyAccessTime FROM creators
                    WHERE userId = ?; """
        params = (creator_id, )

        cursor.execute(query, params)
        rsp = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return rsp

def update_spotify_tokens(access_token, start_time, creator_id):
    conn = sqlite3.connect('cvdj.db')
    cursor = conn.cursor()

    try:
        query = """ UPDATE creators
                    SET spotifyAccessToken = ?, spotifyAccessTime = ?
                    WHERE creatorId = ?; """
        params = (access_token, start_time, creator_id)

        cursor.execute(query, params)
        conn.commit()
        print("Refreshed spotify access tokens.")

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()