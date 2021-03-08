from colorama import Fore
import sys, select

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
import recommendation as reco


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
                  "0 - Get current playback status\n" \
                  "1 - Modify playback\n" \
                  "2 - Search artist/track/album \n" \
                  "3 - Add current song to playlist\n" \
                  "4 - Add songs to queue\n" \
                  "5 - Find first occurrence of an artist in your playlists\n" \
                  "6 - Playlist features\n"

        number_of_options = utl.find_largest_number_in_string(message)

        if not skip_choice:
            user_choice = utl.specify_int_in_range(0, number_of_options, message=message, error='x')

        utl.clear_terminal()

        if user_choice == 0:
            utl.clear_terminal()
            while True:
                gcps.get_current_playback_status(sp)

                print("Do you want to modify playback ? y/n")
                print("('a' = add current song to playlist)")
                i, o, e = select.select([sys.stdin], [], [], 10)
                "TODO: You should only refresh progress bar, if it is not a new song or new device ..."
                if (i):
                    resp = sys.stdin.readline().strip()
                    if resp == "y" or resp == "n" or resp == "a":
                        response = resp
                        utl.clear_terminal()
                        break
                utl.clear_terminal()

            # gcps.get_current_playback_status(sp)
            # response = utl.proceed_or_refresh(message="Do you want to modify playback (r = refresh) ?")

            skip_choice = False
            if response == 'y':
                user_choice = 1
                skip_choice = True
            if response == 'r':
                user_choice = 0
                skip_choice = True
            if response == 'a':
                user_choice = 3
                skip_choice = True

        # modify playback
        if user_choice == 1:
            legal_values = modi.print_feedback_info_modify()
            modify_mod = input("Modify ('x' = exit): ")
            skip_choice = False
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

        # search for artist
        if user_choice == 2:

            message_search = Fore.LIGHTBLUE_EX + "What do you want to do? \n" + Fore.WHITE + \
                             "0 - Search Artist \n" \
                             "1 - Search Track \n" \
                             "2 - Search Album \n"

            number_of_options_search = utl.find_largest_number_in_string(message_search)

            user_choice_search = utl.specify_int_in_range(0, number_of_options_search, message=message_search,
                                                          error='x')

            utl.clear_terminal()

            if user_choice_search == 0:
                astq.search_for_artist_show_tracks_grouped_by_album_add_queue(sp)

            if user_choice_search == 1:
                print("Not implemented yet")

            if user_choice_search == 2:
                print("Not implemented yet")

        if user_choice == 3:
            output_log = add_cur_song.add_current_song_to_playlist2(sp=sp, public=True, private=True,
                                                                    collaborative=True)
            utl.clear_terminal()
            check_list = isinstance(output_log, list)

            if utl.RepresentsString(output_log) and check_list == False:
                print(output_log + "\n")
            elif len(output_log) > 0:
                for i in output_log:
                    print(Fore.BLUE + i.split("was")[0] + Fore.WHITE + i.split("was")[1])
                print()
                print()

        if user_choice == 4:
            utl.clear_terminal()

            queue_message = Fore.LIGHTBLUE_EX + "How do you want to add songs to queue?\n\n" + Fore.WHITE + \
                "1. Search for song and add to queue \n" \
                "2. Add random songs based on related artists to the artists you are following\n" \
                "3. Add random songs from all your playlists \n" \
                "4. Choose artists you are following. (x) \n" \
                "5. Search for artists and add songs from related artists. \n" \
                "6. Search for artist and choose between his/her songs. \n" \
                "7. Search for artists, songs from these artists only.\n" \
                "8. Find songs by genre (x) \n" \
                "9. Add songs based on tracks, artists and/or genre. \n"

            add_song_queue_choice = utl.specify_int_in_range(1, 9,
                                                             message=queue_message + "\nChoose the number "
                                                                                     "corresponding to what you want "
                                                                                     "to do.",
                                                             error='x')

            utl.clear_terminal()

            if int(add_song_queue_choice) == 1:
                track_search = input("Track search: ")
                utl.clear_terminal()
                track_info = utl_sp.search_one_type(sp, track_search, "track", limit=3)
                # -1 comes when user says 'x' to quit
                if track_info != -1:
                    # track_info [name, id, uri]
                    artist_name = utl_sp.get_artist_name_from_track_id(sp, track_info[1])
                    utl_sp.add_song_to_queue(sp, track_info[1], track_info[0], artist_name, "")
                    # may use this function. Can search for artist, album and track.
                    # you should make a smart way to let the user specify what to search for.
                    # astq.add_desired_song_to_queue("artist:" + track_search, sp, type='track', limit=3)
                print()

            if int(add_song_queue_choice) == 2:
                print("You will add random songs based on artists relevant to the artists you are following.\n")
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50,
                                                                   Fore.LIGHTBLUE_EX + "Specify the number of tracks you want to add to queue (1-50). " + Fore.WHITE)

                random_dict = {1: "uniform", 2: "relevance"}

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
                print()
                crq.add_x_random_top_track_from_random_follower_to_queue(sp, int(number_of_tracks_to_add),
                                                                         random_artist, random_track)

            if int(add_song_queue_choice) == 3:
                print(Fore.LIGHTBLUE_EX + "\nAdd random songs from all of your playlists\n" + Fore.WHITE)
                number_of_tracks_to_add = utl.specify_int_in_range(1, 50,
                                                                   Fore.LIGHTBLUE_EX + "Choose number of tracks to add to queue (1-50). " + Fore.WHITE)
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

                add_chosen_artist = artist_dict[utl.specify_int_in_range(1, 2,
                                                                         Fore.LIGHTBLUE_EX + "\nWill you include the chosen artists with the related artists? " + Fore.WHITE + "\n\n1. True\n2. False ")]
                print()
                print(
                    Fore.LIGHTBLUE_EX + "You will now search for the artists you want to find related artists to. \n" + Fore.WHITE)
                crq.add_related_artists_from_searched_artists(sp, number_of_tracks_to_add, random_artist=random_artist,
                                                              random_track=random_track,
                                                              include_given_artist=add_chosen_artist)

            if int(add_song_queue_choice) == 6:
                artist_info = sfa.search_for_one_artist_until_correct(sp)
                trackName, trackURIs, artist_name = sfa.show_all_tracks_from_artist_id(artist_info[2], sp,
                                                                                       artist_info[3])
                astq.let_user_specify_which_songs_to_queue(trackURIs, trackName, artist_name, sp)

            if int(add_song_queue_choice) == 7:
                print("7. Search for artists, songs from these artists only.\n")

                print(Fore.LIGHTBLUE_EX + "You will now search for artists: \n" + Fore.WHITE)
                artists = crq.search_for_artists(sp)

                number_of_tracks_to_add = utl.specify_int_in_range(1, 50,
                                                                   Fore.LIGHTBLUE_EX + "\nChoose number of tracks to add to queue (1-50). \n" + Fore.WHITE)

                track_dict = {1: "top", 2: "all"}
                message_artist = Fore.LIGHTBLUE_EX + "\nHow would you pick songs from your chosen artists?\n" \
                                 + Fore.WHITE + "1. Randomly pick among top 10 songs. \n" \
                                                "2. Randomly pick among all of the artists' songs.\n"

                top_all = track_dict[utl.specify_int_in_range(1, 2, message_artist)]
                crq.add_random_songs_from_searched_artists(artists=artists, spotify_object=sp,
                                                           number_of_songs_to_add=number_of_tracks_to_add,
                                                           top_all=top_all)

            # Find songs by genre (x).
            if int(add_song_queue_choice) == 8:
                print("Not implemented. ")

            # Add songs based on tracks, artists and/or genre.
            if int(add_song_queue_choice) == 9:
                reco.add_recommendation_seeds_to_queue(sp=sp)

        # Find first occurrence of an artist in your playlists.
        if user_choice == 5:
            fooc.first_occurance(sp)

        if user_choice == 6:
            print("TODO")
            print("Add next_track() / pause_playback / previous_track() ")
            print("recommendation_genre_seeds(), recommendations()")
            print("Start a track: sp.start_playback(uris=['spotify:track:7lEptt4wbM0yJTvSG5EBof'])")
            print("Add to queue should also include songs by the artists you are following. "
                  "'Include the artists uou are following?'")

        print()
        # break the while loop and end spotipy
        if user_choice == -1:
            break

        # check if the user wants to proceed. Main reason to have this is
        # that the user can see the output from last spotify feature call. (add random songs to queue.
        # otherwise it would just call clear terminal and all information would be gone
        if not skip_choice:
            if utl.proceed():
                utl.clear_terminal()
            else:
                break


spotify_terminal_interface()
