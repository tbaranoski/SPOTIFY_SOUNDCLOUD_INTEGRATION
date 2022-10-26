import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import Spotify_Config

#Without User Authentication (For now)
#Reference: https://github.com/plamere/spotipy/blob/master/README.md

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=Spotify_Config.SPOTIFY_ID,
                                                           client_secret=Spotify_Config.SPOTIFY_SECRET))

results = sp.search(q='lil uzi', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])