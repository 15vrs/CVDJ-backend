# Handle calls to authorize accounts with spotify.

import requests
import time
from urllib.parse import urlencode

# Authorization variables
CLIENT_ID = 'ce5b366904544b58beb4a235b44ffc6c'
CLIENT_SECRET = '9cbf5485772e4527b806a5619a7d6f39'

TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

## Client credential flow
def client_credientials():
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL

    payload = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'grant_type': 'client_credentials',
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    return res_data['access_token'], res_data['expires_in'], time.time()

## Authorization code flow
def get_access_token(code, redirect_uri):
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL
    
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': f'{redirect_uri}/callback/'
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    access_token = res_data['access_token']
    refresh_token = res_data['refresh_token']

    return access_token, refresh_token, time.time()

def refresh_access_token(refresh_token):
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    access_token = res_data['access_token']

    return access_token, time.time()