from threading import Timer
from spotify.spotify_api import SpotifyApi
from spotify.rooms import Room

## Spotify room object.
class SpotifyRoom(Room):

    def __init__(self, code, redirect_uri):
        super().__init__() # id, emotion, users emotions set, users device_ids set
        self.spotify_api = SpotifyApi(code, redirect_uri)

        # Playback data.
        self.playlist_id = self.spotify_api.create_playlist(self.id)
        self.is_playing = False
        self.progress = 0
        self.song = None
        self.artist = None
        self.album_art = None

        # Counter for updating room.
        timer = RepeatTimer(5, self.update_room())

    # Return access token.
    def get_access_token(self):
        return self.spotify_api.get_token()

    # Return playlist ID.
    def get_playlist_id(self):
        return self.playlist_id

    # Update room emotion and playlist.
    def update_room(self):
        user_emotion = self.get_user_emotion()
        print("MOCHI")

    # Transfer playback to new device id.
    def transfer(self, device_id):
        self.spotify_api.transfer(device_id, self.is_playing) #API

        # Update playback data.
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

            # Update playback data.
            self.is_playing = False
            playback_data = self.spotify_api.get_playback() #API
            self.progress = playback_data['progress_ms']
            self.song = playback_data['item']['name']
            self.artist = playback_data['item']['artists'][0]['name']
            self.album_art = playback_data['item']['album']['images'][0]['url']

        return {
            'song': self.song,
            'artist': self.artist,
            'albumArt': self.album_art
        }

    # Pause play for all users.
    def pause(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.pause(i) #API

        # Update playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

        return {
            'song': self.song,
            'artist': self.artist,
            'albumArt': self.album_art
        }

    # Skip next for all users.
    def skip_next(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.skip_next(i) #API

        # Update playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

        return {
            'song': self.song,
            'artist': self.artist,
            'albumArt': self.album_art
        }

    # Skip previous for all users.
    def skip_previous(self):
        devices = self.get_spotify_devices() #ROOM
        for i in devices:
            if i is not None:
                self.spotify_api.skip_previous(i) #API

        # Update playback data.
        self.is_playing = False
        playback_data = self.spotify_api.get_playback() #API
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

        return {
            'song': self.song,
            'artist': self.artist,
            'albumArt': self.album_art
        }

## Repeated timer object.
class RepeatTimer(object):

    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False