class Room:
    def __init__(self, id, creator_user_id, access_token, refresh_token, playlist_id, playlist_uri):
        self.room_number = id
        self.creator = creator_user_id
        self.users = {creator_user_id}
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.playlist_id = playlist_id
        self.playlist_uri = playlist_uri

        self.is_playing = False
        self.queue = []

    def __str__(self):
        return f'Room number: {self.room_number}\nUsers: {self.users}\nPlaylist URI: {self.playlist_uri}\nTokens: {self.access_token}, {self.refresh_token}'

    def add_user_to_room(self, user_id):
        if user_id not in self.users:
            self.users.add(user_id)
    
    def remove_user_from_room(self, user_id):
        if user_id in self.users:
            self.users.remove(user_id)