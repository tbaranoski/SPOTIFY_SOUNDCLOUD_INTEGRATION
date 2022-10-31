import Spotify_Config
from remote_spotify import remote
import spotipy
import Spotify_Config


#logging
import logging

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
    REDIRECT_URI = "http://localhost:8888/callback"  #No clue what this does yet
    SpotifyId = Spotify_Config.USER_NAME #Not sure if this is correct
    Authenticated_bool = False


    #Code Copied From https://github.com/ruckshan-ratnam/Spotify-Remote README.md
    try:
        token = spotipy.util.prompt_for_user_token(SpotifyId, scope, client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
        Authenticated_bool = True
    except:
        Authenticated_bool = False
        #log unsucessfull Spotify Authentication. I added this line
        logging.error("ERROR Authenticating Spotify Login in Control_Playback_Spotify.py")

        #Code that was copied
        os.remove(f".cache-{Spotify_Config.USER_NAME}")
        token = spotipy.util.prompt_for_user_token(SpotifyId, scope, client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)


    #return the remote object if Authentication was succesfull
    if(Authenticated_bool == True):
        spotify_object = spotipy.Spotify(auth=token)    
        remote_obj = remote(spotify_object)
        return remote_obj

    else:
        return None


########################################################################
########################################################################
def Control_Spotify_Playback(remote = None, command = None):

    #Determine if music should be paused, played, skipped, repeated, or skipped to previous track
    #If the funciton did not recieve valid inputs then log error
    if((command == None) or (remote == None)):
        logging.error("No command for playback was given in Control_Playback_Spotify.py")

    #pause the current song
    elif(command == "pause"):
        remote.pause(device=None)

    #resume where song left off
    elif(command == "play"):

        #Get Current song offset and play from there. Logic in remote.py
        remote.play(key=None,location=None)

    #Skip to next song
    elif((command == "skip") or (command =="next")):
        remote.next(device=None)

    #Go to last Song
    elif((command == "last") or (command == "previous")):
        remote.last(device=None)

    #Repeat Song
    elif((command == "repeat") or (command == "loop")):
        remote.rep(off = False, device = None)
    
########################################################################
########################################################################

