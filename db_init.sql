CREATE TABLE IF NOT EXISTS rooms(
    roomId INTEGER PRIMARY KEY,
    spotifyPlaylistId TEXT,
    averageEmotion NVARCHAR(10)
);

CREATE TABLE IF NOT EXISTS creators(
    creatorId INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    roomId INTEGER,
    spotifyAccessToken TEXT,
    spotifyRefreshToken TEXT,
    spotifyAccessTime DATETIME,
    FOREIGN KEY (userId) REFERENCES users (userId),
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);

CREATE TABLE IF NOT EXISTS users(
    userId INTEGER PRIMARY KEY,
    roomId INTEGER,
    lastVideoStill BLOB,
    emotionData TEXT,
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);