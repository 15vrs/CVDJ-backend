import base64
import glob
import json
from io import BytesIO

import requests
from azure.cognitiveservices.vision.face import FaceClient
from flask import jsonify
from msrest.authentication import CognitiveServicesCredentials

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

# Will be used to handle image stream from front-end
def emotion_with_stream(test):
    print(test)
    with open('test-url.txt', 'r') as file:
        data = file.read()

    with open('test.png', 'wb') as file:
        file.write(base64.decodebytes(data))
    print(type(data))
    tt = data.encode('utf-8')
    face = face_client.face.detect_with_stream(tt, detectionModel='detection_02')
    print(face)