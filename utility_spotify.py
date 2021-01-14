import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorama import Fore
import utility_functions as utl
import os

USER_NAME = 'olemabo'
scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
        'playlist-modify-public playlist-modify-private user-read-currently-playing'
scope += ' user-read-private user-top-read playlist-read-private playlist-read-collaborative'


def create_spotify_object(scope=scope, username=USER_NAME):
    # Create our spotify object with permissions
    global_path = os.path.dirname(os.path.abspath(__file__))
    auth = SpotifyOAuth(username=username, scope=scope, open_browser=True, cache_path=global_path + "/.cache")
    return spotipy.Spotify(oauth_manager=auth)



def create_spotify_object_non_auth(username=USER_NAME):
    return spotipy.Spotify(spotipy.SpotifyClientCredentials())



def search_one_type(sp, search_name, type, limit=3):
    """

    :param sp: spotify object. Scope must include 'user-read-private'
    :param search_name: what to search for ('coldplay')
    :param type: type of the search (‘artist’, ‘album’, ‘track’, ‘playlist’, ‘show’, or ‘episode’)
    :param limit: number of searches to return (10)
    :return: chosen info about the search [name, id, uri]
    """
    while True:
        search_result = sp.search(q=type + ":" + search_name, limit=limit, type=type)[type+"s"]
        print(type.capitalize() + " search: ", search_name.capitalize(), "\n")
        extra_type_info = {'artist': ['genres', 0], 'album': ['artists', 0, 'name'],
                           'track': ['artists', 0, 'name'], 'playlist': ['owner', 'display_name'],
                           'show': ['publisher'], 'episode': ['description']}
        line_adjustment = 28
        print("Number \t " + type.capitalize() + " "*(line_adjustment-len(type.capitalize())) + str(extra_type_info[type][0]).capitalize())
        search_dict = dict()
        for idx, item in enumerate(search_result['items']):
            search_uri = item['uri']
            search_id = item['id']

            name, emoji_len_count = utl.shorten_long_names_count_emojis(item, max_letters=line_adjustment-3)

            extra_info = item
            for i in extra_type_info[type]:
                if type == 'artist' and i == 0 and len(extra_info) == 0:
                    if len(extra_info) == 0:
                        extra_info = "No info"
                else:
                    extra_info = extra_info[i]

            print(str(idx+1) + " \t " + str(name) + " "*(line_adjustment-len(name) - emoji_len_count) + extra_info)
            search_dict[idx + 1] = [name, search_id, search_uri]
        choose_search = input("\n1. Chose corresponding number to desired " + str(type) + "."
                            "\n2. Increase number of searches by specifing a larger number than " + str(len(search_dict)) +
                             ".\n3. Specify a new search. \n4. 'x' to exit:   ")
        if utl.RepresentsInt(choose_search) and int(choose_search) > 0 and int(choose_search) <= len(search_dict):
            return search_dict[int(choose_search)]
        if choose_search == 'x':
            return -1
        utl.clear_terminal()
        if not utl.RepresentsInt(choose_search):
            search_name = choose_search
        if utl.RepresentsInt(choose_search):
            if int(choose_search) > len(search_dict):
                limit = int(choose_search)



def return_device_info(sp):
    """
    [id, name, type, is_active], number of devices found
    :return: dict(1: [83d4d3e983c92e8bc80d8e59cf23a3a1f862b775, G8341, Smartphone, True], 2: [ ... ], 3: [ ... ]]), 3
    """
    #sp = create_spotify_object(scope='user-read-playback-state ')
    device_data = sp.devices()['devices']
    device_dict = dict()
    number_of_devices = len(device_data)
    print("Number of devices found: ", number_of_devices)
    for idx, i in enumerate(device_data):
        device_dict[idx+1] = [i['id'], i['name'], i['type'], i['is_active']]
    return device_dict, number_of_devices


def find_current_song_return_id(sp):
    #spotify_object = create_spotify_object(scope='user-read-playback-state')
    data = sp.currently_playing()
    if data == None:
        print("The device is not active.")
        return -1, -1, -1, -1
    track_uri = data['item']['uri']
    track_name = data['item']['name']
    artist_name = data['item']['artists'][0]['name']
    playing_type = data['currently_playing_type']  # track, ...
    return track_name, artist_name, track_uri, playing_type


