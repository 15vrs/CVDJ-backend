DELETE FROM rooms;
DELETE FROM creators;
DELETE FROM users;

INSERT INTO rooms VALUES (1, '6rzDJ7iqTwKjVsqHf7oxTy', null);
INSERT INTO rooms VALUES (2, '6rzDJ7iqTwKjVsqHf7oxTy', null);
INSERT INTO rooms VALUES (3, '6rzDJ7iqTwKjVsqHf7oxTy', null);

INSERT INTO creators VALUES (1, 1, 1, 'BQAni4fsVS8lq73Hn3_LlBBYAXMXpBfOjVpYyWRv6YehLIEnPWBiIm8chgL5XPP2XqXlyx-VaaaPoBcZ8vGDIJFAQnaz1UAuX_wQtRxxTGOoxvX6BEGsz29JdWHAFI7u9a-ue8YGQbWcrJcexMGKbfty8DOGNzfYM6l-zZXzUup3aEV2PxND9Gdv1nHpBiQkJSeRSXj2xF17JrMMyfux6Q8vok0J_wHn2Zy-naR3-R-qRaH0kRezOkg8S6zd4otHNAy_aN5KDA',	'AQBUJNwr0p72EKkaPJcSv1MRfkWSN6tlA_CMIYv2zTiMW7G39uIoxzABnP0ARw2FePjiwmJ-Jk2IVgYBsmsBApFdPb96_GrbwvdPt-n1exFkLlQV4u8xNQV2pWuK3cGE86o', 1613661592.41431);
INSERT INTO creators VALUES (2, 3, 2, 'BQAni4fsVS8lq73Hn3_LlBBYAXMXpBfOjVpYyWRv6YehLIEnPWBiIm8chgL5XPP2XqXlyx-VaaaPoBcZ8vGDIJFAQnaz1UAuX_wQtRxxTGOoxvX6BEGsz29JdWHAFI7u9a-ue8YGQbWcrJcexMGKbfty8DOGNzfYM6l-zZXzUup3aEV2PxND9Gdv1nHpBiQkJSeRSXj2xF17JrMMyfux6Q8vok0J_wHn2Zy-naR3-R-qRaH0kRezOkg8S6zd4otHNAy_aN5KDA',	'AQBUJNwr0p72EKkaPJcSv1MRfkWSN6tlA_CMIYv2zTiMW7G39uIoxzABnP0ARw2FePjiwmJ-Jk2IVgYBsmsBApFdPb96_GrbwvdPt-n1exFkLlQV4u8xNQV2pWuK3cGE86o', 1613661592.41431);
INSERT INTO creators VALUES (3, 4, 3, 'BQAni4fsVS8lq73Hn3_LlBBYAXMXpBfOjVpYyWRv6YehLIEnPWBiIm8chgL5XPP2XqXlyx-VaaaPoBcZ8vGDIJFAQnaz1UAuX_wQtRxxTGOoxvX6BEGsz29JdWHAFI7u9a-ue8YGQbWcrJcexMGKbfty8DOGNzfYM6l-zZXzUup3aEV2PxND9Gdv1nHpBiQkJSeRSXj2xF17JrMMyfux6Q8vok0J_wHn2Zy-naR3-R-qRaH0kRezOkg8S6zd4otHNAy_aN5KDA',	'AQBUJNwr0p72EKkaPJcSv1MRfkWSN6tlA_CMIYv2zTiMW7G39uIoxzABnP0ARw2FePjiwmJ-Jk2IVgYBsmsBApFdPb96_GrbwvdPt-n1exFkLlQV4u8xNQV2pWuK3cGE86o', 1613661592.41431);

INSERT INTO users (userId, roomId, emotionData) VALUES (1, 1, '{"anger": 1.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (2, 1, '{"anger": 0.575, "contempt": 0, "disgust": 0.006, "fear": 0.008, "happiness": 0.394, "neutral": 0.013, "sadness": 0, "surprise": 0.004}');
INSERT INTO users (userId, roomId, emotionData) VALUES (3, 2, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (4, 3, '{"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 1.0, "surprise": 0.0}');