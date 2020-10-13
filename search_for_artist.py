import utility_functions as utl
import utility_spotify as utl_sp
from colorama import Fore


def search_for_artist(artist_name, spotify_object, type='artist', limit=1):
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
        chosen_artist = input("\nYou can search again simply by write the artist name again.\nIf you found your artist, choose the corresponding number to your artist: ")
        if utl.RepresentsInt(chosen_artist) and (int(chosen_artist) > len(items) or int(chosen_artist) < 1):
            utl.clear_terminal()
            print("Your number was out of range. Try again.")

        if utl.RepresentsInt(chosen_artist) and int(chosen_artist) <= len(items) and int(chosen_artist) >= 1:
            return_artist = items[int(chosen_artist) - 1]
            utl.clear_terminal()
            print("Artist name: ", Fore.LIGHTBLUE_EX + return_artist['name'] + Fore.WHITE)
            print("Followers: ", return_artist['followers']['total'])
            return dict_number_to_track_id[int(chosen_artist)]

        else:
            utl.clear_terminal()
            artist_name = chosen_artist



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


#see_who_I_am_following()
#playlist_info = see_my_public_playlists()
#get_playlist_tracks(playlist_info[1])
#current_user_recently_played(limit=25)
#current_user_saved_tracks(limit=50, offset=0)
#
#
#track = sp.track('https://open.spotify.com/track/2Mb9K8vDqygdZ7FVWi2IRa')
#print(track)




