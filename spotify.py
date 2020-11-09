# Import statements
import base64
import json
import requests
import time

# Authorization variables
CLIENT_ID = 'ce5b366904544b58beb4a235b44ffc6c'
CLIENT_SECRET = '9cbf5485772e4527b806a5619a7d6f39'
TOKEN_URL = f'https://accounts.spotify.com/api/token'

# Client credential authorization flow
def auth_client_credientials():
    global CLIENT_ID, CLIENT_SECRET, TOKEN_URL

    payload = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'grant_type': 'client_credentials',
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    return res_data['access_token'], res_data['expires_in'], time.time()

# Global variables
BEARER_TOKEN, EXPIRES_IN, START_TIME = auth_client_credientials()
BASE_API_URL = f'https://api.spotify.com/v1'

# Search
def search(query):
    global BASE_API_URL, BEARER_TOKEN, EXPIRES_IN, START_TIME

    if (time.time() - START_TIME) > EXPIRES_IN:
        BEARER_TOKEN, EXPIRES_IN, START_TIME = auth_client_credientials()

    # possible_types = 'album,artist,playlist,track,show,episode'
    # market = 'US'
    # limit = 1
    # offset = 0
    types = 'track'
    search_url = f'{BASE_API_URL}/search?q={query}&type={types}'

    payload={}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }

    res = requests.get(search_url, data=payload, headers=headers)
    res_data = res.json()

    return res_data