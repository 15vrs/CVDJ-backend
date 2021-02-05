import base64
import glob
import json
from io import BytesIO

import requests
from azure.cognitiveservices.vision.face import FaceClient
from flask import jsonify
from msrest.authentication import CognitiveServicesCredentials
from database.store_image import insert_BLOB, update_user_emotions, update_BLOB
from database.retrieve_image import read_image_BLOB_data

# Azure properties
SUBSCRIPTION_KEY = 'a7f97fe3646d49dea6a12ede3c1c7804'
RESOURCE_ENDPOINT = 'https://test498.cognitiveservices.azure.com'
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
    response = requests.post(FACE_URL, params=params, headers=headers, json={"url": image_url}, verify=False)
    json_response = extract_json(response.text)
    j = json.loads(json_response)
    return j["faceAttributes"]


def extract_json(data):
    return data[1:-1]

# Needs to have userId as an input
def emotion_with_stream(data):
    userId = data['userId']
    image = data['image']
    stream = BytesIO(image)
    response = face_client.face.detect_with_stream(stream, return_face_id=True, return_face_attributes=['emotion'])
    for face in response:
        save_emotion_data(userId, face.face_attributes.emotion)
    if len(response) == 1:
        return str(response[0].face_attributes.emotion)
    return "More than one face"


def save_emotion_data(userId, data):
    emotion = {
        "anger": data.anger,
        "contempt": data.contempt,
        "disgust": data.disgust,
        "fear": data.fear,
        "happiness": data.happiness,
        "neutral": data.neutral,
        "sadness": data.sadness,
        "surprise": data.surprise
    }
    update_user_emotions(userId, data)
