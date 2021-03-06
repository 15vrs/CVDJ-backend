from spotify.spotify_api import SpotifyApi
from database.rooms import Room

class SpotifyRoom(Room):

    # Create Spotify Room object.
    def __init__(self, code, redirect_uri):

        # Playback data
        self.playlist_id = None
        self.is_playing = False
        self.progress = 0
        self.song = None
        self.artist = None
        self.album_art = None

        self.spotify_api = SpotifyApi(code, redirect_uri)
        Room.__init__(self) # id, emotion, users emotions set, users device_ids set

    ## Getters
    def get_access_token(self):
        return self.spotify_api.get_token()

    # Transfer playback to new device id.
    def transfer(self, device_id):
        self.spotify_api.transfer(device_id, self.is_playing) #API

        # Update room playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

    # Start/resume play for all users.
    def play(self):

        # Avoid call if room is already playing.
        if not self.is_playing:
            devices = self.get_spotify_devices() #ROOM
            for i in devices:
                if i is not None:
                    self.spotify_api.play(i, self.playlist_id, self.progress) #API

            # Update room playback data.
            self.is_playing = False
            playback_data = self.spotify_api.get_playback() #API
            self.progress = playback_data['progress_ms']
            self.song = playback_data['item']['name']
            self.artist = playback_data['item']['artists'][0]['name']
            self.album_art = playback_data['item']['album']['images'][0]['url']

    # Pause play for all users.
    def pause(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.pause(i) #API

        # Update room playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

    # Skip next for all users.
    def skip_next(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.skip_next(i) #API

        # Update room playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

    # Skip previous for all users.
    def skip_previous(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.skip_previous(i) #API

        # Update room playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']