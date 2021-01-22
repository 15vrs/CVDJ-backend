import json
import requests
from flask import jsonify
from store_image import store_image
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import glob
import base64
from io import BytesIO

# Azure properties
SUBSCRIPTION_KEY = 'a7f97fe3646d49dea6a12ede3c1c7804'
RESOURCE_ENDPOINT = 'https://test498.cognitiveservices.azure.com'
FACE_URL = RESOURCE_ENDPOINT + '/face/v1.0/detect'

face_client = FaceClient(RESOURCE_ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

# Get emotion from a single image provided as a url
def emotion(image_url):
    # store_image(image_url)
    # response = requests.get('http://localhost:4200/82db2fd4-5b7d-4040-86eb-8a92e97b1c98')
    # print(response)

    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }
    response = requests.post(FACE_URL, params=params, headers=headers, json={"url": image_url}, verify=False)
    return jsonify(response.json())

def emotion_with_stream():
    # test_image = glob.glob('test-url.txt')
    with open('test-url.txt', 'r') as file:
        data = file.read()
    
    with open('test.png', 'wb') as file:
        file.write(base64.decodebytes(data))
    # image = open(test_image[0], 'r+b')
    # img = data.encode('utf-8')
    print(type(data))
    tt = data.encode('utf-8')
    # bytes_img = base64.decodebytes(tt)
    face = face_client.face.detect_with_stream(tt, detectionModel='detection_02')
    print(face)