# Handling calls to Spotify Web API.

import requests
import time
import json
from spotipy.spotify_auth import client_credientials

## Spotify calls not requiring user sign in ##
## https://developer.spotify.com/documentation/web-api/reference/search/search/
## https://developer.spotify.com/documentation/web-api/reference/tracks/

# Global variables
BEARER_TOKEN, EXPIRES_IN, START_TIME = client_credientials()
BASE_API_URL = 'https://api.spotify.com/v1'

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
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    res = requests.get(search_url, headers=headers).json()

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
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    res = requests.get(url, headers=headers).json()

    # Return spotify results as json object
    return res

## Spotify API calls requiring user sign-in ##
## https://developer.spotify.com/documentation/web-api/reference-beta/#category-playlists
## https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-current-users-profile

def get_user_id(token):
    global BASE_API_URL

    url = f'{BASE_API_URL}/me'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers).json()

    return res['id']

# Create a playlist
def create_playlist(token, user_id, room_id):
    global BASE_API_URL

    url = f'{BASE_API_URL}/users/{user_id}/playlists'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'name': f'CVDJ Room #{room_id} Playlist',
        'public': True,
        'collaborative': False,
        'description': None
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload)).json()

    # Return playlist ID and playlist URI
    return res['id'], res['uri']
