from ctypes import sizeof
import logging
import sys
import SoundCloud_Config

#Remote controller for playback for Soundcloud API
def Control_Soundcloud_Playback(remote = None, command = None):

    #Get Soundcloud USER ID
    soundcloud_account_dict = remote.get_account_details()
    USER_ID = soundcloud_account_dict['id']
  
    #Get list Names: (Liked Songs, and ALL USER Playlists)


    #If a remote is given and command is given for playback
    if((remote != None) and (command != None)):
        
        #Get liked songs and select playlists
        liked_songs = remote.get_tracks_liked(limit=100)
        print_song_names(remote, liked_songs)


        #Play Soundcloud    
        if(command == "play"):
            
            user_details_dict = remote.get_user_details(user_id = USER_ID)
            #print(user_details_dict)

    ##If a remote is NOT given OR command is NOT given for playback
    else:
        if(remote == None):
            logging.error("No Soundcloud API OBJECT passed in Control_Playback_Soundcloud.py")
        
        elif(command == None):
            logging.error("No COMMAND for Soundcloud given in Control_Playback_Soundcloud.py")

        else:
            logging.error("Problem in Control_Soundcloud_Playback.py Control_Soundcloud_Playback() flow Error Code:")
            sys.exit(0)



def print_song_names(remote = None, liked_songs = None):

    if((liked_songs != None) and (remote!= None)):

        #Get the title for each song
        collection_array = liked_songs['collection']

        #Print the liked song names:
        print("Liked Songs:")
        i = 0

       #Print the title for all liked songs with metadata
        for x in collection_array:
            i = i + 1 #itterate counter

            #Print song names
            song_dictionary = remote.get_track_details(track_id = x)

            #If dictionary returned is not empty then print
            if(song_dictionary != None):

                song_title = song_dictionary['title']
                counter_string = str(i)
                print(counter_string +".", song_title)

            #If No song metadata is returned
            else:
                counter_string = str(i)
                print(counter_string +".")


    else:
        logging.error("song IDs not given to print_song_names in Control_Playback_Soundcloud.py")

#helper function for debugging and getting SONG IDS
def print_song_ids(array):

    counter = 0
    for x in array:
        counter = counter + 1
        str_counter = str(counter)
        print(str_counter + ". ", x)
