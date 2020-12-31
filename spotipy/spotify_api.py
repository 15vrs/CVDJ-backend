# Handling calls to Spotify Web API.

import requests
import time

from spotipy.spotify_auth import client_credientials

# Global variables
BEARER_TOKEN, EXPIRES_IN, START_TIME = client_credientials()
BASE_API_URL = 'https://api.spotify.com/v1'
BASE_PLAYER_URL = f'{BASE_API_URL}/me/player'

# Search
def search(emotion, offset):

    # Check OAuth
    global BASE_API_URL, BEARER_TOKEN, EXPIRES_IN, START_TIME
    if (time.time() - START_TIME) > EXPIRES_IN:
        BEARER_TOKEN, EXPIRES_IN, START_TIME = client_credientials()

    # Function variables
    limit = 50
    type = 'track'

    # Call to spotify API
    search_url = f'{BASE_API_URL}/search?q={emotion}&type={type}&limit={limit}&offset={offset}'
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    res = requests.get(search_url, data=payload, headers=headers).json()

    # Return a list of track ids.
    return res

# Get audio features
def get_audio_features(track_ids):

    # Check OAuth
    global BASE_API_URL, BEARER_TOKEN, EXPIRES_IN, START_TIME
    if (time.time() - START_TIME) > EXPIRES_IN:
        BEARER_TOKEN, EXPIRES_IN, START_TIME = client_credientials()

    # Function variables
    x = ','.join(track_ids)

    # Call to spotify API
    url = f'{BASE_API_URL}/audio-features/?ids={x}'
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    res = requests.get(url, data=payload, headers=headers).json()

    # Return spotify results as json object
    return res

# # Get Information About The User's devices
# def user_player_devices(token):
#     global BASE_PLAYER_URL

#     url = f'{BASE_PLAYER_URL}/devices'
#     payload = {}
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}'
#     }
#     res = requests.get(url, data=payload, headers=headers).json()

#     return res