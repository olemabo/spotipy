import utility_spotify as utl_sp
import utility_functions as utl
import random
import search_for_artist as search


def return_artist_top_tracks(artist_id, sp):
    """
    return top 10 tracks for artist with artist id equal to artist_id
    :param artist_id: artist_id - the artist ID, URI or URL
    :param sp: spotipy object
    :return: list with top 10 tracks for that artist (json)
    """
    return sp.artist_top_tracks(artist_id)['tracks']


def return_artist_related_artists(artist_id, sp):
    """
    return top 20 related artists of the artist with artist id equal to artist_id
    :param artist_id: artist_id - the artist ID, URI or URL
    :param sp: spotipy object
    :return: list with top 20 related artists (json)
    """
    return sp.artist_related_artists(artist_id)['artists']


def return_all_related_artists_to_list(artist_id, sp, include_given_artist=False):
    related_artists = return_artist_related_artists(artist_id, sp)
    all_related_artists = []
    if include_given_artist:
        all_related_artists.append(return_artist_info(sp.artist(artist_id)))
    for related_artist in related_artists:
        all_related_artists.append(return_artist_info(related_artist))
    return all_related_artists


def return_artist_info(artist_json):
    """
    filter out relevant artist info from artist json
    :param artist_json: json of artist info
    :return: artist_id, artist_name, followers, popularity
    """
    followers = artist_json['followers']['total']
    artist_id = artist_json['id']
    artist_name = artist_json['name']
    popularity = artist_json['popularity']
    return artist_id, artist_name, followers, popularity


def find_random_artist_from_related_artists(artist_id, sp, how_random="uniform", include_given_artist=False):
    """
    Randomly return the info of random relevant artist to the artist_id given.
    :param artist_id: the id for a desired artist
    :param sp: spotify object
    :param how_random: 'uniform' -> equal probability to select every artist
                    'relevantness' -> higher probability to select artist most relevant to artist_id
    :return: (artist id, artist name, followers, popularity)
             ('33Cf4O1KAVbtQa00scMi2A', 'AK', 24718, 55)

    """
    related_list = return_all_related_artists_to_list(artist_id, sp, include_given_artist=include_given_artist)
    number_of_related_artists = len(related_list)
    choice_list = []
    if how_random == "uniform":
        choice_list = [i for i in range(0, number_of_related_artists)]
    if how_random == "relevance":
        for i in range(0, number_of_related_artists):
            for j in range(i+1):
                choice_list.append(number_of_related_artists - 1 - i)
    random.shuffle(choice_list)

    idx = random.randint(0, len(choice_list)-1)
    random_index = choice_list[idx]
    return related_list[random_index]



def search_for_artists(spotify_object):
    artists = []
    artists_name = []
    while True:
        your_artist_name = input("Search for new artist ('x' = exit): ")
        if your_artist_name == 'x':
            break
        info = search.search_for_artist(your_artist_name, spotify_object, type='artist', limit=3)
        if info == None:
            break
        if info != -1:
            artists.append(info)
            artists_name.append(info[3])
            print("Your current list: ", artists_name, "\n")
    return artists



def make_choice_list(number_of_related_artists, how_random="uniform"):
    choice_list = []
    if how_random == "uniform":
        choice_list = [i for i in range(0, number_of_related_artists)]
    if how_random == "relevance":
        for i in range(0, number_of_related_artists):
            for j in range(i + 1):
                choice_list.append(number_of_related_artists - 1 - i)
    random.shuffle(choice_list)
    return choice_list


def return_nice_list_of_top_tracks(artist_id, sp):
    top_tracks = return_artist_top_tracks(artist_id, sp)
    nice_list_top_tracks = []
    for track in top_tracks:
        nice_list_top_tracks.append([track['id'], track['name'], track['popularity']])
    return nice_list_top_tracks



def return_track_info(track_json):
    track_id = track_json['id']
    track_name = track_json['name']
    track_artist = track_json['artists']['name']
    return track_id, track_name, track_artist


def return_who_user_is_following(sp):
    """
    :param sp: spotipy object
    :return: list of all the artists the user is following [[artist_id, artist_name, followers, popularity], ... []]
    """
    following_list = []
    current_user_followed = sp.current_user_followed_artists(limit=10)['artists']
    followers = current_user_followed['items']
    for following in followers:
        followers = following['followers']['total']
        artist_id = following['id']
        artist_name = following['name']
        popularity = following['popularity']
        following_list.append([artist_id, artist_name, followers, popularity])

    next_info = sp.next(current_user_followed)
    while next_info:
        followers = next_info['artists']['items']
        for following in followers:
            followers = following['followers']['total']
            artist_id = following['id']
            artist_name = following['name']
            popularity = following['popularity']
            following_list.append([artist_id, artist_name, followers, popularity])
        next_info = sp.next(next_info['artists'])

    return following_list


