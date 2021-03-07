# Handling calls to Spotify Web API.
import requests
import time
import json
import math
import urllib.parse as urlparse
from urllib.parse import urlencode

# Global variables
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_URL = 'https://api.spotify.com/v1'
PLAYER_URL = 'https://api.spotify.com/v1/me/player'
CLIENT_ID = 'ce5b366904544b58beb4a235b44ffc6c'
CLIENT_SECRET = '9cbf5485772e4527b806a5619a7d6f39'

class SpotifyApi:
    
    def __init__(self, code, redirect_uri):
        try:
            self.__get_access_token(code, redirect_uri)
            self.__get_user_id()
            self.__create_playlist()
        except:
            self.refresh_token = None
            self.access_token = None
            self.expire_time = None

            self.user_id = None
            self.playlist_id = None

    # Get access token.
    def get_token(self):
        try:
            if (time.time() > self.expire_time):
                self.__refresh_access_token()
        finally:
            return self.access_token

    ## TOKEN: Authorization code flow - https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    # Request refresh and access tokens.
    def __get_access_token(self, code, redirect_uri):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'{redirect_uri}/callback/'
        }

        res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload).json()

        self.refresh_token = res['refresh_token']
        self.access_token = res['access_token']
        self.expire_time = math.floor(time.time() + res['expires_in'])

    # Request a refreshed access token.
    def __refresh_access_token(self):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload).json()

        self.access_token = res['access_token']
        self.expire_time = math.floor(time.time() + res['expires_in'])

    ## API
    # Get Spotify user id.
    # https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids
    def __get_user_id(self):
        url = f'{API_URL}/me'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        res = requests.get(url, headers=headers).json()
        self.user_id = res['id']
    
    # Create a playlist
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-create-playlist
    def __create_playlist(self, room_id):
        token = self.get_token()
            
        url = f'{API_URL}/users/{self.user_id}/playlists'
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
        self.playlist_id = res['id']

    # Search playlists
    # https://developer.spotify.com/documentation/web-api/reference/search/search/
    def search_playlist(self, query):
        token = self.get_token()
        playlist_ids = []

        params = {
            'q': query,
            'type': 'playlist',
            'limit': 50, # maximum limit
        }

        search_url = f'{API_URL}/search?q={query}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        res = requests.get(search_url, headers=headers).json()
        items = res['playlists']['items']

        try:
            playlist_ids = [i['id'] for i in items if i['id'] is not None]
        finally:
            return playlist_ids

    # Get audio features
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-features
    def get_audio_features(self, track_ids):
        token = self.get_token()
        audio_features = []

        x = ','.join([i for i in track_ids if i is not None])

        url = f'{API_URL}/audio-features/?ids={x}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        res = requests.get(url, headers=headers).json()

        try:
            audio_features = list(res['audio_features'])
        finally:
            return audio_features

    # Get the track ids that are on the given playlist.
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-playlists-tracks
    def get_playlist_tracks(self, playlist_id):
        token = self.get_token()
        track_ids = []

        url = f'{API_URL}/playlists/{playlist_id}/tracks'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        res = requests.get(url, headers=headers).json()
        
        try:
            track_ids = [i['track']['id'] for i in res['items'] if i['track'] is not None]
        finally:
            return track_ids

    # Add track to playlist
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-add-tracks-to-playlist
    def add_track_to_playlist(self, track_id):
        token = self.get_token()
            
        url = f'{API_URL}/playlists/{self.playlist_id}/tracks'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'uris': [f'spotify:track:{track_id}']
        }
        requests.post(url, headers=headers, data=json.dumps(payload)).json()

    ## PLAYER - https://developer.spotify.com/documentation/web-api/reference/#category-player
    # Get the user's current playback.
    def get_playback(self):
        token = self.get_token()
        playback_data = None
            
        url = f'{PLAYER_URL}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            playback_data = requests.get(url, headers=headers).json()
        finally:
            return playback_data

    # Transfer a user's playback.
    def transfer(self, ids, play):
        token = self.get_token()

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'device_ids': [ids],
            'play': play
        }
        requests.put(PLAYER_URL, headers=headers, data=json.dumps(payload))

    # Start/resume a user's playback.
    def play(self, device_id, uri, position):
        token = self.get_token()

        url = f'{PLAYER_URL}/play?device_id={device_id}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'context_uri': uri,
            'position_ms': position
        }
        requests.put(url, headers=headers, data=json.dumps(payload))

    # Pause a user's playback.
    def pause(self, device_id):
        token = self.get_token()

        url = f'{PLAYER_URL}/pause?device_id={device_id}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        requests.put(url, headers=headers)

    # Skip user's playback to next track.
    def skip_next(self, device_id):
        token = self.get_token()

        url = f'{PLAYER_URL}/next?device_id={device_id}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        requests.post(url, headers=headers)

    # Skip user's playback to previous track
    def skip_previous(self, device_id):
        token = self.get_token()

        url = f'{PLAYER_URL}/previous?device_id={device_id}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        requests.post(url, headers=headers)
