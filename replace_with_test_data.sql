DELETE FROM rooms;
DELETE FROM users;
DELETE FROM song_history;

INSERT INTO rooms VALUES (001, null);
INSERT INTO rooms VALUES (002, null);
INSERT INTO rooms VALUES (003, "Anger");

INSERT INTO users (userId, roomId, lastVideoStill) VALUES (100, 001, null);
INSERT INTO users (userId, roomId, lastVideoStill) VALUES (101, 001, null);
INSERT INTO users (userId, roomId, lastVideoStill) VALUES (102, 002, null);
INSERT INTO users (userId, roomId, lastVideoStill) VALUES (103, 003, null);

INSERT INTO song_history (roomId, songId, timePlayed) VALUES (001, "boppin", null);
INSERT INTO song_history (roomId, songId, timePlayed) VALUES (001, "boppin2", null);
INSERT INTO song_history (roomId, songId, timePlayed) VALUES (001, "boppin3", null);
INSERT INTO song_history (roomId, songId, timePlayed) VALUES (003, "anger song", null);