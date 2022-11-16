import logging
 
#Queue class for setting up a queue between multiple music platforms
class playback_queue:
    def __init__(self, array = []):
        self.array = array

    #return the next song
    def get_next_up(self):
        temp_obj = (self.array).pop()
        return temp_obj

    #add a song object to queue
    def add_queue(self, obj = None):
        
        if((obj != None) and (len(self.array) == 0)):
            (self.array).append(obj)

        elif(obj != None):
            (self.array).insert(0, obj)

        else:
            logging.error("Can not add object to queue")
    #Remove a song object from queue
    def remove_queue(self, obj = None):
       
        if(obj != None):
            
            ### From: https://www.geeksforgeeks.org/python-remove-given-element-from-the-list/ ###
            if obj in self.array:
                (self.array).pop((self.array).index(obj))
            ######################################################################################
            else:
                logging.info("Object requested to REMOVE from queue can not be found")
        else:
            logging.error("No Song object given to be removed from queue")

    #Print the contents of the queue in order
    def print_queue(self):

        num_songs_in_queue = len(self.array)
        self.bold_print_format()

        #Print the song names backwards
        counter = 0
        for i in range(num_songs_in_queue-1,0,-1):
            counter = counter + 1
            str_counter = (str(counter)) +'. '
            temp_song = self.array[i]
            temp_platform = self.get_platform(song = temp_song)
            print('{:4} {:^60} {:^60}'.format(str_counter, temp_song.name, temp_platform))
            
        #PRINT LAST SONG
        temp_song = self.array[0]
        counter = counter + 1
        str_counter = (str(counter)) +'. '
        temp_platform = self.get_platform(song = temp_song)
        print('{:4} {:^60} {:^60}'.format(str_counter, temp_song.name, temp_platform))
        print("\n")

    #Returns a string whether it is spotify or Soundcloud
    def get_platform(self, song = None):
           
        #If song is from Soundcloud class
        if(((type(song).__name__)) == "Song"):
            return "Soundcloud"
        
        #If song is from Spotify class
        elif(((type(song).__name__)) == "Spotify_Song"):
            return "Spotify"

        else:
            logging.error("Song object can NOT be identified as Soundcloud Song or Spotify Song") 
            return "N/A" #temp
        

    #Helper Function for printing header in bold
    def bold_print_format(self):

        print ('\033[1m') #Bold FONT ON
        print("\n")
        print('{:^60} {:^60}'.format("Song Queue", "Platform"))
        print ('\033[0m') #Bold FONT OFF

    ####################################################################################
    #Print a single song from the queue
    def print_single_song(self, temp_song):

        temp_platform = self.get_platform(song = temp_song)
        print("\n")
        print('{:^20} {:^60} {:^60}'.format("SONG: ", temp_song.name, temp_platform))