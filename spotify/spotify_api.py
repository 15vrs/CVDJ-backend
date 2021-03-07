# Handling calls to Spotify Web API.
import requests
import time
import json
import math
from urllib.parse import urlencode

# Global variables
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_URL = 'https://api.spotify.com/v1'
PLAYER_URL = 'https://api.spotify.com/v1/me/player'
CLIENT_ID = 'ce5b366904544b58beb4a235b44ffc6c'
CLIENT_SECRET = '9cbf5485772e4527b806a5619a7d6f39'

## TOKEN: Authorization code flow - https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
# Request refresh and access tokens.
def get_access_tokens(code, redirect_uri):
    refresh_token = None
    access_token = None
    expire_time = 0

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': f'{redirect_uri}/callback/'
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload).json()

    try:
        refresh_token = res['refresh_token']
        access_token = res['access_token']
        expire_time = math.floor(time.time() + res['expires_in'])
    finally:
        return refresh_token, access_token, expire_time

# Request a refreshed access token.
def refresh_access_tokens(refresh_token):
    access_token = None
    expire_time = 0

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload).json()

    try:
        access_token = res['access_token']
        expire_time = math.floor(time.time() + res['expires_in'])
    finally:
        return access_token, expire_time

## API
# Get Spotify user id.
# https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids
def get_spotify_id(access_token):
    spotify_id = 0

    url = f'{API_URL}/me'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    res = requests.get(url, headers=headers).json()

    try:
        spotify_id = res['id']
    finally:
        return spotify_id

# Create a playlist
# https://developer.spotify.com/documentation/web-api/reference/#endpoint-create-playlist
def create_playlist(access_token, room_id, spotify_id):
    playlist_id = 0

    url = f'{API_URL}/users/{spotify_id}/playlists'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'name': f'CVDJ Room #{room_id} Playlist',
        'public': True,
        'collaborative': False,
        'description': None
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload)).json()

    try:
        playlist_id = res['id']
    finally:
        return playlist_id

# Search playlists
# https://developer.spotify.com/documentation/web-api/reference/search/search/
def search_playlist(access_token, query):
    playlist_ids = []
    params = urlencode({
        'q': query,
        'type': 'playlist',
        'limit': 50, # maximum limit
    })

    search_url = f'{API_URL}/search?{params}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    res = requests.get(search_url, headers=headers).json()
    items = res['playlists']['items']

    try:
        playlist_ids = [i['id'] for i in items if i['id'] is not None]
    finally:
        return playlist_ids

# Get audio features
# https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-features
def get_audio_features(access_token, track_ids):
    audio_features = []

    x = ','.join([i for i in track_ids if i is not None])

    url = f'{API_URL}/audio-features/?ids={x}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    res = requests.get(url, headers=headers).json()

    try:
        audio_features = list(res['audio_features'])
    finally:
        return audio_features

# Get the track ids that are on the given playlist.
# https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-playlists-tracks
def get_playlist_tracks(access_token, playlist_id):
    track_ids = []

    url = f'{API_URL}/playlists/{playlist_id}/tracks'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    res = requests.get(url, headers=headers).json()
    
    try:
        track_ids = [i['track']['id'] for i in res['items'] if i['track'] is not None]
    finally:
        return track_ids

# Add track to playlist
# https://developer.spotify.com/documentation/web-api/reference/#endpoint-add-tracks-to-playlist
def add_track_to_playlist(access_token, playlist_id, track_id):
    url = f'{API_URL}/playlists/{playlist_id}/tracks'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'uris': [f'spotify:track:{track_id}']
    }
    requests.post(url, headers=headers, data=json.dumps(payload)).json()

## PLAYER - https://developer.spotify.com/documentation/web-api/reference/#category-player
# Get the user's current playback.
def get_playback(access_token):
    playback_data = None
        
    url = f'{PLAYER_URL}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        playback_data = requests.get(url, headers=headers).json()
    finally:
        return playback_data

# Transfer a user's playback.
def transfer(access_token, ids, is_playing):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'device_ids': [ids],
        'play': is_playing
    }
    requests.put(PLAYER_URL, headers=headers, data=json.dumps(payload))

# Start/resume a user's playback.
def play(access_token, device_id, uri, position):
    url = f'{PLAYER_URL}/play?device_id={device_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'context_uri': uri,
        'position_ms': position
    }
    requests.put(url, headers=headers, data=json.dumps(payload))

# Pause a user's playback.
def pause(access_token, device_id):
    url = f'{PLAYER_URL}/pause?device_id={device_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    requests.put(url, headers=headers)

# Skip user's playback to next track.
def skip_next(access_token, device_id):
    url = f'{PLAYER_URL}/next?device_id={device_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    requests.post(url, headers=headers)

# Skip user's playback to previous track
def skip_previous(access_token, device_id):
    url = f'{PLAYER_URL}/previous?device_id={device_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    requests.post(url, headers=headers)
