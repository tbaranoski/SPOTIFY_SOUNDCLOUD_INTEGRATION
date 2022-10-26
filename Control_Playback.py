from Spotify_Config import SPOTIFY_ID
from remote import remote
from spotipy.util import util
import Spotify_Config

def Setup_Spotify_Remote():

    ###   Possible Scopes to use when authenticating   ###
    #user-read-private
    #user-read-playback-state
    #user-library-read
    #playlist-read-private
    #user-modify-playback-state

    #Set Scope parameter
    scope = 'user-read-private user-library-read playlist-read-private user-read-playback-state user-modify-playback-state'

    #Get Authentication Keys
    CLIENT_ID = Spotify_Config.SPOTIFY_ID
    CLIENT_SECRET = Spotify_Config.SPOTIFY_SECRET
    REDIRECT_URI = 'https://example.com/callback/'  #No clue what this does yet

    #Code Copied From https://github.com/ruckshan-ratnam/Spotify-Remote README.md
    try:
        token = util.prompt_for_user_token(SpotifyId, scope, client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(SpotifyId, scope, client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)

    spotify_object = spotipy.Spotify(auth=token)    


