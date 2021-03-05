import utility_spotify as utl_sp
import spotipy
import argparse, sys
from colorama import Fore
import utility_functions as utl


legal_attributes = ['repeat', 'shuffle', 'volume', 'seek', 'transfer']

"""
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("modify",
                        #help='[' + Fore.BLUE + 'repeat' + Fore.WHITE + ', ' + Fore.LIGHTMAGENTA_EX + 'seek'
                        #+ Fore.WHITE + ',' + Fore.LIGHTCYAN_EX + ' shuffle' + Fore.YELLOW + ' transfer'  + Fore.WHITE + '] ' +
                        help= ' What to modify with the current playback:  '
                        + Fore.BLUE + ' repeat' + Fore.WHITE + ': Set the current device on repeat.'
                        + Fore.LIGHTMAGENTA_EX + ' seek' + Fore.WHITE + ': Move to a specific ms in track.'
                        + Fore.LIGHTCYAN_EX + ' shuffle' + Fore.WHITE + ': Toggle playback shuffling.'
                        + Fore.YELLOW + ' transfer' + Fore.WHITE + ': Change the current active device.'
                        + Fore.LIGHTRED_EX + ' volume' + Fore.WHITE + ': Adjust volume. (not finished)',
                                        type=str)


    parser.add_argument("modify_parameter", help= Fore.BLUE + 'Repeat' + Fore.WHITE + ": 'track' (set track repeat), 'playlist' (set the playlist on repeat)"
                                                " or 'off' (turn off repeat)  "
                                                + Fore.LIGHTMAGENTA_EX + 'Seek' + Fore.WHITE +
                                                  ': Find position in current track (%%). '
                                                + Fore.LIGHTCYAN_EX + 'Shuffle' + Fore.WHITE +
                                                  ': Turn on/off shuffle (True/False). '
                                                + Fore.YELLOW + 'Transfer' + Fore.WHITE +
                                                  ': No input needed (whatever). '
                                                + Fore.LIGHTRED_EX + 'Volume' + Fore.WHITE +
                                                  ': Adjust volume to a percentage (10). ',
                                        type=str)


    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()


    if sys.argv[1].lower() not in legal_attributes:
        parser.print_help()
        parser.exit()

    attri = ['repeat', 'seek', 'shuffle', 'volume']
    attri_notes = ["You are missing the last parameter. Must be one of these:\n'track' (set track repeat), \n'playlist' (play playlist over and over)\n'off' (turn off repeat)",
                   'You are missing the last parameter.\nSpecify where to play the current track in percentage of total time. (25)',
                   'You are missing the last parameter.\nTurn on/off shuffle (True/False)',
                   'You are missing the last parameter.\nAdjust volume to a percentage (10)'
                   ]

    if len(sys.argv[1:]) == 1 and sys.argv[1].lower() in ['repeat', 'shuffle', 'volume', 'seek']:
        idx = np.where(sys.argv[1].lower() == np.array(attri))[0][0]
        print(attri_notes[idx])
        parser.exit()

    args = parser.parse_args()
"""

def print_feedback_info_modify():
    space = 0
    print("What to modify with the current playback? \n\nModify: \n"
                        + Fore.BLUE + " "*space + 'repeat' + Fore.WHITE + ': Set the current device on repeat.\n'
                        + Fore.LIGHTMAGENTA_EX + " "*space + 'seek' + Fore.WHITE + ': Move to a specific ms in track.\n'
                        + Fore.LIGHTCYAN_EX + " "*space + 'shuffle' + Fore.WHITE + ': Toggle playback shuffling.\n'
                        + Fore.YELLOW + " "*space + 'transfer' + Fore.WHITE + ': Change the current active device.\n'
                        + Fore.LIGHTRED_EX + " "*space + 'volume' + Fore.WHITE + ': Adjust volume. (not finished)\n')

    return legal_attributes

