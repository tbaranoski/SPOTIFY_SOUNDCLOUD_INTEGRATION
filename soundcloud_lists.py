#List object to store metadata and data regarding 
#list of songs and number of valid songs/unpopulate songs (No metadata returned from API)

import logging
from unicodedata import name

#Stores all the playlists
class SoundCloud_Data:
    def __init__(self, playlists = []):
        self.playlists_array = playlists
        try:
            self.num_playlists = len(self.playlists_array)
        except:
            self.num_playlists = 0

    #Add a playlist
    def add_playlist(self, temp_array):
        self.playlists_array.append(temp_array)
        self.num_playlists = len(self.playlists_array)

    def print_num_playlists(self):
        print("Number of playlists in Object Saved: ", self.num_playlists)

    def print_all_data(self):

        counter = 0
        #Itterate through each plalist
        for i in self.playlists_array:
            counter += 1
            str_counter = str(counter) + ". "

            print ('\033[1m') #Bold FONT ON
            print("\n")
            print("User Playlist No.",str(counter),":",i.name, "\n")
            print ('\033[0m') #Bold FONT OFF

            #Itterate through each song in playlist
            counter_2 = 0
            for song in i.Song_objects_array:
                counter_2 += 1
                temp_string = str(counter_2) + '. '
                print(temp_string, song.name, "<",song.ID, ">")
                
                #Print if stream id populated or not
                if(song.stream_url != None):
                    print("stream URL populated")
                else:
                    print("No stream URL")
                    logging.error("No stream URL!")

#################################################################################################
#################################################################################################
#Class to Store a list of Songs
class List:
    def __init__(self, description = None, name = None, total_num_songs = None,total_num_populated_songs = None,song_ids = None, array_dictionaries = None, array_stream_urls = []):
        self.description = description
        self.name = name
        self.total_num_songs = total_num_songs
        self.total_num_populated_songs = total_num_populated_songs #num songs with metadata
        self.song_ids = song_ids
        self.array_dictionaries = array_dictionaries
        self.array_stream_urls = array_stream_urls

        self.Song_objects_array = []

        #Confirm the arrays given are the same length
        if(len(self.array_dictionaries) != len(self.song_ids)):
            logging.error("Size of array_dicitonaries and song_ids arrays not same length in soundcloud_lists.py. Data NOT congreunt")            

        else:
        #Create the individual song objects
            self.create_Song_objects()


    #Used for debugging to print IDS
    def print_song_IDS(self):

        counter = 0
        for x in self.song_ids:
            counter = counter + 1
            str_counter = str(counter)
            print(str_counter + ". ", x)

    #Prints the metadata for each song in the list
    def print_metadata(self):

        counter = 0
        for x in self.Song_objects_array:
            counter = counter + 1
            string_counter = str(counter) + '. '
            print('{:4} {:^60} {:^60}'.format(string_counter ,x.name, x.ID))
            

    #Add Song_Data object for each valid song
    def create_Song_objects(self):

        #If we have non empty list of valid Song IDs then create Song objects        
        if(((len(self.song_ids) != 0) and (self.song_ids != None)) and (len(self.array_stream_urls) == len(self.song_ids))):

            #Itterate through all the songs and create objects for each one
            counter = 0
            for x in (self.array_dictionaries):
                temp_obj = Song(ID = self.song_ids[counter], name = x['title'], stream_url= self.array_stream_urls[counter]) #create Song object
                counter = counter + 1
                self.Song_objects_array.append(temp_obj)

        #If song ID list is empty or set to None
        else:
            logging.error("Can Not create Song Object. Song IDs is not populated")


#################################################################################################
#################################################################################################
#Class to Store Song_Data for a specific song
class Song:
    def __init__(self, ID = None, name = None, stream_url = None):
        self.ID = ID
        self.name = name

        #Try to add m3u streaming (Points to stream url)
        try:
            self.stream_url = stream_url
        except:
            pass





#################################################################################################
#################################################################################################