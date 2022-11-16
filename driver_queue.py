import logging
logging.basicConfig(level=logging.INFO)

#import queue
from playback_queue import playback_queue


#Timing imports
import threading
import time
start_time = time.time()

#Spotify Driver Imports
##############################################################################
import Spotify_Authentication
import Control_Playback_Spotify
import time #for testing and pausing
import get_spotify_lists

import Spotify_Config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_lists import Spotify_Data,Spotify_List,Spotify_Song
##############################################################################

#Soundcloud Driver Imports
from soundcloudpy import Soundcloud
import SoundCloud_Config
import Control_Playback_Soundcloud
import get_soundcloud_lists
from soundcloud_lists import SoundCloud_Data

#Driver for the queue. Main Driver for both SOundcloud and Spotify API
def main():
    ##############################################################################################################################################################################
    #Set up Spotify AUthentication
    #SetUp SPotify COntrol Remote
    
    remote_object_Spotify = Control_Playback_Spotify.Setup_Spotify_Remote()

    #Create Spotify object
    spotify_object = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Spotify_Config.SPOTIFY_ID, client_secret=Spotify_Config.SPOTIFY_SECRET, redirect_uri=Spotify_Config.REDIRECT_URI, scope="user-library-read"))

    #Get Spotify Songs from Playlists
    spotify_playlists = get_spotify_lists.get_lists(spotify_obj = spotify_object)
    spot_data_object = get_spotify_lists.add_spotify_playlists(temp_list = spotify_playlists, spot_obj= spotify_object)

    #Test
    spot_data_object.print_all_data()
    
    ###############################################################################################################################################################################################
    ###############################################################################################################################################################################################
    ###  Set Up SOundcloud   ###
    
    #Authenticate Soundcloud API Key
    #Note follow readme in soundcloud-py to figure out how to get API ID and Key. Add to Soundcloud_Config.py
    soundcloud_account_obj = Soundcloud(SoundCloud_Config.SOUNDCLOUD_SECRET, SoundCloud_Config.SOUNDCLOUD_ID)

    #If the soundcloud authentication is succesfull get control of API    
    if(soundcloud_account_obj != None):
        #Control_Playback_Soundcloud.Control_Soundcloud_Playback(remote = soundcloud_account, command = "play")
         
        soundcloud_d = SoundCloud_Data()
                
        soundcloud_data_object = get_soundcloud_lists.Get_Soundcloud_lists(remote = soundcloud_account_obj, soundcloud_data_obj = soundcloud_d)
        soundcloud_data_object.print_all_data()

    else:
        logging.error("Soundcloud Data Object Not populated")

    #End of program
    print("--- %s seconds ---" % (time.time() - start_time))



    ###Test Queue
    queue_obj = playback_queue()

    #Add to queue
    queue_obj.add_queue(obj = (spot_data_object.playlists_array[1].Song_objects_array[0]))
    queue_obj.add_queue(obj = (spot_data_object.playlists_array[1].Song_objects_array[2]))
    queue_obj.add_queue(obj = (soundcloud_data_object.playlists_array[1].Song_objects_array[0]))
    queue_obj.add_queue(obj = (spot_data_object.playlists_array[1].Song_objects_array[3]))
    queue_obj.print_queue()

    #Print the top of the queue
    queue_obj.remove_queue(obj = (soundcloud_data_object.playlists_array[1].Song_objects_array[0]))
    queue_obj.print_queue()

    #Test Print Queue by popping off front most song
    queue_obj.print_single_song(queue_obj.get_next_up())

    #Tets Print Rest of Queue...SHould be two songs
    queue_obj.print_queue()




####################################################################################################################################
####################################################################################################################################
###    END OF DRIVER    ###
main()