def choices_between_min_max(min, max):
    while True:
        choice_input = input("\nChoose desired number between " +str(min) + " and " + str(max) + ": ")
        if utl.RepresentsInt(choice_input):
            if int(choice_input) >= min and int(choice_input) <= max:
                return int(choice_input)


def choices_true_false(message):
    while True:
        choice_input = input(message)
        if choice_input not in ["True", "true", "false", "False"]:
            continue
        return choice_input


def print_feedback_info_modify_parameter(modify):
    space = 3
    if modify == "repeat":
        print("Choose between: ")
        repeat_dict = {1: "track", 2: "playlist", 3: "off"}
        print("\n1. 'track' (set track repeat)"
              "\n2. 'playlist' (set the playlist on repeat)" 
              "\n3. 'off' (turn off repeat) \n")
        return repeat_dict[choices_between_min_max(1, 3)]

    if modify == "seek":
        print("Find position in current track (%). ")
        return choices_between_min_max(0, 100)

    if modify == "shuffle":
        return choices_true_false("Turn on/off shuffle. True/False: ")

    if modify == "volume":
        print("Adjust volume to a percentage (%). ")
        return choices_between_min_max(0, 100)

    if modify == "transfer":
        return "No transfer needed"



def set_repeat(state="track"):
    """
    Set the current playing device on repeat. The device must be active, otherwise
    an error will occur.
    :param state:
        track (set track repeat),
        context (play the playlist over and over)
        off (turn off repeat)
    :return:
    """
    if state == 'playlist':
        state = 'context'
    sp = utl_sp.create_spotify_object(scope='user-modify-playback-state')
    if state not in ["track", "context", "off"]:
        print("\nModify parameter must be either 'track', 'context' or 'off'")
        print("track: set track repeat \ncontext: play the playlist over and over \noff: turn off repeat")
        return -1
    try:
        sp.repeat(state=state)
        if state == "off":
            print("Repeat: OFF")
        else:
            print("\n" + str(state.capitalize()) + " repeat: ON")
        track_name, artist_name, track_uri, playing_type = utl_sp.find_current_song_return_id(sp=sp)
        print("Currently playing: '" + str(track_name) + "' by " + str(artist_name) + "\n")
    except spotipy.exceptions.SpotifyException:
        print("In set_repeat()")
        print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
        print("One device must play music before this can be done.")


def seek_to_ms_in_current_track(position_ms, device_id=None):
    sp = utl_sp.create_spotify_object(scope='user-modify-playback-state')

    if not utl.RepresentsFloat(position_ms):
        print("\nModify parameter must be a float number.")
        print("The number is how long into the song to start in percentage.\n")
        return -1
    if utl.RepresentsFloat(position_ms) and float(position_ms) < 0 or float(position_ms) > 100:
            print("\nModify parameter must be between 0-100.")
            print("The number is how long into the song to start in percentage.\n")
            return -1
    else:
        position_ms = float(position_ms)
    try:
        data = sp.currently_playing()
        track_duration = data['item']['duration_ms']
        position_ms = int(position_ms / 100 * int(track_duration))
        sp.seek_track(position_ms=position_ms, device_id=device_id)
        track_name, artist_name, track_uri, playing_type = utl_sp.find_current_song_return_id(sp=sp)
        print("\nSuccessfully moved to" + str(utl.convertMillis(position_ms)[3]) + " in the song: '" + str(track_name) + "'"
            "\nCurrent time: " + str(utl.convertMillis(position_ms)[3]) +
            "\nTotal time: " + " "*2 + str(utl.convertMillis(track_duration)[3]) + "\n")
    except spotipy.exceptions.SpotifyException:
        print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
        print("One device must play music before this can be done.")


