from colorama import Fore

# my functions
import utility_spotify as utl_sp
import utility_functions as utl
import modify_playback as modi
import add_current_song_to_playlist as add_cur_song
import get_current_playback_status as gcps
import create_relevant_queue as crq
import search_for_artist as sfa
import add_song_to_queue as astq
import first_occurance_of_artist as fooc


def spotify_terminal_interface():
    scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing ' \
            'user-read-private user-top-read playlist-read-private playlist-read-collaborative'
    sp = utl_sp.create_spotify_object(scope=scope)
    current_user_info = sp.current_user()
    user_uri = current_user_info['uri']
    utl.clear_terminal()
    skip_choice = False
    user_choice = None

    print("Welcome! \n" \
                  "Your are connected with " + str(current_user_info['id']) + "'s account.\n")

    while True:

        message = Fore.LIGHTBLUE_EX + "What do you want to do? \n" + Fore.WHITE + \
                  "0 - Search artist\n" \
                  "1 - Modify playback\n" \
                  "2 - Get current playback status \n" \
                  "3 - Add current song to playlist\n" \
                  "4 - Add songs to queue\n" \
                  "5 - Find first occurrence of an artist in your playlists "

        number_of_options = utl.find_largest_number_in_string(message)

        if not skip_choice:
            user_choice = utl.specify_int_in_range(0, number_of_options, message=message, error='x')

        utl.clear_terminal()

        if user_choice == 0:
            # Put all this in a function
            spotifyObject = sp
            #searchQuery = "coldplay"
            #searchResults = spotifyObject.search(q=searchQuery, limit=1, offset=0, type="artist")
            #print(searchResults, searchResults['artists']['items'][0]['id'])
            search_result_NAME_ID_URL = utl_sp.search_one_type(sp, "Search", type='artist', limit=5)
            # Artist details
            #artist = searchResults['artists']['items'][0]
            #print(artist['name'])
            #print(str(artist['followers']['total']) + " followers")
            #print(artist['genres'][0])
            #print()
            #webbrowser.open(artist['images'][0]['url'])
            #artistID = artist['id']
            artistID = search_result_NAME_ID_URL[1]
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
            modify_mod = input("Modify ('x' = exit): ")
            if modify_mod == 'x':
                utl.clear_terminal()
                continue
            if modify_mod not in legal_values:
                utl.clear_terminal()
                user_choice = 1
                skip_choice = True
                continue


            modify_para = modi.print_feedback_info_modify_parameter(modify_mod)
            modi.modify_spotify(modify_mod, modify_para)
            skip_choice = False



        if user_choice == 2:
            utl.clear_terminal()
            gcps.get_current_playback_status(sp)
            response = utl.proceed_or_refresh(message="Do you want to modify playback (r = refresh) ?")
            if response == 'y':
                user_choice = 1
                skip_choice = True
            if response == 'r':
                user_choice = 2
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
                    "1. Search for song and add to queue (x)\n" \
                    "2. Add random songs based on related artists to the artists you are following\n" \
                    "3. Add random songs from all your playlists \n" \
                    "4. Choose artists you are following. (x) \n" \
                    "5. Search for artists and add songs from related artists. \n" \
                    "6. Search for artist and chose between his/her songs. (x) \n" \
                    "7. Search for artists, songs from these artists only.\n" \
                    "8. Find songs by genre (x) \n"
            add_song_queue_choice = utl.specify_int_in_range(1, 7, message=queue_message + "\nChoose the number corresponding to what you want to do.", error='x')

            utl.clear_terminal()

            if int(add_song_queue_choice) == 1:
                print("Not yet implemented")
                #a = utl_sp.search_one_type(sp, "Dawn", "track", limit=3)
                #print(a)
                # may use this function. Can search for artist, album and track.
                # you should make a smart way to let the user specify what to search for.
                a = astq.add_desired_song_to_queue("artist:cold", sp, type='track', limit=3)
                print(a)
                b = 0

            if int(add_song_queue_choice) == 2:
                print("You will add random songs based on artists relevant to the artists you are following.\n")
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50, Fore.LIGHTBLUE_EX + "Specify the number of tracks you want to add to queue (1-50). " + Fore.WHITE)

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
                print(Fore.LIGHTBLUE_EX + "\nAdd random songs from all of your playlists\n" + Fore.WHITE)
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50, Fore.LIGHTBLUE_EX + "Choose number of tracks to add to queue (1-50). " + Fore.WHITE)
                crq.queue_from_random_playlist(sp, number_of_tracks_to_add)

            if int(add_song_queue_choice) == 4:
                print("not yet implemented")

            if int(add_song_queue_choice) == 5:
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50,
                                                                   Fore.LIGHTBLUE_EX + "\nChoose number of tracks to add to queue (1-50). " + Fore.WHITE)

                random_dict = {1: "uniform", 2: "relevance"}
                artist_dict = {1: True, 2: False}

                message_artist = Fore.LIGHTBLUE_EX + "\nWhen a random artist you follow is picked, we will have to pick one of 20 relevant artists.\n" \
                                                     "How will you choose the relevant artist? \n\n" + Fore.WHITE + \
                                 "1. Equal probability of picking all the relevant artists. \n" \
                                 "2. Higher probability of picking more relevant artists."

                message_track = Fore.LIGHTBLUE_EX + "\nWhen a relevant artists is found, we will have to pick one of its top 10 tracks.\n" \
                                                    "How will you choose among the top tracks? \n\n" + Fore.WHITE + \
                                "1. Equal probability of picking all the tracks. \n" \
                                "2. Higher probability of picking more popular tracks."

                random_artist = random_dict[utl.specify_int_in_range(1, 2, message_artist)]
                random_track = random_dict[utl.specify_int_in_range(1, 2, message_track)]

                add_chosen_artist = artist_dict[utl.specify_int_in_range(1, 2, Fore.LIGHTBLUE_EX + "\nWill you include the chosen artists with the related artists? " + Fore.WHITE + "\n\n1. True\n2. False ")]
                print()
                print(Fore.LIGHTBLUE_EX + "You will now search for the artists you want to find related artists to. \n" + Fore.WHITE)
                crq.add_related_artists_from_searched_artists(sp, number_of_tracks_to_add, random_artist=random_artist, random_track=random_track, include_given_artist=add_chosen_artist)

            if int(add_song_queue_choice) == 6:
                print("Not yet implemented")
                a = sfa.search_for_one_artist_until_correct(sp)
                print("Artist info: ", a)
                print("Remains to find all songs for given artist to chose from")


            if int(add_song_queue_choice) == 7:
                print("7. Search for artists, songs from these artists only.\n")

                print(Fore.LIGHTBLUE_EX + "You will now search for artists: \n" + Fore.WHITE)
                artists = crq.search_for_artists(sp)

                number_of_tracks_to_add = utl.specify_int_in_range(1, 50,
                                                                   Fore.LIGHTBLUE_EX + "\nChoose number of tracks to add to queue (1-50). " + Fore.WHITE)

                track_dict = {1: "top", 2: "all"}
                message_artist = Fore.LIGHTBLUE_EX + "\nHow would you pick songs from your chosen artits?\n\n" + Fore.WHITE + \
                                 "1. Randomly pick among top 10 songs. \n" \
                                 "2. Randomly pick among all of the artists' songs."

                top_all = track_dict[utl.specify_int_in_range(1, 2, message_artist)]
                crq.add_random_songs_from_searched_artists(artists=artists, spotify_object=utl_sp.create_spotify_object(),
                                                           number_of_songs_to_add=number_of_tracks_to_add, top_all=top_all)

                print()

        if user_choice == 5:
            fooc.first_occurance(sp)
            print()

        if user_choice == 6:
            print("TODO")
            print("Add next_track() / pause_playback / previous_track() ")
            print("recommendation_genre_seeds(), recommendations()")
            print("Start a track: sp.start_playback(uris=['spotify:track:7lEptt4wbM0yJTvSG5EBof'])")
            print("Add to queue should also include songs by the artists you are following. 'Include the artists uou are following?'")
        # break the while loop and end spotipy
        if user_choice == -1:
            break

        if skip_choice == False:
            if  utl.proceed():
                utl.clear_terminal()
            else:
                break

spotify_terminal_interface()

