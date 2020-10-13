import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# https://towardsdatascience.com/using-python-to-create-spotify-playlists-of-the-samples-on-an-album-e3f20187ee5e

# function description (inputs, return uzw)
# https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/

# https://medium.com/better-programming/how-to-extract-any-artists-data-using-spotify-s-api-python-and-spotipy-4c079401bc37



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



scope = "user-library-read"
token = SpotifyOAuth(scope=scope)
print(token.redirect_uri)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

token = SpotifyOAuth(scope=scope)
sp = spotipy.Spotify(auth_manager=token)
print(sp.current_user())
print(1/0)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri="https://example.com/callback/", scope=scope))

results = sp.current_user_saved_tracks()
print(results)
auth_manager = SpotifyClientCredentials()
auth_manager = SpotifyOAuth()
sp = spotipy.Spotify(auth_manager=auth_manager)
print(sp.current_user())
playlists = sp.user_playlists()
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None


yoste_uri = 'spotify:artist:2wwZDwSBHaVaOI6cE2hfhf'


auth = SpotifyClientCredentials()

token = auth.get_access_token()
print(token)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(), auth_manager=SpotifyOAuth())
#spotify = spotipy.Spotify(auth=token)
print(spotify.artist_top_tracks(artist_id="2wwZDwSBHaVaOI6cE2hfhf"))
results = spotify.artist_albums(yoste_uri, album_type='appears_on')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


search_str = 'Radiohe'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
result = sp.search('Yoste')
print(result)
result = sp.search('dwiojdoej')
print(result)
print("\n\n hehe")
#spotify.add_to_queue(uri='https://open.spotify.com/track/3iSqkvJmmEfvG65MI0Ua8R?si=xkcbuSaIT2eT6TYTVQFdag')
print(spotify.current_user_playlists())