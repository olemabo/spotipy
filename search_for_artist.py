import utility_functions as utl
import utility_spotify as utl_sp
from colorama import Fore
import random


def search_for_artist(artist_name, spotify_object, type='artist', limit=1):
    """

    :param artist_name:
    :param spotify_object:
    :param type:
    :param limit:
    :return:
    """
    while True:
        result = spotify_object.search(q=type+':' + artist_name, type=type, limit=limit)['artists']
        # type = album , artist, playlist, track, show and episode
        items = result['items']
        if len(items) == 0:
            print("No artists named " + str(artist_name) + " were found. ")
            return -1
        dict_number_to_track_id = dict()
        print("\n" + Fore.LIGHTBLUE_EX + "Number " + Fore.LIGHTMAGENTA_EX + "  Artist" + Fore.CYAN + 20*" "+ " Main genre" + Fore.WHITE)
        for idx, artist in enumerate(items):
            spotify_id = artist['href']
            artist_uri = artist['uri']
            artist_id = artist['id']
            genres = " "
            if len(artist['genres']) > 0:
                genres = utl.convert_list_string_to_sentence(artist['genres'])
                genres = artist['genres'][0]
            print(idx+1, "\t", artist['name'], " "*(25-len(artist['name'])), genres)

            dict_number_to_track_id[idx+1] = [spotify_id, artist_uri, artist_id, artist['name']]
        chosen_artist = input("\nYou can search again by writing the artist name again ('x' = exit).\nIf you found your artist, choose the corresponding number to your artist (larger number will increase the number of search results): ")
        if chosen_artist == 'x':
            break
        if utl.RepresentsInt(chosen_artist) and (int(chosen_artist) > len(items) or int(chosen_artist) < 1):
            utl.clear_terminal()
            print("Your number was out of range. Try again.")
            if int(chosen_artist) > 0:
                limit = int(chosen_artist)

        elif utl.RepresentsInt(chosen_artist) and int(chosen_artist) <= len(items) and int(chosen_artist) >= 1:
            return_artist = items[int(chosen_artist) - 1]
            utl.clear_terminal()
            print("Artist name: ", Fore.LIGHTBLUE_EX + return_artist['name'] + Fore.WHITE)
            print("Followers: ", return_artist['followers']['total'], "\n")
            return dict_number_to_track_id[int(chosen_artist)]

        else:
            utl.clear_terminal()
            artist_name = chosen_artist


def search_for_artist_show_tracks_grouped_by_album(spotifyObject):
    # Artist details
    start_input = input("Artist search: ")
    utl.clear_terminal()
    search_result_NAME_ID_URL = utl_sp.search_one_type(spotifyObject, start_input, type='artist', limit=5)
    if search_result_NAME_ID_URL == -1:
        return -1, -1, -1
    artist_id = search_result_NAME_ID_URL[1]
    artist_name = search_result_NAME_ID_URL[0]
    return show_all_tracks_from_artist_id(artist_id, spotifyObject, artist_name)



def show_all_tracks_from_artist_id(artistID, spotifyObject, artist_name):
    # Album and track details
    trackURIs = []
    trackArt = []
    trackName = []
    z = 0

    albumResults = spotifyObject.artist_albums(artistID)
    albumResults = albumResults['items']
    print()
    for item in albumResults:
        print("ALBUM: " + item['name'])
        albumID = item['id']
        albumArt = item['images'][0]['url']

        # Extract track data
        trackResults = spotifyObject.album_tracks(albumID)
        trackResults = trackResults['items']

        for item in trackResults:
            print(str(z) + ": " + item['name'])
            trackURIs.append(item['uri'])
            trackArt.append(albumArt)
            trackName.append(item['name'])
            z += 1
        print()
    print()
    return trackName, trackURIs, artist_name

