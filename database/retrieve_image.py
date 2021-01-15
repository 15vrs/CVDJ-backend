import sqlite3
from sqlite3 import Error

def write_to_file(userId, image):
    filename = str(userId) + "LVS.png"
    with open(filename, 'wb') as from_db:
        from_db.write(image)
    return filename

def read_image_BLOB_data(userId):
    try:
        conn = sqlite3.connect('cvdj.db')
        cursor = conn.cursor()
        print("Connected to SQLite db.")

        sql_select_blob_query = """ SELECT lastVideoStill
                                    FROM users
                                    WHERE userId = ? """
        cursor.execute(sql_select_blob_query, (userId,))
        row = cursor.fetchone()
        video_still = row[0]
        print(f"Storing last video still in {userId}LVS.png")
        write_to_file(userId, video_still)
        cursor.close()

    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("Db connection is closed.")

read_image_BLOB_data(200)