DELETE FROM rooms;
DELETE FROM creators;
DELETE FROM users;

INSERT INTO rooms VALUES (1, null, null);
INSERT INTO rooms VALUES (2, null, null);
INSERT INTO rooms VALUES (3, "Anger", null);

INSERT INTO creators (creatorId, userId, roomId) VALUES (1, 1, 1);
INSERT INTO creators (creatorId, userId, roomId) VALUES (2, 3, 2);
INSERT INTO creators (creatorId, userId, roomId) VALUES (3, 4, 3);

INSERT INTO users (userId, roomId) VALUES (1, 1);
INSERT INTO users (userId, roomId) VALUES (2, 1);
INSERT INTO users (userId, roomId) VALUES (3, 2);
INSERT INTO users (userId, roomId) VALUES (4, 3);