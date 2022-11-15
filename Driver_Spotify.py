import Spotify_Authentication
import Control_Playback_Spotify
import time #for testing and pausing
import get_spotify_lists

import Spotify_Config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_lists import Spotify_Data,Spotify_List,Spotify_Song



import logging

#Set log level to INFO to debug (WARNING is default)
logging.basicConfig(level=logging.INFO)



######     MAIN TEST DRIVER      ###########################################
############################################################################
def main():
    
    #Authenticate Spotify Login
    #Spotify_Authentication.Authenticate_Spotify_Login()
    
    remote_object = Control_Playback_Spotify.Setup_Spotify_Remote()

    #Create Spotify object
    spotify_object = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Spotify_Config.SPOTIFY_ID, client_secret=Spotify_Config.SPOTIFY_SECRET, redirect_uri=Spotify_Config.REDIRECT_URI, scope="user-library-read"))

    #Get Spotify Songs from Playlists
    ##########################################################################################################
    spotify_playlists = get_spotify_lists.get_lists(spotify_obj = spotify_object)
    
    
    spot_data_object = get_spotify_lists.add_spotify_playlists(temp_list = spotify_playlists, spot_obj= spotify_object)
    spot_data_object.print_all_data()

    #See if Spotify and Remote have been Authenticated Succesfully...If so control playback
    if(remote_object != None):
        print("if")
        #Test Pause
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "pause")
        #time.sleep(1)
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "play")
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "next")
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "last")
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "repeat")

    else:
        logging.error("Can Not Control Spotify Playback in Driver.py")

    #finish Statement
    print("Finished Spotify Authentication")



############################################################################
############################################################################

main()