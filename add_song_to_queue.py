import spotipy
import sys
import argparse
from colorama import Fore
import operator
import utility_functions as utl
import utility_spotify as utl_sp


#  how to use scope variables
#https://developer.spotify.com/documentation/general/guides/scopes/

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("query", help='Specify artist, track and album you want to find. You can specify all of them and the names '
                                      'must not be absolutely correct. Write like this: '
                                      '"artist:coldplay'
                                      'album:viva la vida '
                                      'track:Death and all his friends". ("artist:coldplay")', type=str)
    parser.add_argument("limit", help="Look for this number of search results. If you are precice with artist, album and track search, a small number here is enough. "
                                      " (10) ", type=int)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()


def print_query(query, print_to_screen=True):
    """
    Print query nice if it is correctly specified.
    query = "artist:coldplay track:fix you" would give this:
    Search for:
        artist: Coldplay
        track: Fix you
    :param query: input query (see add_desired_song_to_queue() for detailed description )
    :return: -1 if query is not correctly written, otherwise it returns the same query as the input
    """
    strings_must_be_some_of_these = ["artist:", "track:", "album:"]
    all_idxes = [[len(query)]]
    idx = []
    # see if query includes one/several of the strings it must include, with index for where the strings are found
    for string in strings_must_be_some_of_these:
        start_idx = utl.find_str(query, string)
        if start_idx != -1:
            idx.append([start_idx, string])
            all_idxes.append([start_idx])
    if len(idx) == 0:
        print("\nWrong input: " + Fore.RED + str(query) + Fore.WHITE)
        print("Remember, input must include at least one of the following words: [artist, track, album] followed by a ':'. "
              "\nExample: artist:coldplay album:viva la vida")
        return -1
    idx = sorted(idx, key=operator.itemgetter(0), reverse=False)
    all_idxes = sorted(all_idxes, key=operator.itemgetter(0), reverse=False)
    if print_to_screen:
        print("Search for: ")
    for i in range(len(idx)):
        if str(query[all_idxes[i+1][0] - 1]) != " " and i != len(idx)-1:
            print("\nWrong input: " + Fore.RED + str(query) + Fore.WHITE)
            print(
                "Remember, there must be space between input search. "
                "\nOK: artist:coldplay album:viva la vida"
                "\nNOT OK: artist:coldplayalbum:viva la vida")
            return -1
        if print_to_screen:
            print(idx[i][1] + " ", str(query[(all_idxes[i][0] + len(idx[i][1])):all_idxes[i+1][0]]).capitalize())
    return query


def search_for_track(query, spotify_object, type='track', limit=3):
    while print_query(query) == -1:
        query = input("Try to search again: ")
        print("\n")

    # result: list with length equal to limit, each element is all info about searched track
    result = spotify_object.search(q=query, type=type, limit=limit, offset=0)[type + "s"]['items']

    dict_number_to_track_id = dict()
    N_1, N_2 = 3, 25
    print("\n" + Fore.LIGHTBLUE_EX + "Number " + Fore.YELLOW + "  Track " + Fore.WHITE + " "*(N_2-6) + Fore.LIGHTMAGENTA_EX + "Artist / Album (populatity factor)" + Fore.WHITE)
    for count, info in enumerate(result):
        album_name = info['album']['name']
        song_uri = info['href']
        song_id = info['id']
        popularity = info['popularity']
        artist = info['artists'][0]['name']

        song_name, emoji_len_count = utl.shorten_long_names_count_emojis(info=info, max_letters=(N_2-5))
        album_name, emoji_len_count = utl.shorten_long_names_count_emojis(info=info['album'], max_letters=25)
        second_n = N_2 - len(str(song_name))
        first_n = N_1 - len(str(count+1)) + 1
        print(str(count+1) + ":" + " "*first_n + "    " + str(song_name) + " "*second_n + str(artist) + " / "
              + str(album_name) + " (" +str(popularity) + ")")
        dict_number_to_track_id[count+1] = [song_id,song_name, artist]
    return dict_number_to_track_id