def shuffle(state=True, device_id=None):
    if state not in ['false', 'False', 'True', 'true']:
        print("\nWrong input. The modify parameter must be eiter 'True', 'true', 'False' or 'false'. ")
        print("False/false = turn off shuffle.")
        print("True/true = turn on shuffle and reshuffle the shuffle list.\n")
        return -1
    if state == 'false' or state == 'False':
        state = False
    else:
        state = True
    sp = utl_sp.create_spotify_object(scope='user-modify-playback-state')
    try:
        if state == True:
            sp.shuffle(state=False, device_id=device_id)
        sp.shuffle(state=state, device_id=device_id)
        if state == True:
            print("\nShuffle: ", utl.check_or_cross(what='check'), "\n")
        if state == False:
            print("\nShuffle: ", utl.check_or_cross(what='cross'), "\n")
    except spotipy.exceptions.SpotifyException:
        print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
        print("One device must play music before this can be done.")



def transfer_playback(device_id, sp):
    """
    Transfer playback to another device. Note that the API accepts a list of device ids, but only actually supports one.
    :param device_id: this will be the new active device
    :return:
    """
    try:
        sp.transfer_playback(device_id=device_id, force_play=True)
        print("Transfer done successfully.\n")
    except spotipy.exceptions.SpotifyException:
        print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
        print("One device must play music before this can be done.")
        return 0


def let_the_user_see_current_active_devices_and_choose_one(sp):
    dict_devices, total_active_devices = utl_sp.return_device_info(sp)
    if total_active_devices == 0:
        print("No devices found.")
        return -1
    print("\n" + Fore.LIGHTBLUE_EX + "Number \t" + Fore.YELLOW + " Name " + Fore.WHITE + " " * (23) + Fore.LIGHTMAGENTA_EX + "Type" + Fore.WHITE)
    for device in range(1, total_active_devices+1):
        active_info = " "
        if dict_devices[device][3] == True:
           active_info = " (Active)"
        print(str(device) + " \t " + str(dict_devices[device][1]) + " "*(28-len(str(dict_devices[device][1]))) + str(dict_devices[device][2]) + active_info)
    if total_active_devices == 1:
        print("\nOnly one device available. Chosen number must be 1.")
        return dict_devices[1]
    print("\nChoose the desired device to play from. Specify the matching" + Fore.LIGHTBLUE_EX + " number: " + Fore.WHITE)
    chosen_device = choices_between_min_max(1, total_active_devices)
    return dict_devices[chosen_device]


def adjust_volume(volume_percent):
    if utl.RepresentsInt(volume_percent):
        sp = utl_sp.create_spotify_object(scope='user-modify-playback-state')
        dict_devices, total_active_devices = utl_sp.return_device_info(sp)
        for device in dict_devices.values():
            if device[3] == True and device[2] == 'Computer':
                try:
                    sp.volume(volume_percent=int(volume_percent))
                    print("\nVolume changed to " + str(volume_percent) + "\n")
                    return 0
                except spotipy.exceptions.SpotifyException:
                    print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
                    print("One device must play music before this can be done.")
                    return 0
        print("\nCan't change volume on this device. Must be computer. \n")
    else:
        print("Input must be int. ")


def modify_spotify(modify="", arg_para=""):
    if modify == 'repeat':
        set_repeat(state=str(arg_para))

    if modify == 'seek':
        seek_to_ms_in_current_track(position_ms=arg_para)

    if modify == 'shuffle':
        shuffle(state=arg_para)

    if modify == 'transfer':
        sp = utl_sp.create_spotify_object(scope='user-modify-playback-state')
        device_info = let_the_user_see_current_active_devices_and_choose_one(sp)
        transfer_playback(device_info[0], sp)

    if modify == 'volume':
        adjust_volume(arg_para)

    return -1


if __name__ == "__main__":
    #TODO should have one single spotify object with plenty of scopes, otherwise it may be errors when you run different scripts with different spotify object scopes
    modify_mod = args.modify.lower()
    modify_para = args.modify_parameter
    modify_spotify(modify_mod, modify_para)