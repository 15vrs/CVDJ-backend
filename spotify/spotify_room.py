from threading import Timer
from spotify.spotify_api import SpotifyApi
from spotify.rooms import insert_room, delete_room, set_emotion, get_users_emotions, get_spotify_devices

THRESHOLD = 0.09

## Spotify room object.
class SpotifyRoom(SpotifyApi):

    def __init__(self, code, redirect_uri):
        self.id = insert_room() # id, emotion, users emotions set, users device_ids set
        super().__init__(code, redirect_uri)
        self.room_update()

        # Playback data.
        self.is_playing = False
        self.progress = 0
        self.song = None
        self.artist = None
        self.album_art = None

    def __del__(self):
        delete_room(self.id)

    # Transfer playback to new device id.
    def room_transfer(self, device_id):
        self.transfer(device_id, self.is_playing)

        # Update playback data.
        self.is_playing = False
        playback_data = self.get_playback()
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

    # Start/resume play for all users.
    def room_play(self):

        # Avoid call if room is already playing.
        if not self.is_playing:
            devices = get_spotify_devices(self.id)
            for i in devices:
                if i is not None:
                    self.play(i, self.playlist_id, self.progress)

            # Update playback data.
            playback_data = self.get_playback()
            self.is_playing = False
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
    def room_pause(self):
        devices = get_spotify_devices(self.id)
        for i in devices:
            if i is not None:
                self.pause(i)

        # Update playback data.
        self.is_playing = False
        playback_data = self.get_playback()
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
    def room_skip_next(self):
        devices = get_spotify_devices(self.id)
        for i in devices:
            if i is not None:
                self.skip_next(i)

        # Update playback data.
        self.is_playing = False
        playback_data = self.get_playback()
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
    def room_skip_previous(self):
        devices = get_spotify_devices(self.id)
        for i in devices:
            if i is not None:
                self.skip_previous(i)

        # Update playback data.
        self.is_playing = False
        playback_data = self.get_playback()
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

        return {
            'song': self.song,
            'artist': self.artist,
            'albumArt': self.album_art
        }

    # Update room emotion and playlist.
    def room_update(self):
        #TODO:
        Timer(5.0, self.room_update).start()
        print("DEBUG")

        user_emotions = get_users_emotions(self.id)
        num_users = len(user_emotions)
        if num_users > 0:
            emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral':0, 'sadness': 0, 'surprise': 0}
            for e in emotions:
                emotions[e] = sum([i[e] for i in user_emotions]) / num_users
            emotion = max(emotions, key=emotions.get)
            set_emotion(emotion)

            existing = self.get_playlist_tracks(self.playlist_id)
            energy = self.__room_energy(emotions)
            valence = self.__room_valence(emotions)

            # Find a new track id to add to playlist.
            new_track_id = 0
            playlist_ids = self.search_playlist(emotion)
            for i in playlist_ids:
                track_ids = self.get_playlist_tracks(i)
                audio_features = self.get_audio_features(track_ids)
                for j in audio_features:
                    check_duplicate = (j['id'] in existing)
                    check_energy = (abs(j['energy'] - energy) < THRESHOLD)
                    check_valence = (abs(j['valence'] - valence) < THRESHOLD)
                    if check_duplicate and check_energy and check_valence:
                        new_track_id = j['id']
                        break

            # Add new track to playlist.
            self.add_track_to_playlist(new_track_id, self.playlist_id)

    ## Private helper functions.
    def __room_energy(self, emotions):
        A = emotions['anger']
        C = emotions['contempt']
        D = emotions['disgust']
        F = emotions['fear']
        H = emotions['happiness']
        # N = emotions['neutral']
        # SA = emotions['sadness']
        SU = emotions['surprise']
        energy = (5*SU + 4*A + 3*F + 2*C + 2*D + H) / 5
        return energy

    def __room_valence(self, emotions):
        A = emotions['anger']
        C = emotions['contempt']
        D = emotions['disgust']
        F = emotions['fear']
        H = emotions['happiness']
        # N = emotions['neutral']
        SA = emotions['sadness']
        SU = emotions['surprise']
        valence = ((H+SU) - (A+C+D+F+SA) + 1) / 2
        return valence
