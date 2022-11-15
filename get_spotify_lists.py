import logging
import spotipy
from spotify_lists import Spotify_Data,Spotify_List,Spotify_Song

#Retruns an array of playlists
def get_lists(spotify_obj = None):
    playlists = None

    if(spotify_obj !=None):
        try:
            playlists = spotify_obj.current_user_playlists()
        except:
            logging.error("Can not get Spotify Playlists in get_spotify_lists.py")

    else:
        logging.error("Not a valid Spotify Remote. Can not get Spotify playliosts in get_spotify_lists.py")


    #If playlists are returned then return back
    if(playlists != None):
        return playlists['items']

    else:
        return None

#Spotify API only lets you pull song data for 100 songs at a time from playlist. This function will return all data from playlist
#by making multiple API calls.
def get_all_songs_in_playlist(spot_obj = None, playlist_id_temp1 = None):

    arr_total = []
    if((playlist_id_temp1 != None) or (spot_obj!= None)):

        #Get first itteration and add to arr_total
        temp_list = spot_obj.playlist_tracks(playlist_id = playlist_id_temp1, limit = 100, offset=0)
        arr_total = temp_list['items']
        #If there are more songs, keep pulling data
        counter = 0
        while((len(temp_list['items'])) == 100):
            temp_list = []
            counter = counter + 1
            temp_list = spot_obj.playlist_tracks(playlist_id = playlist_id_temp1, limit = 100, offset = (counter * 100))
            arr_total.extend(temp_list['items'])

        #return list of ALL songs
        return arr_total

    else:
        logging.error("No playlist ID given in get_all_songs_in_playlist()")



######################################################################################
#Itterates through each spotify playlist and adds metadata to data structure
def add_spotify_playlists(temp_list = None, spot_obj = None):

    #Error catcher
    if((temp_list == None) or (len(temp_list) == 0) or (spot_obj == None)):
        logging.error("Can not add spotify playlists, no valid playlisyts provided in add_spotify_playlists()")
        return None

    #Add spotify songs and playlists
    Spotify_Data_obj = Spotify_Data() #Spotify Data object

    #itterate through playlists
    for playlist_num in temp_list:

        #If plalist is public examine it
        public_bool = playlist_num['public']
        if public_bool == True:

            #Get playlist info for ALL songs. Call helper to call multiple API calls if over 100 songs
            playlist_id_temp = playlist_num['id']
            play_items = get_all_songs_in_playlist(spot_obj = spot_obj, playlist_id_temp1 = playlist_id_temp)

            
            playlist_name = playlist_num['name']
            playlist_description = playlist_num['description']
            play_id = playlist_num['id']
    
            counter = 0
            song_duration_array = []
            song_ids_array = []
            song_names_array = []
            #Itterate through each plylist and get each song metadata
            for x in play_items:
                counter = counter + 1
                counter_str = str(counter)

                track_dictionary = x['track']
                song_duration_array.append(track_dictionary['duration_ms'])
                song_ids_array.append(track_dictionary['id'])
                song_names_array.append(track_dictionary['name'])

            #Create playlist object
            playlist_temp = Spotify_List(description = playlist_description, name = playlist_name, total_num_songs = counter,total_num_populated_songs = counter,song_ids = song_ids_array, array_time_ids = song_duration_array, names_array = song_names_array, playlist_id = play_id)
            Spotify_Data_obj.add_playlist(playlist_temp)
    
    #print_spot_data_structure(spot_obj = Spotify_Data_obj)

    #Return the data structure
    return Spotify_Data_obj
        
        
def print_spot_data_structure(spot_obj = None):

    if(spot_obj != None):
        spot_obj.print_all_data()
    
    else:
        logging.error("Can NOT print Spotify metadata")