def find_random_top_track_from_artist(sp, artist_id, how_random="uniform"):
    list_top_tracks = return_nice_list_of_top_tracks(artist_id, sp)
    number_of_top_tracks = len(list_top_tracks)
    choice_list = make_choice_list(number_of_top_tracks, how_random)
    random_idx = random.randint(0, len(choice_list) - 1)
    song_number = choice_list[random_idx]
    return list_top_tracks[song_number], song_number


def find_random_unique_top_tracks_from_artist(sp, artist_id, num_to_add):
    list_top_tracks = return_nice_list_of_top_tracks(artist_id, sp)
    number_of_top_tracks = len(list_top_tracks)

    rand_idxes = []
    while True:
        rand_idx = random.randint(0, number_of_top_tracks - 1)
        if rand_idx not in rand_idxes:
            rand_idxes.append(rand_idx)
        if len(rand_idxes) == number_of_top_tracks:
            print("Less songs than songs you want to add")
            break
        if len(rand_idxes) == num_to_add:
            break

    list_songs = []
    for rand_idx in rand_idxes:
        list_songs.append(list_top_tracks[rand_idx])
    return list_songs, rand_idxes


def add_x_random_top_track_from_random_follower(sp, number_of_tracks_to_add=1, random_artist="uniform", random_track="uniform", include_given_artist=True):
    following = return_who_user_is_following(sp)
    number_of_following = len(following)
    tracks_to_add = []
    for add in range(number_of_tracks_to_add):
        random_following_artist_idx = random.randint(0, number_of_following - 1)
        random_following_artist = following[random_following_artist_idx]
        randomRelatedArtist_id_name_followers_popu = find_random_artist_from_related_artists(random_following_artist[0], sp, how_random=random_artist, include_given_artist=include_given_artist)
        randomTopTrack_id_name_popu, song_number = find_random_top_track_from_artist(sp, artist_id=randomRelatedArtist_id_name_followers_popu[0], how_random=random_track)
        track_id_to_add_to_queue = randomTopTrack_id_name_popu[0]
        track_name_to_add_to_queue = randomTopTrack_id_name_popu[1]
        #print("Random artists you are following: ", random_following_artist[1])
        #print("Random relevant artist of " + str(random_following_artist[1]) + ": " + str(randomRelatedArtist_id_name_followers_popu[1]))
        #print("Random song from random relevant artist: ", randomTopTrack_id_name_popu[1])
        #print()
        tracks_to_add.append([track_id_to_add_to_queue, track_name_to_add_to_queue, randomRelatedArtist_id_name_followers_popu[1], random_following_artist[1]])
        #print(random_following_artist, randomTopTrack_id_name_popu, randomRelatedArtist_id_name_followers_popu[1])
    return tracks_to_add


def add_x_random_top_track_from_random_follower_to_queue(sp, number_of_tracks_to_add=1, random_artist="uniform", random_track="uniform"):
    tracks_to_add = add_x_random_top_track_from_random_follower(sp, number_of_tracks_to_add, random_artist, random_track)
    for track in tracks_to_add:
        # track = ['2cEBG31c2Y7mfRlLY8g1ah', 'Pictures', 'Benjamin Francis Leftwich', 'Ben Howard']
        if utl_sp.add_song_to_queue(sp, track[0], track[1], track[2], track[3]):
            continue
        else:
            break



def add_related_artists_from_searched_artists(spotify_object, number_of_songs_to_add, random_artist="uniform", random_track="uniform", include_given_artist=False):
    artists = search_for_artists(spotify_object)
    number_of_artists = len(artists)
    start_idx = random.randint(0, number_of_artists - 1)
    tracks_to_add = []
    for add in range(number_of_songs_to_add):
        # artist = ['https://api.spotify.com/v1/artists/2wwZDwSBHaVaOI6cE2hfhf', 'spotify:artist:2wwZDwSBHaVaOI6cE2hfhf', '2wwZDwSBHaVaOI6cE2hfhf', 'Yoste']
        artist = artists[start_idx]
        randomRelatedArtist_id_name_followers_popu = find_random_artist_from_related_artists(artist[1],
                                                                                             spotify_object,
                                                                                             how_random=random_artist,
                                                                                             include_given_artist=include_given_artist)
        randomTopTrack_id_name_popu, song_number = find_random_top_track_from_artist(spotify_object, artist_id=
                                                        randomRelatedArtist_id_name_followers_popu[0], how_random=random_track)

        #print(randomRelatedArtist_id_name_followers_popu[1], song_number, start_idx, artist[3], randomTopTrack_id_name_popu[1])

        track_id_to_add_to_queue = randomTopTrack_id_name_popu[0]
        track_name_to_add_to_queue = randomTopTrack_id_name_popu[1]
        tracks_to_add.append([track_id_to_add_to_queue, track_name_to_add_to_queue, randomRelatedArtist_id_name_followers_popu[1], artist[3]])

        start_idx += 1
        if start_idx == (number_of_artists):
            start_idx = 0

    for track in tracks_to_add:
        # track = ['2cEBG31c2Y7mfRlLY8g1ah', 'Pictures', 'Benjamin Francis Leftwich', 'Ben Howard']
        if utl_sp.add_song_to_queue(spotify_object, track[0], track[1], track[2], track[3]):
            continue
        else:
            break


