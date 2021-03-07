from threading import Timer
import time
import spotify.spotify_api as spotify_api

THRESHOLD = 0.09

## Spotify room object.
class SpotifyRoom():

    def __init__(self, code, redirect_uri):
        self.refresh_token, self.access_token, self.expire_time = spotify_api.get_access_token(code, redirect_uri)
        self.user_id = None
        self.playlist_id = None

        # Player data.
        self.is_playing = False
        self.progress = 0
        self.song = None
        self.artist = None
        self.album_art = None

    # Transfer playback to new device id.
    def room_transfer(self):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)

        playback_data = spotify_api.get_playback(self.access_token)

        self.is_playing = False
        self.progress = playback_data['progress_ms']
        self.song = playback_data['item']['name']
        self.artist = playback_data['item']['artists'][0]['name']
        self.album_art = playback_data['item']['album']['images'][0]['url']

    # Start/resume play for all users.
    def room_play(self, devices):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)

        # Avoid call if room is already playing.
        if not self.is_playing:
            for i in devices:
                if i is not None:
                    spotify_api.play(self.access_token, i, self.playlist_id, self.progress)
            playback_data = spotify_api.get_playback(self.access_token)

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
    def room_pause(self, devices):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)

        for i in devices:
            if i is not None:
                spotify_api.pause(self.access_token, i)
        playback_data = spotify_api.get_playback(self.access_token)

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

    # Skip next for all users.
    def room_skip_next(self, devices):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)


        for i in devices:
            if i is not None:
                spotify_api.skip_next(self.access_token, i)
        playback_data = spotify_api.get_playback(self.access_token)

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

    # Skip previous for all users.
    def room_skip_previous(self, devices):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)

        for i in devices:
            if i is not None:
                spotify_api.skip_previous(self.access_token, i)
        playback_data = spotify_api.get_playback(self.access_token)

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

    # Update room emotion and playlist.
    def room_update(self, user_emotions):
        if time.time() > self.expire_time:
            self.access_token, self.expire_time = spotify_api.refresh_access_token(self.refresh_token)

        #TODO:
        Timer(5.0, self.room_update).start()
        print("DEBUG")

        num_users = len(user_emotions)
        if num_users > 0:
            emotions = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral':0, 'sadness': 0, 'surprise': 0}
            for i in user_emotions:
                print(i)
            for e in emotions:
                emotions[e] = sum([i[e] for i in user_emotions]) / num_users
            emotion = max(emotions, key=emotions.get)

            existing = spotify_api.get_playlist_tracks(self.access_token, self.playlist_id)
            energy = self.__room_energy(emotions)
            valence = self.__room_valence(emotions)

            # Find a new track id to add to playlist.
            new_track_id = 0
            playlist_ids = spotify_api.search_playlist(self.access_token, emotion)
            for i in playlist_ids:
                track_ids = spotify_api.get_playlist_tracks(self.access_token, i)
                audio_features = spotify_api.get_audio_features(self.access_token, track_ids)
                for j in audio_features:
                    check_duplicate = (j['id'] in existing)
                    check_energy = (abs(j['energy'] - energy) < THRESHOLD)
                    check_valence = (abs(j['valence'] - valence) < THRESHOLD)
                    if check_duplicate and check_energy and check_valence:
                        new_track_id = j['id']
                        break

            # Add new track to playlist.
            spotify_api.add_track_to_playlist(self.access_token, self.playlist_id, new_track_id)

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
