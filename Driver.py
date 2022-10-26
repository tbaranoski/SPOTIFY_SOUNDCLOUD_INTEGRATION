import Spotify_Authentication
import 


import logging

#Set log level to INFO to debug (WARNING is default)
logging.basicConfig(level=logging.WARNING)


######     MAIN TEST DRIVER      ###########################################
############################################################################
def main():
    
    #Authenticate Spotify Login
    Spotify_Authentication.Authenticate_Spotify_Login()
    


    print("Finished Spotify Authentication")



############################################################################
############################################################################

main()