def search_for_one_artist_until_correct(spotify_object, search_type="artist", can_choose_current_artist=False):
    info_text = "Search for new artist ('x' = exit"
    if can_choose_current_artist:
        # get current artist
        track_name, artist_name, track_uri, playing_type = utl_sp.find_current_song_return_id(spotify_object)
        print("Current artist: " + Fore.CYAN + artist_name + Fore.WHITE)
        if track_name != -1:
            info_text += ", 'c' = search for current artist"

    while True:
        your_artist_name = input(info_text + "): ")
        if your_artist_name == 'c':
            track_name, artist_name, track_uri, playing_type = utl_sp.find_current_song_return_id(spotify_object)
            artist_id = utl_sp.get_artist_id_from_track_id(spotify_object, track_uri)
            return [0, 0, artist_id, artist_name, 0]
        if your_artist_name == 'x':
            break
        info = search_for_artist(your_artist_name, spotify_object, type=search_type, limit=3)
        if info == None:
            break
        if info != -1:
            return info


def see_who_I_am_following():
    sp = utl_sp.create_spotify_object(scope='user-follow-read')
    data = sp.current_user_followed_artists(limit=30)['artists']
    print("I am following:")
    for i in data['items']:
        print(i['name'])
    print("\n")




def current_user_recently_played(limit=50):
    sp = utl_sp.create_spotify_object(scope='user-read-recently-played')
    data = sp.current_user_recently_played(limit=limit)
    print(Fore.CYAN + "My recently played songs: " + Fore.WHITE)
    for idx, i in enumerate(data['items']):
        print(idx + 1, i['track']['name'], "/", i['track']['artists'][0]['name'])
    print("\n")


def current_user_saved_tracks(limit=50, offset=0):
    sp = utl_sp.create_spotify_object(scope='user-library-read')
    print(Fore.CYAN + "My recently played songs: " + Fore.WHITE)
    offset, limit, tracks_saved, counter = 0, 50, 0, 1
    while True:
        data = sp.current_user_saved_tracks(limit=limit, offset=offset)
        for i in data['items']:
            print(counter, i['track']['name'], "/", i['track']['artists'][0]['name'])
            counter += 1
        temp_num = len(data['items'])
        if temp_num != 50:
            tracks_saved += temp_num
            break
        tracks_saved += temp_num
        offset += 50
    print("\nTotal tracks saved: ", tracks_saved)
    return tracks_saved


def get_playlist_tracks(playlist_id):
    sp = utl_sp.create_spotify_object(scope='user-library-read')
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=5)
    print(playlist_tracks)



def random_song_artist(sp, artistID, num_to_add):
    # Album and track details
    trackURIs = []
    trackName = []
    trackID = []
    z = 0

    # Extract album data
    albumResults = sp.artist_albums(artistID)
    albumResults = albumResults['items']

    for item in albumResults:
        albumID = item['id']
        # Extract track data
        trackResults = sp.album_tracks(albumID)
        trackResults = trackResults['items']

        for item in trackResults:
            trackURIs.append(item['uri'])
            trackID.append(item['id'])
            trackName.append(item['name'])
            z += 1

    num_songs = len(trackURIs) - 1
    rand_idxes = []
    while True:
        rand_idx = random.randint(0, num_songs)
        if rand_idx not in rand_idxes:
            rand_idxes.append(rand_idx)
        if len(rand_idxes) == num_songs:
            print("Less songs than songs you want to add")
            break
        if len(rand_idxes) == num_to_add:
            break

    popularity = sp.artist(artistID)['popularity']
    list_of_songs = []
    for rand_idx in rand_idxes:
        list_of_songs.append([trackURIs[rand_idx], trackName[rand_idx], popularity])
    return list_of_songs, rand_idxes


#see_who_I_am_following()
#playlist_info = see_my_public_playlists()
#get_playlist_tracks(playlist_info[1])
#current_user_recently_played(limit=25)
#current_user_saved_tracks(limit=50, offset=0)
#
#
#track = sp.track('https://open.spotify.com/track/2Mb9K8vDqygdZ7FVWi2IRa')
#print(track)




