import pymssql
from pymssql import Error

server = 'cvdj.database.windows.net'
database = 'cvdj'
username = 'cvdjadmin'
password = 'elec498!' 

conn = pymssql.connect(server, username, password, database)
cursor = conn.cursor()
try:
    cursor.execute("""  DROP TABLE IF EXISTS users;
                        DROP TABLE IF EXISTS rooms;

                        CREATE TABLE rooms(
                            roomId INTEGER NOT NULL IDENTITY PRIMARY KEY,
                            accessToken TEXT,
                            refreshToken TEXT,
                            tokenExpireTime INTEGER,
                            playlistId TEXT,
                            isPlaying INTEGER NOT NULL DEFAULT(0)
                        );
                                                
                        CREATE TABLE users(
                            userId INTEGER NOT NULL IDENTITY PRIMARY KEY,
                            roomId INTEGER NOT NULL,
                            emotionData TEXT,
                            spotifyDevice TEXT,
                            FOREIGN KEY (roomId) REFERENCES rooms (roomId)
                        );""")
    conn.commit()

except Error as e:
    conn.rollback()
    print(e)

finally:
    cursor.close()
    conn.close()