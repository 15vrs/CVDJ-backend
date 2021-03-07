-- DROP TABLE rooms;
-- DROP TABLE users;

CREATE TABLE IF NOT EXISTS rooms(
    roomId INTEGER PRIMARY KEY,
    spotifyRoom TEXT
    -- spotifyPlaylistId TEXT,
    -- spotifyAccessToken TEXT,
    -- averageEmotion NVARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    userId INTEGER PRIMARY KEY,
    roomId INTEGER NOT NULL,
    emotionData TEXT,
    spotifyDevice TEXT,
    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
);