DELETE FROM rooms;
DELETE FROM creators;
DELETE FROM users;

INSERT INTO rooms VALUES (1, '6rzDJ7iqTwKjVsqHf7oxTy', null);
INSERT INTO rooms VALUES (2, '6rzDJ7iqTwKjVsqHf7oxTy', null);
INSERT INTO rooms VALUES (3, '6rzDJ7iqTwKjVsqHf7oxTy', null);

INSERT INTO creators VALUES (1, 1, 1, 'BQBIII2oqlvdxF3L_UNUqWv3kKPOIvh3oVmoDhI6JYR-_-ir32sJb6uiIok3ZZH94TydPIJm8vsF4IOkOcRXXmgfide7UTo0qH08x2NnhRbros73PMOfBuLkhC9jw-Oi1h9tSaOBdw8vqbeBXaDm8jR4mg2qssKPZUD-uL2DdSqIIPAaoOAoqbbGEi3paY9WNDyVumJ59UNYQoBHDSz_LgSZ8PqQj_jWiz7wgF9l5QiJMb9O8g5yUVRPEw', 'AQDYI2f2sl6UbmYwhJ84By9i-p2WG2RPHF1bXe3v35xfh_vbkSluoFTkx4QOeB9k247Fi5-UorgUfITKgmT-eU9DczchFjFyJi1udog9spzMwRhLHpmf0mC7dyYC_pqCPeQ', 1612645692.8018088);
INSERT INTO creators VALUES (2, 3, 2, 'BQBIII2oqlvdxF3L_UNUqWv3kKPOIvh3oVmoDhI6JYR-_-ir32sJb6uiIok3ZZH94TydPIJm8vsF4IOkOcRXXmgfide7UTo0qH08x2NnhRbros73PMOfBuLkhC9jw-Oi1h9tSaOBdw8vqbeBXaDm8jR4mg2qssKPZUD-uL2DdSqIIPAaoOAoqbbGEi3paY9WNDyVumJ59UNYQoBHDSz_LgSZ8PqQj_jWiz7wgF9l5QiJMb9O8g5yUVRPEw', 'AQDYI2f2sl6UbmYwhJ84By9i-p2WG2RPHF1bXe3v35xfh_vbkSluoFTkx4QOeB9k247Fi5-UorgUfITKgmT-eU9DczchFjFyJi1udog9spzMwRhLHpmf0mC7dyYC_pqCPeQ', 1612645692.8018088);
INSERT INTO creators VALUES (3, 4, 3, 'BQBIII2oqlvdxF3L_UNUqWv3kKPOIvh3oVmoDhI6JYR-_-ir32sJb6uiIok3ZZH94TydPIJm8vsF4IOkOcRXXmgfide7UTo0qH08x2NnhRbros73PMOfBuLkhC9jw-Oi1h9tSaOBdw8vqbeBXaDm8jR4mg2qssKPZUD-uL2DdSqIIPAaoOAoqbbGEi3paY9WNDyVumJ59UNYQoBHDSz_LgSZ8PqQj_jWiz7wgF9l5QiJMb9O8g5yUVRPEw', 'AQDYI2f2sl6UbmYwhJ84By9i-p2WG2RPHF1bXe3v35xfh_vbkSluoFTkx4QOeB9k247Fi5-UorgUfITKgmT-eU9DczchFjFyJi1udog9spzMwRhLHpmf0mC7dyYC_pqCPeQ', 1612645692.8018088);

INSERT INTO users (userId, roomId, emotionData) VALUES (1, 1, '{"anger": 1.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (2, 1, '{"anger": 0.575, "contempt": 0, "disgust": 0.006, "fear": 0.008, "happiness": 0.394, "neutral": 0.013, "sadness": 0, "surprise": 0.004}');
INSERT INTO users (userId, roomId, emotionData) VALUES (3, 2, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (4, 3, '{"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 1.0, "surprise": 0.0}');