import spotipy
import utility_spotify as utl_sp
import utility_functions as utl
import json
import modify_playback as modi
import add_current_song_to_playlist as add_cur_song
from colorama import Fore

def proceed():
    still_do_things = input("Do you want to continue? y/n: ")
    while still_do_things not in ['y', 'n']:
        still_do_things = input("Wrong input. Do you want to exit? y/n: ")
    if still_do_things == 'y':
        return True

    else:
        return False


def all():
    scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing ' \
            'user-read-private user-top-read playlist-read-private playlist-read-collaborative'
    sp = utl_sp.create_spotify_object(scope=scope)
    current_user_info = sp.current_user()
    user_uri = current_user_info['uri']
    utl.clear_terminal()

    #print(json.dumps(current_user_info, sort_keys=True, indent=4))
    skip_choice = False
    user_choice = None
    while True:

        message = "Welcome! \n" \
                  "Your are connected with " + str(current_user_info['id']) + "'s account.\n\n" \
                  "What do you want to do\n" \
                  "0 - Search artist\n" \
                  "1 - Modify playback\n" \
                  "2 - Get current playback (song, repeat, shuffle ... )\n" \
                  "3 - Add current song to playlist\n"

        number_of_options = 3

        if not skip_choice:
            user_choice = utl.specify_int_in_range(0, number_of_options, message=message, error='x')

        if user_choice == 0:
            spotifyObject = sp
            searchQuery = "coldplay"
            searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
            print(searchResults, searchResults['artists']['items'][0]['id'])
            print(utl_sp.search_one_type(sp, searchQuery, type='artist', limit=10))
            # Artist details
            artist = searchResults['artists']['items'][0]
            print(artist['name'])
            print(str(artist['followers']['total']) + " followers")
            print(artist['genres'][0])
            print()
            #webbrowser.open(artist['images'][0]['url'])
            artistID = artist['id']

            # Album and track details
            trackURIs = []
            trackArt = []
            z = 0

            # Extract album data
            albumResults = spotifyObject.artist_albums(artistID)
            albumResults = albumResults['items']

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
                    z += 1
                print()

        # modify playback
        if user_choice == 1:
            legal_values = modi.print_feedback_info_modify()
            modify_mod = input("Modify: ")
            if modify_mod not in legal_values:
                utl.clear_terminal()
                user_choice = 1
                skip_choice = True
                continue

            modify_para = modi.print_feedback_info_modify_parameter(modify_mod)

            modi.modify_spotify(modify_mod, modify_para)
            # still do spotipy things
            still_proceed = proceed()
            if not still_proceed:
                break

            skip_choice = False
            utl.clear_terminal()



        if user_choice == 2:
            utl.clear_terminal()
            print("Not implemented")


        if user_choice == 3:
            output_log = add_cur_song.add_current_song_to_playlist2(sp=sp, public=True, private=True, collaborative=True)
            utl.clear_terminal()
            if len(output_log) > 0:
                for i in output_log:
                    print(Fore.BLUE + i.split("was")[0] + Fore.WHITE + i.split("was")[1])
                print()
                print()
        # break the while loop and end spotipy
        if user_choice == -1:
            break

all()

