import json
from io import BytesIO
import requests

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import database.users as users

# Azure properties
SUBSCRIPTION_KEY = 'bc67fef798e4492a9cff3ee6d0000b19'
RESOURCE_ENDPOINT = 'https://cvdj-face.cognitiveservices.azure.com/'
FACE_URL = RESOURCE_ENDPOINT + '/face/v1.0/detect'

face_client = FaceClient(RESOURCE_ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

# Get emotion from a single image provided as a url
def emotion(image_url):
    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }
    response = requests.post(FACE_URL, params=params, headers=headers, json={'url': image_url}, verify=False)
    json_response = __extract_json(response.text)
    j = json.loads(json_response)
    return j['faceAttributes']

# Needs to have userId as an input
def emotion_with_stream(user_id, data):
    userId = user_id
    image = data
    stream = BytesIO(image)
    response = face_client.face.detect_with_stream(stream, return_face_id=True, return_face_attributes=['emotion'])
    if len(response) == 1:
        data = save_emotion_data(userId, response[0].face_attributes.emotion)
        return json.dumps(str(data))
    elif len(response) > 1:
        data = average_emotion_data(userId, response)
        return json.dumps(str(data))
    else:
        return json.dumps(str({
        'anger': 0,
        'contempt': 0,
        'disgust': 0,
        'fear': 0,
        'happiness': 0,
        'neutral': 0,
        'sadness': 0,
        'surprise': 0
    }))

def average_emotion_data(userId, faces):
    emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'sadness': 0, 'surprise': 0}
    for face in faces:
        emotions['anger'] += face.face_attributes.emotion.anger
        emotions['contempt'] += face.face_attributes.emotion.contempt
        emotions['disgust'] += face.face_attributes.emotion.disgust
        emotions['fear'] += face.face_attributes.emotion.fear
        emotions['happiness'] += face.face_attributes.emotion.happiness
        emotions['sadness'] += face.face_attributes.emotion.sadness
        emotions['surprise'] += face.face_attributes.emotion.surprise
    for e in emotions:
        emotions[e] /= len(faces)
    users.set_emotion_data(userId, emotions)
    return emotions

def save_emotion_data(userId, face):
    emotion = {
        'anger': face.anger,
        'contempt': face.contempt,
        'disgust': face.disgust,
        'fear': face.fear,
        'happiness': face.happiness,
        'neutral': face.neutral,
        'sadness': face.sadness,
        'surprise': face.surprise
    }
    users.set_emotion_data(userId, emotion)
    return emotion

## Private helper functions.
def __extract_json(data):
    return data[1:-1]
