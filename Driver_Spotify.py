import Spotify_Authentication
import Control_Playback_Spotify
import time #for testing and pausing


import logging

#Set log level to INFO to debug (WARNING is default)
logging.basicConfig(level=logging.INFO)


######     MAIN TEST DRIVER      ###########################################
############################################################################
def main():
    
    #Authenticate Spotify Login
    #Spotify_Authentication.Authenticate_Spotify_Login()
    print("Start Test")
    remote_object = Control_Playback_Spotify.Setup_Spotify_Remote()

    #See if Spotify and Remote have been Authenticated Succesfully...If so control playback
    if(remote_object != None):

        #Test Pause
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "pause")
        #time.sleep(1)
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "play")
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "next")
        #Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "last")
        Control_Playback_Spotify.Control_Spotify_Playback(remote = remote_object, command = "loop")

    else:
        logging.error("Can Not Control Spotify Playback in Driver.py")

    #finish Statement
    print("Finished Spotify Authentication")



############################################################################
############################################################################

main()