DELETE FROM rooms;
DELETE FROM users;

INSERT INTO rooms VALUES (1, 'neutral');
INSERT INTO rooms VALUES (2, 'neutral');
INSERT INTO rooms VALUES (3, 'neutral');

INSERT INTO users (userId, roomId, emotionData) VALUES (1, 1, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (2, 1, '{"anger": 0.575, "contempt": 0, "disgust": 0.006, "fear": 0.008, "happiness": 0.394, "neutral": 0.013, "sadness": 0, "surprise": 0.004}');
INSERT INTO users (userId, roomId, emotionData) VALUES (3, 2, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (4, 3, '{"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 1.0, "surprise": 0.0}');