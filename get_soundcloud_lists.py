import logging
import sys
from soundcloud_lists import List, Song

#Gets the Lists of valid songs from the users SOundcloud
#Current lists include:
#1. Likes list
#2. User Playlist(s)


#Helper FUnction: Get Soundcloud USER ID
def get_USER_ID(remote):
    #Get Soundcloud USER ID
    soundcloud_account_dict = remote.get_account_details()
    USER_ID = soundcloud_account_dict['id']

    if(USER_ID != None):
        try:
            return USER_ID
        except:
            logging.error("Could Not Extract valid USER_ID from GET_USER_ID in get_Soundcloud_lists.py")
            return None

    #No User ID returned 
    else:
        logging.error("No User ID returned in get_Soundcloud_lists.py")
        return None

#####################################################################################################################
#####################################################################################################################
#Returns an array of all songs in the list that have metadata
def get_valid_songs(remote = None, ID_array = None, print_bool = False):
    
    valid_IDs = []
    valid_dictionaries = []

    if((remote != None) and (ID_array != None)):
    #Print the liked song names:

        if(print_bool == True):
            print("Liked Songs:")
        
        i = 0
       #Print the title for all liked songs with metadata
        for x in ID_array:
            i = i + 1 #itterate counter

            #Print song names
            song_dictionary = remote.get_track_details(track_id = x)

            #If dictionary returned is not empty then print
            if(song_dictionary != None):

                #Save song ID in valid_IDs list
                valid_IDs.append(x)
                valid_dictionaries.append(song_dictionary)

                #Print the songs if print flag is True
                if(print_bool == True):
                    song_title = song_dictionary['title']
                    counter_string = str(i)
                    print(counter_string +".", song_title)

            #If No song metadata is returned
            else:
                counter_string = str(i)
                if(print_bool == True):
                    print(counter_string +".")

        return ([valid_IDs, valid_dictionaries])

    #Not a valid object remote given
    else:
        logging.error("Not a valid remote or array in get_valid_songs() in get_soundcloud_lists.py")
        return None

#####################################################################################################################
#####################################################################################################################
def Get_Soundcloud_lists(remote = None,soundcloud_data_obj = None):

    #If soundcloud remote object is valid
    if(remote != None):

        #Get User ID
        USER_ID = get_USER_ID(remote)
        
        #Get Lists of Song IDS
        if(USER_ID != None):

            #Get Valid Liked Songs list
            ##################################################################################
            #liked_songs = remote.get_tracks_liked(limit=100)
            user_dictionary = remote.get_user_details(user_id = USER_ID)
            num_liked_songs = user_dictionary['likes_count']
            liked_songs = remote.get_tracks_liked(limit=20) #num_liked_songs)
            
            #Extract the Song IDS as an array
            liked_song_IDS = liked_songs['collection']
            double_array = get_valid_songs(remote = remote, ID_array = liked_song_IDS)

            valid_IDs_array = double_array[0]
            valid_dictionaries = double_array[1]
            
            #Get the stream URLS and append to an array
            array_urls = []
            for song_ID in valid_IDs_array:
                stream_url = remote.get_stream_url(song_ID)
                array_urls.append(stream_url)

            #Create List object
            liked_songs_object = List(description = "Liked Songs", name = 'Likes', total_num_songs = num_liked_songs, total_num_populated_songs = len(valid_IDs_array), song_ids = valid_IDs_array, array_dictionaries = valid_dictionaries, array_stream_urls = array_urls)
            soundcloud_data_obj.add_playlist(temp_array = liked_songs_object) #added
            
            #Get all user playlists
            ##################################################################################
            #playlist_array = remote.get_account_playlists()
            user_playlists = (remote.get_playlists_from_user(user_id = USER_ID, limit = 15))['collection']
            
            #Itterate through Users playlists
            counter = 0
            for i in user_playlists:
                #counter += 1
                
                playlist_details = remote.get_playlist_details(i['id'])

                #Reset temp arrays
                list_tracks = playlist_details['tracks']
                song_IDs = []
                valid_IDs_array = []
                valid_dictionaries = []

                #Get all song IDS and respective dictionary
                for x in list_tracks:
                    song_IDs.append(x['id']) #append song IDs to list

                #Get valid IDS (only songs with metadata provided)                
                double_array = get_valid_songs(remote = remote, ID_array = song_IDs)
                valid_IDs_array = double_array[0]
                valid_dictionaries = double_array[1]

                 #Get the stream URLS and appned to an array
                array_urls_temp = []
                for song_ID in valid_IDs_array:
                    stream_url = remote.get_stream_url(song_ID)
                    array_urls_temp.append(stream_url)

                #Create a List object
                playlist_object_temp = List(description = i['title'], name = i['title'], total_num_songs = len(list_tracks), total_num_populated_songs = len(valid_IDs_array), song_ids = valid_IDs_array, array_dictionaries = valid_dictionaries, array_stream_urls = array_urls_temp)
                soundcloud_data_obj.add_playlist(temp_array = playlist_object_temp) #added

            ##################################################################################



            #Test Driver start
            #################################################################
            #print("The number of playlists in object is: ",soundcloud_data_obj.print_num_playlists())

            soundcloud_data_obj.print_all_data()

            #Try to get stream data for just one song. First get ID
            #example_song_ID = soundcloud_data_obj.playlists_array[0].Song_objects_array[0].ID
            #print(example_song_ID)

            #stream_dict = remote.get_stream_url(example_song_ID)
            #print("type: ", type(stream_dict))
            #print("stream_dict: ", stream_dict)

            #################################################################
            #Test Driver End



        #If no USER_ID is returned exit program
        else:
            sys.exit("Program exited. No valid USER_ID")
    
    #Non Valid Remote object
    else:
        logging.error("Soundcloud Remote object is not valid in Get_Soundcloud_lists() in get_Soundcloud_lists.py")


