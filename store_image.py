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
        # create user entry first then update?? 
        sql_insert_blob_query = """ INSERT INTO users (userId, roomId, lastVideoStill)
                                    VALUES (?, ?, ?); """
        binary_photo = convert_to_binary_data(photo)
        data_tuple = (userId, roomId, binary_photo)
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

insert_BLOB(200, 2, "physics crew.jpg")