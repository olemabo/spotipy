import utility_spotify as utl_sp
import utility_functions as utl
import dateutil.parser as dp
from tqdm import tqdm
import search_for_artist as s_art
from colorama import Fore
import search_for_artist as search


def collect_all_playlists(sp):
    all_playlists = []
    playlists = sp.current_user_playlists()
    for playlist_info in playlists['items']:
        all_playlists.append(playlist_info)
    while playlists['next']:
        playlists = sp.next(playlists)
        for playlist_info in playlists['items']:
            all_playlists.append(playlist_info)
    return all_playlists


def check_if_artist_is_in_playlist(sp, playlist_uri, find_this_artist_id):
    playlist_info = sp.playlist_tracks(playlist_uri)
    times_seconds = []
    for idx, track in enumerate(playlist_info['items']):
        added_at = track['added_at']
        num_artists = len(track['track']['album']['artists'])
        # in case the track is found in the playlist, but removed from spotify somehow
        if num_artists == 0:
            continue
        artist_id = track['track']['album']['artists'][0]['id']
        #if len(track['track']['album']['artists']) > 1:
        #    print(track['track']['album']['artists'])
        #print(len(track['track']['album']['artists']))
        artist_uri = track['track']['album']['artists'][0]['uri']

        if find_this_artist_id == artist_id:
            track_name = track['track']['name']
            times_seconds.append([utl.convert_ISO_time_to_seconds(added_at), added_at, track_name])

    return times_seconds


def find_artist(sp):
    artist = input("Which artist do you want to search for: ")
    artist_info = s_art.search_for_artist(artist, sp, limit=15)
    return artist_info[2], artist_info[3]


def first_occurance(sp):
    print(Fore.LIGHTBLUE_EX + "\nYYou can now specify an artists and find out when he/she first occurred in your playlists.\n" +Fore.WHITE)
    artist_id, artist_name = search.search_for_one_artist_until_correct(sp)[2:4]
    my_playlists = sp.current_user_playlists()
    all_playlists = utl_sp.select_playlists(sp, my_playlists, remove_spotify_playlist=True)
    all_occurrence_in_seconds = []
    print("Start to go through " + str(len(all_playlists)) + " playlists... ")
    for i in tqdm(range(len(all_playlists))):
        playlist_uri = all_playlists[i]['uri']
        playlist_name = all_playlists[i]['name']
        artist_occurance = check_if_artist_is_in_playlist(sp, playlist_uri, artist_id)
        if len(artist_occurance) > 0:
            artist_occurance.append(playlist_name)
            all_occurrence_in_seconds.append(artist_occurance)
    if len(all_occurrence_in_seconds) == 0:
        print("\nYou don't have a single song from this artist in your playlists.")

    first_occ_in_seconds = all_occurrence_in_seconds[0][0]
    first_occ_in_seconds.append(all_occurrence_in_seconds[0][-1])

    for occurance_in_playlist in all_occurrence_in_seconds:
        num_occ_in_playlist = len(occurance_in_playlist) - 1
        for track in range(num_occ_in_playlist):
            if int(occurance_in_playlist[track][0]) < int(first_occ_in_seconds[0]):
                first_occ_in_seconds = occurance_in_playlist[track]
                first_occ_in_seconds.append(occurance_in_playlist[-1])
    timesplit = str(first_occ_in_seconds[1]).split("T")

    year = timesplit[0].split("-")[0]
    month = utl_sp.get_month_name_from_month_number(timesplit[0].split("-")[1])
    day = timesplit[0].split("-")[2]
    date = day + ". " + month + " " + year
    print("\nYour first song by " + Fore.LIGHTBLUE_EX + str(artist_name).capitalize() + Fore.WHITE + ""
        "\nAdded " + Fore.LIGHTGREEN_EX + str(date) + Fore.WHITE + " at " + timesplit[1][:-1])
    print("Song name: " + Fore.CYAN + str(first_occ_in_seconds[2]) + Fore.WHITE +
          "\nIn playlist: " + Fore.YELLOW + str(first_occ_in_seconds[-1]) + Fore.WHITE)


#scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
#        'playlist-modify-public playlist-modify-private user-read-currently-playing'
#scope += ' user-read-private user-top-read playlist-read-private playlist-read-collaborative'


#first_occurance(scope=scope)