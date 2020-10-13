import utility_spotify as utl_sp
from utility_functions import clear_terminal
import time
import sys


def get_currently_playing_song():
    sp = utl_sp.create_spotify_object(scope='user-read-currently-playing')
    sys.stdout.write("Song: ")  # return to start of line, after '['
    while True:
        data = sp.currently_playing()
        playlist_uri = data['context']['uri']
        current_time_ms = data['progress_ms']
        artist_id = data['item']['id']
        track_name = data['item']['name']
        artist_name = data['item']['artists'][0]['name']
        track_duration = data['item']['duration_ms']
        playing_type = data['currently_playing_type'] # track, ...
        is_playing = data['is_playing']
        action = data['actions']['disallows'].items()
        current_action = "" # ('pausing', True)
        for i in action:
            current_action = i
        #print(artist_id, artist_name, track_name, track_duration)
        #print(playlist_uri)
        #print(current_time_ms / track_duration * 100)

        total = 40
        percentage = current_time_ms / track_duration
        played = int(total * percentage)
        unplayed = total - played
        sys.stdout.write("Song: " + str(track_name)) # return to start of line, after '['
        sys.stdout.write("\nArtist: " + str(artist_name)) # return to start of line, after '['
        sys.stdout.write("\nStatus: " + str(current_action[0])) # return to start of line, after '['
        sys.stdout.write("\n[" + "*" * (played) + " "*unplayed + "]") # return to start of line, after '['
        sys.stdout.flush()
        time.sleep(1)
        clear_terminal()

get_currently_playing_song()