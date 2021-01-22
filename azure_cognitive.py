import json
import requests
from flask import jsonify

# Azure properties
SUBSCRIPTION_KEY = 'a7f97fe3646d49dea6a12ede3c1c7804'
RESOURCE_ENDPOINT = 'https://test498.cognitiveservices.azure.com'
FACE_URL = RESOURCE_ENDPOINT + '/face/v1.0/detect'

# Get emotion from a single image provided as a url
def emotion(image_url):
    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }
    response = requests.post(FACE_URL, params=params, headers=headers, json={"url": image_url}, verify=False)
    return jsonify(response.json())