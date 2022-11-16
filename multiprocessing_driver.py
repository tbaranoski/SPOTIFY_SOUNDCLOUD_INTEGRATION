### Multithreaded Queue initializer   ####
import multiprocessing
from multiprocessing import Process, Queue, Value, Pipe
from time import sleep

#import threading libraries
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

########################################################################################################
#Helper Function: Get Soundcloud Data
def get_soundcloud_data(connection,temp_obj = None):
    if(temp_obj != None):

        soundcloud_data_object = get_soundcloud_lists.Get_Soundcloud_lists(account_obj = temp_obj)
        connection.send(soundcloud_data_object)

    else:
        logging.error("No soundcloud object passes to get_soundcloud_data")

########################################################################################################
#Helper Function: Get Spotify Data
def get_spotify_data(connection, temp_obj = None):
    if(temp_obj != None):

        spotify_playlists = get_spotify_lists.get_lists(spotify_obj = temp_obj)
        soundcloud_data_object = get_spotify_lists.add_spotify_playlists(temp_list = spotify_playlists, spot_obj= temp_obj)
        connection.send(soundcloud_data_object)

    else:
        logging.error("No soundcloud object passes to get_soundcloud_data")

###############################################################################################################
#Driver for the queue. Main Driver for both SOundcloud and Spotify API
def main():
    if __name__ == '__main__':

         
        #Itialize objects with multithreading
        initialize_objects_array = initialize_objects_multithreaded()
    
        spotify_object = initialize_objects_array[0]
        spotify_object = initialize_objects_array[1]
        soundcloud_object = initialize_objects_array[2]

        #Get Data Structures with Multiprocessing
        #create Pipes to Pipe data structures back from Processes running in parallel
        conn1, conn2 = Pipe()
        conn3, conn4 = Pipe()

        #Setup Processes and targets
        p1 = Process(target = get_soundcloud_data, args=(conn2,soundcloud_object))
        #p2 = Process(target = get_spotify_data, args=(conn4,spotify_object))

        #Start processes
        p1.start()
        #p2.start()

        #Pipe values
        soundcloud_data_object = conn1.recv()
        #spotify_data_object = conn3.recv()

        #test print
        print(type(soundcloud_data_object))
        #print(type(spotify_data_object))
       
        print("--- %s seconds ---" % (time.time() - start_time))
       




####################################################################################################################################
####################################################################################################################################
###    END OF DRIVER    ###
main()
