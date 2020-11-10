import json
import requests
from flask import jsonify

# Azure properties
SUBSCRIPTION_KEY = 'a7f97fe3646d49dea6a12ede3c1c7804'
RESOURCE_ENDPOINT = 'https://test498.cognitiveservices.azure.com'

# Get emotion from a single image containing a face
def emotion():
    FACE_URL = RESOURCE_ENDPOINT + '/face/v1.0/detect'

    image_url = 'https://image.cnbcfm.com/api/v1/image/106202554-1571960310657gettyimages-1182969985.jpeg'

    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'emotion',
        'returnFaceId': 'true'
    }

    response = requests.post(FACE_URL, params=params, headers=headers, json={"url": image_url}, verify=False)

    return jsonify(response.json())