DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS rooms(
    roomId INTEGER PRIMARY KEY,
    accessToken TEXT,
    refreshToken TEXT,
    tokenExpireTime TEXT,
    playlistId TEXT,
    isPlaying INTEGER NOT NULL DEFAULT(0)
);

CREATE TABLE IF NOT EXISTS users(
    userId INTEGER PRIMARY KEY,
    roomId INTEGER NOT NULL,
    emotionData TEXT,
    spotifyDevice TEXT,
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);