import sqlite3
from sqlite3 import Error

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_BLOB(userId, roomId, photo):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        print("Connected to SQLite db.")
        sql_insert_blob_query = """ INSERT INTO users (userId, roomId, lastVideoStill)
                                    VALUES (?, ?, ?); """
        data_tuple = (userId, roomId, photo)
        cursor.execute(sql_insert_blob_query, data_tuple)
        conn.commit()
        print("Image inserted successfully as a BLOB into users table.")
        cursor.close()
    
    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("Db connection is closed.")

# For use with storing a bytestream image
def update_BLOB(userId, photo):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        print("Connected to SQLite db.")
        sql_insert_blob_query = """ UPDATE users 
                                    SET lastVideoStill = ?
                                    WHERE userId = ?; """
        data_tuple = (photo, userId)
        cursor.execute(sql_insert_blob_query, data_tuple)
        conn.commit()
        print("Image updated successfully as a BLOB into users table.")
        cursor.close()
    
    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("Db connection is closed.")


def insert_user_emotions(userId, data):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        print("Connected to SQLite db.")
        sql_insert_blob_query = """ INSERT INTO users (userId, emotionData)
                                    VALUES (?, ?); """
        data_tuple = (userId, photo)
        cursor.execute(sql_insert_blob_query, data_tuple)
        conn.commit()
        print(f"Successfully inserted user {userId}'s emotion data.")
        cursor.close()
    
    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("Db connection is closed.")


# What gets called when new emotion data comes in
def update_user_emotions(userId, data):
    try:
        print(data)
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        print("Connected to SQLite db.")
        sql_insert_blob_query = """ UPDATE users 
                                    SET emotionData = ?
                                    WHERE userId = ?; """
        data_tuple = (str(data), userId)
        cursor.execute(sql_insert_blob_query, data_tuple)
        conn.commit()
        print(f"Successfully updated user {userId}'s emotion data.")
        cursor.close()
    
    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("Db connection is closed.")