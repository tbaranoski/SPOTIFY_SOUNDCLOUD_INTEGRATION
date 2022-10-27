import logging
import spotipy
from fuzzywuzzy import fuzz

class remote:
    def __init__(self,spotify_object):
        self.spotify_object = spotify_object
        self.user_albums = self.album_maker(spotify_object)
        self.user = (spotify_object.me())['product']
    
    # Given a spotify_object
    # Return all tracks that the user has with a limit of 50
    def album_maker(self,spotipy_object):
        names = []
        album = []
        user_spotify_album = spotipy_object.current_user_saved_albums(limit=50,offset=0)

        for x in range (0,len(user_spotify_album['items'])):
            names.append(((user_spotify_album['items'][x]['album']['name']),(user_spotify_album['items'][x]['album']['uri'])))
        
        for x in range (0,len(names)):
            album.append((names[x],self.scrape_track(user_spotify_album,x)))
        return album

    # Helper function for album_maker
    def scrape_track(self,user_album,album_num):
        tracks = []
        track_ammount = int(user_album['items'][album_num]['album']['total_tracks'])

        for x in range (0,track_ammount):
            tracks.append(((user_album['items'][album_num]['album']['tracks']['items'][x]['name']),(user_album['items'][album_num]['album']['tracks']['items'][x]['uri'])))
        
        return tracks
    
    # Given the name of track
    # Return the location of track in self.user_albums
    # Send a search API request if we can`t find the track from user album
    def search(self,key,type=None,multiple=False):
        location = []
        # If user gives us a type then search Spotify
        if type is not None:
            search = self.spotify_object.search(key, limit=5, type = type )
            search = search['tracks']['items']
            for items in search:
                if len(key) > 5:
                    if fuzz.token_sort_ratio(key,items['name']) > 70:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
                else:
                    if fuzz.ratio(key,items['name']) > 75:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
        # Do a quick search to see if the user has the track in thier library
        if type is None and multiple is False:
            print("type is none")
            for x in range(0,len(self.user_albums)):
                for y in range (0,len(self.user_albums[x][1])):
                    # Add FuzzyWuzzy to make search better
                    # If the key len is bigger than five, average length of a word, use fuzz.token_sort_ratio for maybe better results
                    if len(key) > 5:
                        if fuzz.token_sort_ratio(key,self.user_albums[x][1][y][0]) > 70:
                            location.append(x)
                            location.append(y)
                    # If the key len is less than five, average length of a word, use fuzz.ratio to find if string are simialr
                    elif len(key) < 5:
                        if fuzz.ratio(key,self.user_albums[x][1][y][0]) > 50:
                            location.append(x)
                            location.append(y)
        # If multiple tracks given
        if multiple is True:
            search = self.spotify_object.search(key, limit=5, type = 'track' )
            search = search['tracks']['items']
            for items in search:
                if len(key) > 5:
                    if fuzz.token_sort_ratio(key,items['name']) > 70:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
                else:
                    if fuzz.ratio(key,items['name']) > 75:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
        # If the length of location is zero then user does not have track in library
        if len(location) == 0:
            print("len(location)")
            search = self.spotify_object.search(key, limit=5, type = 'track' )
            search = search['tracks']['items']
            for items in search:
                if len(key) > 5:
                    if fuzz.token_sort_ratio(key,items['name']) > 70:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
                else:
                    if fuzz.ratio(key,items['name']) > 75:
                        location.append(items['name'])
                        location.append(items['uri'])
                        break
        return location

    # Given the name of the device
    # Return the device ID of given name
    def findDevice(self,deviceName):
        devices = self.spotify_object.devices()
        if len(devices['devices']) > 0:
            for device in devices['devices']:
                # Add FuzzyWuzzy to make finding devices easy
                if fuzz.token_sort_ratio(deviceName,device['name']) > 50:
                    return device['id']                
        else:
            print("No active devices found")

    # Given no arguments
    # Resume playback
    #
    # Given a track name
    # Play track at current_playback
    #
    # Given location
    # Play current track at location
    #
    # Given track and location
    # Play track at location
    def play(self,key=None,location=None):

        # Check some states
        # See if user can even use play method
        if self.user == 'open' or self.user == 'free':
            return 'must have premium'
        # @TODO Add support for playlist and mutliple songs
        # Added support for multiple songs

        #Added Statement for playing with a specific offset_ms (where song left off)
        elif((key==None) and (location==None)):
            logging.info("Custom play with offset_ms ran")

            #Current Song info
            current_song_dictionary = self.spotify_object.current_user_playing_track()
            time_stamp_ms = current_song_dictionary['progress_ms']

            self.spotify_object.start_playback(uris = [((self.spotify_object.currently_playing())['item']['uri']),((self.spotify_object.currently_playing())['item']['uri'])], position_ms=time_stamp_ms)
            print("Playing " + ((self.spotify_object.currently_playing())['item']['name']) + " at current device at time(ms):", time_stamp_ms)


        elif isinstance(key,list) and location is not None:
            logging.info("Remote-Play Option1")
            uris = []
            for x in key:
                uris.append((self.search(x,multiple=True))[1])
            self.spotify_object.start_playback(uris=uris,device_id=self.findDevice(location))
        elif isinstance(key,list) and location is None:
            logging.info("Remote-Play Option2")
            uris = []
            for x in key:
                uris.append((self.search(x,multiple=True))[1])
                print(uris)
            self.spotify_object.start_playback(uris = uris)
        # If user gives no key and no location then resume playback on current location
        elif key is None and location is None:
            logging.info("Remote-Play Option3")
            self.spotify_object.start_playback(uris = [((self.spotify_object.currently_playing())['item']['uri']),((self.spotify_object.currently_playing())['item']['uri'])])
            self.next()
            print("Playing " + ((self.spotify_object.currently_playing())['item']['name']) + " at current device")
        # If user gives no location but gives us a key then play given key at current device playback
        elif location is None and key is not None:
            logging.info("Remote-Play Option4")
            album_location = self.search(str(key))
            track_id = str(self.user_albums[album_location[0]][1][album_location[1]][1])
            self.spotify_object.start_playback(uris = [track_id,track_id])
            self.next()
            print("Playing " + (track_id) + " at current device")
        # If user gives key and location then play key at device
        elif key is not None and location is not None:
            logging.info("Remote-Play Option5")
            album_location = self.search(str(key))
            track_id = self.user_albums[album_location[0]][1][album_location[1]][1]
            location = self.findDevice(location)
            self.spotify_object.start_playback(device_id=location,uris=[track_id,track_id])
            self.next()
            print("Playing " + (self.user_albums[album_location[0]][1][album_location[1]][0]) + " at " + location)
        # If user gives only location then start to play at location
        elif key is None and location is not None:
            logging.info("Remote-Play Option6")
            self.spotify_object.start_playback(device_id = self.findDevice(location),uris = [((self.spotify_object.currently_playing())['item']['uri']),((self.spotify_object.currently_playing())['item']['uri'])])
            self.next()
            print("Playing " + ((self.spotify_object.currently_playing())['item']['name']) + " at " + location)


    # Pause playback
    # If given device in normal name like desktop, iphone...
    # Pause playback on current_playback or target device
    def pause(self,device=None):

        #Determine if music is currentlly playing first
        current_song_dictionary = self.spotify_object.current_user_playing_track()
        is_playing = current_song_dictionary['is_playing']

        #If playing then can pause
        if(is_playing == True):
             # See if user has premium
            if self.user == 'open' or self.user == 'free':
                return 'must have premium'
            # If user gives us no device then assume the current playing device
            elif device is None:
                self.spotify_object.pause_playback()
            # If user gives us the device name then pause playback at that device
            elif device is not None:
                self.spotify_object.pause_playback(device_id = self.findDevice(device))

        #If not currentlly playing, can not pause. Log it
        elif(is_playing == False):
            logging.info("Can not pause, music is already paused in remote()")
        
        else:
            logging.error("current_user_playing_track not producing approprate dictionary of data")

    # Go to next track
    # If givin device
    # Then go to next track on current_playback or target device
    def next(self,device=None):
        # If device is None then go to next track on current playback
        if device is None:
            self.spotify_object.next_track()
        # If deivce is given then play next track on device
        else:
            self.spotify_object.next_track(device_id = self.findDevice(device))

    # Go to previous track
    # If givin device
    # Then go to last track on current_playback or target device
    def last(self,device=None):
        # If device is None then go to last song from current playback
        if device is None:
            self.spotify_object.previous_track()
        # If deivce is given then go back to last track on device
        else:
            self.spotify_object.previous_track(device_id = self.findDevice(device))
    
    # Repeat song
    # If givin device and/or repeat
    # Then repeat will be turned on/off on current_playback or other device
    def rep(self, off = False, device = None):
        # If device is not given and off is False then repeat track
        if device is None and off is False:
            self.spotify_object.repeat('track')
        # If off is not False then turn repeat off 
        elif not off:
            self.spotify_object.repeat('off')
        # If device is not None and off is False then turn repeat on at device
        else:
            self.spotify_object.repeat('track',device_id = self.findDevice(device))