import utility_spotify as utl_sp
import spotipy
from colorama import Fore


# This script will add the current played spotify song to a public playlist of your choice
# TODO: add to a new playlist
# TODO: must check if the song is already in the list


def add_current_song_to_playlist2(sp, public=True, private=True, collaborative=True):
    track_name, artist_name, track_uri, playing_type = utl_sp.find_current_song_return_id(sp)
    if track_name == -1:
        return 0
    print(str(playing_type).capitalize() + " name: " + Fore.LIGHTBLUE_EX + str(track_name) + Fore.WHITE)
    print("Artist name: ", artist_name)
    print("You will now have to choose which playlists to add the song to.")
    playlists = utl_sp.see_my_public_playlists(sp, public, private, collaborative)
    if playlists == -1:
        return -1

    while True:
        still_want_to_add = input("\nDo you still want to add the song to these playlists? (y/n): ")
        if still_want_to_add == 'n':
            return -1
        if still_want_to_add == 'y':
            break

    output_log = []
    for playlist in playlists:
        # CHECK IF THE TRACK IS IN THE PLAYLIST
        if utl_sp.check_if_track_is_in_playlist(track_uri, playlist[2], sp):
            print("\nThe song is already in the playlist: ", playlist[0])
            add_anyway = input("Do you want to add it anyway? (y/n) ")
            while add_anyway not in ['y', 'n']:
                add_anyway = input("Wrong input. Do you want to add it anyway? (y/n)")
            if add_anyway == 'n':
                continue
        # user must specify if want to add anyway
        try:
            sp.playlist_add_items(playlist[1], [track_uri])
        except spotipy.exceptions.SpotifyException:
            print("You cannot add tracks to a playlist you don't own.")
            return "You cannot add tracks to a playlist you don't own."
        print(Fore.BLUE + track_name + Fore.WHITE + " was successfully added to the " + str(playlist[0]) + " playlist.")
        output_log.append(track_name + " was successfully added to the " + str(playlist[0]) + " playlist.")
    return output_log



if __name__ == "__main__":

    scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing'
    scope += ' user-read-private user-top-read playlist-read-private playlist-read-collaborative'
    sp = utl_sp.create_spotify_object(scope)

    add_current_song_to_playlist2(sp=sp, public=True, private=True, collaborative=True)






