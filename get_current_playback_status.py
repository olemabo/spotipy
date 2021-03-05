from colorama import Fore
import sys, select
import utility_functions as utl
from time import sleep

def return_artists_as_string(artists):
    """
    Return a nice string to print of all the artists of a song
    :param artists: list of json's with different artists
    :return: string to print with all the artists making a song
    """
    if len(artists) == 1:
        print("Artists: " + Fore.LIGHTMAGENTA_EX + artists[0]["name"] + Fore.WHITE)
        return "Artist: " + artists[0]["name"]
    tot_string = ""
    seperate_sign = []
    for i in range(len(artists)-2):
        seperate_sign.append(", ")
    seperate_sign.append(" and ")
    seperate_sign.append(" ")
    for idx, artist in enumerate(artists):
        tot_string += artist["name"] + seperate_sign[idx]
    print("Artists: " + Fore.LIGHTMAGENTA_EX + tot_string + Fore.WHITE)
    return "Artists: " + tot_string


def print_standard_info(spotify_object, current_playback):
    song_artist_info = current_playback['item']
    shuffle_dict = {"True": "ON", "False": "OFF"}
    shuffle_repeat = {"off": "OFF", "context": "playlist repeat", "track": "track repeat"}
    print("Username: " + spotify_object.current_user()['display_name'])
    print("Device: " + current_playback['device']['name'] + " (" + current_playback['device']['type'] + ")")
    print("Repeat state: " + shuffle_repeat[current_playback['repeat_state']])
    print("Shuffle state: " + shuffle_dict[str(current_playback['shuffle_state'])])
    print("Volume percent: " + str(current_playback['device']['volume_percent']) + "%\n")
    if song_artist_info['name'] != song_artist_info['album']['name']:
        print("Currently playing: " + Fore.LIGHTBLUE_EX + song_artist_info['name'] + Fore.WHITE + " (" +
              song_artist_info['album']['name'] + ")")
    else:
        print("Currently playing: " + Fore.LIGHTBLUE_EX + song_artist_info['name'] + Fore.WHITE)

    data = spotify_object.currently_playing()
    action = data['actions']['disallows'].items()
    current_action = ""  # ('pausing', True)
    for i in action:
        current_action = i
    print("Status: " + str(current_action[0]))  # return to start of line, after '['

#artists_string = return_artists_as_string(song_artist_info['album']['artists'])
#print(artists_string)


def get_current_playback_status(spotify_object):
    current_playback = spotify_object.current_playback()
    if current_playback == None:
        print("The current device is not active at the moment. ")
        return -1

    print_standard_info(spotify_object, current_playback)

    data = spotify_object.currently_playing()

    current_time_ms = data['progress_ms']
    track_duration = data['item']['duration_ms']

    total = 20
    percentage = current_time_ms / track_duration
    #played = int(total * percentage)
    #unplayed = total - played
    #print("[" + '\033[5;36m\033[5;47m' + "*" * (played) + " " * unplayed + "]\n")  # return to start of line, after '['

    played = int(percentage * 100)
    unitColor = '\033[5;37m\033[5;47m'
    endColor = '\033[0;0m\033[0;0m'
    print('|' + unitColor + '\033[7m' + ' '*(played//4) + ' \033[27m' + endColor + ' '*((100-played)//4) + '|\n')