def add_desired_song_to_queue(query, spotify_object, type='track', limit=3):
    """
    This function will give you the possibility to search spotify for songs you would like to add to your queue. You must have an active device
    in order to do so, otherwise this function will terminate. You can find the desired song to add by searching with three different parameters:
    [track, album, artist].
    :param query: search string. Must at least one of the words [track, album, artist] followed by a ':' and your search word.
    You can use more than one, but then they must be separated with a blank space.
    OK: "artist:coldplay"
    OK: "artist:coldplay album:viva la vida"
    NOT OK: "artist:coldplayalbum:viva la vida" (missing blank space between each category)
    NOT OK: "artistcoldplay albumviva la vida" (missing ':')
    :param spotify_object: a proper spotify object with authorization parameters correctly given.
    :param type: what to search for (type="track")
    :param limit: number of search results (5)
    :return:
    """
    while True:
        # here you can have different functions giving a dict as output

        if query == 'playlist':
            utl_sp.see_my_public_playlists(private_public_collaborative=int(limit))
            # baluba function if query=baluba, then add 'limit' number of random songs to queue, then break
            #baluba(limit)
            print("No implemented yet. Will give random songs somehow. Limit will tell how many random songs to add")
            break

        # add limit number of random songs from 1 artist

        if query == 'baluba':
            # baluba function if query=baluba, then add 'limit' number of random songs to queue, then break
            #baluba(limit)
            print("No implemented yet. Will give random songs somehow. Limit will tell how many random songs to add")
            break

        # normal adding, by searching in normal manner
        dict_number_to_track_id = search_for_track(query, spotify_object, type=type, limit=limit)

        happy = input(Fore.WHITE + "\nDid you find the song you want to queue? If so, enter the corresponding" + Fore.LIGHTBLUE_EX + " number" +Fore.WHITE +" to add it. "
                      "\nMultiple songs can be added. Separate the desired song numbers with either ':' or '-'. "
                      "\n1-5 would include song number 1, 2, 3, 4 and 5. \n1:3 would include song number 1 and 3."
                        "\n1-3:7 would include song number 1, 2, 3 and 7. \nMake sure that the numbers you choose are found under" + Fore.LIGHTBLUE_EX + " Number." + Fore.WHITE +                                                                                                                                                                                                                                                                   ""
                      "\nOtherwise, enter" + Fore.YELLOW + " 'no' " + Fore.WHITE + " to search again or " + Fore.LIGHTRED_EX + " 'exit' " + Fore.WHITE + " to stop the search. ")

        if happy == 'exit':
            break
        if happy == 'no':
            new_query = input('\nSearch again for songs. Do not use " " this time. \n'
                              "If you write 'same', then same search will be used. " + Fore.LIGHTGREEN_EX + '\nNew search: ' + Fore.WHITE)
            if new_query == 'same':
                print("Use this search: ", query)
                new_query = query
            else:
                while print_query(new_query, print_to_screen=False) == -1:
                    new_query = input(Fore.LIGHTGREEN_EX + "\nTry to search again: " + Fore.WHITE)

            limit = input(Fore.LIGHTGREEN_EX + "Number of search results: " + Fore.WHITE)
            while not utl.RepresentsInt(limit):
                limit = input(Fore.LIGHTGREEN_EX + "Wrong input. Try again. Look for this number of search results: " + Fore.WHITE)
            limit = int(limit)
            query = new_query
        else:
            adding_numbers = utl.convert_song_numbers_to_useful_numbers(happy, limit)
            if adding_numbers == -1:
                utl.clear_terminal()
                print("Something wrong with your input. Input: ", happy)
                print("Error: ")
                utl.convert_song_numbers_to_useful_numbers(happy, limit)
                print("\n")
                continue

            print("\n")
            utl.clear_terminal()
            for num in adding_numbers:
                happy = num
                if int(happy) in dict_number_to_track_id.keys():
                    # must check if there is an active device, otherwise we can not add songs to the queue and the function termiantes
                    try:
                        spotify_object.add_to_queue(uri=dict_number_to_track_id[int(happy)][0])
                        print(Fore.LIGHTGREEN_EX + str(dict_number_to_track_id[int(happy)][1]) + " (" + str(dict_number_to_track_id[int(happy)][2]) + ")" + Fore.WHITE + " was added to the queue. ")
                    except spotipy.exceptions.SpotifyException:
                        print("Player command failed: No active device found, reason: NO_ACTIVE_DEVICE.")
                        print("One device must play music before this can be done.")
                        return 0
            return 0
        utl.clear_terminal()



if __name__ == "__main__":

    scope = 'user-modify-playback-state user-library-read user-read-email user-read-private user-top-read user-modify-playback-state user-read-playback-state'
    #result = utl_sp.create_spotify_object(scope=scope).search(q=args.query, type="playlist", limit=5, offset=0)
    #print(result)
    sp = utl_sp.create_spotify_object(scope=scope)
    add_desired_song_to_queue(query=args.query, spotify_object=sp, limit=args.limit)
