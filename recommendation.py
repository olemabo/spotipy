import utility_functions as utl
import utility_spotify as utl_sp
from colorama import Fore
import search_for_artist as sfa

def return_x_recommendations_based_on_input_seed(sp, seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None):
    """
    Get a list of recommended tracks for one to five seeds. (at least one of seed_artists, seed_tracks and seed_genres are needed)
    :param seed_artists: a list of artist IDs, URIs or URLs
    :param seed_genres: a list of genre names. Available genres for recommendations can be found by calling recommendation_genre_seeds
    :param seed_tracks: a list of track IDs, URIs or URLs
    :param limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 100
    :param country: An ISO 3166-1 alpha-2 country code. If provided, all results will be playable in this country.
    :return: A list of recommended tracks for one to five seeds.
    [
            track_name,
            track_id,
            track_popularity,
            duration_ms,
            album_name,
            album_id,
            artist_list ( [ [artist_1_id, artist_1_name], [artist_2_id, artist_2_name], ... ] )
    """
    if seed_artists == None and seed_tracks == None and seed_genres == None:
        raise ValueError("Must include input data about at least one of the following: seed_artists, seed_genres and seed_tracks.")

    legal_recommendations = sp.recommendation_genre_seeds()['genres']
    for genre_seed in seed_genres:
        if genre_seed not in legal_recommendations:
            raise ValueError("Illegal genre seed")

    recommendations = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit, country=country)
    track_information_list_json = recommendations['tracks']

    recommendation_list_to_return = []

    for track_info in track_information_list_json:
        artists = track_info['album']['artists']
        artist_list = []
        for artist in artists:
            temp_artist_id = artist['id']
            temp_artist_name = artist['name']
            artist_list.append([temp_artist_name, temp_artist_id])
        album_name = track_info['name']
        album_id = track_info['id']
        track_id = track_info['id']
        track_name = track_info['name']
        track_popularity = track_info['popularity']
        duration_ms = track_info['duration_ms']

        recommendation_list_to_return.append([
            track_name,
            track_id,
            track_popularity,
            duration_ms,
            album_name,
            album_id,
            artist_list,
        ])

    return recommendation_list_to_return


def let_user_search_for_recommendation_seed(sp):
    chosen_tracks_id, chosen_genres, chosen_artists_id = [], [], []
    chosen_tracks_names, chosen_artists_names = [], []
    legal_recommendations = 0
    utl.clear_terminal()
    while True:
        if len(chosen_tracks_id) > 0 or len(chosen_genres) > 0 or len(chosen_artists_id) > 0:
            print("Current chosen seeds: \n")
            if len(chosen_tracks_id) > 0:
                print(Fore.CYAN + "Tracks: " + Fore.WHITE + utl.convert_list_string_to_sentence(chosen_tracks_names))
                if (len(chosen_tracks_names[-1].split("and")) == 2):
                    chosen_tracks_names[-1] = chosen_tracks_names[-1].split("and")[-1][1:]

            if len(chosen_artists_id) > 0:
                print(Fore.YELLOW + "Artists: " + Fore.WHITE + utl.convert_list_string_to_sentence(chosen_artists_names))
                if (len(chosen_artists_names[-1].split("and")) == 2):
                    chosen_artists_names[-1] = chosen_artists_names[-1].split("and")[-1][1:]

            if len(chosen_genres) > 0:
                print(Fore.LIGHTMAGENTA_EX + "Genres: " + Fore.WHITE + utl.convert_list_string_to_sentence(chosen_genres))
                if (len(chosen_genres[-1].split("and")) == 2):
                    chosen_genres[-1] = chosen_genres[-1].split("and")[-1][1:]
            print()
        else:
            print("Add info before generating tracks based on your input.\n")
        message = "1: Add track seed\n" \
              "2: Add artist seed\n" \
              "3: Add genre seed\n" \
              "4: Finish searching\n"
        option = utl.specify_int_in_range(1, 4, message=message, error='x')
        if option == 1:
            utl.clear_terminal()
            print("Search for tracks to add to the feed.\n")
            track_info = search_for_tracks(sp)
            if track_info[1] not in chosen_tracks_id:
                chosen_tracks_id.append(track_info[1])
                # track_info[0] = short name, track_info[3] = full name
                chosen_tracks_names.append(track_info[3])

        if option == 2:
            utl.clear_terminal()
            print("Search for artists to add to the feed.\n")
            artist_info = search_for_artists(sp)
            if artist_info[2] not in chosen_artists_id:
                chosen_artists_id.append(artist_info[2])
                chosen_artists_names.append(artist_info[3])

        if option == 3:
            utl.clear_terminal()
            print("Search for genres to add to the feed.\n")
            genre_info, legal_recommendations = search_for_genre(sp, legal_recommendations)
            for new_genre in genre_info:
                if new_genre.capitalize() not in chosen_genres:
                    chosen_genres.append(new_genre.capitalize())

        if option == 4:
            for idx, genre in enumerate(chosen_genres):
                chosen_genres[idx] = genre.lower()
            print()
            break

        if option == -1:
            return None, None, None
        utl.clear_terminal()
    return chosen_tracks_id, chosen_genres, chosen_artists_id


