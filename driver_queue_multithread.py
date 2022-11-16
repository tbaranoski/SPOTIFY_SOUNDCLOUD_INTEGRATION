### Multithreaded Queue initializer   ####
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, wait

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

#Itialize Three objects with Multithreading
def initialize_objects_multithreaded():

    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = [] #Stores thread return values (objects)

        #Submit thread tasks for setting up objects
        tasks.append(executor.submit(Control_Playback_Spotify.Setup_Spotify_Remote))
        tasks.append(executor.submit(spotipy.Spotify, auth_manager=SpotifyOAuth(client_id=Spotify_Config.SPOTIFY_ID, client_secret=Spotify_Config.SPOTIFY_SECRET, redirect_uri=Spotify_Config.REDIRECT_URI, scope="user-library-read")))
        tasks.append(executor.submit(Soundcloud, SoundCloud_Config.SOUNDCLOUD_SECRET, SoundCloud_Config.SOUNDCLOUD_ID))
        
        wait(tasks) #wait for threads to finish
        
        #Return initialized objects for APIs
        try:
            if((tasks[0].result() != None) or (tasks[1].result() != None) or (tasks[2].result() != None)):
                return [tasks[0].result(), tasks[1].result(), tasks[2].result()]
        except:
            logging.error("Multithreading object initialization error")
            return None


#Function gets songs for Spotify and SOundcloud API and returns the data structure objects. Does with multithreading
def get_songs_mutithreaded(spotify_object = None, soundcloud_object = None):

    #Make sure arguments for function are valid
    if((spotify_object != None) and (soundcloud_object != None)):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [] #Stores thread return values (objects)
    
            #Submit thread tasks for getting songs from API
            tasks.append(executor.submit(get_spotify_lists.add_spotify_playlists, temp_list = (get_spotify_lists.get_lists(spotify_obj = spotify_object)), spot_obj= spotify_object))
            tasks.append(executor.submit(get_soundcloud_lists.Get_Soundcloud_lists, account_obj = soundcloud_object))

            wait(tasks) #wait for threads to finish

            #Return populated data structures (Spotify and SOundcloud)
            try:
                if((tasks[0].result() != None) or (tasks[1].result() != None)):
                    return [tasks[0].result(), tasks[1].result()]
            except:
                logging.error("Multithreading object initialization error")
                return None

    else:
        logging.error("parameters passed into get_songs_mutithreaded() are NOT valid")
###############################################################################################################
#Driver for the queue. Main Driver for both SOundcloud and Spotify API
def main():
    
    #Itialize objects with multithreading
    initialize_objects_array = initialize_objects_multithreaded()
    
    spotify_object = initialize_objects_array[0]
    spotify_object = initialize_objects_array[1]
    soundcloud_object = initialize_objects_array[2]

    #Populate Data Structures to store songs with multithreading
    data_arrays = get_songs_mutithreaded(spotify_object = spotify_object, soundcloud_object = soundcloud_object)
    spot_data_object = data_arrays[0]
    soundcloud_data_object = data_arrays[1]

    #Test
    spot_data_object.print_all_data()   
    soundcloud_data_object.print_all_data()


    #End of program
    print("--- %s seconds ---" % (time.time() - start_time))


    ### Aditional Timing
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
