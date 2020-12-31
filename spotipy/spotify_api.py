# Handling calls to Spotify Web API.

import requests
import time
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

## Spotify calls requiring user sign in (not used) ##
## https://developer.spotify.com/documentation/web-api/reference/player/ ##

# Global variables 
BASE_PLAYER_URL = f'{BASE_API_URL}/me/player'

# Get info about the current user's devices
def user_player_devices(token):
    global BASE_PLAYER_URL

    url = f'{BASE_PLAYER_URL}/devices'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(url, headers=headers).json()

    return res

# Transfer a user's playback to devices
def change_player_devices(token, devices):
    global BASE_PLAYER_URL

    url = f'{BASE_PLAYER_URL}/'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'device_ids': devices,
        'play': True
    }
    res = requests.get(url, headers=headers, data=payload).json()

    return res

# Add a track to queue
def add_to_queue(token, track_uri):
    global BASE_PLAYER_URL

    url = f'{BASE_PLAYER_URL}/queue?uri={track_uri}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.post(url, headers=headers).json()

    return res

# Start/resume playback
def play(token):
    global BASE_PLAYER_URL

    url = f'{BASE_PLAYER_URL}/play'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.put(url, headers=headers).json()

    return res

# Pause playback
def pause(token):
    global BASE_PLAYER_URL

    url = f'{BASE_PLAYER_URL}/pause'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.put(url, headers=headers).json()

    return res

# Skip to next track
def next_track(token):
    global BASE_PLAYER_URL

    url = 'f{BASE_PLAYER_URL}/next'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    res = requests.post(url, headers=headers).json()

    return res