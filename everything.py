import spotipy
import utility_spotify as utl_sp
import utility_functions as utl
import json
import modify_playback as modi
import add_current_song_to_playlist as add_cur_song
from colorama import Fore
import get_current_playback_status as gcps
import create_relevant_queue as crq

#print(json.dumps(current_user_info, sort_keys=True, indent=4))


def spotify_terminal_interface():
    scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing ' \
            'user-read-private user-top-read playlist-read-private playlist-read-collaborative'
    sp = utl_sp.create_spotify_object(scope=scope)
    current_user_info = sp.current_user()
    user_uri = current_user_info['uri']
    utl.clear_terminal()
    #print(utl.print_nice_json_format(sp.current_user_playing_track()))
    skip_choice = False
    user_choice = None
    while True:

        message = "Welcome! \n" \
                  "Your are connected with " + str(current_user_info['id']) + "'s account.\n\n" \
                  "What do you want to do\n" \
                  "0 - Search artist\n" \
                  "1 - Modify playback\n" \
                  "2 - Get current playback status \n" \
                  "3 - Add current song to playlist\n" \
                  "4 - Add songs to queue\n" \
                  "5 TODO "

        number_of_options = 4

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
            still_proceed = utl.proceed()
            if not still_proceed:
                break

            skip_choice = False
            utl.clear_terminal()



        if user_choice == 2:
            utl.clear_terminal()
            gcps.get_current_playback_status(sp)
            if utl.proceed(message="Do you want to modify playback?"):
                user_choice = 1
                skip_choice = True


        if user_choice == 3:
            output_log = add_cur_song.add_current_song_to_playlist2(sp=sp, public=True, private=True, collaborative=True)
            utl.clear_terminal()
            if len(output_log) > 0:
                for i in output_log:
                    print(Fore.BLUE + i.split("was")[0] + Fore.WHITE + i.split("was")[1])
                print()
                print()


        if user_choice == 4:
            utl.clear_terminal()
            queue_message = Fore.LIGHTBLUE_EX + "How do you want to add songs to queue?\n\n" + Fore.WHITE + \
                    "1. Search for song and add to queue \n" \
                    "2. Add random songs to queue based on related artists to the artists you are following\n" \
                    "3. Add random songs from all your playlists\n" \
                    "4. Choose artists you are following. Or search for artists. \n"
            add_song_queue_choice = utl.specify_int_in_range(0, 3, message=queue_message + "\nChoose the number corresponding to what you want to do.", error='x')

            if int(add_song_queue_choice) == 1:
                print("Not yet implemented")
            if int(add_song_queue_choice) == 2:
                print("\nYou will add random songs based on artists relevant to the artists you are following.\n")
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50, Fore.LIGHTBLUE_EX + "Choose number of tracks to add to queue (1-50). " + Fore.WHITE)

                random_dict = {1: "uniform", 2: "relevance"}

                message_artist = Fore.LIGHTBLUE_EX +"\nWhen a random artist you follow is picked, we will have to pick one of 20 relevant artists.\n" \
                                  "How will you choose the relevant artist? \n\n" + Fore.WHITE + \
                                 "1. Equal probability of picking all the relevant artists. \n" \
                                 "2. Higher probability of picking more relevant artists."

                message_track = Fore.LIGHTBLUE_EX + "\nWhen a relevant artists is found, we will have to pick one of its top 10 tracks.\n" \
                                 "How will you choose among the top tracks? \n\n" + Fore.WHITE + \
                                 "1. Equal probability of picking all the tracks. \n" \
                                 "2. Higher probability of picking more popular tracks."

                random_artist = random_dict[utl.specify_int_in_range(1, 2, message_artist)]
                random_track = random_dict[utl.specify_int_in_range(1, 2, message_track)]
                print()
                crq.add_x_random_top_track_from_random_follower_to_queue(sp, int(number_of_tracks_to_add), random_artist, random_track)

            if int(add_song_queue_choice) == 3:
                print("Not yet implemented")

            print()
            print()

        if user_choice == 5:
            print("TODO")
            print("Add next_track() / pause_playback / previous_track() ")
            print("recommendation_genre_seeds(), recommendations()")
            print("Start a track: sp.start_playback(uris=['spotify:track:7lEptt4wbM0yJTvSG5EBof'])")
            print("Add to queue should also include songs by the artists you are following. 'Include the artists uou are following?'")
        # break the while loop and end spotipy
        if user_choice == -1:
            break


spotify_terminal_interface()

