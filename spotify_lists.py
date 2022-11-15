import logging

#stores all the spotify plalists
class Spotify_Data:

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

    #Prints all metadata of the Spotify Data
    def print_all_data(self):

        counter = 0
        #Itterate through each plalist
        for i in self.playlists_array:
            counter += 1
            str_counter = str(counter) + ". "

            print ('\033[1m') #Bold FONT ON
            print("\n")
            print("User Playlist No.",str(counter),":",i.name,"\tID: ",i.playlist_id, "\n")
            print ('\033[0m') #Bold FONT OFF

            #Itterate through each song in playlist
            counter_2 = 0
            for song in i.Song_objects_array:
                counter_2 += 1
                temp_string = str(counter_2) + '. '
                print(temp_string, song.name, "<",song.ID, ">", " ", song.duration_ms)


#Class that stores information on each playlist
class Spotify_List:
    def __init__(self, description = None, name = None, total_num_songs = None,total_num_populated_songs = 0,song_ids = [], array_time_ids = [], names_array = [], playlist_id = None):
        self.description = description
        self.name = name
        self.total_num_songs = total_num_songs
        self.song_ids = song_ids
        self.song_duration = array_time_ids
        self.names_array = names_array
        self.playlist_id = playlist_id

        self.Song_objects_array = []        
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
            print('{:4} {:^60} {:^60} {:^60}'.format(string_counter ,x.name, x.ID, x.duration_ms))
            

    #Add Song_Data object for each valid song
    def create_Song_objects(self):

        #If we have non empty list of valid Song IDs then create Song objects        
        if((len(self.song_ids) != 0) and (self.song_ids != None)):

            #Itterate through all the songs and create objects for each one
            counter = 0
            for x in (self.song_ids):
                temp_obj = Spotify_Song(ID = self.song_ids[counter], name = self.names_array[counter], duration = self.song_duration[counter]) #create Spotify Song object
                counter = counter + 1
                self.Song_objects_array.append(temp_obj)

        #If song ID list is empty or set to None
        else:
            logging.error("Can Not create Spotify Song Object. Song IDs is not populated")

#Class that stores Spotify Songs
class Spotify_Song:
    def __init__(self, ID = None, name = None, duration = None):
        self.ID = ID
        self.name = name
        self.duration_ms = duration