def add_random_songs_from_searched_artists(artists, spotify_object, number_of_songs_to_add, top_all="top"):
    number_of_artists = len(artists)
    start_idx = random.randint(0, number_of_artists - 1)
    tracks_to_add = []

    number_songs_per_artist = [0] * len(artists)
    for i in range(number_of_songs_to_add):
        number_songs_per_artist[start_idx] = number_songs_per_artist[start_idx] + 1
        start_idx += 1
        if start_idx == (number_of_artists):
            start_idx = 0


    tracks_to_add = []
    for idx, num_to_add in enumerate(number_songs_per_artist):

        artist = artists[idx]

        if top_all == "top":
            randomTopTrack_id_name_popu, song_number = find_random_unique_top_tracks_from_artist(spotify_object, artist[1], num_to_add)

        if top_all == "all":
            randomTopTrack_id_name_popu, song_number = search.random_song_artist(spotify_object, artist[1], num_to_add)

        for track in randomTopTrack_id_name_popu:
            track_id_to_add_to_queue = track[0]
            track_name_to_add_to_queue = track[1]
            tracks_to_add.append(
                [track_id_to_add_to_queue, track_name_to_add_to_queue, artist[3],
                 artist[3]])

    random.shuffle(tracks_to_add)

    for track in tracks_to_add:
        print(track)
        # track = ['2cEBG31c2Y7mfRlLY8g1ah', 'Pictures', 'Benjamin Francis Leftwich', 'Ben Howard']
        if utl_sp.add_song_to_queue(spotify_object, track[0], track[1], track[2], track[3]):
            continue
        else:
            break


def queue_from_random_playlist(sp, number_of_tracks_to_add):
    playlists = utl_sp.return_all_playlists(sp, public=True, private=True, collaborative=True, printing=False)
    keys = list(playlists.keys())
    tracks_to_add = []
    for num in range(number_of_tracks_to_add):
        rand_key = random.choice(keys)
        # [['name'], ['id'], ['uri'], print_color]
        playlist_name = playlists[rand_key][0]
        playlist_uri = playlists[rand_key][2]
        info = return_random_song_in_playlist(sp, playlist_uri)
        tracks_to_add.append([info[0], info[1], info[2], playlist_name])

    for track in tracks_to_add:
        # track = ['2cEBG31c2Y7mfRlLY8g1ah', 'Pictures', 'Benjamin Francis Leftwich']
        if utl_sp.add_song_to_queue(sp, track[0], track[1], track[2], track[3]):
            continue
        else:
            break



def return_random_song_in_playlist(sp, playlist_uri):
    playlistTracks_uri_name_artist = return_all_songs_in_playlist(sp, playlist_uri)
    rand_idx = random.choice(playlistTracks_uri_name_artist)
    return rand_idx


def return_all_songs_in_playlist(sp, playlist_uri):
    playlist_info = sp.playlist_tracks(playlist_uri)['items']
    nice_format = []
    for track_json in playlist_info:
        track_uri = track_json['track']['uri']
        track_name = track_json['track']['name']
        # print(track_json['track']['album']['artists'])
        track_artist = track_json['track']['album']['artists'][0]['name']
        nice_format.append([track_uri, track_name, track_artist])
    return nice_format




#add_random_songs_from_searched_artists(utl_sp.create_spotify_object(), 3)

def test_space():
    sp = utl_sp.create_spotify_object()
    artist_id = '2wwZDwSBHaVaOI6cE2hfhf'
    artist_related = return_artist_related_artists(artist_id, sp)
    artist_top_tracks = return_artist_top_tracks(artist_id, sp)
    #print(utl.print_nice_json_format(artist_related[0]))
    #print(utl.print_nice_json_format(artist_top_tracks[0]))
    #print(artist_related, "\n", len(artist_related))
    #print(artist_top_tracks,"\n", len(artist_top_tracks))
    #print(return_who_user_is_following(sp))
    #print(utl.print_nice_json_format(return_who_user_is_following(sp)))
    #return_all_related_artists_to_list("2wwZDwSBHaVaOI6cE2hfhf", sp)
    #find_random_artist_from_related_artists(artist_id, sp)

    tracks_to_add = add_x_random_top_track_from_random_follower(sp, number_of_tracks_to_add=5, how_random="relevance")
    print(tracks_to_add)

