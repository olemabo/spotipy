import utility_spotify as utl_sp

scope = 'user-read-private user-read-playback-state user-modify-playback-state ' \
            'playlist-modify-public playlist-modify-private user-read-currently-playing ' \
            'user-read-private user-top-read playlist-read-private playlist-read-collaborative'
sp = utl_sp.create_spotify_object(scope=scope)

def get_collarborative_and_followed_playlist(sp):
    playlist = utl_sp.return_all_playlists(sp, public=False, private=False,
                                           collaborative=True, printing=True, remove_spotify_playlist=False)
    return playlist


#get_collarborative_and_followed_playlist(sp)