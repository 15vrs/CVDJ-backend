import pyodbc
from pyodbc import Error

DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = 'tcp:cvdj.database.windows.net'
DATABASE = 'cvdj'
USERNAME = 'cvdjadmin'
PASSWORD = 'elec498!' 

conn = pyodbc.connect('DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
cursor = conn.cursor()
try:
    cursor.execute("""  IF NOT EXISTS (SELECT * FROM rooms)
                            CREATE TABLE rooms(
                                roomId INTEGER NOT NULL IDENTITY PRIMARY KEY,
                                accessToken TEXT,
                                refreshToken TEXT,
                                tokenExpireTime TEXT,
                                playlistId TEXT,
                                isPlaying INTEGER NOT NULL DEFAULT(0)
                            );

                        IF NOT EXISTS (SELECT * FROM users)                        
                            CREATE TABLE users(
                                userId INTEGER NOT NULL IDENTITY PRIMARY KEY,
                                roomId INTEGER NOT NULL,
                                emotionData TEXT,
                                spotifyDevice TEXT,
                                FOREIGN KEY (roomId) REFERENCES rooms (roomId)
                            );
                        
                        INSERT INTO rooms VALUES (
                            'BQDi23QDxX5MFHjvy7PV2pz7dlqFCcsISfvvh-Tprdt1KAd4UfCBo0O9faJH9ZIJlgtvGEKWp4j_JDgnQq5iNFq-qE3fg3rhPRQZekWil2KyWdXWhTh8ukZzbpNkLMZIIxIUmO7_sbiWDragFnIDRbbwfNKCfcPtXnXagJc_i7kOFmef8usndjaDSpcIN37a6tfKnl9hZ-wES0yymdNQP0FVBnDrRKq3M_81MVdJrwzEwwCwN0Zz4m072sXC',
                            'AQC-gL7DnvESak5L8yTZ8UJM1Tq95Bwh_jifKb-8uakbPtmm0hZKUrxmBZIiWrjzcJ16qMlMLlxSUSH-EKrLT-tCEqkCLq0Az0qs6hkp5HtRxZ6gJCKGts_TIcbUbvWTENQ',
                            '1615301838',
                            '6rzDJ7iqTwKjVsqHf7oxTy',
                            0
                        );  
                        """)
    conn.commit()

except Error as e:
    conn.rollback()
    print(e)

finally:
    cursor.close()
    conn.close()