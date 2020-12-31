# Handle calls to authorize accounts with spotify.

import requests
import time
import random
from urllib.parse import urlencode

# Authorization variables
CLIENT_ID = 'ce5b366904544b58beb4a235b44ffc6c'
CLIENT_SECRET = '9cbf5485772e4527b806a5619a7d6f39'
REDIRECT_URI = 'http://127.0.0.1:5000/callback/'

TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

# Client credential flow
def client_credientials():
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL

    payload = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'grant_type': 'client_credentials',
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    return res_data['access_token'], res_data['expires_in'], time.time()

# Authorization code flow
def authorization_code():
    global CLIENT_ID, REDIRECT_URI, AUTHORIZE_URL

    state = ''
    for _ in range(16):
        state += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

    scope = 'user-read-playback-state user-modify-playback-state'

    query_dict = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scope,
        'show_dialog': False
    }
    query_string = f'{AUTHORIZE_URL}?{urlencode(query=query_dict)}'

    return query_string, state

def get_access_token(code):
    global CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL
    
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    access_token = res_data['access_token']
    refresh_token = res_data['refresh_token']
    expires_in = res_data['expires_in']

    return access_token, refresh_token, expires_in, time.time()

def refresh_access_token(refresh_token):
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL

    payload = {
        'grant-type': 'refresh_token',
        'refresh_token': refresh_token
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    access_token = res_data['access_token']
    expires_in = res_data['expires_in']

    return access_token, expires_in, time.time()