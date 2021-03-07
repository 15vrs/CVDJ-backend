import spotify.users as users
import spotify.rooms as rooms

# Route: /create_room.
def create_spotify_room(code, redirect_uri):
    room_id = insert_room()
    user_id = insert_user(room_id)
    return room_id, user_id, room.get_token(), room.playlist_id

# Route: /join_room.
def join_spotify_room(room_id):
    room = rooms[int(room_id)]
    user_id = insert_user(room_id)
    return user_id, room.get_token(), room.playlist_id

# Route: /leave_room.
def leave_spotify_room(room_id, user_id):
    room = rooms[int(room_id)]
    delete_user(user_id)

    devices_set = room.get_spotify_devices()
    if len(devices_set) == 0:
        del room

# Route: /add_device.
def add_spotify_device(room_id, user_id, device_id):
    room = rooms[int(room_id)]
    set_device_id(user_id, device_id)
    room.room_transfer(device_id)

# Route: /play_room.
def play_spotify_room(room_id):
    room = rooms[int(room_id)]
    return room.room_play()

# Route: /pause_room.
def pause_spotify_room(room_id):
    room = rooms[int(room_id)]
    return room.room_pause()

# Route: /skip_next.
def spotify_skip_next(room_id):
    room = rooms[int(room_id)]
    return room.room_skip_next()

# Route: /skip_previous.
def spotify_skip_previous(room_id):
    room = rooms[int(room_id)]
    return room.room_skip_previous()
        