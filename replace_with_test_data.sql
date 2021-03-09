DELETE FROM rooms;
DELETE FROM users;

INSERT INTO rooms VALUES (1, 
                          'BQDi23QDxX5MFHjvy7PV2pz7dlqFCcsISfvvh-Tprdt1KAd4UfCBo0O9faJH9ZIJlgtvGEKWp4j_JDgnQq5iNFq-qE3fg3rhPRQZekWil2KyWdXWhTh8ukZzbpNkLMZIIxIUmO7_sbiWDragFnIDRbbwfNKCfcPtXnXagJc_i7kOFmef8usndjaDSpcIN37a6tfKnl9hZ-wES0yymdNQP0FVBnDrRKq3M_81MVdJrwzEwwCwN0Zz4m072sXC',
                          'AQC-gL7DnvESak5L8yTZ8UJM1Tq95Bwh_jifKb-8uakbPtmm0hZKUrxmBZIiWrjzcJ16qMlMLlxSUSH-EKrLT-tCEqkCLq0Az0qs6hkp5HtRxZ6gJCKGts_TIcbUbvWTENQ',
                          '1615301838',
                          '6rzDJ7iqTwKjVsqHf7oxTy',
                          0);
INSERT INTO rooms VALUES (2, 
                          'BQDi23QDxX5MFHjvy7PV2pz7dlqFCcsISfvvh-Tprdt1KAd4UfCBo0O9faJH9ZIJlgtvGEKWp4j_JDgnQq5iNFq-qE3fg3rhPRQZekWil2KyWdXWhTh8ukZzbpNkLMZIIxIUmO7_sbiWDragFnIDRbbwfNKCfcPtXnXagJc_i7kOFmef8usndjaDSpcIN37a6tfKnl9hZ-wES0yymdNQP0FVBnDrRKq3M_81MVdJrwzEwwCwN0Zz4m072sXC',
                          'AQC-gL7DnvESak5L8yTZ8UJM1Tq95Bwh_jifKb-8uakbPtmm0hZKUrxmBZIiWrjzcJ16qMlMLlxSUSH-EKrLT-tCEqkCLq0Az0qs6hkp5HtRxZ6gJCKGts_TIcbUbvWTENQ',
                          '1615301838',
                          '6rzDJ7iqTwKjVsqHf7oxTy',
                          0);
INSERT INTO rooms VALUES (3,
                          'BQDi23QDxX5MFHjvy7PV2pz7dlqFCcsISfvvh-Tprdt1KAd4UfCBo0O9faJH9ZIJlgtvGEKWp4j_JDgnQq5iNFq-qE3fg3rhPRQZekWil2KyWdXWhTh8ukZzbpNkLMZIIxIUmO7_sbiWDragFnIDRbbwfNKCfcPtXnXagJc_i7kOFmef8usndjaDSpcIN37a6tfKnl9hZ-wES0yymdNQP0FVBnDrRKq3M_81MVdJrwzEwwCwN0Zz4m072sXC',
                          'AQC-gL7DnvESak5L8yTZ8UJM1Tq95Bwh_jifKb-8uakbPtmm0hZKUrxmBZIiWrjzcJ16qMlMLlxSUSH-EKrLT-tCEqkCLq0Az0qs6hkp5HtRxZ6gJCKGts_TIcbUbvWTENQ',
                          '1615301838',
                          '6rzDJ7iqTwKjVsqHf7oxTy',
                          0);

INSERT INTO users (userId, roomId, emotionData) VALUES (1, 1, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (2, 1, '{"anger": 0.575, "contempt": 0, "disgust": 0.006, "fear": 0.008, "happiness": 0.394, "neutral": 0.013, "sadness": 0, "surprise": 0.004}');
INSERT INTO users (userId, roomId, emotionData) VALUES (3, 2, '{"anger": 0.0, "contempt": 0.0, "disgust": 1.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0}');
INSERT INTO users (userId, roomId, emotionData) VALUES (4, 3, '{"anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 0.0, "neutral": 0.0, "sadness": 1.0, "surprise": 0.0}');