def recommendation_function(sp):
    """

    :param sp:
    :return: [ ['Motion Picture Soundtrack', '79M3U8vzBBfSFRyxFFGVRl', 34, 179609,
    'Motion Picture Soundtrack', '79M3U8vzBBfSFRyxFFGVRl',
    [['Shallou', '7C3Cbtr2PkH2l4tOGhtCsk']], ... ]

    """
    chosen_tracks_id, chosen_genres, chosen_artists_id = let_user_search_for_recommendation_seed(sp)
    if len(chosen_tracks_id) > 0 or len(chosen_genres) > 0 or len(chosen_artists_id) > 0:
        limit = utl.specify_int_in_range(1, 100, message="How many tracks do you want to generate (1-100)? ")
        recommendations = return_x_recommendations_based_on_input_seed(sp, seed_artists=chosen_artists_id, seed_genres=chosen_genres, seed_tracks=chosen_tracks_id, limit=limit, country=None)
        return recommendations
    else:
        return -1

def search_for_artists(sp):
    """
    :param sp: spotify object
    :return: ['https://api.spotify.com/v1/artists/40HDiLfKm0tXk2FxlJx6aO', 'spotify:artist:40HDiLfKm0tXk2FxlJx6aO', '40HDiLfKm0tXk2FxlJx6aO', 'Jim Yosef']
    """
    search_artist = sfa.search_for_one_artist_until_correct(sp, search_type="artist", can_choose_current_artist=False)
    return search_artist

def search_for_tracks(sp):
    search_track = utl_sp.search_one_type(sp, "Fix You", type="track", limit=3, line_adjustment=28)
    return search_track


def search_for_genre(sp, show_choosen_genres=True, legal_recommendations=0):
    """

    :return: ['chill', 'opera', ...]
    """
    if legal_recommendations == 0:
        legal_recommendations = sp.recommendation_genre_seeds()['genres']
    genre_dict, tot_genres = utl_sp.show_info_and_append_to_dict(legal_recommendations, columns=4)

    nice_numbers = utl_sp.specify_number_in_range_from_list(genre_dict, what_to_choose_from="genre")

    if nice_numbers == -1:
        return [], []

    return_playlist = []
    if show_choosen_genres:
        print("\nYour choice(s): ")
    for idx, num in enumerate(nice_numbers):
        return_playlist.append(genre_dict[int(num)])
        if show_choosen_genres:
            print("Genre name: " + str(return_playlist[idx]) + Fore.WHITE)

    return return_playlist, legal_recommendations

def add_recommendation_seeds_to_queue(sp):
    recommendations = recommendation_function(sp)
    for recommendation in recommendations:
        track_id = recommendation[1]
        track_name = recommendation[0]
        main_artist_name = recommendation[6][0][0]
        # recommendation = ['Motion Picture Soundtrack', '79M3U8vzBBfSFRyxFFGVRl', 34, 179609, 'Motion Picture Soundtrack', '79M3U8vzBBfSFRyxFFGVRl', [['Shallou', '7C3Cbtr2PkH2l4tOGhtCsk']]
        if utl_sp.add_song_to_queue(sp, track_id, track_name, main_artist_name, ""):
            continue
        else:
            break


scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing ' \
            'user-read-private user-top-read playlist-read-private playlist-read-collaborative'

sp = utl_sp.create_spotify_object(scope=scope)

# add_recommendation_seeds_to_queue(sp)