def color_names(print_str, info, number, name):
    owner = info['owner']['display_name']
    collab = info['collaborative']
    public = info['public']
    return_color = Fore.WHITE
    if owner != USER_NAME and not collab:
        print_str += str(number) + ": " + Fore.LIGHTRED_EX + name + Fore.WHITE
        return_color = Fore.LIGHTRED_EX
    elif collab:
        print_str += str(number) + ": " + Fore.YELLOW + name + Fore.WHITE
        return_color = Fore.YELLOW

    elif public:
        print_str += str(number) + ": " + name + Fore.LIGHTCYAN_EX + "*" + Fore.WHITE
        return_color = Fore.LIGHTCYAN_EX

    else:
        print_str += str(number) + ": " + Fore.WHITE + name + Fore.WHITE

    return print_str, return_color





def show_tracks_and_append_to_dict(data, dict_number_to_playlist, start_count=0, columns=3, jumps=28, printing=True):
    """
    :param data:
    :param dict_number_to_playlist:
    :param start_count:
    :param columns:
    :param jumps:
    :return: [['name'], ['id'], ['uri'], print_color]
    """
    #num_playlists = len(data['items'])
    num_playlists = len(data)
    odd = len(data) % columns
    #odd = len(data['items']) % columns

    for idx in range(num_playlists//columns):
        print_str = ""
        tot_emoji = 0
        for column in range(columns):
            info = data[idx * columns + column]
            number = idx * columns + column + 1 + start_count

            name, num_emojier = utl.shorten_long_names_count_emojis(info, max_letters=15)
            tot_emoji += num_emojier
            print_str, print_color = color_names(print_str, info, number, name)

            print_str += " "*(jumps*(column+1) - len(print_str) - tot_emoji)
            dict_number_to_playlist[number] = [info['name'], info['id'], info['uri'], print_color]
        if printing:
            print(print_str)

    if odd > 0:
        last_str = ""
        for idx, num in enumerate(range(num_playlists - odd, num_playlists)):
            info = data[num]
            number = num + 1 + start_count

            name, num_emojier = utl.shorten_long_names_count_emojis(info, max_letters=15)

            last_str, print_color = color_names(last_str, info, number, name)

            last_str += " " * (jumps*(idx+1) - len(last_str))
            dict_number_to_playlist[number] = [info['name'], info['id'], info['uri'], print_color]
        if printing:
            print(last_str)

    return dict_number_to_playlist, number


def set_dividable_limits_based_on_num_playlists(total_playlists):
    if total_playlists >= 90:
        columns = 4
        jumps = 35
        limit = 16 * 3
    if total_playlists < 90:
        columns = 3
        jumps = 40
        limit = 3 * 13
    if total_playlists < 30:
        columns = 2
        jumps = 40
        limit = 2 * 25

    return columns, jumps, limit


def filter_playlists(playlist_to_use, i, public, private, collaborative, remove_spotify_playlist):
    # this will filter out playlists not made be you (collaborative playlists not made be you will still pass)
    if remove_spotify_playlist and i['owner']['display_name'] != USER_NAME and i['collaborative'] == False:
        return playlist_to_use
    elif i['public'] == public:
        playlist_to_use.append(i)
    elif private:
        if i['public'] == False:
            playlist_to_use.append(i)
    elif i['collaborative'] == collaborative:
        playlist_to_use.append(i)
    return playlist_to_use


def select_playlists(sp, data, public=True, private=True, collaborative=True, remove_spotify_playlist=False):
    playlist_to_use = []
    for i in data['items']:
        playlist_to_use = filter_playlists(playlist_to_use, i, public, private, collaborative, remove_spotify_playlist)

    while data['next']:
        data = sp.next(data)
        for i in data['items']:
            playlist_to_use = filter_playlists(playlist_to_use, i, public, private, collaborative, remove_spotify_playlist)

    return playlist_to_use


def see_my_public_playlists(sp, public=True, private=True, collaborative=True):
    data = sp.current_user_playlists()
    playlist_to_show = select_playlists(sp, data, public, private, collaborative)

    print("\n" + Fore.LIGHTRED_EX + "*" + Fore.WHITE +
          ": These playlists are not made by you. You therefore not add songs to these\n"
          + Fore.YELLOW + "*" + Fore.WHITE + ": These playlists are collaborative. You are free to add.\n"
          + Fore.CYAN + "*" + Fore.WHITE + ": Private playlists.")
    print("\nMy playlists: " + Fore.WHITE)

    dict_number_to_playlist = dict()
    total_playlists = len(playlist_to_show)
    columns, jumps, limit = set_dividable_limits_based_on_num_playlists(total_playlists)

    dict_number_to_playlist, counter = show_tracks_and_append_to_dict(playlist_to_show, dict_number_to_playlist,
                                                                      columns=columns, jumps=jumps)

    chosen_playlist = input("\nChoose a playlist by specifying the corresponding number (x to exit): ")
    if chosen_playlist == 'x':
        return -1
    nice_numbers = utl.convert_song_numbers_to_useful_numbers(chosen_playlist, total_playlists)

    while nice_numbers == -1:
        chosen_playlist = input("Try again. Choose a playlist by specifying the corresponding number (x to exit): ")
        if chosen_playlist == 'x':
            return -1
        nice_numbers = utl.convert_song_numbers_to_useful_numbers(chosen_playlist, total_playlists)

    return_playlist = []
    print("\nYour choice(s): ")
    for idx, num in enumerate(nice_numbers):
        return_playlist.append(dict_number_to_playlist[int(num)])
        print("Playlist name: " + return_playlist[idx][-1] + str(return_playlist[idx][0]) + Fore.WHITE)
    return return_playlist


def return_all_playlists(sp, public=True, private=True, collaborative=True, printing=False):
    data = sp.current_user_playlists()
    playlist_to_show = select_playlists(sp, data, public, private, collaborative)

    dict_number_to_playlist = dict()
    total_playlists = len(playlist_to_show)
    columns, jumps, limit = set_dividable_limits_based_on_num_playlists(total_playlists)

    dict_number_to_playlist, counter = show_tracks_and_append_to_dict(playlist_to_show, dict_number_to_playlist,
                                                                      columns=columns, jumps=jumps, printing=printing)
    return dict_number_to_playlist





def check_playlist_for_specific_track(playlists, track_uri, what_to_compare='uri'):
    for playlist in playlists['items']:
        uri = playlist['track']['uri']
        id = playlist['track']['id']
        href = playlist['track']['href']
        urel = playlist['track']['external_urls']['spotify']
        check_dict = {'id': id, 'href': href, 'uri': uri, 'urel': urel}
        if check_dict[what_to_compare] == track_uri:
            return True


def check_if_track_is_in_playlist(track_uri, playlist_uri, sp):
    #sp = create_spotify_object(scope='user-follow-read playlist-read-private playlist-read-collaborative')
    playlists = sp.playlist(playlist_uri)['tracks']
    while playlists:
        if check_playlist_for_specific_track(playlists, track_uri):
            return True
        playlists = sp.next(playlists)
    return False


def add_song_to_queue(spotify_object, id, track_name, artist, following_artist):
    try:
        print(Fore.LIGHTRED_EX)
        spotify_object.add_to_queue(id)
        print(Fore.WHITE + str(following_artist) + " -> " + Fore.LIGHTGREEN_EX + str(track_name) + Fore.WHITE + " (" + str(artist) + ")" + " was added to the queue.")
        return 1
    except Exception as e:
        #print(Fore.LIGHTRED_EX + "Player command failed: No active device found. Reason: NO_ACTIVE_DEVICE.")
        #print("One device must play music before this can be done." + Fore.WHITE)
        print(Fore.LIGHTRED_EX + str(e) + Fore.WHITE)
        return 0


def get_month_name_from_month_number(month_num):
    month_dict = {"01": "Jan.", "02": "Feb.", "03": "March", "04": "April", "05": "May", "06": "June",
                  "07": "July", "08": "Aug.", "09": "Sept.", "10": "Oct.", "11": "Nov.", "12": "Dec.",}
    return month_dict[month_num]

#playlist_uri = 'https://open.spotify.com/playlist/5r5lGanRM2v1RJK1jhsxAJ'
#song_uri = 'https://open.spotify.com/track/2Mb9K8vDqygdZ7FVWi2IRa'
#rand_play_uri = 'https://open.spotify.com/playlist/1mbI8kCENLNuMFN2dm4Y5z'
#print(check_if_track_is_in_playlist(song_uri, rand_play_uri))
#print(check_if_track_is_in_playlist('https://open.spotify.com/track/57BGVV6wcyhbn3hsjlqEZB', rand_play_uri))



    #username = 'olemabo'
    #cache_path = "/home/ole/Dropbox/spotify/.cache-" + str(username)
    #auth = SpotifyOAuth(cache_path=cache_path, scope=scope, open_browser=False)
    #print(auth.cache_path)
    #return spotipy.Spotify(auth_manager=SpotifyPKCE(cache_path=cache_path, scope=scope, open_browser=False))



  #try:
    #    token = util.prompt_for_user_token(username, scope)  # add scope
    #except (AttributeError, JSONDecodeError):
    #    os.remove(f".cache-{username}")
    #    token = util.prompt_for_user_token(username, scope)  # add scope

    # Create our spotify object with permissions
    #auth_manager = SpotifyOAuth(scope=scope)
    #spotipy.Spotify(auth_manager=auth_manager)
    #spotifyObject = spotipy.Spotify(auth=token)
    #spotifyObject = spotipy.Spotify(auth=auth_manager)