CREATE TABLE IF NOT EXISTS rooms(
    roomId INTEGER PRIMARY KEY,
    spotifyPlaylistId TEXT,
    spotifyPlaylistURI TEXT,
    averageEmotion NVARCHAR(10)
);

CREATE TABLE IF NOT EXISTS users(
    userId INTEGER PRIMARY KEY,
    roomId INTEGER,
    emotionData TEXT,
    lastVideoStill BLOB,
    spotifyAccessToken TEXT,
    spotifyRefreshToken TEXT,
    spotifyAccessTime DATETIME,
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);

CREATE TABLE IF NOT EXISTS song_history(
    id INTEGER PRIMARY KEY,
    roomId INTEGER NOT NULL,
    songId NVARCHAR(50) NOT NULL,
    timePlayed DATETIME,
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);